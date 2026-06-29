import 'package:flutter/material.dart';

import 'core/theme.dart';

void main() => runApp(const InhpApp());

class InhpApp extends StatelessWidget {
  const InhpApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'INHP',
      theme: inhpTheme,
      home: const Scaffold(
        body: Center(child: Text('Integrated National Health Platform — offline-first')),
      ),
    );
  }
}
