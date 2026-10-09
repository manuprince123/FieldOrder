import 'dart:convert';
import 'package:dio/dio.dart';
import 'backoff_calculator.dart';

abstract class LocalDatabaseDelegate {
  Future<List<Map<String, dynamic>>> getPendingOutboxItems();
  Future<void> markOrderSynced(String orderId, String serverOrderNo);
  Future<void> markOrderNeedsReview(String orderId, String reason);
  Future<void> markOrderFailed(String orderId, String errorMessage);
  Future<void> updateOutboxRetry(int outboxId, int attempts, DateTime nextAttemptAt, String error);
  Future<void> deleteOutboxItem(int outboxId);
  Future<String?> getLastPullTimestamp(String entityType);
  Future<void> saveLastPullTimestamp(String entityType, String timestamp);
  Future<void> upsertCustomersDelta(List<Map<String, dynamic>> customers);
  Future<void> upsertProductsDelta(List<Map<String, dynamic>> products);
}

class SyncEngine {
  final Dio dio;
  final LocalDatabaseDelegate db;

  SyncEngine({required this.dio, required this.db});

  /// Step 1: Push Outbox Loop
  Future<void> processOutbox() async {
    final pendingItems = await db.getPendingOutboxItems();
    final now = DateTime.now().toUtc();

    for (final item in pendingItems) {
      final nextAttemptAt = DateTime.parse(item['next_attempt_at'] as String);
      if (nextAttemptAt.isAfter(now)) {
        continue; // Respect exponential backoff window
      }

      final outboxId = item['id'] as int;
      final orderId = item['entity_id'] as String;
      final idempotencyKey = item['idempotency_key'] as String;
      final payload = jsonDecode(item['payload_json'] as String) as Map<String, dynamic>;
      final currentAttempts = item['attempts'] as int;

      try {
        final response = await dio.post(
          '/orders',
          data: payload,
          options: Options(
            headers: {'Idempotency-Key': idempotencyKey},
          ),
        );

        if (response.statusCode == 200 || response.statusCode == 201) {
          // 4. On 200 or 201: mark order synced, store server_order_no, delete outbox row
          final serverOrderNo = response.data['server_order_no'] as String;
          await db.markOrderSynced(orderId, serverOrderNo);
          await db.deleteOutboxItem(outboxId);
        }
      } on DioException catch (e) {
        final statusCode = e.response?.statusCode;

        if (statusCode == 409) {
          // 6. On 409: mark order needs_review, store reason, stop retrying until rep edits
          final reason = e.response?.data?['detail']?['error']?.toString() ?? 'Stock conflict';
          await db.markOrderNeedsReview(orderId, reason);
          await db.deleteOutboxItem(outboxId);
        } else if (statusCode != null && statusCode >= 400 && statusCode < 500 && statusCode != 401) {
          // 7. On 422 or other 4xx: mark failed with message, no automatic retry
          final msg = e.response?.data?.toString() ?? 'Validation error';
          await db.markOrderFailed(orderId, msg);
          await db.deleteOutboxItem(outboxId);
        } else {
          // 5. On network error or 5xx: exponential backoff (30s, 1m, 2m, 5m, 15m cap) with jitter
          final newAttempts = currentAttempts + 1;
          final nextTime = BackoffCalculator.getNextAttemptTimestamp(newAttempts, now: now);
          await db.updateOutboxRetry(
            outboxId,
            newAttempts,
            nextTime,
            e.message ?? 'Network connection error',
          );
        }
      } catch (err) {
        final newAttempts = currentAttempts + 1;
        final nextTime = BackoffCalculator.getNextAttemptTimestamp(newAttempts, now: now);
        await db.updateOutboxRetry(outboxId, newAttempts, nextTime, err.toString());
      }
    }
  }

  /// Step 2: Delta Pull for Customers & Products
  Future<void> deltaPull() async {
    final lastCustomerPull = await db.getLastPullTimestamp('customers');
    final custRes = await dio.get('/customers', queryParameters: {
      if (lastCustomerPull != null) 'updated_since': lastCustomerPull,
      'limit': 100,
    });

    if (custRes.statusCode == 200) {
      final items = List<Map<String, dynamic>>.from(custRes.data['items'] ?? []);
      // Skip overwriting local customers that have is_dirty = true
      await db.upsertCustomersDelta(items);
      await db.saveLastPullTimestamp('customers', custRes.data['server_time'] as String);
    }

    final lastProductPull = await db.getLastPullTimestamp('products');
    final prodRes = await dio.get('/products', queryParameters: {
      if (lastProductPull != null) 'updated_since': lastProductPull,
      'limit': 200,
    });

    if (prodRes.statusCode == 200) {
      final items = List<Map<String, dynamic>>.from(prodRes.data['items'] ?? []);
      // Server is authority for products, prices, and stock
      await db.upsertProductsDelta(items);
      await db.saveLastPullTimestamp('products', prodRes.data['server_time'] as String);
    }
  }
}
