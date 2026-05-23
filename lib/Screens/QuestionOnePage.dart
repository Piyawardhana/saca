import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'OtherPainPage.dart';
import 'VoiceOtherPainPage.dart';

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

  bool isListening = false;
  String recordedDurationText = '';

  final List<Map<String, String>> durationOptions = [
    {'en': '1 Day', 'pit': '1 Tjintu'},
    {'en': '2 Days', 'pit': '2 Tjintu'},
    {'en': '3 Days', 'pit': '3 Tjintu'},
    {'en': '4 Days', 'pit': '4 Tjintu'},
    {'en': '5 Days', 'pit': '5 Tjintu'},
    {'en': '6 Days', 'pit': '6 Tjintu'},
    {'en': '7 Days', 'pit': '7 Tjintu'},
    {'en': '8 Days', 'pit': '8 Tjintu'},
    {'en': '9 Days', 'pit': '9 Tjintu'},
    {'en': '10 Days', 'pit': '10 Tjintu'},
    {'en': '1 Week', 'pit': '1 Wiki'},
    {'en': '3 Weeks', 'pit': '3 Wiki'},
    {'en': '1 Month', 'pit': '1 Pira'},
    {'en': 'More than 1 Month', 'pit': 'Pira kutju alatji'},
  ];

  int selectedDurationIndex = 0;

  String get selectedDuration => durationOptions[selectedDurationIndex]['en']!;

  String get selectedDurationText => widget.isEnglish
      ? durationOptions[selectedDurationIndex]['en']!
      : durationOptions[selectedDurationIndex]['pit']!;

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  void setDuration(String value) {
    final index = durationOptions.indexWhere((item) => item['en'] == value);
    if (index != -1) {
      selectedDurationIndex = index;
    }
  }

  Future<void> recordDuration() async {
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
          recordedDurationText = result.recognizedWords;

          if (words.contains('more')) {
            setDuration('More than 1 Month');
          } else if (words.contains('month')) {
            setDuration('1 Month');
          } else if (words.contains('three week') || words.contains('3 week')) {
            setDuration('3 Weeks');
          } else if (words.contains('week')) {
            setDuration('1 Week');
          } else if (words.contains('ten') || words.contains('10')) {
            setDuration('10 Days');
          } else if (words.contains('nine') || words.contains('9')) {
            setDuration('9 Days');
          } else if (words.contains('eight') || words.contains('8')) {
            setDuration('8 Days');
          } else if (words.contains('seven') || words.contains('7')) {
            setDuration('7 Days');
          } else if (words.contains('six') || words.contains('6')) {
            setDuration('6 Days');
          } else if (words.contains('five') || words.contains('5')) {
            setDuration('5 Days');
          } else if (words.contains('four') || words.contains('4')) {
            setDuration('4 Days');
          } else if (words.contains('three') || words.contains('3')) {
            setDuration('3 Days');
          } else if (words.contains('two') || words.contains('2')) {
            setDuration('2 Days');
          } else if (words.contains('one') || words.contains('1')) {
            setDuration('1 Day');
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

  Widget durationSlider() {
    return Column(
      children: [
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(18),
          decoration: BoxDecoration(
            color: const Color(0xFFF0EBDB).withOpacity(0.85),
            borderRadius: BorderRadius.circular(20),
            border: Border.all(
              color: const Color(0xFF30161A).withOpacity(0.15),
            ),
          ),
          child: Column(
            children: [
              Text(
                selectedDurationText,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  color: Color(0xFF30161A),
                  fontSize: 25,
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(height: 16),
              SliderTheme(
                data: SliderTheme.of(context).copyWith(
                  activeTrackColor: const Color(0xFF30161A),
                  inactiveTrackColor: Colors.white,
                  thumbColor: const Color(0xFF30161A),
                  overlayColor: const Color(0xFF30161A).withOpacity(0.15),
                  trackHeight: 8,
                  valueIndicatorColor: const Color(0xFF30161A),
                  valueIndicatorTextStyle: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w800,
                  ),
                ),
                child: Slider(
                  value: selectedDurationIndex.toDouble(),
                  min: 0,
                  max: (durationOptions.length - 1).toDouble(),
                  divisions: durationOptions.length - 1,
                  label: selectedDurationText,
                  onChanged: (value) {
                    setState(() {
                      selectedDurationIndex = value.round();
                    });
                  },
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        Wrap(
          spacing: 8,
          runSpacing: 8,
          alignment: WrapAlignment.center,
          children: List.generate(durationOptions.length, (index) {
            final selected = selectedDurationIndex == index;
            final text = widget.isEnglish
                ? durationOptions[index]['en']!
                : durationOptions[index]['pit']!;

            return GestureDetector(
              onTap: () {
                setState(() {
                  selectedDurationIndex = index;
                });
              },
              child: Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 12,
                  vertical: 8,
                ),
                decoration: BoxDecoration(
                  color: selected
                      ? const Color(0xFF30161A)
                      : Colors.white.withOpacity(0.85),
                  borderRadius: BorderRadius.circular(20),
                  border: Border.all(
                    color: const Color(0xFF30161A).withOpacity(0.2),
                  ),
                ),
                child: Text(
                  text,
                  style: TextStyle(
                    color: selected ? Colors.white : const Color(0xFF30161A),
                    fontSize: 13,
                    fontWeight: FontWeight.w800,
                  ),
                ),
              ),
            );
          }),
        ),
      ],
    );
  }

  @override
  void dispose() {
    speech.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final heading = t(
      'How long have you had the pain?',
      'Pika nyanga yaaltji-yaaltji nyinangi?',
    );

    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SafeArea(
          bottom: false,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(22),
            child: Column(
              children: [
                HeadingWithMic(
                  text: t('Questions', 'Kulintjaku tjuta'),
                  speakText: 'Questions. How long have you had the pain?',
                ),
                const SizedBox(height: 24),
                Container(
                  width: 780,
                  padding: const EdgeInsets.all(28),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.72),
                    borderRadius: BorderRadius.circular(28),
                  ),
                  child: Column(
                    children: [
                      Text(
                        '1. $heading',
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          fontSize: 25,
                          fontWeight: FontWeight.w900,
                          color: Color(0xFF30161A),
                        ),
                      ),
                      const SizedBox(height: 28),
                      durationSlider(),
                      if (widget.voiceMode) ...[
                        const SizedBox(height: 24),
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: const Color(0xFFF0EBDB).withOpacity(0.75),
                            borderRadius: BorderRadius.circular(16),
                          ),
                          child: Text(
                            t(
                              'Hint: Say "1 day", "5 days", "10 days", "1 week", "3 weeks", "1 month", or "more than 1 month".',
                              'Hint: 1 Tjiṉṯu, 5 Tjiṉṯu, 10 Tjiṉṯu, 1 Wiki, 3 Wiki, 1 Piṟa.',
                            ),
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                              color: Color(0xFF30161A),
                              fontSize: 15,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                        const SizedBox(height: 22),
                        GestureDetector(
                          onTap: recordDuration,
                          child: AnimatedContainer(
                            duration: const Duration(milliseconds: 250),
                            width: isListening ? 120 : 108,
                            height: isListening ? 120 : 108,
                            decoration: BoxDecoration(
                              shape: BoxShape.circle,
                              color: isListening
                                  ? Colors.red
                                  : const Color(0xFF30161A),
                            ),
                            child: Icon(
                              isListening
                                  ? Icons.stop_rounded
                                  : Icons.mic_rounded,
                              color: const Color(0xFFF0EBDB),
                              size: 48,
                            ),
                          ),
                        ),
                        const SizedBox(height: 14),
                        Text(
                          isListening
                              ? t('Listening...', 'Kulini...')
                              : t('Tap mic to record duration',
                                  'Mic patjara duration wangkara'),
                          style: const TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w800,
                            color: Color(0xFF30161A),
                          ),
                        ),
                        const SizedBox(height: 18),
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.85),
                            borderRadius: BorderRadius.circular(18),
                          ),
                          child: Text(
                            recordedDurationText.isEmpty
                                ? t('Recorded duration appears here',
                                    'Recorded duration nyanganyi')
                                : recordedDurationText,
                            style: const TextStyle(
                              fontSize: 16,
                              color: Color(0xFF30161A),
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                        ),
                      ],
                    ],
                  ),
                ),
                const SizedBox(height: 28),
                CustomButton(
                  text: t('Next', 'Ankula'),
                  icon: Icons.arrow_forward_rounded,
                  onPressed: () {
                    if (widget.voiceMode) {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => VoiceOtherPainPage(
                            isEnglish: widget.isEnglish,
                            symptoms: widget.symptoms,
                            inputText: widget.inputText,
                            duration: selectedDuration,
                            voiceMode: widget.voiceMode,
                          ),
                        ),
                      );
                    } else {
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
                    }
                  },
                ),
              ],
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