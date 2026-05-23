import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/BodyScanLoadingPage.dart';

class ReviewPage extends StatelessWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;
  final String duration;
  final String severity;
  final bool takingMedication;
  final bool voiceMode;

  const ReviewPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
    required this.duration,
    required this.severity,
    required this.takingMedication,
    this.voiceMode = false,
  });

  String t(String en, String pit) => isEnglish ? en : pit;

  Widget infoBox(String title, String value) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.75),
        borderRadius: BorderRadius.circular(18),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            title,
            style: const TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.w900,
              color: Color(0xFF30161A),
            ),
          ),
          const SizedBox(height: 8),
          Text(
            value,
            style: const TextStyle(
              fontSize: 15,
              fontWeight: FontWeight.w600,
              color: Color(0xFF30161A),
            ),
          ),
        ],
      ),
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

  @override
  Widget build(BuildContext context) {
    final lifestyleItems = symptoms.where(isLifestyleItem).toList();

    final symptomItems = symptoms.where((item) {
      return !isLifestyleItem(item);
    }).toList();

    final selectedSymptomsText = symptomItems.isEmpty
        ? inputText
        : symptomItems.join(', ');

    final lifestyleText = lifestyleItems.isEmpty
        ? t('Not provided', 'Wiya')
        : lifestyleItems.join(', ');

    return Scaffold(
      appBar: AppBar(
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
),
      body: AppBackground(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            children: [
              Text(
                t('Review Your Answers', 'Answer nyawa'),
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 30,
                  fontWeight: FontWeight.w900,
                  color: Color(0xFF30161A),
                ),
              ),
              const SizedBox(height: 24),

              infoBox(
                t('Selected symptoms/body parts', 'Pika/body part'),
                selectedSymptomsText.trim().isEmpty
                    ? t('Not provided', 'Wiya')
                    : selectedSymptomsText,
              ),

              infoBox(t('Duration', 'Nyinanytja'), duration),

              infoBox(t('Severity', 'Pika level'), severity),

              infoBox(
                t('Medication taken', 'Medicine'),
                takingMedication ? t('Yes', 'Uwa') : t('No', 'Wiya'),
              ),

              infoBox(
                t('Food/Lifestyle Changes', 'Food/Lifestyle change'),
                lifestyleText,
              ),

              const SizedBox(height: 26),

              CustomButton(
                text: t('Analyse', 'Analyse'),
                icon: Icons.analytics_rounded,
                onPressed: () {
                  final fullInputText = [
                    inputText,
                    symptoms.join(', '),
                  ].where((e) => e.trim().isNotEmpty).join(', ');

                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => BodyScanLoadingPage(
                        isEnglish: isEnglish,
                        symptoms: symptoms,
                        duration: duration,
                        takingMedication: takingMedication,
                        severity: severity,
                        inputText: fullInputText,
                        voiceMode: voiceMode,
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