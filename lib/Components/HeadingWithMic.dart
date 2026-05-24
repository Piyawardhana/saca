import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';

class HeadingWithMic extends StatelessWidget {
  final String text;
  final String speakText;
  final bool isEnglish;
  final double fontSize;

  const HeadingWithMic({
    super.key,
    required this.text,
    required this.speakText,
    required this.isEnglish,
    this.fontSize = 30,
  });

  Future<void> _speak() async {
    final FlutterTts flutterTts = FlutterTts();

    await flutterTts.setLanguage(
      isEnglish ? 'en-AU' : 'en-AU',
    );

    await flutterTts.setSpeechRate(0.5);

    await flutterTts.setPitch(1.0);

    await flutterTts.speak(speakText);
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Flexible(
          child: Text(
            text,
            textAlign: TextAlign.center,
            style: TextStyle(
              fontSize: fontSize,
              fontWeight: FontWeight.w900,
              color: const Color(0xFF30161A),
            ),
          ),
        ),
        const SizedBox(width: 8),
        IconButton(
          onPressed: _speak,
          icon: const Icon(
            Icons.mic_none_rounded,
            color: Color(0xFF30161A),
            size: 28,
          ),
        ),
      ],
    );
  }
}