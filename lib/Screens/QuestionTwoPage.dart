import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'QuestionThreePage.dart';

class QuestionTwoPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;
  final String duration;
  final bool voiceMode;

  const QuestionTwoPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
    required this.duration,
    this.voiceMode = false,
  });

  @override
  State<QuestionTwoPage> createState() => _QuestionTwoPageState();
}

class _QuestionTwoPageState extends State<QuestionTwoPage> {
  final stt.SpeechToText speech = stt.SpeechToText();
  final TextEditingController voiceTextController = TextEditingController();

  bool isListening = false;
  int selectedPainScore = 5;

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  String get severity {
    if (selectedPainScore <= 3) return 'Low';
    if (selectedPainScore <= 6) return 'Moderate';
    return 'High';
  }

  Color get severityColor {
    if (selectedPainScore <= 3) return Colors.green;
    if (selectedPainScore <= 6) return Colors.orange;
    return Colors.red;
  }

  Future<void> recordPainScore() async {
    final available = await speech.initialize();
    if (!available) return;

    setState(() {
      isListening = true;
    });

    speech.listen(
      localeId: 'en_US',
      onResult: (result) {
        final words = result.recognizedWords.toLowerCase();

        setState(() {
          voiceTextController.text = result.recognizedWords;

          if (words.contains('ten') || words.contains('10')) {
            selectedPainScore = 10;
          } else if (words.contains('nine') || words.contains('9')) {
            selectedPainScore = 9;
          } else if (words.contains('eight') || words.contains('8')) {
            selectedPainScore = 8;
          } else if (words.contains('seven') || words.contains('7')) {
            selectedPainScore = 7;
          } else if (words.contains('six') || words.contains('6')) {
            selectedPainScore = 6;
          } else if (words.contains('five') || words.contains('5')) {
            selectedPainScore = 5;
          } else if (words.contains('four') || words.contains('4')) {
            selectedPainScore = 4;
          } else if (words.contains('three') || words.contains('3')) {
            selectedPainScore = 3;
          } else if (words.contains('two') || words.contains('2')) {
            selectedPainScore = 2;
          } else if (words.contains('one') || words.contains('1')) {
            selectedPainScore = 1;
          }
        });
      },
    );

    await Future.delayed(const Duration(seconds: 4));
    await speech.stop();

    if (!mounted) return;

    setState(() {
      isListening = false;
    });
  }

  Widget painScoreButton(int score) {
    final selected = selectedPainScore == score;

    return GestureDetector(
      onTap: () {
        setState(() {
          selectedPainScore = score;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        width: 52,
        height: 52,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          color: selected ? const Color(0xFFE8BE2F) : const Color(0xFF30161A),
          borderRadius: BorderRadius.circular(10),
          boxShadow: selected
              ? [
                  BoxShadow(
                    color: Colors.orange.withOpacity(0.45),
                    blurRadius: 12,
                    offset: const Offset(0, 5),
                  ),
                ]
              : [],
        ),
        child: Text(
          '$score',
          style: TextStyle(
            color: selected ? const Color(0xFF30161A) : Colors.white,
            fontSize: 20,
            fontWeight: FontWeight.w900,
          ),
        ),
      ),
    );
  }

  Widget voiceRecordSection() {
    if (!widget.voiceMode) return const SizedBox.shrink();

    return Column(
      children: [
        const SizedBox(height: 26),
        GestureDetector(
          onTap: recordPainScore,
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 220),
            width: isListening ? 92 : 76,
            height: isListening ? 92 : 76,
            decoration: BoxDecoration(
              color: isListening ? Colors.red : const Color(0xFF30161A),
              shape: BoxShape.circle,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.25),
                  blurRadius: 14,
                  offset: const Offset(0, 6),
                ),
              ],
            ),
            child: Icon(
              isListening ? Icons.stop_rounded : Icons.mic_rounded,
              color: Colors.white,
              size: 40,
            ),
          ),
        ),
        const SizedBox(height: 12),
        Text(
          isListening
              ? t('Listening...', 'Kulini...')
              : t('Tap mic and say pain score', 'Mic patjala pain score wangkara'),
          style: const TextStyle(
            color: Color(0xFF30161A),
            fontSize: 16,
            fontWeight: FontWeight.w900,
          ),
        ),
        const SizedBox(height: 14),
        SizedBox(
          width: 450,
          child: TextField(
            controller: voiceTextController,
            readOnly: true,
            maxLines: 2,
            decoration: InputDecoration(
              filled: true,
              fillColor: Colors.white.withOpacity(0.92),
              hintText: t(
                'Recorded speech will appear here',
                'Recorded wangka nyanganyi',
              ),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(18),
                borderSide: BorderSide.none,
              ),
            ),
            style: const TextStyle(
              color: Color(0xFF30161A),
              fontSize: 16,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
      ],
    );
  }

  Widget severityScaleCard() {
    return Container(
      width: 760,
      padding: const EdgeInsets.all(28),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.72),
        borderRadius: BorderRadius.circular(24),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.16),
            blurRadius: 16,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Column(
        children: [
          Wrap(
            spacing: 12,
            runSpacing: 12,
            alignment: WrapAlignment.center,
            children: List.generate(
              10,
              (index) => painScoreButton(index + 1),
            ),
          ),
          const SizedBox(height: 24),
          Container(
            width: 520,
            height: 20,
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(18),
              gradient: const LinearGradient(
                colors: [
                  Colors.green,
                  Colors.orange,
                  Colors.red,
                ],
              ),
            ),
          ),
          const SizedBox(height: 18),
          const SizedBox(
            width: 560,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Mild', style: TextStyle(fontWeight: FontWeight.w900)),
                Text('Moderate', style: TextStyle(fontWeight: FontWeight.w900)),
                Text('Severe', style: TextStyle(fontWeight: FontWeight.w900)),
              ],
            ),
          ),
          const SizedBox(height: 22),
          Text(
            '${t('Pain Score', 'Pika score')}: $selectedPainScore',
            style: TextStyle(
              color: severityColor,
              fontSize: 24,
              fontWeight: FontWeight.w900,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            '${t('Severity', 'Pika')}: $severity',
            style: TextStyle(
              color: severityColor,
              fontSize: 18,
              fontWeight: FontWeight.w800,
            ),
          ),
          voiceRecordSection(),
        ],
      ),
    );
  }

  @override
  void dispose() {
    voiceTextController.dispose();
    speech.stop();
    super.dispose();
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
          Icon(Icons.favorite_rounded, color: Color(0xFF30161A)),
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
                Navigator.popUntil(context, (route) => route.isFirst);
              },
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            children: [
              HeadingWithMic(
                text: t('How bad is the pain?', 'Pika level yaaltji?'),
                speakText: t(
                  'How bad is the pain? Select or say a number from one to ten.',
                  'Pika level yaaltji? Number 1 munu 10 ngurkantja.',
                ),
                isEnglish: widget.isEnglish,
              ),
              const SizedBox(height: 34),
              severityScaleCard(),
              const SizedBox(height: 34),
              CustomButton(
                text: t('Next', 'Ankula'),
                icon: Icons.arrow_forward_rounded,
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => QuestionThreePage(
                        isEnglish: widget.isEnglish,
                        symptoms: widget.symptoms,
                        duration: widget.duration,
                        severity: selectedPainScore.toString(),
                        inputText: widget.inputText,
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
    );
  }
}