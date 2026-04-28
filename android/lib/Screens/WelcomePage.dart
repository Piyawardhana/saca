import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/LanguagePage.dart';

class WelcomePage extends StatelessWidget {
  const WelcomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar('SACA Welcome'),
      body: AppBackground(
        child: Center(
          child: Container(
            width: 760,
            margin: const EdgeInsets.all(24),
            padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 36),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.28),
              borderRadius: BorderRadius.circular(28),
              border: Border.all(
                color: Colors.white.withOpacity(0.35),
              ),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    shape: BoxShape.circle,
                    color: Colors.white.withOpacity(0.88),
                  ),
                  child: const Icon(
                    Icons.favorite_rounded,
                    color: Color(0xFF2563EB),
                    size: 34,
                  ),
                ),
                const SizedBox(height: 20),
                const Text(
                  'Adaptive Clinical\nAssistant (SACA)',
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 42,
                    height: 1.15,
                    fontWeight: FontWeight.w800,
                    color: Color(0xFF0F172A),
                  ),
                ),
                const SizedBox(height: 14),
                
                const SizedBox(height: 30),
                CustomButton(
                  text: 'Get Started',
                  icon: Icons.arrow_forward_rounded,
                  width: 250,
                  gradientColors: const [
                    Color(0xFF0F172A),
                    Color(0xFF1E3A8A),
                  ],
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => const LanguagePage(),
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  PreferredSizeWidget _appBar(String title) {
    return AppBar(
      titleSpacing: 20,
      backgroundColor: Colors.white.withOpacity(0.92),
      elevation: 0,
      shadowColor: Colors.transparent,
      surfaceTintColor: Colors.transparent,
      title: Row(
        children: const [
          Icon(Icons.favorite_rounded, color: Color(0xFF2563EB)),
          SizedBox(width: 10),
          Text(
            'SACA',
            style: TextStyle(
              color: Color(0xFF0F172A),
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }
}