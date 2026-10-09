import '../entities/customer.dart';

abstract class CustomerRepository {
  Stream<List<Customer>> watchCustomers({String? searchQuery, String? cityFilter});
  Future<Customer?> getCustomerById(String id);
  Future<void> saveCustomerLocally(Customer customer);
  Future<void> syncCustomersFromRemote();
}
