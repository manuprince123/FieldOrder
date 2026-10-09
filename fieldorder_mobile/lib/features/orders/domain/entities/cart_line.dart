import 'package:equatable/equatable.dart';

enum OrderUnit {
  piece,
  box,
  carton;

  static OrderUnit fromString(String val) {
    switch (val.toLowerCase()) {
      case 'carton':
        return OrderUnit.carton;
      case 'box':
        return OrderUnit.box;
      default:
        return OrderUnit.piece;
    }
  }

  String get displayName {
    switch (this) {
      case OrderUnit.carton:
        return 'Carton';
      case OrderUnit.box:
        return 'Box';
      case OrderUnit.piece:
        return 'Piece';
    }
  }
}

class CartLine extends Equatable {
  final String productId;
  final String productName;
  final OrderUnit unit;
  final int quantity;
  final int unitPricePaise; // Stored in integer paise (e.g. ₹288.00 = 28800)
  final double discountPercent; // Line discount percentage (e.g. 5.0%)
  final int unitsPerCarton;
  final int unitsPerBox;

  const CartLine({
    required this.productId,
    required this.productName,
    required this.unit,
    required this.quantity,
    required this.unitPricePaise,
    this.discountPercent = 0.0,
    this.unitsPerCarton = 24,
    this.unitsPerBox = 12,
  });

  /// Factory helper for creating from Rupee double
  factory CartLine.fromRupees({
    required String productId,
    required String productName,
    required OrderUnit unit,
    required int quantity,
    required double unitPriceRupees,
    double discountPercent = 0.0,
    int unitsPerCarton = 24,
    int unitsPerBox = 12,
  }) {
    return CartLine(
      productId: productId,
      productName: productName,
      unit: unit,
      quantity: quantity,
      unitPricePaise: (unitPriceRupees * 100).round(),
      discountPercent: discountPercent,
      unitsPerCarton: unitsPerCarton,
      unitsPerBox: unitsPerBox,
    );
  }

  /// Price in Rupees (for display)
  double get unitPriceRupees => unitPricePaise / 100.0;

  /// Total physical items in individual pieces
  int get totalPieces {
    switch (unit) {
      case OrderUnit.carton:
        return quantity * unitsPerCarton;
      case OrderUnit.box:
        return quantity * unitsPerBox;
      case OrderUnit.piece:
        return quantity;
    }
  }

  /// Line gross total in Paise (integer arithmetic prevents 0.1 + 0.2 float errors)
  int get grossTotalPaise {
    return quantity * unitPricePaise;
  }

  double get grossTotalRupees => grossTotalPaise / 100.0;

  /// Line discount amount in Paise
  int get discountAmountPaise {
    return (grossTotalPaise * (discountPercent / 100.0)).round();
  }

  double get discountAmountRupees => discountAmountPaise / 100.0;

  /// Net line total in Paise
  int get netTotalPaise {
    return grossTotalPaise - discountAmountPaise;
  }

  double get netTotalRupees => netTotalPaise / 100.0;

  CartLine copyWith({
    String? productId,
    String? productName,
    OrderUnit? unit,
    int? quantity,
    int? unitPricePaise,
    double? discountPercent,
    int? unitsPerCarton,
    int? unitsPerBox,
  }) {
    return CartLine(
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      unit: unit ?? this.unit,
      quantity: quantity ?? this.quantity,
      unitPricePaise: unitPricePaise ?? this.unitPricePaise,
      discountPercent: discountPercent ?? this.discountPercent,
      unitsPerCarton: unitsPerCarton ?? this.unitsPerCarton,
      unitsPerBox: unitsPerBox ?? this.unitsPerBox,
    );
  }

  @override
  List<Object?> get props => [
        productId,
        productName,
        unit,
        quantity,
        unitPricePaise,
        discountPercent,
        unitsPerCarton,
        unitsPerBox,
      ];
}
