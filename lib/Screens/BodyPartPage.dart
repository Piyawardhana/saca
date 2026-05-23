import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Screens/SymptomSelectionPage.dart';

class BodyPartPage extends StatelessWidget {
  final bool isEnglish;

  const BodyPartPage({
    super.key,
    required this.isEnglish,
  });

  String t(String en, String pit) {
    return isEnglish ? en : pit;
  }

  static const List<Map<String, String>> bodyParts = [
    {
      'key': 'head',
      'title': 'Head',
      'pit': 'Kata',
      'image': 'assets/bodyparts/head.png',
    },
    {
      'key': 'chest',
      'title': 'Chest',
      'pit': 'Chest',
      'image': 'assets/bodyparts/chest.png',
    },
    {
      'key': 'abdomen',
      'title': 'Abdomen',
      'pit': 'Tjuni',
      'image': 'assets/bodyparts/abdomen.png',
    },
    {
      'key': 'back',
      'title': 'Back',
      'pit': 'Back',
      'image': 'assets/bodyparts/back.png',
    },
    {
      'key': 'arm',
      'title': 'Arm',
      'pit': 'Arm',
      'image': 'assets/bodyparts/arm.png',
    },
    {
      'key': 'leg',
      'title': 'Leg',
      'pit': 'Leg',
      'image': 'assets/bodyparts/leg.png',
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(22),
            child: Column(
              children: [
                Text(
                  t('Select Body Part', 'Kurunpa nintila'),
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 30,
                    fontWeight: FontWeight.w900,
                    color: Color(0xFF30161A),
                  ),
                ),
                const SizedBox(height: 22),
                Expanded(
                  child: GridView.builder(
                    itemCount: bodyParts.length,
                    gridDelegate:
                        const SliverGridDelegateWithFixedCrossAxisCount(
                      crossAxisCount: 2,
                      crossAxisSpacing: 18,
                      mainAxisSpacing: 18,
                      childAspectRatio: 0.95,
                    ),
                    itemBuilder: (context, index) {
                      final part = bodyParts[index];
                      final label =
                          isEnglish ? part['title']! : part['pit']!;

                      return GestureDetector(
                        onTap: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (_) => SymptomSelectionPage(
                                isEnglish: isEnglish,
                                bodyPartKey: part['key']!,
                                bodyPartLabel: label,
                              ),
                            ),
                          );
                        },
                        child: Container(
                          decoration: BoxDecoration(
                            color: Colors.white.withOpacity(0.55),
                            borderRadius: BorderRadius.circular(26),
                            border: Border.all(
                              color: Colors.white.withOpacity(0.55),
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: Colors.black.withOpacity(0.12),
                                blurRadius: 12,
                                offset: const Offset(0, 6),
                              ),
                            ],
                          ),
                          child: Column(
                            children: [
                              Expanded(
                                child: Padding(
                                  padding: const EdgeInsets.all(16),
                                  child: Image.asset(
                                    part['image']!,
                                    fit: BoxFit.contain,
                                    errorBuilder: (context, error, stackTrace) {
                                      return const Icon(
                                        Icons.image_not_supported_rounded,
                                        size: 60,
                                        color: Color(0xFF30161A),
                                      );
                                    },
                                  ),
                                ),
                              ),
                              Container(
                                width: double.infinity,
                                padding:
                                    const EdgeInsets.symmetric(vertical: 14),
                                decoration: const BoxDecoration(
                                  gradient: LinearGradient(
                                    colors: [
                                      Color(0xFF30161A),
                                      Color(0xFF5A2A2F),
                                    ],
                                  ),
                                  borderRadius: BorderRadius.vertical(
                                    bottom: Radius.circular(26),
                                  ),
                                ),
                                child: Text(
                                  label,
                                  textAlign: TextAlign.center,
                                  style: const TextStyle(
                                    color: Color(0xFFF0EBDB),
                                    fontSize: 20,
                                    fontWeight: FontWeight.w800,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      );
                    },
                  ),
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
      backgroundColor: Colors.white.withOpacity(0.94),
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
    );
  }
}