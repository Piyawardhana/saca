import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'QuestionThreePage.dart';

class QuestionTwoPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;
  final String duration;

  const QuestionTwoPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
    required this.duration,
  });

  @override
  State<QuestionTwoPage> createState() => _QuestionTwoPageState();
}

class _QuestionTwoPageState extends State<QuestionTwoPage> {
  final Map<String, double> severityValues = {};

  @override
  void initState() {
    super.initState();
    for (final symptom in widget.symptoms) {
      severityValues[symptom] = 5;
    }
  }

  double get overallValue {
    if (severityValues.isEmpty) return 0;
    return severityValues.values.reduce((a, b) => a + b) /
        severityValues.length;
  }

  String get overallSeverity => _severityLabel(overallValue);

  String _severityLabel(double value) {
    if (value <= 3) return 'Low';
    if (value <= 6) return 'Moderate';
    return 'High';
  }

  Color _severityColor(double value) {
    if (value <= 3) return Colors.green;
    if (value <= 6) return Colors.orange;
    return Colors.red;
  }

  Widget _glassCard({
    required Widget child,
    EdgeInsets padding = const EdgeInsets.all(22),
  }) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(26),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 14, sigmaY: 14),
        child: Container(
          width: 780,
          padding: padding,
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.42),
            borderRadius: BorderRadius.circular(26),
            border: Border.all(
              color: Colors.white.withOpacity(0.55),
              width: 1.4,
            ),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withOpacity(0.08),
                blurRadius: 16,
                offset: const Offset(0, 8),
              ),
            ],
          ),
          child: child,
        ),
      ),
    );
  }

  PreferredSizeWidget _appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white.withOpacity(0.94),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      leading: IconButton(
        onPressed: () => Navigator.pop(context),
        icon: const Icon(Icons.arrow_back_ios_new_rounded),
      ),
      title: const Row(
        children: [
          Icon(Icons.favorite_rounded, color: Color(0xFF2563EB)),
          SizedBox(width: 10),
          Text(
            'SACA',
            style: TextStyle(
              color: Color(0xFF0F172A),
              fontWeight: FontWeight.w800,
            ),
          ),
        ],
      ),
    );
  }

  Widget _pageTitle() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          widget.isEnglish ? 'Assess each symptom' : 'Pika nintila',
          style: const TextStyle(
            fontSize: 30,
            fontWeight: FontWeight.w900,
            color: Color(0xFF0F172A),
          ),
        ),
        const SizedBox(width: 10),
        const Icon(Icons.mic_none_rounded, color: Color(0xFF2563EB)),
      ],
    );
  }

  Widget _symptomSeverityCard(String symptom) {
    final value = severityValues[symptom] ?? 5;
    final color = _severityColor(value);
    final label = _severityLabel(value);

    return _glassCard(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            symptom,
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w900,
              color: Color(0xFF0F172A),
            ),
          ),
          const SizedBox(height: 14),

          SliderTheme(
            data: SliderTheme.of(context).copyWith(
              activeTrackColor: color,
              inactiveTrackColor: Colors.grey.shade300,
              thumbColor: color,
              overlayColor: color.withOpacity(0.18),
              trackHeight: 6,
              thumbShape: const RoundSliderThumbShape(
                enabledThumbRadius: 13,
              ),
              overlayShape: const RoundSliderOverlayShape(
                overlayRadius: 24,
              ),
            ),
            child: Slider(
              value: value,
              min: 1,
              max: 10,
              divisions: 9,
              label: label,
              onChanged: (newValue) {
                setState(() {
                  severityValues[symptom] = newValue;
                });
              },
            ),
          ),

          const SizedBox(height: 8),

          ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: TweenAnimationBuilder<double>(
              tween: Tween<double>(begin: 0, end: value / 10),
              duration: const Duration(milliseconds: 450),
              builder: (context, animatedValue, _) {
                return LinearProgressIndicator(
                  value: animatedValue,
                  minHeight: 14,
                  color: color,
                  backgroundColor: Colors.grey.shade300,
                );
              },
            ),
          ),

          const SizedBox(height: 12),

          Text(
            '${widget.isEnglish ? "Selected severity" : "Pika"}: $label',
            style: TextStyle(
              color: color,
              fontSize: 17,
              fontWeight: FontWeight.w900,
            ),
          ),
        ],
      ),
    );
  }

  Widget _overallSeverityCard() {
    final color = _severityColor(overallValue);

    return _glassCard(
      padding: const EdgeInsets.all(22),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(11),
                decoration: BoxDecoration(
                  color: color.withOpacity(0.18),
                  shape: BoxShape.circle,
                ),
                child: Icon(
                  Icons.health_and_safety_rounded,
                  color: color,
                  size: 28,
                ),
              ),
              const SizedBox(width: 14),
              Expanded(
                child: Text(
                  '${widget.isEnglish ? "Current overall severity" : "Pika"}: $overallSeverity',
                  style: TextStyle(
                    color: color,
                    fontSize: 21,
                    fontWeight: FontWeight.w900,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 18),
          ClipRRect(
            borderRadius: BorderRadius.circular(20),
            child: TweenAnimationBuilder<double>(
              tween: Tween<double>(begin: 0, end: overallValue / 10),
              duration: const Duration(milliseconds: 600),
              builder: (context, animatedValue, _) {
                return LinearProgressIndicator(
                  value: animatedValue,
                  minHeight: 15,
                  color: color,
                  backgroundColor: Colors.grey.shade300,
                );
              },
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
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            children: [
              _pageTitle(),
              const SizedBox(height: 24),

              if (widget.symptoms.isEmpty)
                _glassCard(
                  child: Text(
                    widget.isEnglish
                        ? 'No symptoms were selected. Please continue to see a basic result.'
                        : 'Pika wiya. Ankula.',
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w700,
                      color: Color(0xFF0F172A),
                    ),
                  ),
                ),

              for (final symptom in widget.symptoms) ...[
                _symptomSeverityCard(symptom),
                const SizedBox(height: 18),
              ],

              _overallSeverityCard(),

              const SizedBox(height: 30),

              CustomButton(
                text: widget.isEnglish ? 'Next' : 'Ankula',
                icon: Icons.arrow_forward_rounded,
                gradientColors: const [
                  Color(0xFFFFA000),
                  Color(0xFFFF7A00),
                ],
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => QuestionThreePage(
                        isEnglish: widget.isEnglish,
                        symptoms: widget.symptoms,
                        duration: widget.duration,
                        severity: overallSeverity,
                        inputText: widget.inputText,
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