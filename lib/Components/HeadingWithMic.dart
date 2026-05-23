import 'package:flutter/material.dart';
import 'package:flutter_tts/flutter_tts.dart';

class HeadingWithMic extends StatelessWidget {
  final String text;
  final String speakText;
  final double fontSize;

  const HeadingWithMic({
    super.key,
    required this.text,
    required this.speakText,
    this.fontSize = 30,
  });

  Future<void> _speak() async {
    final FlutterTts tts = FlutterTts();
    await tts.stop();
    await tts.setLanguage('en-US');
    await tts.setSpeechRate(0.45);
    await tts.setVolume(1.0);
    await tts.speak(speakText);
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