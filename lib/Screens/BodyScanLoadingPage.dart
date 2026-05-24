import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/ResultPage.dart';
import 'package:saca_project/services/api_service.dart';
import 'package:saca_project/services/translation_service.dart';

class BodyScanLoadingPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String duration;
  final bool takingMedication;
  final String severity;
  final String inputText;
  final bool voiceMode;

  const BodyScanLoadingPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.duration,
    required this.takingMedication,
    required this.severity,
    required this.inputText,
    this.voiceMode = false,
  });

  @override
  State<BodyScanLoadingPage> createState() => _BodyScanLoadingPageState();
}

class _BodyScanLoadingPageState extends State<BodyScanLoadingPage>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scanAnimation;

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  bool isLifestyleItem(String value) {
    final s = value.toLowerCase().trim();

    return s.contains('no major change') ||
        s.contains('new food') ||
        s.contains('food poisoning') ||
        s.contains('less sleep') ||
        s.contains('high stress') ||
        s.contains('heavy physical work') ||
        s.contains('travel recently') ||
        s.contains('alcohol') ||
        s.contains('smoking');
  }

  List<String> get medicalSymptoms {
    return widget.symptoms.where((item) => !isLifestyleItem(item)).toList();
  }

  List<String> get lifestyleAnswers {
    return widget.symptoms.where((item) => isLifestyleItem(item)).toList();
  }

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _scanAnimation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );

    _runPrediction();
  }

  Future<void> _runPrediction() async {
    try {
      final cleanSymptoms = medicalSymptoms.toSet().toList();
      final cleanLifestyle = lifestyleAnswers.toSet().toList();

      final fullText = [
        cleanSymptoms.join(', '),
        'Duration: ${widget.duration}',
        'Severity: ${widget.severity}',
        'Medication taken: ${widget.takingMedication ? "Yes" : "No"}',
      ].where((e) => e.trim().isNotEmpty).join(', ');

      String apiInputText = fullText;

      if (!widget.isEnglish) {
        apiInputText = await TranslationService.toEnglish(fullText);
      }

      debugPrint('========== API INPUT ==========');
      debugPrint('Full text before translation: $fullText');
      debugPrint('Text sent to API: $apiInputText');
      debugPrint('Pain score: ${_severityToPainScore(widget.severity)}');
      debugPrint('Body parts/symptoms: ${cleanSymptoms.join(', ')}');
      debugPrint('Lifestyle answers: ${cleanLifestyle.join(', ')}');
      debugPrint('===============================');

      final result = await ApiService.predict(
        text: apiInputText,
        painScore: _severityToPainScore(widget.severity),
        bodyPart: cleanSymptoms.join(', '),
      );

      String disease = 'Unknown';

      if (result['possible_diseases'] != null &&
          result['possible_diseases'] is List &&
          result['possible_diseases'].isNotEmpty) {
        disease =
            result['possible_diseases'][0]['name']?.toString() ?? 'Unknown';
      } else {
        disease = result['predicted_disease']?.toString() ??
            result['disease']?.toString() ??
            result['possible_disease']?.toString() ??
            'Unknown';
      }

      String recommendation = result['recommendation']?.toString() ??
          result['advice']?.toString() ??
          'Please consult a doctor if symptoms continue.';

      String finalSeverity = result['severity']?.toString() ?? widget.severity;

      debugPrint('========== API OUTPUT ==========');
      debugPrint(result.toString());
      debugPrint('Disease: $disease');
      debugPrint('Recommendation: $recommendation');
      debugPrint('Severity: $finalSeverity');
      debugPrint('================================');

      if (!widget.isEnglish) {
        disease = await TranslationService.toPitjantjatjara(disease);
        recommendation =
            await TranslationService.toPitjantjatjara(recommendation);
        finalSeverity =
            await TranslationService.toPitjantjatjara(finalSeverity);
      }

      await Future.delayed(const Duration(seconds: 3));
      if (!mounted) return;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => ResultPage(
            isEnglish: widget.isEnglish,
            symptoms: cleanSymptoms,
            duration: widget.duration,
            takingMedication: widget.takingMedication,
            severity: finalSeverity,
            inputText: fullText,
            disease: disease,
            recommendation: recommendation,
            voiceMode: widget.voiceMode,
          ),
        ),
      );
    } catch (e) {
      debugPrint('========== API ERROR ==========');
      debugPrint(e.toString());
      debugPrint('==============================');

      await Future.delayed(const Duration(seconds: 3));
      if (!mounted) return;

      String disease = 'Prediction unavailable';
      String recommendation =
          'Backend connection failed. Please check the API server.';

      if (!widget.isEnglish) {
        disease = await TranslationService.toPitjantjatjara(disease);
        recommendation =
            await TranslationService.toPitjantjatjara(recommendation);
      }

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => ResultPage(
            isEnglish: widget.isEnglish,
            symptoms: medicalSymptoms.toSet().toList(),
            duration: widget.duration,
            takingMedication: widget.takingMedication,
            severity: widget.severity,
            inputText: widget.inputText,
            disease: disease,
            recommendation: recommendation,
            voiceMode: widget.voiceMode,
          ),
        ),
      );
    }
  }

  int _severityToPainScore(String severity) {
    final s = severity.toLowerCase();

    if (s.contains('high')) return 8;
    if (s.contains('moderate')) return 5;
    if (s.contains('low') || s.contains('mild')) return 2;

    return 5;
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  PreferredSizeWidget _appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white.withOpacity(0.95),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      automaticallyImplyLeading: false,
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: Center(
          child: Container(
            width: 520,
            padding: const EdgeInsets.all(30),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.82),
              borderRadius: BorderRadius.circular(28),
              border: Border.all(color: Colors.white.withOpacity(0.7)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.10),
                  blurRadius: 20,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                HeadingWithMic(
                  text: widget.isEnglish
                      ? 'Scanning your symptoms'
                      : 'Pika tjuta nyanganyi',
                  speakText: t(
                    'Scanning your symptoms. Please wait while SACA prepares your result.',
                    'Pika tjuta nyanganyi. SACA result palyantjaku paṯaṟa nyinama.',
                  ),
                  isEnglish: widget.isEnglish,
                  fontSize: 26,
                ),
                const SizedBox(height: 24),
                SizedBox(
                  width: 180,
                  height: 300,
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      Icon(
                        Icons.accessibility_new_rounded,
                        size: 210,
                        color: const Color(0xFF30161A).withOpacity(0.25),
                      ),
                      AnimatedBuilder(
                        animation: _scanAnimation,
                        builder: (context, child) {
                          return Positioned(
                            top: 20 + (_scanAnimation.value * 230),
                            child: Container(
                              width: 170,
                              height: 8,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(20),
                                gradient: const LinearGradient(
                                  colors: [
                                    Color(0xFF30161A),
                                    Color(0xFF5A2A2F),
                                  ],
                                ),
                              ),
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 18),
                Text(
                  widget.isEnglish
                      ? 'Please wait while SACA prepares your result...'
                      : 'SACA nyangatja palyalkatinya...',
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFF30161A),
                  ),
                ),
                const SizedBox(height: 22),
                const CircularProgressIndicator(
                  color: Color(0xFF30161A),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}