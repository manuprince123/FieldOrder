import 'package:flutter_test/flutter_test.dart';
import 'package:fieldorder_mobile/core/sync/backoff_calculator.dart';
import 'package:fieldorder_mobile/features/orders/domain/entities/cart_line.dart';

void main() {
  group('BackoffCalculator Unit Tests', () {
    test('Attempt 0 returns ~30 seconds duration', () {
      final interval = BackoffCalculator.getNextInterval(0);
      expect(interval.inSeconds, greaterThanOrEqualTo(25));
      expect(interval.inSeconds, lessThanOrEqualTo(35));
    });

    test('Attempt 4 caps at 15 minutes', () {
      final interval = BackoffCalculator.getNextInterval(4);
      expect(interval.inMinutes, greaterThanOrEqualTo(13));
      expect(interval.inMinutes, lessThanOrEqualTo(17));
    });

    test('Higher attempts clamp to maximum interval', () {
      final interval10 = BackoffCalculator.getNextInterval(10);
      expect(interval10.inMinutes, greaterThanOrEqualTo(13));
      expect(interval10.inMinutes, lessThanOrEqualTo(17));
    });
  });

  group('CartLine & Integer Paise Arithmetic Tests', () {
    test('Calculates gross paise without floating point error', () {
      final line = CartLine.fromRupees(
        productId: 'prd_001',
        productName: 'Maggi Noodles',
        unit: OrderUnit.carton,
        quantity: 3,
        unitPriceRupees: 288.50,
        discountPercent: 10.0,
        unitsPerCarton: 24,
      );

      expect(line.unitPricePaise, equals(28850));
      expect(line.grossTotalPaise, equals(3 * 28850));
      expect(line.totalPieces, equals(3 * 24));
      expect(line.netTotalPaise, equals(77895));
      expect(line.netTotalRupees, equals(778.95));
    });

    test('OrderUnit parses correctly from string', () {
      expect(OrderUnit.fromString('carton'), equals(OrderUnit.carton));
      expect(OrderUnit.fromString('box'), equals(OrderUnit.box));
      expect(OrderUnit.fromString('piece'), equals(OrderUnit.piece));
      expect(OrderUnit.fromString('unknown'), equals(OrderUnit.piece));
    });
  });
}
