import 'package:equatable/equatable.dart';
import 'cart_line.dart';

enum OrderStatus {
  draft,
  confirmed,
  syncing,
  synced,
  failed,
  needsReview;

  static OrderStatus fromString(String val) {
    switch (val.toLowerCase()) {
      case 'confirmed':
        return OrderStatus.confirmed;
      case 'syncing':
        return OrderStatus.syncing;
      case 'synced':
        return OrderStatus.synced;
      case 'failed':
        return OrderStatus.failed;
      case 'needs_review':
        return OrderStatus.needsReview;
      default:
        return OrderStatus.draft;
    }
  }

  String toDbString() {
    switch (this) {
      case OrderStatus.confirmed:
        return 'confirmed';
      case OrderStatus.syncing:
        return 'syncing';
      case OrderStatus.synced:
        return 'synced';
      case OrderStatus.failed:
        return 'failed';
      case OrderStatus.needsReview:
        return 'needs_review';
      case OrderStatus.draft:
        return 'draft';
    }
  }
}

class OrderEntity extends Equatable {
  final String id; // Client UUID
  final String customerId;
  final String customerName;
  final OrderStatus status;
  final String notes;
  final double subtotal;
  final double discount;
  final double total;
  final DateTime createdAt;
  final DateTime? confirmedAt;
  final String? serverOrderNo;
  final String? syncError;
  final List<CartLine> lines;

  const OrderEntity({
    required this.id,
    required this.customerId,
    required this.customerName,
    required this.status,
    this.notes = '',
    required this.subtotal,
    required this.discount,
    required this.total,
    required this.createdAt,
    this.confirmedAt,
    this.serverOrderNo,
    this.syncError,
    required this.lines,
  });

  /// Section 4.4 Rule: Edit allowed for drafts only; confirmed orders are locked
  bool get isEditable => status == OrderStatus.draft;

  /// Whether order requires rep attention on 409 conflict
  bool get isConflict => status == OrderStatus.needsReview;

  @override
  List<Object?> get props => [
        id,
        customerId,
        customerName,
        status,
        notes,
        subtotal,
        discount,
        total,
        createdAt,
        confirmedAt,
        serverOrderNo,
        syncError,
        lines,
      ];
}
