import 'package:flutter_test/flutter_test.dart';
import 'package:supersaver_sync/app/app.dart';
import 'package:supersaver_sync/counter/counter.dart';

void main() {
  group('App', () {
    testWidgets('renders CounterPage', (tester) async {
      await tester.pumpWidget(const App());
      expect(find.byType(CounterPage), findsOneWidget);
    });
  });
}
