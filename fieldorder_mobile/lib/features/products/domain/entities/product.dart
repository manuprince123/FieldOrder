import 'package:equatable/equatable.dart';

enum StockStatus {
  inStock,
  lowStock,
  outOfStock;

  static StockStatus fromQty(int qty) {
    if (qty <= 0) return StockStatus.outOfStock;
    if (qty < 20) return StockStatus.lowStock;
    return StockStatus.inStock;
  }
}

class Product extends Equatable {
  final String id;
  final String sku;
  final String name;
  final String category;
  final String baseUnit;
  final int unitsPerCarton;
  final int unitsPerBox;
  final double price;
  final int stockQuantity;
  final String? barcode;
  final DateTime updatedAt;

  const Product({
    required this.id,
    required this.sku,
    required this.name,
    required this.category,
    this.baseUnit = 'piece',
    this.unitsPerCarton = 24,
    this.unitsPerBox = 12,
    required this.price,
    required this.stockQuantity,
    this.barcode,
    required this.updatedAt,
  });

  StockStatus get stockStatus => StockStatus.fromQty(stockQuantity);

  bool get isAvailable => stockQuantity > 0;

  @override
  List<Object?> get props => [
        id,
        sku,
        name,
        category,
        baseUnit,
        unitsPerCarton,
        unitsPerBox,
        price,
        stockQuantity,
        barcode,
        updatedAt,
      ];
}
