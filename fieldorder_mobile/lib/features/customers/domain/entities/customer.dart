import 'package:equatable/equatable.dart';

class Customer extends Equatable {
  final String id;
  final String name;
  final String phone;
  final String address;
  final String city;
  final double outstandingBalance;
  final DateTime? lastOrderAt;
  final DateTime updatedAt;
  final bool isDirty;
  final bool isDeleted;

  const Customer({
    required this.id,
    required this.name,
    required this.phone,
    required this.address,
    required this.city,
    this.outstandingBalance = 0.0,
    this.lastOrderAt,
    required this.updatedAt,
    this.isDirty = false,
    this.isDeleted = false,
  });

  bool get hasOverdueBalance => outstandingBalance > 0.0;

  Customer copyWith({
    String? id,
    String? name,
    String? phone,
    String? address,
    String? city,
    double? outstandingBalance,
    DateTime? lastOrderAt,
    DateTime? updatedAt,
    bool? isDirty,
    bool? isDeleted,
  }) {
    return Customer(
      id: id ?? this.id,
      name: name ?? this.name,
      phone: phone ?? this.phone,
      address: address ?? this.address,
      city: city ?? this.city,
      outstandingBalance: outstandingBalance ?? this.outstandingBalance,
      lastOrderAt: lastOrderAt ?? this.lastOrderAt,
      updatedAt: updatedAt ?? this.updatedAt,
      isDirty: isDirty ?? this.isDirty,
      isDeleted: isDeleted ?? this.isDeleted,
    );
  }

  @override
  List<Object?> get props => [
        id,
        name,
        phone,
        address,
        city,
        outstandingBalance,
        lastOrderAt,
        updatedAt,
        isDirty,
        isDeleted,
      ];
}
