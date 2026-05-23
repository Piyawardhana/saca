import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/QuestionTwoPage.dart';

class OtherPainPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;
  final String duration;
  final bool voiceMode;

  const OtherPainPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
    required this.duration,
    this.voiceMode = false,
  });

  @override
  State<OtherPainPage> createState() => _OtherPainPageState();
}

class _OtherPainPageState extends State<OtherPainPage> {
  final Set<String> selectedChanges = {};

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  final List<Map<String, dynamic>> options = [
    {
      'label': 'New Food',
      'pit': 'New food',
      'icon': Icons.restaurant_rounded,
    },
    {
      'label': 'Food Poisoning Suspected',
      'pit': 'Food poisoning pika',
      'icon': Icons.sick_rounded,
    },
    {
      'label': 'Less Sleep',
      'pit': 'Sleep wiya',
      'icon': Icons.bedtime_rounded,
    },
    {
      'label': 'High Stress',
      'pit': 'Stress palya wiya',
      'icon': Icons.psychology_rounded,
    },
    {
      'label': 'Heavy Physical Work',
      'pit': 'Work tjuta',
      'icon': Icons.fitness_center_rounded,
    },
    {
      'label': 'Travel Recently',
      'pit': 'Travel palyanu',
      'icon': Icons.flight_takeoff_rounded,
    },
    {
      'label': 'Alcohol or Smoking',
      'pit': 'Smoking/alcohol',
      'icon': Icons.smoking_rooms_rounded,
    },
    {
      'label': 'No Major Change',
      'pit': 'Change wiya',
      'icon': Icons.check_circle_rounded,
    },
  ];

  void toggleOption(String value) {
    setState(() {
      if (value == 'No Major Change') {
        selectedChanges.clear();
        selectedChanges.add(value);
        return;
      }

      selectedChanges.remove('No Major Change');

      if (selectedChanges.contains(value)) {
        selectedChanges.remove(value);
      } else {
        selectedChanges.add(value);
      }
    });
  }

  Widget optionCard(Map<String, dynamic> item) {
    final label = item['label'] as String;
    final pit = item['pit'] as String;
    final icon = item['icon'] as IconData;
    final selected = selectedChanges.contains(label);

    return GestureDetector(
      onTap: () => toggleOption(label),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 220),
        padding: const EdgeInsets.all(18),
        decoration: BoxDecoration(
          color: selected
              ? const Color(0xFFF0EBDB).withOpacity(0.95)
              : Colors.white.withOpacity(0.72),
          borderRadius: BorderRadius.circular(24),
          border: Border.all(
            color: selected ? const Color(0xFF30161A) : Colors.white,
            width: 2,
          ),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.06),
              blurRadius: 10,
              offset: const Offset(0, 5),
            ),
          ],
        ),
        child: Row(
          children: [
            Icon(
              icon,
              color: const Color(0xFF30161A),
              size: 34,
            ),
            const SizedBox(width: 14),
            Expanded(
              child: Text(
                t(label, pit),
                style: const TextStyle(
                  color: Color(0xFF30161A),
                  fontSize: 17,
                  fontWeight: FontWeight.w900,
                ),
              ),
            ),
            Icon(
              selected
                  ? Icons.check_circle_rounded
                  : Icons.radio_button_unchecked_rounded,
              color: const Color(0xFF30161A),
              size: 28,
            ),
          ],
        ),
      ),
    );
  }

  void goNext() {
    final updatedSymptoms = [
      ...widget.symptoms,
      ...selectedChanges,
    ];

    final updatedInputText = [
      widget.inputText,
      selectedChanges.join(', '),
    ].where((e) => e.trim().isNotEmpty).join(', ');

    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (_) => QuestionTwoPage(
          isEnglish: widget.isEnglish,
          symptoms: updatedSymptoms,
          inputText: updatedInputText,
          duration: widget.duration,
          voiceMode: widget.voiceMode,
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
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SafeArea(
          bottom: false,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(22),
            child: Column(
              children: [
                Text(
                  t(
                    'Have there been any recent food or lifestyle changes?',
                    'Food/lifestyle change nyuntumpa nyinanyi?',
                  ),
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Color(0xFF30161A),
                    fontSize: 30,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 12),
                Text(
                  t(
                    'Select anything that may have affected your health.',
                    'Health-ku affect palyanu nyawa.',
                  ),
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    color: Color(0xFF30161A),
                    fontSize: 16,
                    fontWeight: FontWeight.w700,
                  ),
                ),
                const SizedBox(height: 26),
                Container(
                  width: 760,
                  padding: const EdgeInsets.all(22),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.60),
                    borderRadius: BorderRadius.circular(28),
                    border: Border.all(
                      color: Colors.white.withOpacity(0.70),
                    ),
                  ),
                  child: GridView.builder(
                    shrinkWrap: true,
                    physics: const NeverScrollableScrollPhysics(),
                    itemCount: options.length,
                    gridDelegate:
                        const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      mainAxisSpacing: 16,
                      crossAxisSpacing: 16,
                      childAspectRatio: 2.6,
                    ),
                    itemBuilder: (context, index) {
                      return optionCard(options[index]);
                    },
                  ),
                ),
                const SizedBox(height: 28),
                CustomButton(
                  text: t('Next', 'Ankula'),
                  icon: Icons.arrow_forward_rounded,
                  onPressed: goNext,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}