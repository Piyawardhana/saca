import 'package:flutter/material.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/QuestionTwoPage.dart';
import 'package:saca_project/Screens/ReviewPage.dart';

class OtherPainPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;
  final String duration;
  final bool voiceMode;

  final String? severity;
  final bool? takingMedication;

  const OtherPainPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
    required this.duration,
    this.voiceMode = false,
    this.severity,
    this.takingMedication,
  });

  @override
  State<OtherPainPage> createState() => _OtherPainPageState();
}

class _OtherPainPageState extends State<OtherPainPage> {
  final stt.SpeechToText speech = stt.SpeechToText();
  final TextEditingController voiceTextController = TextEditingController();

  bool isListening = false;
  final Set<String> selectedChanges = {};

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  final List<Map<String, dynamic>> options = [
    {'label': 'New Food', 'pit': 'New food', 'icon': Icons.restaurant_rounded},
    {'label': 'Food Poisoning Suspected', 'pit': 'Food poisoning pika', 'icon': Icons.sick_rounded},
    {'label': 'Less Sleep', 'pit': 'Sleep wiya', 'icon': Icons.bedtime_rounded},
    {'label': 'High Stress', 'pit': 'Stress palya wiya', 'icon': Icons.psychology_rounded},
    {'label': 'Heavy Physical Work', 'pit': 'Work tjuta', 'icon': Icons.fitness_center_rounded},
    {'label': 'Travel Recently', 'pit': 'Travel palyanu', 'icon': Icons.flight_takeoff_rounded},
    {'label': 'Alcohol or Smoking', 'pit': 'Smoking/alcohol', 'icon': Icons.smoking_rooms_rounded},
    {'label': 'No Major Change', 'pit': 'Change wiya', 'icon': Icons.check_circle_rounded},
  ];

  void toggleOption(String value) {
    setState(() {
      if (value == 'No Major Change') {
        selectedChanges.clear();
        selectedChanges.add(value);
        return;
      }

      selectedChanges.remove('No Major Change');

      if (selectedChanges.contains(value)) {
        selectedChanges.remove(value);
      } else {
        selectedChanges.add(value);
      }
    });
  }

  void selectVoiceOption(String value) {
    if (value == 'No Major Change') {
      selectedChanges.clear();
      selectedChanges.add(value);
      return;
    }

    selectedChanges.remove('No Major Change');
    selectedChanges.add(value);
  }

  void detectLifestyle(String words) {
    final w = words.toLowerCase();

    setState(() {
      if (w.contains('no change') || w.contains('nothing') || w.contains('no major')) {
        selectVoiceOption('No Major Change');
        return;
      }

      if (w.contains('new food') || w.contains('food')) {
        selectVoiceOption('New Food');
      }
      if (w.contains('poison')) {
        selectVoiceOption('Food Poisoning Suspected');
      }
      if (w.contains('sleep')) {
        selectVoiceOption('Less Sleep');
      }
      if (w.contains('stress')) {
        selectVoiceOption('High Stress');
      }
      if (w.contains('work') || w.contains('physical') || w.contains('heavy')) {
        selectVoiceOption('Heavy Physical Work');
      }
      if (w.contains('travel')) {
        selectVoiceOption('Travel Recently');
      }
      if (w.contains('alcohol') || w.contains('smoking') || w.contains('smoke')) {
        selectVoiceOption('Alcohol or Smoking');
      }
    });
  }

  Future<void> startVoiceLifestyle() async {
    final available = await speech.initialize();
    if (!available) return;

    setState(() {
      isListening = true;
    });

    speech.listen(
      localeId: 'en_US',
      onResult: (result) {
        voiceTextController.text = result.recognizedWords;
        detectLifestyle(result.recognizedWords);
      },
    );

    await Future.delayed(const Duration(seconds: 4));
    await speech.stop();

    if (!mounted) return;

    setState(() {
      isListening = false;
    });
  }

  Widget optionCard(Map<String, dynamic> item) {
    final label = item['label'] as String;
    final pit = item['pit'] as String;
    final icon = item['icon'] as IconData;
    final selected = selectedChanges.contains(label);

    return GestureDetector(
      onTap: () => toggleOption(label),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 220),
        padding: const EdgeInsets.all(18),
        decoration: BoxDecoration(
          color: selected
              ? const Color(0xFFF0EBDB).withOpacity(0.95)
              : Colors.white.withOpacity(0.72),
          borderRadius: BorderRadius.circular(24),
          border: Border.all(
            color: selected ? const Color(0xFF30161A) : Colors.white,
            width: 2,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.06),
              blurRadius: 10,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: Row(
          children: [
            Icon(icon, color: const Color(0xFF30161A), size: 34),
            const SizedBox(width: 14),
            Expanded(
              child: Text(
                t(label, pit),
                style: const TextStyle(
                  color: Color(0xFF30161A),
                  fontSize: 17,
                  fontWeight: FontWeight.w900,
                ),
              ),
            ),
            Icon(
              selected ? Icons.check_circle_rounded : Icons.radio_button_unchecked_rounded,
              color: const Color(0xFF30161A),
              size: 28,
            ),
          ],
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
          onTap: startVoiceLifestyle,
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
              : t('Tap mic and say lifestyle change', 'Mic patjala lifestyle wangkara'),
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

  void goNext() {
    final updatedSymptoms = [
  ...widget.symptoms,
  ...selectedChanges,
].toSet().toList();

    final updatedInputText = [
      widget.inputText,
      selectedChanges.join(', '),
    ].where((e) => e.trim().isNotEmpty).join(', ');

    if (widget.severity != null && widget.takingMedication != null) {
      Navigator.push(
        context,
        MaterialPageRoute(
          builder: (_) => ReviewPage(
            isEnglish: widget.isEnglish,
            symptoms: updatedSymptoms,
            inputText: updatedInputText,
            duration: widget.duration,
            severity: widget.severity!,
            takingMedication: widget.takingMedication!,
            voiceMode: widget.voiceMode,
          ),
        ),
      );
      return;
    }

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
  void dispose() {
    voiceTextController.dispose();
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
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(22),
            child: Column(
              children: [
                HeadingWithMic(
                  text: t(
                    'Have there been any recent food or lifestyle changes?',
                    'Food/lifestyle change nyuntumpa nyinanyi?',
                  ),
                  speakText: t(
                    'Select or say anything that may have affected your health.',
                    'Health-ku affect palyanu nyawa.',
                  ),
                  isEnglish: widget.isEnglish,
                ),
                const SizedBox(height: 26),
                Container(
                  width: 760,
                  padding: const EdgeInsets.all(22),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.60),
                    borderRadius: BorderRadius.circular(28),
                    border: Border.all(
                      color: Colors.white.withOpacity(0.70),
                    ),
                  ),
                  child: Column(
                    children: [
                      GridView.builder(
                        shrinkWrap: true,
                        physics: const NeverScrollableScrollPhysics(),
                        itemCount: options.length,
                        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 2,
                          mainAxisSpacing: 16,
                          crossAxisSpacing: 16,
                          childAspectRatio: 2.6,
                        ),
                        itemBuilder: (context, index) {
                          return optionCard(options[index]);
                        },
                      ),
                      voiceRecordSection(),
                    ],
                  ),
                ),
                const SizedBox(height: 28),
                CustomButton(
                  text: t('Next', 'Ankula'),
                  icon: Icons.arrow_forward_rounded,
                  onPressed: goNext,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}