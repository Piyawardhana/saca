import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/HumanBodySelectionPage.dart';

class SymptomSelectionPage extends StatefulWidget {
  final bool isEnglish;
  final String bodyPartKey;
  final String bodyPartLabel;

  const SymptomSelectionPage({
    super.key,
    required this.isEnglish,
    required this.bodyPartKey,
    required this.bodyPartLabel,
  });

  @override
  State<SymptomSelectionPage> createState() => _SymptomSelectionPageState();
}

class _SymptomSelectionPageState extends State<SymptomSelectionPage> {
  final Set<String> selectedSymptoms = {};

  String t(String en, String pit) {
    return widget.isEnglish ? en : pit;
  }

  final Map<String, List<Map<String, String>>> symptomsByBodyPart = {
    'head': [
      {'name': 'Headache', 'pit': 'Kata pika', 'image': 'assets/diseases/headache.png'},
      {'name': 'Dizziness', 'pit': 'Mirri-mirri', 'image': 'assets/diseases/dizziness.png'},
      {'name': 'Fever', 'pit': 'Mapalku', 'image': 'assets/diseases/fever.png'},
    ],
    'chest': [
      {'name': 'Chest Pain', 'pit': 'Chest pika', 'image': 'assets/diseases/chest_pain.png'},
      {'name': 'Breathing Trouble', 'pit': 'Wangka breath wiya', 'image': 'assets/diseases/breathing trouble.png'},
      {'name': 'Cough', 'pit': 'Cough', 'image': 'assets/diseases/cough.png'},
    ],
    'abdomen': [
      {'name': 'Stomach Pain', 'pit': 'Tjuni pika', 'image': 'assets/diseases/stomach_pain.png'},
      {'name': 'Vomiting', 'pit': 'Vomiting', 'image': 'assets/diseases/vomiting.png'},
      {'name': 'Diarrhea', 'pit': 'Diarrhea', 'image': 'assets/diseases/diarrhea.png'},
    ],
    'back': [
      {'name': 'Back Pain', 'pit': 'Back pika', 'image': 'assets/diseases/back_pain.png'},
      {'name': 'Muscle Pain', 'pit': 'Muscle pika', 'image': 'assets/diseases/muscle_pain.png'},
      {'name': 'Injury', 'pit': 'Injury', 'image': 'assets/diseases/injury.png'},
    ],
    'arm': [
      {'name': 'Arm Pain', 'pit': 'Arm pika', 'image': 'assets/diseases/arm_pain.png'},
      {'name': 'Arm Swelling', 'pit': 'Arm swelling', 'image': 'assets/diseases/arm_swelling.jpeg'},
      {'name': 'Injury', 'pit': 'Injury', 'image': 'assets/diseases/injury.png'},
    ],
    'leg': [
      {'name': 'Leg Pain', 'pit': 'Leg pika', 'image': 'assets/diseases/leg_pain.jpg'},
      {'name': 'Leg Swelling', 'pit': 'Leg swelling', 'image': 'assets/diseases/leg_swelling.jpg'},
      {'name': 'Muscle Pain', 'pit': 'Muscle pika', 'image': 'assets/diseases/muscle_pain.png'},
    ],
  };

  @override
  Widget build(BuildContext context) {
    final symptoms = symptomsByBodyPart[widget.bodyPartKey] ?? [];

    return Scaffold(
      appBar: _appBar(context), // ✅ ADDED
      body: AppBackground(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(22),
            child: Column(
              children: [
                Text(
                  '${t('Select Symptoms for', 'Pika tjuta nintila')} ${widget.bodyPartLabel}',
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 28,
                    fontWeight: FontWeight.w900,
                    color: Color(0xFF30161A),
                  ),
                ),
                const SizedBox(height: 22),
                Expanded(
                  child: ListView.separated(
                    itemCount: symptoms.length,
                    separatorBuilder: (_, __) => const SizedBox(height: 16),
                    itemBuilder: (context, index) {
                      final symptom = symptoms[index];
                      final name = widget.isEnglish ? symptom['name']! : symptom['pit']!;
                      final englishName = symptom['name']!;
                      final image = symptom['image']!;
                      final isSelected = selectedSymptoms.contains(englishName);

                      return GestureDetector(
                        onTap: () {
                          setState(() {
                            if (isSelected) {
                              selectedSymptoms.remove(englishName);
                            } else {
                              selectedSymptoms.add(englishName);
                            }
                          });
                        },
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 200),
                          padding: const EdgeInsets.all(14),
                          decoration: BoxDecoration(
                            color: isSelected
                                ? const Color(0xFFF0EBDB).withOpacity(0.85)
                                : Colors.white.withOpacity(0.55),
                            borderRadius: BorderRadius.circular(24),
                            border: Border.all(
                              color: isSelected
                                  ? const Color(0xFF30161A)
                                  : Colors.white.withOpacity(0.55),
                              width: 2,
                            ),
                          ),
                          child: Row(
                            children: [
                              Container(
                                width: 90,
                                height: 90,
                                padding: const EdgeInsets.all(10),
                                decoration: BoxDecoration(
                                  color: Colors.white.withOpacity(0.85),
                                  borderRadius: BorderRadius.circular(18),
                                ),
                                child: Image.asset(image),
                              ),
                              const SizedBox(width: 18),
                              Expanded(
                                child: Text(
                                  name,
                                  style: const TextStyle(
                                    fontSize: 20,
                                    fontWeight: FontWeight.w900,
                                    color: Color(0xFF30161A),
                                  ),
                                ),
                              ),
                              Icon(
                                isSelected
                                    ? Icons.check_circle_rounded
                                    : Icons.radio_button_unchecked,
                                color: const Color(0xFF30161A),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
                ),
                const SizedBox(height: 18),
                CustomButton(
                  text: t('Next', 'Ankula'),
                  icon: Icons.arrow_forward_rounded,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => HumanBodySelectionPage(
                          isEnglish: widget.isEnglish,
                          symptoms: selectedSymptoms.toList(),
                          inputText: selectedSymptoms.join(', '),
                        ),
                      ),
                    );
                  },
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