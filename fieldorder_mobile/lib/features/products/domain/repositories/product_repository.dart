import '../entities/product.dart';

abstract class ProductRepository {
  Stream<List<Product>> watchProducts({String? category, String? searchQuery});
  Future<Product?> getProductById(String id);
  Future<Product?> getProductByBarcode(String barcode);
  Future<void> syncProductsFromRemote();
}
