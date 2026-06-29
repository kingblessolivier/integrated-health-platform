import 'package:flutter_test/flutter_test.dart';
import 'package:inhp_mobile/main.dart';

void main() {
  testWidgets('app boots and shows the title', (tester) async {
    await tester.pumpWidget(const InhpApp());
    expect(find.textContaining('Integrated National Health Platform'), findsOneWidget);
  });
}
