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
  final double unitPrice;
  final double discount; // percentage e.g. 5.0
  final int unitsPerCarton;
  final int unitsPerBox;

  const CartLine({
    required this.productId,
    required this.productName,
    required this.unit,
    required this.quantity,
    required this.unitPrice,
    this.discount = 0.0,
    this.unitsPerCarton = 24,
    this.unitsPerBox = 12,
  });

  /// Total units in individual pieces
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

  /// Line gross subtotal before line discount
  double get grossTotal {
    return quantity * unitPrice;
  }

  /// Line discount amount in currency
  double get discountAmount {
    return grossTotal * (discount / 100.0);
  }

  /// Net line total after discount
  double get netTotal {
    return grossTotal - discountAmount;
  }

  CartLine copyWith({
    String? productId,
    String? productName,
    OrderUnit? unit,
    int? quantity,
    double? unitPrice,
    double? discount,
    int? unitsPerCarton,
    int? unitsPerBox,
  }) {
    return CartLine(
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      unit: unit ?? this.unit,
      quantity: quantity ?? this.quantity,
      unitPrice: unitPrice ?? this.unitPrice,
      discount: discount ?? this.discount,
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
        unitPrice,
        discount,
        unitsPerCarton,
        unitsPerBox,
      ];
}
