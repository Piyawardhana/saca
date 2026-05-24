import 'package:flutter/material.dart';
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
  int selectedPainScore = 5;

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  bool shouldUseForSeverity(String item) {
    final s = item.toLowerCase().trim();

    final blockedItems = [
      'new food',
      'food poisoning suspected',
      'less sleep',
      'high stress',
      'heavy physical work',
      'travel recently',
      'alcohol or smoking',
      'no major change',
    ];

    return !blockedItems.contains(s);
  }

  List<String> get painItems =>
      widget.symptoms.where(shouldUseForSeverity).toList();

  String get severity {
    if (selectedPainScore <= 3) return 'Low';
    if (selectedPainScore <= 6) return 'Moderate';
    return 'High';
  }

  String get severityText {
    if (selectedPainScore <= 3) return t('Low', 'Low');
    if (selectedPainScore <= 6) return t('Moderate', 'Moderate');
    return t('High', 'High');
  }

  Color get severityColor {
    if (selectedPainScore <= 3) return Colors.green;
    if (selectedPainScore <= 6) return Colors.orange;
    return Colors.red;
  }

  Widget _painScoreButton(int score) {
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

  Widget _severityScaleCard() {
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
              (index) => _painScoreButton(index + 1),
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
                  Colors.yellow,
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
                Text(
                  'Low',
                  style: TextStyle(
                    color: Color(0xFF30161A),
                    fontSize: 16,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                Text(
                  'Moderate',
                  style: TextStyle(
                    color: Color(0xFF30161A),
                    fontSize: 16,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                Text(
                  'High',
                  style: TextStyle(
                    color: Color(0xFF30161A),
                    fontSize: 16,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 22),

          Text(
            '${t('Selected severity', 'Pika level')}: $severityText',
            style: TextStyle(
              color: severityColor,
              fontSize: 22,
              fontWeight: FontWeight.w900,
            ),
          ),

          if (painItems.isNotEmpty) ...[
            const SizedBox(height: 18),
            Text(
              '${t('For', 'For')}: ${painItems.join(', ')}',
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: Color(0xFF30161A),
                fontSize: 15,
                fontWeight: FontWeight.w700,
              ),
            ),
          ],
        ],
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
                  'How bad is the pain? Select a number from 1 to 10.',
                  'Pika level yaaltji? Number 1 munu 10 ngurkantja.',
                ),
                isEnglish: widget.isEnglish,
              ),
              const SizedBox(height: 34),

              _severityScaleCard(),

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
                        severity: severity,
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