/// Weight-based paediatric dose (mg), rounded to 0.1 mg. Mirrors the server's
/// `paediatric_dose_mg` so offline iCCM dosing matches what the server validates (docs/51).
double paediatricDoseMg(double weightKg, double mgPerKg) {
  if (weightKg <= 0 || mgPerKg <= 0) {
    throw ArgumentError('weightKg and mgPerKg must be positive');
  }
  return double.parse((weightKg * mgPerKg).toStringAsFixed(1));
}
