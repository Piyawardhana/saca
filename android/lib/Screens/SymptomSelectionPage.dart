import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/SymptomTile.dart';
import 'package:saca_project/Screens/QuestionOnePage.dart';

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
  final Set<String> selected = {};

  final Map<String, List<String>> symptomMap = {
    'head': ['Headache', 'Migraine', 'Dizziness', 'Head Pressure'],
    'chest': ['Chest Pain', 'Chest Congestion', 'Breathing Difficulty', 'Tight Chest'],
    'ear': ['Ear Pain', 'Ear Block', 'Hearing Issue', 'Ear Infection'],
    'back': ['Back Pain', 'Muscle Strain', 'Stiff Back'],
    'stomach': ['Stomach Pain', 'Bloating', 'Nausea', 'Indigestion'],
    'arm': ['Arm Pain', 'Swelling', 'Weakness', 'Muscle Tightness'],
    'hip': ['Hip Pain', 'Joint Pain', 'Movement Difficulty', 'Stiff Hip'],
    'leg': ['Leg Pain', 'Ankle Pain', 'Swelling', 'Cramps'],
    'nose': ['Running Nose', 'Blocked Nose', 'Nose Pain', 'Sinus Pressure'],
    'neck': ['Neck Pain', 'Stiff Neck', 'Neck Swelling', 'Sore Neck'],
    'shoulder': ['Shoulder Pain', 'Frozen Shoulder', 'Shoulder Stiffness', 'Swelling'],
    'mouth': ['Mouth Ulcer', 'Dry Mouth', 'Painful Mouth', 'Tooth Pain'],
  };

  // Head symptom images only for now
  final Map<String, String> headSymptomImages = {
    'Headache': 'assets/images/headache.png',
    'Migraine': 'assets/images/migraine.png',
    'Dizziness': 'assets/images/dizziness.png',
    'Head Pressure': 'assets/images/headpressure.png',
  };

  @override
  Widget build(BuildContext context) {
    final symptoms = symptomMap[widget.bodyPartKey] ?? [];
    final bool isHeadPage = widget.bodyPartKey == 'head';

    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: Padding(
          padding: const EdgeInsets.all(22),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    widget.isEnglish
                        ? 'Select symptoms for ${widget.bodyPartLabel}'
                        : '${widget.bodyPartLabel} pika tjuta nintila',
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      fontSize: 26,
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
              Expanded(
                child: isHeadPage
                    ? _buildHeadVerticalCards(symptoms)
                    : _buildOtherBodyPartGrid(symptoms),
              ),
              const SizedBox(height: 10),
              CustomButton(
                text: widget.isEnglish ? 'Next' : 'Ankula',
                icon: Icons.arrow_forward_rounded,
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => QuestionOnePage(
  isEnglish: widget.isEnglish,
  symptoms: selected.toList(),
  inputText: '',
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

  Widget _buildHeadVerticalCards(List<String> symptoms) {
    return ListView.separated(
      itemCount: symptoms.length,
      separatorBuilder: (_, __) => const SizedBox(height: 16),
      itemBuilder: (context, index) {
        final symptom = symptoms[index];
        final isSelected = selected.contains(symptom);

        return InkWell(
          borderRadius: BorderRadius.circular(24),
          onTap: () {
            setState(() {
              if (isSelected) {
                selected.remove(symptom);
              } else {
                selected.add(symptom);
              }
            });
          },
          child: AnimatedContainer(
            duration: const Duration(milliseconds: 220),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: isSelected
                  ? const Color(0xFFE0ECFF)
                  : Colors.white.withOpacity(0.93),
              borderRadius: BorderRadius.circular(24),
              border: Border.all(
                color: isSelected
                    ? const Color(0xFF2563EB)
                    : Colors.white.withOpacity(0.8),
                width: 2,
              ),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.08),
                  blurRadius: 14,
                  offset: const Offset(0, 8),
                ),
              ],
            ),
            child: Row(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(18),
                  child: Container(
                    width: 110,
                    height: 110,
                    color: const Color(0xFFF8FAFC),
                    child: Image.asset(
                      headSymptomImages[symptom] ?? '',
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        return const Icon(
                          Icons.image_not_supported_rounded,
                          size: 42,
                          color: Color(0xFF2563EB),
                        );
                      },
                    ),
                  ),
                ),
                const SizedBox(width: 18),
                Expanded(
                  child: Text(
                    symptom,
                    style: TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.w700,
                      color: isSelected
                          ? const Color(0xFF1D4ED8)
                          : const Color(0xFF0F172A),
                    ),
                  ),
                ),
                Icon(
                  isSelected
                      ? Icons.check_circle_rounded
                      : Icons.radio_button_unchecked_rounded,
                  color: isSelected
                      ? const Color(0xFF2563EB)
                      : Colors.grey.shade500,
                  size: 30,
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildOtherBodyPartGrid(List<String> symptoms) {
    return GridView.builder(
      itemCount: symptoms.length,
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        crossAxisSpacing: 18,
        mainAxisSpacing: 18,
        childAspectRatio: 2.5,
      ),
      itemBuilder: (context, index) {
        final symptom = symptoms[index];
        return SymptomTile(
          text: symptom,
          selected: selected.contains(symptom),
          onTap: () {
            setState(() {
              if (selected.contains(symptom)) {
                selected.remove(symptom);
              } else {
                selected.add(symptom);
              }
            });
          },
        );
      },
    );
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
}