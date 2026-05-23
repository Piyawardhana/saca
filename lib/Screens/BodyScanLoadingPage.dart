import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/ResultPage.dart';
import 'package:saca_project/Services/PredictionService.dart';

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

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    )..repeat(reverse: true);

    _scanAnimation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.easeInOut,
      ),
    );

    _runPrediction();
  }

  Future<void> _runPrediction() async {
    try {
      final result = await PredictionService.predict(
        text: widget.inputText,
        symptoms: widget.symptoms,
        severity: widget.severity,
        duration: widget.duration,
      );

      final diseases = result['possible_diseases'] as List<dynamic>? ?? [];

      final disease =
          diseases.isNotEmpty ? diseases.first['name'].toString() : 'Unknown';

      final recommendation = result['recommendation']?.toString() ??
          'Please consult a doctor if symptoms continue.';

      final backendSeverity = _mapSeverity(result['severity']?.toString());

      final responseSymptoms = result['symptoms'];
      final finalSymptoms = responseSymptoms is List
          ? responseSymptoms.map((e) => e.toString()).toList()
          : widget.symptoms;

      await Future.delayed(const Duration(seconds: 3));

      if (!mounted) return;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => ResultPage(
            isEnglish: widget.isEnglish,
            symptoms: finalSymptoms,
            duration: widget.duration,
            takingMedication: widget.takingMedication,
            severity: backendSeverity,
            inputText: result['cleaned_text']?.toString() ?? widget.inputText,
            disease: disease,
            recommendation: recommendation,
            voiceMode: widget.voiceMode,
          ),
        ),
      );
    } catch (e) {
      await Future.delayed(const Duration(seconds: 3));

      if (!mounted) return;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => ResultPage(
            isEnglish: widget.isEnglish,
            symptoms: widget.symptoms,
            duration: widget.duration,
            takingMedication: widget.takingMedication,
            severity: widget.severity,
            inputText: widget.inputText,
            disease: 'Prediction unavailable',
            recommendation:
                'Backend connection failed. Please check the API server.',
            voiceMode: widget.voiceMode,
          ),
        ),
      );
    }
  }

  String _mapSeverity(String? value) {
    final v = value?.toLowerCase().trim() ?? '';

    if (v == 'severe' || v == 'high') return 'High';
    if (v == 'moderate') return 'Moderate';
    if (v == 'low') return 'Low';

    return widget.severity;
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
                  speakText:
                      'Scanning your symptoms. Please wait while SACA prepares your result.',
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
                                boxShadow: [
                                  BoxShadow(
                                    color: const Color(0xFF30161A)
                                        .withOpacity(0.45),
                                    blurRadius: 16,
                                    spreadRadius: 3,
                                  ),
                                ],
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