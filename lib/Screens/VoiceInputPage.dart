import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/QuestionOnePage.dart';

class VoiceInputPage extends StatefulWidget {
  final bool isEnglish;

  const VoiceInputPage({
    super.key,
    required this.isEnglish,
  });

  @override
  State<VoiceInputPage> createState() => _VoiceInputPageState();
}

class _VoiceInputPageState extends State<VoiceInputPage> {
  final stt.SpeechToText speech = stt.SpeechToText();
  bool isRecording = false;
  String retrievedText = '';

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  Future<void> toggleRecord() async {
    if (!isRecording) {
      final available = await speech.initialize();

      if (available) {
        setState(() => isRecording = true);

        speech.listen(
          localeId: 'en_US',
          onResult: (result) {
            setState(() {
              retrievedText = result.recognizedWords;
            });
          },
        );
      }
    } else {
      await speech.stop();
      setState(() => isRecording = false);
    }
  }

  @override
  void dispose() {
    speech.stop();
    super.dispose();
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
              width: 620,
              padding: const EdgeInsets.all(30),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.38),
                borderRadius: BorderRadius.circular(28),
                border: Border.all(color: Colors.white.withOpacity(0.45)),
              ),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  HeadingWithMic(
                    text: t('Voice Input', 'Wangka Tjarpanyi'),
                    speakText: 'Voice Input. Tap the microphone and say your symptoms.',
                  ),
                  const SizedBox(height: 24),
                  GestureDetector(
                    onTap: toggleRecord,
                    child: AnimatedContainer(
                      duration: const Duration(milliseconds: 250),
                      width: isRecording ? 120 : 108,
                      height: isRecording ? 120 : 108,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: isRecording ? Colors.red : const Color(0xFF30161A),
                        boxShadow: [
                          BoxShadow(
                            color: isRecording
                                ? Colors.red.withOpacity(0.45)
                                : const Color(0xFF30161A).withOpacity(0.35),
                            blurRadius: 18,
                            spreadRadius: 2,
                          ),
                        ],
                      ),
                      child: Icon(
                        isRecording ? Icons.stop_rounded : Icons.mic_rounded,
                        color: const Color(0xFFF0EBDB),
                        size: 48,
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  Text(
                    isRecording
                        ? t('Listening...', 'Kulini...')
                        : t('Tap mic to speak', 'Mic tjutjura wangka'),
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.w700,
                      color: Color(0xFF30161A),
                    ),
                  ),
                  const SizedBox(height: 22),
                  Container(
                    width: double.infinity,
                    padding: const EdgeInsets.all(18),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.85),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      retrievedText.isEmpty
                          ? t('Recorded voice text appears here', 'Wangka nyanga nyinanyi')
                          : retrievedText,
                      style: const TextStyle(
                        fontSize: 16,
                        color: Color(0xFF30161A),
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  const SizedBox(height: 26),
                  CustomButton(
                    text: t('Next', 'Ankula'),
                    icon: Icons.arrow_forward_rounded,
                    onPressed: () {
                      final symptoms = retrievedText
                          .split(',')
                          .map((e) => e.trim())
                          .where((e) => e.isNotEmpty)
                          .toList();

                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => QuestionOnePage(
                            isEnglish: widget.isEnglish,
                            symptoms: symptoms,
                            inputText: retrievedText,
                            voiceMode: true,
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

    actions: [
      Padding(
        padding: const EdgeInsets.only(right: 10),
        child: Container(
          decoration: BoxDecoration(
            color: const Color(0xFFF0EBDB),
            borderRadius: BorderRadius.circular(14),
          ),
          child: IconButton(
            tooltip: 'Home',
            icon: const Icon(
              Icons.home_rounded,
              color: Color(0xFF30161A),
              size: 28,
            ),
            onPressed: () {
              Navigator.popUntil(
                context,
                (route) => route.isFirst,
              );
            },
          ),
        ),
      ),
    ],
  );
}
}