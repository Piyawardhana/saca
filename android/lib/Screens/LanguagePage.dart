import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/InputMethodPage.dart';

class LanguagePage extends StatelessWidget {
  const LanguagePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(
        title: 'Choose Language',
        context: context,
      ),
      body: AppBackground(
        child: Center(
          child: Container(
            width: 460,
            padding: const EdgeInsets.all(28),
            decoration: _cardDecoration(),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                _heading('Choose Language'),
                const SizedBox(height: 26),
                CustomButton(
                  text: 'English',
                  icon: Icons.language_rounded,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            const InputMethodPage(isEnglish: true),
                      ),
                    );
                  },
                ),
                const SizedBox(height: 16),
                CustomButton(
                  text: 'Pitjantjatjara',
                  icon: Icons.translate_rounded,
                  gradientColors: const [
                    Color(0xFF0F172A),
                    Color(0xFF334155),
                  ],
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) =>
                            const InputMethodPage(isEnglish: false),
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

  Widget _heading(String text) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: const [
        Text(
          'Choose Language',
          style: TextStyle(
            fontSize: 28,
            fontWeight: FontWeight.w800,
            color: Color(0xFF0F172A),
          ),
        ),
        SizedBox(width: 10),
        Icon(Icons.mic_none_rounded, color: Color(0xFF2563EB)),
      ],
    );
  }

  BoxDecoration _cardDecoration() {
    return BoxDecoration(
      color: Colors.white.withOpacity(0.88),
      borderRadius: BorderRadius.circular(28),
      border: Border.all(color: Colors.white.withOpacity(0.7)),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withOpacity(0.10),
          blurRadius: 20,
          offset: const Offset(0, 10),
        ),
      ],
    );
  }

  PreferredSizeWidget _appBar({
    required String title,
    required BuildContext context,
  }) {
    return AppBar(
      backgroundColor: Colors.white.withOpacity(0.92),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      leading: IconButton(
        onPressed: () => Navigator.pop(context),
        icon: const Icon(Icons.arrow_back_ios_new_rounded),
      ),
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