import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/QuestionTwoPage.dart';

class VoiceOtherPainPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;
  final String duration;
  final bool voiceMode;

  const VoiceOtherPainPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
    required this.duration,
    this.voiceMode = false,
  });

  @override
  State<VoiceOtherPainPage> createState() => _VoiceOtherPainPageState();
}

class _VoiceOtherPainPageState extends State<VoiceOtherPainPage> {
  final stt.SpeechToText speech = stt.SpeechToText();
  bool isRecording = false;
  String recordedPainText = '';

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
              recordedPainText = result.recognizedWords;
            });
          },
        );
      }
    } else {
      await speech.stop();
      setState(() => isRecording = false);
    }
  }

  List<String> extractOtherPain(String text) {
    final lower = text.toLowerCase();
    final List<String> painParts = [];

    if (lower.contains('neck')) painParts.add('Neck Pain');
    if (lower.contains('shoulder')) painParts.add('Shoulder Pain');
    if (lower.contains('hand')) painParts.add('Hand Pain');
    if (lower.contains('knee')) painParts.add('Knee Pain');
    if (lower.contains('foot') || lower.contains('feet')) {
      painParts.add('Foot Pain');
    }
    if (lower.contains('throat')) painParts.add('Throat Pain');
    if (lower.contains('ear')) painParts.add('Ear Pain');
    if (lower.contains('eye')) painParts.add('Eye Pain');

    return painParts.toSet().toList();
  }

  @override
  void dispose() {
    speech.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final detectedPain = extractOtherPain(recordedPainText);

    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SafeArea(
          bottom: false,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(22),
            child: Center(
              child: Container(
                width: 720,
                padding: const EdgeInsets.all(28),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.72),
                  borderRadius: BorderRadius.circular(28),
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    HeadingWithMic(
  text: t(
    'Any other pain in your body?',
    'Kurunpa kutjupa pika nyinanyi?',
  ),
  speakText: t(
    'Any other pain in your body? Say neck pain, shoulder pain, hand pain, knee pain, foot pain, throat pain, ear pain, eye pain, or no other pain.',
    'Kurunpa kutjupa pika nyinanyi? Neck pika, shoulder pika, mara pika, knee pika, tjina pika, throat pika, ear pika, eye pika, munu wiya wangkara.',
  ),
  isEnglish: widget.isEnglish,
),
                    const SizedBox(height: 16),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF0EBDB).withOpacity(0.75),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: const Text(
                        'Hint: Say "neck pain", "shoulder pain", "knee pain", "ear pain", "eye pain", or "no other pain".',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          color: Color(0xFF30161A),
                          fontSize: 15,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
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
                          color:
                              isRecording ? Colors.red : const Color(0xFF30161A),
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
                          isRecording
                              ? Icons.stop_rounded
                              : Icons.mic_rounded,
                          color: const Color(0xFFF0EBDB),
                          size: 48,
                        ),
                      ),
                    ),
                    const SizedBox(height: 14),
                    Text(
                      isRecording ? 'Listening...' : 'Tap mic to record',
                      style: const TextStyle(
                        fontSize: 16,
                        color: Color(0xFF30161A),
                        fontWeight: FontWeight.w800,
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
                        recordedPainText.isEmpty
                            ? 'Recorded other pain appears here'
                            : recordedPainText,
                        style: const TextStyle(
                          fontSize: 16,
                          color: Color(0xFF30161A),
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                    ),
                    const SizedBox(height: 18),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF0EBDB).withOpacity(0.75),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      
                    ),
                    const SizedBox(height: 26),
                    CustomButton(
                      text: t('Next', 'Ankula'),
                      icon: Icons.arrow_forward_rounded,
                      onPressed: () {
                        final updatedSymptoms = [
                          ...widget.symptoms,
                          ...detectedPain,
                        ];

                        final updatedInputText = [
                          widget.inputText,
                          recordedPainText,
                        ].where((e) => e.trim().isNotEmpty).join(', ');

                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (_) => QuestionTwoPage(
                              isEnglish: widget.isEnglish,
                              symptoms: updatedSymptoms,
                              inputText: updatedInputText,
                              duration: widget.duration,
                              voiceMode: widget.voiceMode,
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