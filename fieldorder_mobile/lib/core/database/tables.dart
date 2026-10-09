import 'package:drift/drift.dart';

/// Section 7: Local Database Design (Drift)
/// Financial Precision Rule: Currency stored as INTEGER PAISE (1 Rupee = 100 Paise)
/// to eliminate IEEE 754 floating-point inaccuracies (0.1 + 0.2 precision problem).
/// Every syncable table carries updated_at, is_dirty, and is_deleted (soft delete).

@DataClassName('CustomerEntry')
class CustomersTable extends Table {
  TextColumn get id => text()(); // Client UUID or Server ID
  TextColumn get name => text()();
  TextColumn get phone => text()();
  TextColumn get address => text()();
  TextColumn get city => text()();
  IntColumn get outstandingBalancePaise => integer().withDefault(const Constant(0))(); // Integer Paise
  DateTimeColumn get lastOrderAt => dateTime().nullable()();
  DateTimeColumn get updatedAt => dateTime()();
  BoolColumn get isDirty => boolean().withDefault(const Constant(false))();
  BoolColumn get isDeleted => boolean().withDefault(const Constant(false))();

  @override
  Set<Column> get primaryKey => {id};
}

@DataClassName('ProductEntry')
class ProductsTable extends Table {
  TextColumn get id => text()();
  TextColumn get sku => text().unique()();
  TextColumn get name => text()();
  TextColumn get category => text()();
  TextColumn get baseUnit => text().withDefault(const Constant('piece'))();
  IntColumn get unitsPerCarton => integer().withDefault(const Constant(24))();
  IntColumn get unitsPerBox => integer().withDefault(const Constant(12))();
  IntColumn get pricePaise => integer()(); // Integer Paise (e.g. ₹288.00 = 28800)
  IntColumn get stockQty => integer().withDefault(const Constant(0))();
  TextColumn get barcode => text().nullable()();
  DateTimeColumn get updatedAt => dateTime()();

  @override
  Set<Column> get primaryKey => {id};
}

@DataClassName('OrderEntry')
class OrdersTable extends Table {
  TextColumn get id => text()(); // Client UUID
  TextColumn get customerId => text()();
  TextColumn get status => text()(); // draft, confirmed, syncing, synced, failed, needs_review
  TextColumn get notes => text().nullable()();
  IntColumn get subtotalPaise => integer()(); // Subtotal in Paise
  IntColumn get discountPaise => integer().withDefault(const Constant(0))(); // Discount in Paise
  IntColumn get totalPaise => integer()(); // Net Total in Paise
  DateTimeColumn get createdAt => dateTime()();
  DateTimeColumn get confirmedAt => dateTime().nullable()();
  TextColumn get syncStatus => text().withDefault(const Constant('pending'))();
  TextColumn get syncError => text().nullable()();
  TextColumn get serverOrderNo => text().nullable()(); // e.g. ORD-2026-1002
  IntColumn get retryCount => integer().withDefault(const Constant(0))();

  @override
  Set<Column> get primaryKey => {id};
}

@DataClassName('OrderLineEntry')
class OrderLinesTable extends Table {
  TextColumn get id => text()();
  TextColumn get orderId => text().references(OrdersTable, #id)();
  TextColumn get productId => text()();
  TextColumn get productNameSnapshot => text()(); // Snapshot prevents catalog mutations from breaking history
  TextColumn get unit => text()(); // piece, box, carton
  IntColumn get quantity => integer()();
  IntColumn get unitPricePaiseSnapshot => integer()(); // Unit price snapshot in Paise
  IntColumn get discountPaise => integer().withDefault(const Constant(0))();
  IntColumn get lineTotalPaise => integer()(); // Line total in Paise

  @override
  Set<Column> get primaryKey => {id};
}

@DataClassName('OutboxEntry')
class OutboxTable extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get entityType => text()(); // 'order' or 'customer'
  TextColumn get entityId => text()();
  TextColumn get operation => text()(); // 'create' or 'update'
  TextColumn get payloadJson => text()();
  TextColumn get idempotencyKey => text()();
  IntColumn get attempts => integer().withDefault(const Constant(0))();
  DateTimeColumn get nextAttemptAt => dateTime()();
  TextColumn get lastError => text().nullable()();
  DateTimeColumn get createdAt => dateTime()();
}

@DataClassName('SyncMetaEntry')
class SyncMetaTable extends Table {
  TextColumn get key => text()();
  TextColumn get value => text()();

  @override
  Set<Column> get primaryKey => {key};
}
