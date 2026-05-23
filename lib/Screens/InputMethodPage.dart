import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/HumanBodySelectionPage.dart';
import 'package:saca_project/Screens/TextInputPage.dart';
import 'package:saca_project/Screens/VoiceInputPage.dart';

class InputMethodPage extends StatelessWidget {
  final bool isEnglish;

  const InputMethodPage({
    super.key,
    required this.isEnglish,
  });

  String t(String en, String pit) {
    return isEnglish ? en : pit;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SafeArea(
          bottom: false,
          child: Center(
            child: Container(
              width: 520,
              padding: const EdgeInsets.all(30),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.38),
                borderRadius: BorderRadius.circular(28),
                border: Border.all(color: Colors.white.withOpacity(0.45)),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    t('How do you want to tell us?', 'Nyaa wangkaku?'),
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.w900,
                      color: Color(0xFF30161A),
                    ),
                  ),
                  const SizedBox(height: 28),
                  CustomButton(
                    text: t('Text Input', 'Walkatjunanyi'),
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
                    text: t('Voice Input', 'Wangka tjarpanyi'),
                    icon: Icons.mic_rounded,
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
                    text: t('Select Symptom', 'Pika nintila'),
                    icon: Icons.grid_view_rounded,
                    onPressed: () {
                      Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => HumanBodySelectionPage(
      isEnglish: isEnglish,
      symptoms: const [],
      inputText: '',
    ),
  ),
);
                    },
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  PreferredSizeWidget _appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white.withOpacity(0.95),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      leading: IconButton(
        onPressed: () => Navigator.pop(context),
        icon: const Icon(
          Icons.arrow_back_ios_new_rounded,
          color: Color(0xFF30161A),
        ),
      ),
      title: const Row(
        children: [
          Icon(
            Icons.favorite_rounded,
            color: Color(0xFF30161A),
          ),
          SizedBox(width: 10),
          Text(
            'SACA',
            style: TextStyle(
              color: Color(0xFF30161A),
              fontWeight: FontWeight.w900,
              fontSize: 25,
            ),
          ),
        ],
      ),
    );
  }
}