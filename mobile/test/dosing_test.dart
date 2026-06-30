import 'package:flutter_test/flutter_test.dart';
import 'package:inhp_mobile/core/dosing.dart';

void main() {
  test('weight-based dose calculation', () {
    expect(paediatricDoseMg(10, 15), 150.0);
    expect(paediatricDoseMg(7.5, 20), 150.0);
  });

  test('rejects non-positive inputs', () {
    expect(() => paediatricDoseMg(0, 15), throwsArgumentError);
    expect(() => paediatricDoseMg(10, 0), throwsArgumentError);
  });
}
