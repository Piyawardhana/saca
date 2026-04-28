import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';

class ResultPage extends StatelessWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String duration;
  final bool takingMedication;
  final String severity;
  final String inputText;

  const ResultPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.duration,
    required this.takingMedication,
    required this.severity,
    required this.inputText,
  });

  String get advice {
    switch (severity) {
      case 'Low':
        return isEnglish
            ? 'Drink water\nRest\nMonitor symptoms'
            : 'Kapi piti\nNgurra nyinama\nPika nyawa';
      case 'Moderate':
        return isEnglish
            ? 'Rest well\nDrink fluids\nBook a doctor appointment if symptoms continue'
            : 'Ngurra nyinama\nKapi piti\nDoctor booking palyala';
      default:
        return isEnglish
            ? 'Consult a doctor immediately\nDo not delay\nIf urgent, call 000'
            : 'Doctor-kutu mapalku ankula\nWiya alatji\n000 ringamilani';
    }
  }

  Color get dotColor {
    switch (severity) {
      case 'Low':
        return Colors.green;
      case 'Moderate':
        return Colors.orange;
      default:
        return Colors.red;
    }
  }

  Future<void> _callEmergency(BuildContext context) async {
    final Uri callUri = Uri(scheme: 'tel', path: '000');

    if (await canLaunchUrl(callUri)) {
      await launchUrl(callUri);
    } else {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            isEnglish
                ? 'Please call 000 immediately.'
                : '000 ringamilani.',
          ),
        ),
      );
    }
  }

  PreferredSizeWidget _appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white.withOpacity(0.92),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      leading: IconButton(
        onPressed: () => Navigator.pop(context),
        icon: const Icon(Icons.arrow_back_ios_new_rounded),
      ),
      title: Row(
        children: const [
          Icon(Icons.favorite_rounded, color: Color(0xFF2563EB)),
          SizedBox(width: 10),
          Text(
            'SACA',
            style: TextStyle(
              color: Color(0xFF0F172A),
              fontWeight: FontWeight.w700,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final displayedSymptoms =
        symptoms.isEmpty ? inputText : symptoms.join(', ');

    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    isEnglish ? 'Results' : 'Nyangatja',
                    style: const TextStyle(
                      fontSize: 28,
                      fontWeight: FontWeight.w800,
                      color: Color(0xFF0F172A),
                    ),
                  ),
                  const SizedBox(width: 10),
                  const Icon(
                    Icons.mic_none_rounded,
                    color: Color(0xFF2563EB),
                  ),
                ],
              ),
              const SizedBox(height: 20),

              Container(
                width: 780,
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.92),
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: Colors.white.withOpacity(0.7)),
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
                    Row(
                      children: [
                        Icon(
                          Icons.health_and_safety_rounded,
                          color: dotColor,
                          size: 30,
                        ),
                        const SizedBox(width: 10),
                        Text(
                          isEnglish ? 'Severity' : 'Pika',
                          style: const TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.w700,
                            color: Color(0xFF0F172A),
                          ),
                        ),
                        const SizedBox(width: 10),
                        Text(
                          '- $severity',
                          style: TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.w800,
                            color: dotColor,
                          ),
                        ),
                        const SizedBox(width: 10),
                        CircleAvatar(
                          radius: 10,
                          backgroundColor: dotColor,
                        ),
                      ],
                    ),

                    const SizedBox(height: 22),

                    Text(
                      isEnglish ? 'Given Symptoms' : 'Pika tjuta',
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                    const SizedBox(height: 10),

                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF8FAFC),
                        borderRadius: BorderRadius.circular(18),
                      ),
                      child: Text(
                        displayedSymptoms.trim().isEmpty
                            ? (isEnglish ? 'No symptoms provided' : 'Pika wiya')
                            : displayedSymptoms,
                        style: const TextStyle(
                          fontSize: 16,
                          color: Color(0xFF334155),
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ),

                    const SizedBox(height: 20),

                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: const Color(0xFFEFF6FF),
                        borderRadius: BorderRadius.circular(18),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '${isEnglish ? "Duration" : "Nyinanytja"}: $duration',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF1E3A8A),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            '${isEnglish ? "Taking Medication" : "Medicine taking"}: ${takingMedication ? (isEnglish ? "Yes" : "Uwa") : (isEnglish ? "No" : "Wiya")}',
                            style: const TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w600,
                              color: Color(0xFF1E3A8A),
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(height: 22),

                    Text(
                      isEnglish ? 'Advice' : 'Nintintja',
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.w700,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                    const SizedBox(height: 10),

                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: severity == 'High'
                            ? Colors.red.withOpacity(0.08)
                            : const Color(0xFFF8FAFC),
                        borderRadius: BorderRadius.circular(18),
                        border: Border.all(
                          color: severity == 'High'
                              ? Colors.red.withOpacity(0.35)
                              : Colors.transparent,
                        ),
                      ),
                      child: Text(
                        advice,
                        style: TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.w600,
                          color: severity == 'High'
                              ? Colors.red.shade700
                              : const Color(0xFF334155),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 24),

              CustomButton(
                text: isEnglish ? 'Consult Doctor' : 'Doctor-kutu ankula',
                icon: Icons.medical_services_rounded,
                gradientColors: const [
                  Color(0xFF2563EB),
                  Color(0xFF06B6D4),
                ],
                onPressed: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text(
                        isEnglish
                            ? 'Doctor consultation request selected.'
                            : 'Doctor consultation nintiningi.',
                      ),
                    ),
                  );
                },
              ),

              const SizedBox(height: 14),

              if (severity == 'High')
                CustomButton(
                  text: isEnglish ? 'Call 000' : '000 ringamilani',
                  icon: Icons.local_hospital_rounded,
                  gradientColors: const [
                    Colors.redAccent,
                    Colors.red,
                  ],
                  onPressed: () => _callEmergency(context),
                ),
            ],
          ),
        ),
      ),
    );
  }
}