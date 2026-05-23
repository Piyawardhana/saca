import 'dart:ui';
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
  final Map<String, double> severityValues = {};

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  bool shouldShowSeveritySlider(String item) {
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

  List<String> get severityItems =>
      widget.symptoms.where(shouldShowSeveritySlider).toList();

  @override
  void initState() {
    super.initState();
    for (final symptom in severityItems) {
      severityValues[symptom] = 5;
    }
  }

  double get overallValue {
    if (severityValues.isEmpty) return 5;
    return severityValues.values.reduce((a, b) => a + b) /
        severityValues.length;
  }

  String get overallSeverity => _severityLabel(overallValue);

  String _severityLabel(double value) {
    if (value <= 3) return t('Low', 'Low');
    if (value <= 6) return t('Moderate', 'Moderate');
    return t('High', 'High');
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
        filter: ImageFilter.blur(sigmaX: 10, sigmaY: 10),
        child: Container(
          width: 780,
          padding: padding,
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.48),
            borderRadius: BorderRadius.circular(26),
            border: Border.all(
              color: Colors.white.withOpacity(0.55),
              width: 1.4,
            ),
          ),
          child: child,
        ),
      ),
    );
  }

  PreferredSizeWidget _appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white.withOpacity(0.72),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      leading: IconButton(
        onPressed: () => Navigator.pop(context),
        icon: const Icon(Icons.arrow_back_ios_new_rounded,
            color: Color(0xFF30161A)),
      ),
      title: const Row(
        children: [
          Icon(Icons.favorite_rounded, color: Color(0xFF30161A)),
          SizedBox(width: 10),
          Text('SACA',
              style: TextStyle(
                  color: Color(0xFF30161A), fontWeight: FontWeight.w900)),
        ],
      ),
    );
  }

  Widget _pageTitle() {
    return HeadingWithMic(
      text: t('Rate pain severity', 'Pika level nintila'),
      speakText:
          'Rate only the pain severity. Move the slider for each selected pain area.',
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
          Text(symptom,
              style: const TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.w900,
                  color: Color(0xFF30161A))),
          const SizedBox(height: 14),
          SliderTheme(
            data: SliderTheme.of(context).copyWith(
              activeTrackColor: color,
              inactiveTrackColor: const Color(0xFFF0EBDB),
              thumbColor: color,
              overlayColor: color.withOpacity(0.18),
              trackHeight: 6,
            ),
            child: Slider(
              value: value,
              min: 0,
              max: 10,
              divisions: 10,
              label: label,
              onChanged: (newValue) {
                setState(() {
                  severityValues[symptom] = newValue;
                });
              },
            ),
          ),
          Text(
            '${t("Selected severity", "Pika level")}: $label',
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
      child: Text(
        '${t("Current overall pain severity", "Pika overall")}: $overallSeverity',
        style: TextStyle(
          color: color,
          fontSize: 21,
          fontWeight: FontWeight.w900,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final items = severityItems;

    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            children: [
              _pageTitle(),
              const SizedBox(height: 24),
              if (items.isEmpty)
                _glassCard(
                  child: Text(
                    t(
                      'No pain area selected. A default moderate severity will be used.',
                      'Pika area wiya. Moderate level use palyani.',
                    ),
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 17,
                      fontWeight: FontWeight.w700,
                      color: Color(0xFF30161A),
                    ),
                  ),
                ),
              for (final symptom in items) ...[
                _symptomSeverityCard(symptom),
                const SizedBox(height: 18),
              ],
              _overallSeverityCard(),
              const SizedBox(height: 30),
              CustomButton(
                text: t('Next', 'Ankula'),
                icon: Icons.arrow_forward_rounded,
                gradientColors: const [
                  Color(0xFF30161A),
                  Color(0xFF5A2A2F),
                ],
                onPressed: () {
  final allAnswers = widget.symptoms;

  final fullInputText = [
    widget.inputText,
    allAnswers.join(', '),
  ].where((e) => e.trim().isNotEmpty).join(', ');

  Navigator.push(
    context,
    MaterialPageRoute(
      builder: (_) => QuestionThreePage(
        isEnglish: widget.isEnglish,
        symptoms: allAnswers,
        duration: widget.duration,
        severity: overallSeverity,
        inputText: fullInputText,
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