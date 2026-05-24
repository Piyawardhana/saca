import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/QuestionOnePage.dart';

class BodyDetailSelectionPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;

  const BodyDetailSelectionPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
  });

  @override
  State<BodyDetailSelectionPage> createState() =>
      _BodyDetailSelectionPageState();
}

class _BodyDetailSelectionPageState extends State<BodyDetailSelectionPage> {
  final Set<String> selectedDetails = {};

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  List<String> get detailOptions {
    final lower = widget.inputText.toLowerCase();

    final List<String> options = [];

    if (lower.contains('hand')) {
      options.addAll([
        'Palm Pain',
        'Wrist Pain',
        'Thumb Pain',
        'Index Finger Pain',
        'Middle Finger Pain',
        'Ring Finger Pain',
        'Little Finger Pain',
      ]);
    }

    if (lower.contains('leg') || lower.contains('foot')) {
      options.addAll([
        'Thigh Pain',
        'Knee Pain',
        'Calf Pain',
        'Ankle Pain',
        'Foot Pain',
        'Toe Pain',
      ]);
    }

    return options.toSet().toList();
  }

  void toggleDetail(String detail) {
    setState(() {
      if (selectedDetails.contains(detail)) {
        selectedDetails.remove(detail);
      } else {
        selectedDetails.add(detail);
      }
    });
  }

  Widget detailCard(String detail) {
    final selected = selectedDetails.contains(detail);

    return GestureDetector(
      onTap: () => toggleDetail(detail),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 220),
        padding: const EdgeInsets.all(18),
        decoration: BoxDecoration(
          color: selected
              ? const Color(0xFFF0EBDB).withOpacity(0.95)
              : Colors.white.withOpacity(0.65),
          borderRadius: BorderRadius.circular(22),
          border: Border.all(
            color: selected ? const Color(0xFF30161A) : Colors.white,
            width: 2,
          ),
        ),
        child: Row(
          children: [
            Icon(
              selected
                  ? Icons.check_circle_rounded
                  : Icons.radio_button_unchecked_rounded,
              color: const Color(0xFF30161A),
              size: 28,
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Text(
                detail,
                style: const TextStyle(
                  color: Color(0xFF30161A),
                  fontSize: 17,
                  fontWeight: FontWeight.w900,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  void goNext() {
    final updatedSymptoms = [
      ...widget.symptoms,
      ...selectedDetails,
    ];

    final updatedInputText = [
      widget.inputText,
      selectedDetails.join(', '),
    ].where((e) => e.trim().isNotEmpty).join(', ');

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => QuestionOnePage(
          isEnglish: widget.isEnglish,
          symptoms: updatedSymptoms,
          inputText: updatedInputText,
          voiceMode: false,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final options = detailOptions;

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
  text: t('Select Detailed Pain Area', 'Pika detail ngurkantja'),
  speakText: t(
    'Select the detailed pain area. You can choose fingers, wrist, knee, ankle, foot, or toe pain.',
    'Pika detail ngurkantja. Finger, wrist, knee, ankle, foot, munu toe pika ngurkantjaku.',
  ),
  isEnglish: widget.isEnglish,
),
                const SizedBox(height: 22),
                Container(
                  width: 760,
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.72),
                    borderRadius: BorderRadius.circular(28),
                  ),
                  child: Column(
                    children: [
                      if (options.isEmpty)
                        const Text(
                          'No detailed body area needed.',
                          style: TextStyle(
                            color: Color(0xFF30161A),
                            fontSize: 18,
                            fontWeight: FontWeight.w800,
                          ),
                        ),
                      for (final option in options) ...[
                        detailCard(option),
                        const SizedBox(height: 14),
                      ],
                      const SizedBox(height: 8),
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(15),
                        decoration: BoxDecoration(
                          color: const Color(0xFFF0EBDB).withOpacity(0.82),
                          borderRadius: BorderRadius.circular(18),
                        ),
                        child: Text(
                          selectedDetails.isEmpty
                              ? 'Selected: No detailed area selected'
                              : 'Selected: ${selectedDetails.join(', ')}',
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            color: Color(0xFF30161A),
                            fontSize: 16,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                      ),
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
    );
  }
}