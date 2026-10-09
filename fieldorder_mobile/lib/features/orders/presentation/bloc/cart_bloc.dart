import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:equatable/equatable.dart';
import '../../domain/entities/cart_line.dart';
import '../../../products/domain/entities/product.dart';

// Events
abstract class CartEvent extends Equatable {
  const CartEvent();
  @override
  List<Object?> get props => [];
}

class AddProductToCart extends CartEvent {
  final Product product;
  final OrderUnit unit;
  final int quantity;

  const AddProductToCart({
    required this.product,
    this.unit = OrderUnit.carton,
    this.quantity = 1,
  });

  @override
  List<Object?> get props => [product, unit, quantity];
}

class UpdateLineQuantity extends CartEvent {
  final String productId;
  final OrderUnit unit;
  final int delta;

  const UpdateLineQuantity({
    required this.productId,
    required this.unit,
    required this.delta,
  });

  @override
  List<Object?> get props => [productId, unit, delta];
}

class ChangeLineUnit extends CartEvent {
  final String productId;
  final OrderUnit oldUnit;
  final OrderUnit newUnit;

  const ChangeLineUnit({
    required this.productId,
    required this.oldUnit,
    required this.newUnit,
  });

  @override
  List<Object?> get props => [productId, oldUnit, newUnit];
}

class ApplyLineDiscount extends CartEvent {
  final String productId;
  final OrderUnit unit;
  final double discountPercent;

  const ApplyLineDiscount({
    required this.productId,
    required this.unit,
    required this.discountPercent,
  });

  @override
  List<Object?> get props => [productId, unit, discountPercent];
}

class ClearCart extends CartEvent {}

class LoadReorderCart extends CartEvent {
  final List<CartLine> reorderedLines;
  const LoadReorderCart(this.reorderedLines);

  @override
  List<Object?> get props => [reorderedLines];
}

// States
abstract class CartState extends Equatable {
  const CartState();
  @override
  List<Object?> get props => [];
}

class CartEmpty extends CartState {}

class CartActive extends CartState {
  final List<CartLine> lines;
  final double subtotal;
  final double discountTotal;
  final double netTotal;
  final int totalItemsCount;

  const CartActive({
    required this.lines,
    required this.subtotal,
    required this.discountTotal,
    required this.netTotal,
    required this.totalItemsCount,
  });

  @override
  List<Object?> get props => [
        lines,
        subtotal,
        discountTotal,
        netTotal,
        totalItemsCount,
      ];
}

// BLoC
class CartBloc extends Bloc<CartEvent, CartState> {
  CartBloc() : super(CartEmpty()) {
    on<AddProductToCart>(_onAddProduct);
    on<UpdateLineQuantity>(_onUpdateQuantity);
    on<ChangeLineUnit>(_onChangeUnit);
    on<ApplyLineDiscount>(_onApplyDiscount);
    on<ClearCart>((event, emit) => emit(CartEmpty()));
    on<LoadReorderCart>(_onLoadReorderCart);
  }

  void _onAddProduct(AddProductToCart event, Emitter<CartState> emit) {
    List<CartLine> currentLines = [];
    if (state is CartActive) {
      currentLines = List.from((state as CartActive).lines);
    }

    final index = currentLines.indexWhere(
      (l) => l.productId == event.product.id && l.unit == event.unit,
    );

    if (index >= 0) {
      final existing = currentLines[index];
      currentLines[index] = existing.copyWith(
        quantity: existing.quantity + event.quantity,
      );
    } else {
      currentLines.add(CartLine(
        productId: event.product.id,
        productName: event.product.name,
        unit: event.unit,
        quantity: event.quantity,
        unitPrice: event.product.price,
        unitsPerCarton: event.product.unitsPerCarton,
        unitsPerBox: event.product.unitsPerBox,
      ));
    }

    _emitCalculatedState(currentLines, emit);
  }

  void _onUpdateQuantity(UpdateLineQuantity event, Emitter<CartState> emit) {
    if (state is! CartActive) return;
    final currentLines = List<CartLine>.from((state as CartActive).lines);

    final index = currentLines.indexWhere(
      (l) => l.productId == event.productId && l.unit == event.unit,
    );
    if (index < 0) return;

    final updatedQty = currentLines[index].quantity + event.delta;
    if (updatedQty <= 0) {
      currentLines.removeAt(index);
    } else {
      currentLines[index] = currentLines[index].copyWith(quantity: updatedQty);
    }

    _emitCalculatedState(currentLines, emit);
  }

  void _onChangeUnit(ChangeLineUnit event, Emitter<CartState> emit) {
    if (state is! CartActive) return;
    final currentLines = List<CartLine>.from((state as CartActive).lines);

    final index = currentLines.indexWhere(
      (l) => l.productId == event.productId && l.unit == event.oldUnit,
    );
    if (index < 0) return;

    currentLines[index] = currentLines[index].copyWith(unit: event.newUnit);
    _emitCalculatedState(currentLines, emit);
  }

  void _onApplyDiscount(ApplyLineDiscount event, Emitter<CartState> emit) {
    if (state is! CartActive) return;
    final currentLines = List<CartLine>.from((state as CartActive).lines);

    final index = currentLines.indexWhere(
      (l) => l.productId == event.productId && l.unit == event.unit,
    );
    if (index < 0) return;

    currentLines[index] = currentLines[index].copyWith(
      discount: event.discountPercent.clamp(0.0, 100.0),
    );
    _emitCalculatedState(currentLines, emit);
  }

  void _onLoadReorderCart(LoadReorderCart event, Emitter<CartState> emit) {
    _emitCalculatedState(event.reorderedLines, emit);
  }

  void _emitCalculatedState(List<CartLine> lines, Emitter<CartState> emit) {
    if (lines.isEmpty) {
      emit(CartEmpty());
      return;
    }

    double subtotal = 0.0;
    double discountTotal = 0.0;
    int totalPieces = 0;

    for (final line in lines) {
      subtotal += line.grossTotal;
      discountTotal += line.discountAmount;
      totalPieces += line.totalPieces;
    }

    emit(CartActive(
      lines: lines,
      subtotal: subtotal,
      discountTotal: discountTotal,
      netTotal: subtotal - discountTotal,
      totalItemsCount: totalPieces,
    ));
  }
}
