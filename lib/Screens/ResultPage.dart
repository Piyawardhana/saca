import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/InputMethodPage.dart';

class ResultPage extends StatelessWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String duration;
  final bool takingMedication;
  final String severity;
  final String inputText;
  final String disease;
  final String recommendation;
  final bool voiceMode;

final List<String> lifestyleChanges;

  const ResultPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.duration,
    required this.takingMedication,
    required this.severity,
    required this.inputText,
    required this.disease,
    required this.recommendation,
    this.voiceMode = false,
    required this.lifestyleChanges,
  });

  String t(String en, String pit) => isEnglish ? en : pit;

  bool get isSevere {
    final s = severity.toLowerCase().trim();

    return s.contains('severe') ||
        s.contains('high') ||
        s == '7' ||
        s == '8' ||
        s == '9' ||
        s == '10';
  }

  Color get severityColor {
    if (isSevere) return Colors.red;

    final s = severity.toLowerCase().trim();

    if (s.contains('moderate') || s == '4' || s == '5' || s == '6') {
      return Colors.orange;
    }

    return Colors.green;
  }

  String get fallbackAdvice {
    if (isSevere) {
      return t(
        'Consult a doctor immediately\nDo not delay\nCall 000 if urgent',
        'Doctor-kutu mapalku ankula\nWiya alatji\n000 ringamilani',
      );
    }

    final s = severity.toLowerCase().trim();

    if (s.contains('moderate') || s == '4' || s == '5' || s == '6') {
      return t(
        'Rest well\nDrink fluids\nConsult doctor if needed',
        'Ngurra nyinama\nKapi piti\nDoctor-kutu ankula',
      );
    }

    return t(
      'Drink water\nRest\nMonitor symptoms',
      'Kapi piti\nNgurra nyinama\nPika nyawa',
    );
  }

  bool isLifestyleItem(String item) {
    final s = item.toLowerCase().trim();

    return s == 'new food' ||
        s == 'food poisoning suspected' ||
        s == 'less sleep' ||
        s == 'high stress' ||
        s == 'heavy physical work' ||
        s == 'travel recently' ||
        s == 'alcohol or smoking' ||
        s == 'no major change';
  }

  Future<void> _callEmergency(BuildContext context) async {
    final Uri callUri = Uri(scheme: 'tel', path: '000');

    if (await canLaunchUrl(callUri)) {
      await launchUrl(callUri);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(t('Please call 000 immediately.', '000 ringamilani')),
        ),
      );
    }
  }

  Future<void> _bookDoctor(BuildContext context) async {
    await showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: Text(t('Booking Confirmed', 'Booking palya')),
          content: Text(
            t(
              'Doctor booking done successfully.',
              'Doctor booking palya.',
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text(t('OK', 'Palya')),
            ),
          ],
        );
      },
    );

    Navigator.pushAndRemoveUntil(
      context,
      MaterialPageRoute(
        builder: (_) => InputMethodPage(isEnglish: isEnglish),
      ),
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    final displayedSymptoms = symptoms
        .where((item) => !isLifestyleItem(item))
        .toSet()
        .join(', ');

    final finalAdvice =
        recommendation.trim().isNotEmpty ? recommendation : fallbackAdvice;

    return Scaffold(
      extendBody: true,
      appBar: _appBar(context),
      body: AppBackground(
        child: SafeArea(
          bottom: false,
          child: SingleChildScrollView(
            padding: const EdgeInsets.fromLTRB(22, 22, 22, 42),
            child: Column(
              children: [
                HeadingWithMic(
                  text: t('Results', 'Nyangatja'),
                  speakText: isEnglish
                      ? 'Results. Possible disease is $disease. Severity is $severity. Advice: ${finalAdvice.replaceAll('\n', '. ')}'
                      : 'Nyangatja. Possible disease $disease. Pika level $severity. Advice: ${finalAdvice.replaceAll('\n', '. ')}',
                  isEnglish: isEnglish,
                ),
                const SizedBox(height: 24),
                Container(
                  width: 780,
                  padding: const EdgeInsets.all(26),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.78),
                    borderRadius: BorderRadius.circular(28),
                    border: Border.all(
                      color: Colors.white.withOpacity(0.65),
                    ),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.08),
                        blurRadius: 14,
                        offset: const Offset(0, 8),
                      ),
                    ],
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _severityHeader(),
                      const SizedBox(height: 22),
                      _sectionTitle(t('Possible Disease', 'Disease')),
                      const SizedBox(height: 8),
                      _infoBox(
                        disease.trim().isEmpty
                            ? t('Unknown', 'Unknown')
                            : disease,
                      ),
                      const SizedBox(height: 22),
                      _sectionTitle(t('Given Symptoms', 'Pika tjuta')),
                      const SizedBox(height: 8),
                      _infoBox(
                        displayedSymptoms.trim().isEmpty
                            ? t('No symptoms provided', 'Pika wiya')
                            : displayedSymptoms,
                      ),
                      const SizedBox(height: 22),
                      _detailsBox(),
                      const SizedBox(height: 22),
                      _sectionTitle(t('Advice', 'Nintintja')),
                      const SizedBox(height: 8),
                      _adviceBox(finalAdvice),
                    ],
                  ),
                ),
                const SizedBox(height: 28),
                CustomButton(
                  text: t('Consult Doctor', 'Doctor-kutu ankula'),
                  icon: Icons.medical_services_rounded,
                  onPressed: () => _bookDoctor(context),
                ),
                const SizedBox(height: 18),
                if (isSevere)
                  EmergencyButton(
                    text: t('CALL 000 EMERGENCY', '000 ringamilani'),
                    onPressed: () => _callEmergency(context),
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _severityHeader() {
    return Row(
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
            size: 30,
          ),
        ),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            '${t('Severity', 'Pika')}: $severity',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.w900,
              color: severityColor,
            ),
          ),
        ),
      ],
    );
  }

  Widget _sectionTitle(String text) {
    return Text(
      text,
      style: const TextStyle(
        fontSize: 21,
        fontWeight: FontWeight.w900,
        color: Color(0xFF30161A),
      ),
    );
  }

  Widget _infoBox(String text) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: const Color(0xFFF0EBDB).withOpacity(0.72),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Text(
        text,
        style: const TextStyle(
          fontSize: 16,
          color: Color(0xFF30161A),
          fontWeight: FontWeight.w600,
          height: 1.4,
        ),
      ),
    );
  }

  Widget _detailsBox() {
    final lifestyleItems = symptoms.where(isLifestyleItem).toList();

    final lifestyleText = lifestyleItems.isEmpty
        ? t('Not provided', 'Wiya')
        : lifestyleItems.join(', ');

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.58),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(
          color: const Color(0xFF30161A).withOpacity(0.15),
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            '${t('Duration', 'Nyinanytja')}: $duration',
            style: const TextStyle(
              fontSize: 16,
              color: Color(0xFF30161A),
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            '${t('Medication Taken', 'Medicine')}: ${takingMedication ? t('Yes', 'Uwa') : t('No', 'Wiya')}',
            style: const TextStyle(
              fontSize: 16,
              color: Color(0xFF30161A),
              fontWeight: FontWeight.w700,
            ),
          ),
          const SizedBox(height: 8),
          Text(
            '${t('Food/Lifestyle Changes', 'Food/Lifestyle change')}: $lifestyleChanges',
            style: const TextStyle(
              fontSize: 16,
              color: Color(0xFF30161A),
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }

  Widget _adviceBox(String text) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(15),
      decoration: BoxDecoration(
        color: isSevere
            ? Colors.red.withOpacity(0.08)
            : const Color(0xFFF0EBDB).withOpacity(0.72),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(
          color: isSevere ? Colors.red.withOpacity(0.35) : Colors.transparent,
        ),
      ),
      child: Text(
        text,
        style: TextStyle(
          fontSize: 16,
          color: isSevere ? Colors.red.shade700 : const Color(0xFF30161A),
          fontWeight: FontWeight.w700,
          height: 1.4,
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

class EmergencyButton extends StatefulWidget {
  final String text;
  final VoidCallback onPressed;

  const EmergencyButton({
    super.key,
    required this.text,
    required this.onPressed,
  });

  @override
  State<EmergencyButton> createState() => _EmergencyButtonState();
}

class _EmergencyButtonState extends State<EmergencyButton>
    with SingleTickerProviderStateMixin {
  late AnimationController controller;
  late Animation<double> opacity;
  late Animation<double> scale;

  @override
  void initState() {
    super.initState();

    controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 650),
    )..repeat(reverse: true);

    opacity = Tween<double>(begin: 0.45, end: 1.0).animate(controller);

    scale = Tween<double>(begin: 1.0, end: 1.06).animate(
      CurvedAnimation(
        parent: controller,
        curve: Curves.easeInOut,
      ),
    );
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: opacity,
      child: ScaleTransition(
        scale: scale,
        child: GestureDetector(
          onTap: widget.onPressed,
          child: Container(
            width: double.infinity,
            padding: const EdgeInsets.symmetric(vertical: 18),
            decoration: BoxDecoration(
              borderRadius: BorderRadius.circular(28),
              gradient: const LinearGradient(
                colors: [
                  Color(0xFFD32F2F),
                  Color(0xFFFF5252),
                ],
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.red.withOpacity(0.50),
                  blurRadius: 18,
                  spreadRadius: 1,
                  offset: const Offset(0, 6),
                ),
              ],
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(
                  Icons.call_rounded,
                  color: Colors.white,
                  size: 28,
                ),
                const SizedBox(width: 10),
                Text(
                  widget.text,
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 21,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}