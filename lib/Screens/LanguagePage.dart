import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/InputMethodPage.dart';

class LanguagePage extends StatelessWidget {
  const LanguagePage({super.key});

  void goNext(BuildContext context, bool isEnglish) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => InputMethodPage(isEnglish: isEnglish),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AppBackground(
        child: Center(
          child: Container(
            width: 480,
            padding: const EdgeInsets.all(30),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.38),
              borderRadius: BorderRadius.circular(28),
              border: Border.all(color: Colors.white.withOpacity(0.45)),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text(
                  'Choose Language',
                  style: TextStyle(
                    fontSize: 30,
                    fontWeight: FontWeight.w900,
                    color: Color(0xFF30161A),
                  ),
                ),
                const SizedBox(height: 26),
                CustomButton(
                  text: 'English',
                  icon: Icons.language_rounded,
                  onPressed: () => goNext(context, true),
                ),
                const SizedBox(height: 16),
                CustomButton(
                  text: 'Pitjantjatjara',
                  icon: Icons.translate_rounded,
                  onPressed: () => goNext(context, false),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}