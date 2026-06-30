import 'package:flutter_test/flutter_test.dart';
import 'package:inhp_mobile/core/geo.dart';

void main() {
  const square = <(double, double)>[(0, 0), (1, 0), (1, 1), (0, 1)];

  test('point inside the village polygon', () {
    expect(pointInPolygon((0.5, 0.5), square), isTrue);
  });

  test('point outside the village polygon', () {
    expect(pointInPolygon((1.5, 0.5), square), isFalse);
    expect(pointInPolygon((-0.1, 0.5), square), isFalse);
  });

  test('degenerate polygon is never inside', () {
    expect(pointInPolygon((0.5, 0.5), const [(0, 0), (1, 1)]), isFalse);
  });
}
