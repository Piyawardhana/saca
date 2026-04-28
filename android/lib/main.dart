import 'package:flutter/material.dart';
import 'package:saca_project/Screens/WelcomePage.dart';

void main() {
  runApp(const SacaApp());
}

class SacaApp extends StatelessWidget {
  const SacaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'SACA',
      theme: ThemeData(
        useMaterial3: true,
        fontFamily: 'Poppins',
        scaffoldBackgroundColor: const Color(0xFFF5FAFF),
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF2563EB),
        ),
      ),
      home: const WelcomePage(),
    );
  }
}