import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/BodyPartPage.dart';
import 'package:saca_project/Screens/TextInputPage.dart';
import 'package:saca_project/Screens/VoiceInputPage.dart';

class InputMethodPage extends StatelessWidget {
  final bool isEnglish;

  const InputMethodPage({
    super.key,
    required this.isEnglish,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: Center(
          child: Container(
            width: 470,
            padding: const EdgeInsets.all(28),
            decoration: _cardDecoration(),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      isEnglish
                          ? 'How do you want to tell us?'
                          : 'Nyaa wangkaku?',
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 26,
                        fontWeight: FontWeight.w800,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                    const SizedBox(width: 10),
                    const Icon(
                      Icons.mic_none_rounded,
                      color: Color(0xFF2563EB),
                    ),
                  ],
                ),
                const SizedBox(height: 28),
                CustomButton(
                  text: isEnglish ? 'Text Input' : 'Walkatjunanyi',
                  icon: Icons.edit_note_rounded,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => TextInputPage(isEnglish: isEnglish),
                      ),
                    );
                  },
                ),
                const SizedBox(height: 16),
                CustomButton(
                  text: isEnglish ? 'Voice Input' : 'Wangka Tjarpanyi',
                  icon: Icons.mic_rounded,
                  gradientColors: const [
                    Color(0xFF2563EB),
                    Color(0xFF06B6D4),
                  ],
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => VoiceInputPage(isEnglish: isEnglish),
                      ),
                    );
                  },
                ),
                const SizedBox(height: 16),
                CustomButton(
                  text: isEnglish ? 'Select Symptom' : 'Pika Nintila',
                  icon: Icons.grid_view_rounded,
                  gradientColors: const [
                    Color(0xFF0F172A),
                    Color(0xFF1E3A8A),
                  ],
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => BodyPartPage(isEnglish: isEnglish),
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

  PreferredSizeWidget _appBar(BuildContext context) {
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