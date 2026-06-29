import 'package:flutter/material.dart';

// Mirrors the design tokens in docs/05 (Dart side of the shared token set).
const brand = Color(0xFF0E7C7B);
const brandDeep = Color(0xFF06402B);
const warningFill = Color(0xFFF5A623); // use with dark text only
const danger = Color(0xFFD32F2F);
const success = Color(0xFF2E7D32);

final inhpTheme = ThemeData(
  useMaterial3: true,
  colorScheme: ColorScheme.fromSeed(seedColor: brand),
  fontFamily: 'Inter',
);
