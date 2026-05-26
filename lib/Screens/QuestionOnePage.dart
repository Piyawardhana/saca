import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
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
  final stt.SpeechToText speech = stt.SpeechToText();
  final TextEditingController voiceTextController = TextEditingController();

  bool isListening = false;
  String selectedDuration = '';

  String t(String en, String pit) {
    return widget.isEnglish ? en : pit;
  }

 final List<Map<String, String>> durationOptions = [
  {
    'en': '1 Day',
    'pit': 'Tjintu kutju',
  },
  {
    'en': '1–2 Days',
    'pit': 'Tjintu kutju munu kutjara',
  },
  {
    'en': '1 Week',
    'pit': 'Wiki kutju',
  },
  {
    'en': 'More than a week',
    'pit': 'Wiki kutjupa alatji',
  },
];

  Future<void> startVoiceDuration() async {
    final available = await speech.initialize();
    if (!available) return;

    setState(() {
      isListening = true;
    });

    speech.listen(
      onResult: (result) {
        final words = result.recognizedWords.toLowerCase();

        setState(() {
          voiceTextController.text = result.recognizedWords;

          if (words.contains('more') ||
              words.contains('more than a week')) {
            selectedDuration = 'More than a week';
          } else if (words.contains('week')) {
            selectedDuration = '1 Week';
          } else if (words.contains('two') ||
              words.contains('2') ||
              words.contains('1 2') ||
              words.contains('one two')) {
            selectedDuration = '1–2 Days';
          } else if (words.contains('one') || words.contains('1')) {
            selectedDuration = '1 Day';
          }
        });
      },
    );

    await Future.delayed(const Duration(seconds: 4));
    await speech.stop();

    setState(() {
      isListening = false;
    });
  }

Widget durationButton(Map<String, String> item) {

  final value = item['en']!;
  final label =
      widget.isEnglish
          ? item['en']!
          : item['pit']!;

  final selected =
      selectedDuration == value;

  return GestureDetector(
    onTap: () {
      setState(() {
        selectedDuration = value;
      });
    },
    child: AnimatedContainer(
      duration: const Duration(milliseconds: 220),
      width: 450,
      margin: const EdgeInsets.only(bottom: 18),
      padding: const EdgeInsets.symmetric(
        vertical: 24,
        horizontal: 18,
      ),
      decoration: BoxDecoration(
        color: selected
            ? const Color(0xFF7A1C30)
            : const Color(0xFF30161A),
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.20),
            blurRadius: 12,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Text(
        label,
        textAlign: TextAlign.center,
        style: const TextStyle(
          color: Colors.white,
          fontSize: 22,
          fontWeight: FontWeight.w900,
        ),
      ),
    ),
  );
}

  Widget _voiceInputSection() {
    if (!widget.voiceMode) return const SizedBox.shrink();

    return Column(
      children: [
        const SizedBox(height: 22),

        GestureDetector(
          onTap: startVoiceDuration,
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 220),
            width: isListening ? 92 : 78,
            height: isListening ? 92 : 78,
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

        const SizedBox(height: 14),

        Text(
          isListening
              ? t('Listening...', 'Kulini...')
              : t('Tap mic and say duration', 'Mic patjala duration wangkara'),
          style: const TextStyle(
            color: Color(0xFF30161A),
            fontSize: 16,
            fontWeight: FontWeight.w900,
          ),
        ),

        const SizedBox(height: 14),

        SizedBox(
          width: 420,
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

PreferredSizeWidget _appBar(BuildContext context) {return AppBar(
  backgroundColor: Colors.white.withOpacity(0.95),
  elevation: 0,
  surfaceTintColor: Colors.transparent,

  leading: IconButton(
    onPressed: () => Navigator.pop(context),
    icon: const Icon(
      Icons.arrow_back_ios_new_rounded,
      color: Color(0xFF30161A),
      size: 30,
    ),
  ),

  titleSpacing: 0,

  title: const Row(
    children: [
      Icon(
        Icons.favorite_rounded,
        color: Color(0xFF30161A),
        size: 30,
      ),

      SizedBox(width: 12),

      Text(
        'SACA',
        style: TextStyle(
          color: Color(0xFF30161A),
          fontWeight: FontWeight.w900,
          fontSize: 28,
        ),
      ),
    ],
  ),

  actions: [
    Padding(
      padding: const EdgeInsets.only(right: 12),
      child: Center(
        child: Container(
          width: 52,
          height: 52,
          decoration: BoxDecoration(
            color: const Color(0xFFF0EBDB),
            borderRadius: BorderRadius.circular(16),
          ),
          child: IconButton(
            onPressed: () {
              Navigator.popUntil(
                context,
                (route) => route.isFirst,
              );
            },
            icon: const Icon(
              Icons.home_rounded,
              color: Color(0xFF30161A),
              size: 28,
            ),
          ),
        ),
      ),
    ),
  ],
);}

  @override
  void dispose() {
    voiceTextController.dispose();
    speech.stop();
    super.dispose();
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
                    children: [
                      ...durationOptions.map((e) => durationButton(e)).toList(),
                      _voiceInputSection(),
                      const SizedBox(height: 30),

    CustomButton(
      text: widget.isEnglish ? 'Next' : 'Ankula',
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

                const SizedBox(height: 30),

                if (selectedDuration.isNotEmpty)
                  CustomButton(
                    text: widget.isEnglish ? 'Next' : 'Ankula',
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