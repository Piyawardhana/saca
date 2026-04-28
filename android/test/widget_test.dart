import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:saca_project/Screens/WelcomePage.dart';

void main() {
  testWidgets('App loads successfully', (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(
        home: WelcomePage(),
      ),
    );

    expect(find.text('GET STARTED'), findsOneWidget);
  });
}
