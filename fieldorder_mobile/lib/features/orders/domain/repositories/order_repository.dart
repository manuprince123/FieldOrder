import '../entities/order.dart';
import '../entities/cart_line.dart';

abstract class OrderRepository {
  Stream<List<OrderEntity>> watchAllOrders({String? customerId});
  Future<OrderEntity?> getOrderById(String orderId);
  Future<void> saveOrderDraft(OrderEntity order);
  Future<void> confirmAndQueueOrder(OrderEntity order);
  Future<void> updateOrderLines(String orderId, List<CartLine> newLines);
  Future<void> markOrderNeedsReview(String orderId, String conflictReason);
  Future<void> markOrderSynced(String orderId, String serverOrderNo);
  Future<List<OrderEntity>> getOrdersNeedingSync();
}
