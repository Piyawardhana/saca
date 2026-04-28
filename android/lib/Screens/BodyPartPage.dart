import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Screens/SymptomSelectionPage.dart';

class BodyPartPage extends StatelessWidget {
  final bool isEnglish;

  const BodyPartPage({
    super.key,
    required this.isEnglish,
    
  });

  static const List<Map<String, dynamic>> bodyParts = [
    {
      'key': 'head',
      'titleEn': 'Head',
      'titleTr': 'Kata',
      'asset': 'assets/gifs/head.gif',
      'icon': Icons.face_rounded,
    },
    {
      'key': 'chest',
      'titleEn': 'Chest',
      'titleTr': 'Chest',
      'asset': 'assets/gifs/chest.gif',
      'icon': Icons.favorite_outline_rounded,
    },
    {
      'key': 'ear',
      'titleEn': 'Ear',
      'titleTr': 'Ear',
      'asset': 'assets/gifs/ear.gif',
      'icon': Icons.hearing_rounded,
    },
    {
      'key': 'back',
      'titleEn': 'Back',
      'titleTr': 'Back',
      'asset': 'assets/gifs/back.gif',
      'icon': Icons.accessibility_new_rounded,
    },
    {
      'key': 'stomach',
      'titleEn': 'Stomach',
      'titleTr': 'Tjuni',
      'asset': 'assets/gifs/stomach.gif',
      'icon': Icons.circle_outlined,
    },
    {
      'key': 'arm',
      'titleEn': 'Arm',
      'titleTr': 'Arm',
      'asset': 'assets/gifs/arm.gif',
      'icon': Icons.pan_tool_alt_rounded,
    },
    {
      'key': 'hip',
      'titleEn': 'Hip',
      'titleTr': 'Hip',
      'asset': 'assets/gifs/hip.gif',
      'icon': Icons.accessibility_new_rounded,
    },
    {
      'key': 'leg',
      'titleEn': 'Leg / Ankle',
      'titleTr': 'Leg',
      'asset': 'assets/gifs/ankle.gif',
      'icon': Icons.directions_walk_rounded,
    },
    {
      'key': 'nose',
      'titleEn': 'Nose',
      'titleTr': 'Nose',
      'asset': 'assets/gifs/nose.gif',
      'icon': Icons.face_rounded,
    },
    {
      'key': 'neck',
      'titleEn': 'Neck',
      'titleTr': 'Neck',
      'asset': 'assets/gifs/neck.gif',
      'icon': Icons.accessibility_rounded,
    },
    {
      'key': 'shoulder',
      'titleEn': 'Shoulder',
      'titleTr': 'Shoulder',
      'asset': 'assets/gifs/shoulder.gif',
      'icon': Icons.accessibility_new_rounded,
    },
    {
      'key': 'mouth',
      'titleEn': 'Mouth',
      'titleTr': 'Mouth',
      'asset': 'assets/gifs/mouth.gif',
      'icon': Icons.record_voice_over_rounded,
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(
                    isEnglish
                        ? 'Select where the pain is'
                        : 'Pika ngalya nintila',
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
              Expanded(
                child: LayoutBuilder(
                  builder: (context, constraints) {
                    final crossAxisCount = constraints.maxWidth > 1100 ? 3 : 2;

                    return GridView.builder(
                      itemCount: bodyParts.length,
                      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                        crossAxisCount: crossAxisCount,
                        crossAxisSpacing: 22,
                        mainAxisSpacing: 22,
                        childAspectRatio: 1.15,
                      ),
                      itemBuilder: (context, index) {
                        final part = bodyParts[index];
                        final title =
                            isEnglish ? part['titleEn'] : part['titleTr'];

                        return InkWell(
                          borderRadius: BorderRadius.circular(28),
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (_) => SymptomSelectionPage(
                                  isEnglish: isEnglish,
                                  bodyPartKey: part['key'],
                                  bodyPartLabel: part['titleEn'],
                                ),
                              ),
                            );
                          },
                          child: Container(
                            decoration: BoxDecoration(
                              color: Colors.white.withOpacity(0.95),
                              borderRadius: BorderRadius.circular(28),
                              border: Border.all(
                                color: Colors.white.withOpacity(0.85),
                                width: 1.5,
                              ),
                              boxShadow: [
                                BoxShadow(
                                  color: Colors.black.withOpacity(0.08),
                                  blurRadius: 16,
                                  offset: const Offset(0, 8),
                                ),
                              ],
                            ),
                            child: Column(
                              children: [
                                Expanded(
                                  child: Padding(
                                    padding: const EdgeInsets.all(16),
                                    child: ClipRRect(
                                      borderRadius: BorderRadius.circular(18),
                                      child: Container(
                                        width: double.infinity,
                                        color: const Color(0xFFF8FAFC),
                                        child: part['asset'] != null
                                            ? Image.asset(
                                                part['asset'],
                                                fit: BoxFit.contain,
                                                errorBuilder: (
                                                  context,
                                                  error,
                                                  stackTrace,
                                                ) {
                                                  return Center(
                                                    child: Icon(
                                                      part['icon'],
                                                      size: 78,
                                                      color:
                                                          const Color(0xFF2563EB),
                                                    ),
                                                  );
                                                },
                                              )
                                            : Center(
                                                child: Icon(
                                                  part['icon'],
                                                  size: 78,
                                                  color:
                                                      const Color(0xFF2563EB),
                                                ),
                                              ),
                                      ),
                                    ),
                                  ),
                                ),
                                Container(
                                  width: double.infinity,
                                  padding: const EdgeInsets.symmetric(
                                    vertical: 14,
                                    horizontal: 10,
                                  ),
                                  decoration: const BoxDecoration(
                                    gradient: LinearGradient(
                                      colors: [
                                        Color(0xFF0F172A),
                                        Color(0xFF1E3A8A),
                                      ],
                                    ),
                                    borderRadius: BorderRadius.vertical(
                                      bottom: Radius.circular(28),
                                    ),
                                  ),
                                  child: Text(
                                    title,
                                    textAlign: TextAlign.center,
                                    style: const TextStyle(
                                      color: Colors.white,
                                      fontSize: 18,
                                      fontWeight: FontWeight.w700,
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    );
                  },
                ),
              ),
            ],
          ),
        ),
      ),
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