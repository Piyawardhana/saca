import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/ReviewPage.dart';

class QuestionThreePage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String duration;
  final String severity;
  final String inputText;
  final bool voiceMode;

  const QuestionThreePage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.duration,
    required this.severity,
    required this.inputText,
    this.voiceMode = false,
  });

  @override
  State<QuestionThreePage> createState() => _QuestionThreePageState();
}

class _QuestionThreePageState extends State<QuestionThreePage> {
  String selectedMedication = 'Yes';

  bool get takingMedication => selectedMedication == 'Yes';

  String t(String en, String pit) {
    return widget.isEnglish ? en : pit;
  }

  Color get severityColor {
    if (widget.severity == 'High') return Colors.red;
    if (widget.severity == 'Moderate') return Colors.orange;
    return Colors.green;
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
              _pageTitle(),
              const SizedBox(height: 24),
              _questionCard(),
              const SizedBox(height: 22),
              _severityCard(),
              const SizedBox(height: 22),
              if (widget.severity == 'High') _noticeCard(),
              const SizedBox(height: 28),
              CustomButton(
                text: t('See Results', 'Nyangatja nyawa'),
                icon: Icons.arrow_forward_rounded,
                gradientColors: const [
                  Color(0xFF30161A),
                  Color(0xFF5A2A2F),
                ],
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => ReviewPage(
                        isEnglish: widget.isEnglish,
                        symptoms: widget.symptoms,
                        duration: widget.duration,
                        severity: widget.severity,
                        inputText: widget.inputText,
                        takingMedication: takingMedication,
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

  Widget _questionCard() {
    return Container(
      width: 780,
      padding: const EdgeInsets.all(28),
      decoration: _cardDecoration(),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            t(
              '3. Are you taking any medications?',
              '3. Nyuntu medicine taking?',
            ),
            style: const TextStyle(
              fontSize: 23,
              fontWeight: FontWeight.w900,
              color: Color(0xFF30161A),
            ),
          ),
          const SizedBox(height: 24),
          Row(
            children: [
              _optionButton(
                label: t('Yes', 'Uwa'),
                value: 'Yes',
              ),
              const SizedBox(width: 14),
              _optionButton(
                label: t('No', 'Wiya'),
                value: 'No',
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _optionButton({
    required String label,
    required String value,
  }) {
    final bool isSelected = selectedMedication == value;

    return InkWell(
      borderRadius: BorderRadius.circular(16),
      onTap: () {
        setState(() {
          selectedMedication = value;
        });
      },
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 180),
        padding: const EdgeInsets.symmetric(horizontal: 28, vertical: 16),
        decoration: BoxDecoration(
          color: isSelected
              ? const Color(0xFFF0EBDB).withOpacity(0.95)
              : Colors.white.withOpacity(0.85),
          borderRadius: BorderRadius.circular(16),
          border: Border.all(
            color: isSelected ? const Color(0xFF30161A) : Colors.grey.shade300,
            width: 1.5,
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (isSelected) ...[
              const Icon(
                Icons.check_rounded,
                color: Color(0xFF30161A),
                size: 20,
              ),
              const SizedBox(width: 8),
            ],
            Text(
              label,
              style: TextStyle(
                fontSize: 17,
                fontWeight: FontWeight.w900,
                color: isSelected
                    ? const Color(0xFF30161A)
                    : const Color(0xFF334155),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _severityCard() {
    return Container(
      width: 780,
      padding: const EdgeInsets.all(22),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.72),
        borderRadius: BorderRadius.circular(26),
        border: Border.all(
          color: severityColor.withOpacity(0.55),
          width: 1.5,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            blurRadius: 14,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: severityColor.withOpacity(0.15),
              shape: BoxShape.circle,
            ),
            child: Icon(
              Icons.health_and_safety_rounded,
              color: severityColor,
              size: 26,
            ),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Text(
              '${t("Current overall severity", "Pika overall")}: ${widget.severity}',
              style: TextStyle(
                color: severityColor,
                fontSize: 20,
                fontWeight: FontWeight.w900,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _noticeCard() {
    return Container(
      width: 780,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.72),
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.red.withOpacity(0.55), width: 1.5),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            blurRadius: 14,
            offset: const Offset(0, 6),
          ),
        ],
      ),
      child: Text(
        t(
          'Notice: Severity is high. Please consult a doctor immediately.',
          'Pika mularrpa. Doctor-kutu mapalku ankula.',
        ),
        textAlign: TextAlign.center,
        style: const TextStyle(
          color: Colors.red,
          fontWeight: FontWeight.w900,
          fontSize: 17,
        ),
      ),
    );
  }

  Widget _pageTitle() {
    return HeadingWithMic(
      text: t('Questions', 'Kulintjaku tjuta'),
      speakText: 'Questions. Are you taking any medications?',
    );
  }

  BoxDecoration _cardDecoration() {
    return BoxDecoration(
      color: Colors.white.withOpacity(0.72),
      borderRadius: BorderRadius.circular(28),
      border: Border.all(color: Colors.white.withOpacity(0.75)),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withOpacity(0.08),
          blurRadius: 16,
          offset: const Offset(0, 8),
        ),
      ],
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