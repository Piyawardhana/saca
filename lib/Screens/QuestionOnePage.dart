import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/OtherPainPage.dart';

class QuestionOnePage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;
  final bool voiceMode;

  const QuestionOnePage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
    this.voiceMode = false,
  });

  @override
  State<QuestionOnePage> createState() => _QuestionOnePageState();
}

class _QuestionOnePageState extends State<QuestionOnePage> {
  String selectedDuration = '';

  String t(String en, String pit) {
    return widget.isEnglish ? pit : en;
  }

  final List<String> durations = [
    '1 Day',
    '1–2 Days',
    '1 Week',
    'More than a week',
  ];

  Widget _durationButton(String text) {
    final selected = selectedDuration == text;

    return GestureDetector(
      onTap: () {
        setState(() {
          selectedDuration = text;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        width: 360,
        margin: const EdgeInsets.only(bottom: 18),
        padding: const EdgeInsets.symmetric(
          vertical: 22,
          horizontal: 20,
        ),
        decoration: BoxDecoration(
          color: selected
              ? const Color(0xFF6A1B2A)
              : const Color(0xFF30161A),

          borderRadius: BorderRadius.circular(18),

          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.18),
              blurRadius: 12,
              offset: const Offset(0, 6),
            ),
          ],
        ),
        child: Center(
          child: Text(
            text,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 24,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
      ),
    );
  }

  PreferredSizeWidget _appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.transparent,
      elevation: 0,
      leading: Padding(
        padding: const EdgeInsets.all(10),
        child: Container(
          decoration: BoxDecoration(
            color: const Color(0xFF30161A),
            borderRadius: BorderRadius.circular(14),
          ),
          child: IconButton(
            onPressed: () => Navigator.pop(context),
            icon: const Icon(
              Icons.arrow_back_ios_new_rounded,
              color: Colors.white,
            ),
          ),
        ),
      ),
      actions: [
        Padding(
          padding: const EdgeInsets.all(10),
          child: Container(
            decoration: BoxDecoration(
              color: const Color(0xFF30161A),
              borderRadius: BorderRadius.circular(14),
            ),
            child: IconButton(
              onPressed: () {
                Navigator.popUntil(
                    context, (route) => route.isFirst);
              },
              icon: const Icon(
                Icons.home_rounded,
                color: Colors.white,
              ),
            ),
          ),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,

      appBar: _appBar(context),

      body: AppBackground(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(30),
            child: Column(
              children: [
                const SizedBox(height: 90),

                HeadingWithMic(
                  text: widget.isEnglish
                      ? 'How long have you had this?'
                      : 'Yaaltji-yaaltji nyinangi?',
                  speakText: widget.isEnglish
                      ? 'How long have you had this pain?'
                      : 'Pika nyanga yaaltji-yaaltji nyinangi?',
                  isEnglish: widget.isEnglish,
                  fontSize: 34,
                ),

                const SizedBox(height: 40),

                Container(
                  width: 520,
                  padding: const EdgeInsets.all(30),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.75),
                    borderRadius: BorderRadius.circular(28),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.18),
                        blurRadius: 18,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: Column(
                    children: durations
                        .map((e) => _durationButton(e))
                        .toList(),
                  ),
                ),

                const SizedBox(height: 30),

                if (selectedDuration.isNotEmpty)
                  CustomButton(
                    text: widget.isEnglish
                        ? 'Next'
                        : 'Ankula',
                    icon: Icons.arrow_forward_rounded,
                    onPressed: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => OtherPainPage(
                            isEnglish: widget.isEnglish,
                            symptoms: widget.symptoms,
                            inputText: widget.inputText,
                            duration: selectedDuration,
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
    );
  }
}