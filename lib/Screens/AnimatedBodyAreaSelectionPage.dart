import 'dart:math';
import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/InputMethodPage.dart';
import 'package:saca_project/Screens/QuestionOnePage.dart';

class AnimatedBodyAreaSelectionPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;

  const AnimatedBodyAreaSelectionPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
  });

  @override
  State<AnimatedBodyAreaSelectionPage> createState() =>
      _AnimatedBodyAreaSelectionPageState();
}

class _AnimatedBodyAreaSelectionPageState
    extends State<AnimatedBodyAreaSelectionPage>
    with SingleTickerProviderStateMixin {
  late AnimationController controller;
  late Animation<double> animation;

  bool showFront = true;
  String selectedBodyPart = '';

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  @override
  void initState() {
    super.initState();

    controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 650),
    );

    animation = Tween<double>(begin: 0, end: pi).animate(
      CurvedAnimation(
        parent: controller,
        curve: Curves.easeInOut,
      ),
    );
  }

  void flipBody() async {
    if (showFront) {
      await controller.forward();
    } else {
      await controller.reverse();
    }

    setState(() {
      showFront = !showFront;
    });
  }

  void selectPart(String part) {
    setState(() {
      selectedBodyPart = part;
    });
  }

  Widget bodyMarker({
    required double top,
    required double left,
    required String label,
  }) {
    final bool selected = selectedBodyPart == label;

    return Positioned(
      top: top,
      left: left,
      child: GestureDetector(
        onTap: () => selectPart(label),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 220),
          width: selected ? 52 : 42,
          height: selected ? 52 : 42,
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            color: selected ? Colors.red : const Color(0xFF30161A),
            boxShadow: [
              BoxShadow(
                color: selected
                    ? Colors.red.withOpacity(0.55)
                    : Colors.black.withOpacity(0.25),
                blurRadius: selected ? 18 : 8,
                spreadRadius: selected ? 3 : 0,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: const Icon(
            Icons.add_rounded,
            color: Color(0xFFF0EBDB),
            size: 28,
          ),
        ),
      ),
    );
  }

  Widget bodyShape({required bool front}) {
    return SizedBox(
      width: 330,
      height: 520,
      child: Stack(
        alignment: Alignment.center,
        children: [
          Positioned(
            top: 18,
            child: Container(
              width: 78,
              height: 86,
              decoration: BoxDecoration(
                color: const Color(0xFFF1B8AE),
                borderRadius: BorderRadius.circular(45),
              ),
            ),
          ),
          Positioned(
            top: 103,
            child: Container(
              width: front ? 142 : 160,
              height: 180,
              decoration: BoxDecoration(
                color: const Color(0xFFF1B8AE),
                borderRadius: BorderRadius.circular(front ? 48 : 38),
              ),
            ),
          ),
          Positioned(
            top: 128,
            left: 44,
            child: Transform.rotate(
              angle: 0.33,
              child: Container(
                width: 50,
                height: 190,
                decoration: BoxDecoration(
                  color: const Color(0xFFF1B8AE),
                  borderRadius: BorderRadius.circular(28),
                ),
              ),
            ),
          ),
          Positioned(
            top: 128,
            right: 44,
            child: Transform.rotate(
              angle: -0.33,
              child: Container(
                width: 50,
                height: 190,
                decoration: BoxDecoration(
                  color: const Color(0xFFF1B8AE),
                  borderRadius: BorderRadius.circular(28),
                ),
              ),
            ),
          ),
          Positioned(
            top: 276,
            left: 112,
            child: Container(
              width: 48,
              height: 210,
              decoration: BoxDecoration(
                color: const Color(0xFFF1B8AE),
                borderRadius: BorderRadius.circular(26),
              ),
            ),
          ),
          Positioned(
            top: 276,
            right: 112,
            child: Container(
              width: 48,
              height: 210,
              decoration: BoxDecoration(
                color: const Color(0xFFF1B8AE),
                borderRadius: BorderRadius.circular(26),
              ),
            ),
          ),
          if (front) ...[
            bodyMarker(top: 46, left: 144, label: 'Head'),
            bodyMarker(top: 150, left: 144, label: 'Chest'),
            bodyMarker(top: 235, left: 144, label: 'Abdomen'),
            bodyMarker(top: 190, left: 54, label: 'Left Arm'),
            bodyMarker(top: 190, left: 234, label: 'Right Arm'),
            bodyMarker(top: 360, left: 104, label: 'Left Leg'),
            bodyMarker(top: 360, left: 184, label: 'Right Leg'),
          ] else ...[
            bodyMarker(top: 55, left: 144, label: 'Back Head'),
            bodyMarker(top: 140, left: 144, label: 'Upper Back'),
            bodyMarker(top: 235, left: 144, label: 'Lower Back'),
            bodyMarker(top: 145, left: 65, label: 'Left Shoulder'),
            bodyMarker(top: 145, left: 222, label: 'Right Shoulder'),
            bodyMarker(top: 360, left: 104, label: 'Back Left Leg'),
            bodyMarker(top: 360, left: 184, label: 'Back Right Leg'),
          ],
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final updatedSymptoms = [
      ...widget.symptoms,
      if (selectedBodyPart.isNotEmpty) selectedBodyPart,
    ];

    final updatedInputText = [
      widget.inputText,
      if (selectedBodyPart.isNotEmpty) selectedBodyPart,
    ].where((e) => e.trim().isNotEmpty).join(', ');

    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SafeArea(
          bottom: false,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(22),
            child: Column(
              children: [
               HeadingWithMic(
  text: t('Select Pain Area', 'Pika ngurkantja'),
  speakText: t(
    'Select the pain area. Tap the plus button on the body part where you feel pain.',
    'Pika ngurkantja. Plus button patjala body part pika nyinanyangka.',
  ),
  isEnglish: widget.isEnglish,
),
                const SizedBox(height: 14),
                Text(
                  showFront
                      ? t('Front Body View', 'Front body')
                      : t('Back Body View', 'Back body'),
                  style: const TextStyle(
                    color: Color(0xFF30161A),
                    fontSize: 18,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 20),
                Container(
                  width: 760,
                  padding: const EdgeInsets.all(24),
                  decoration: BoxDecoration(
                    color: Colors.white.withOpacity(0.72),
                    borderRadius: BorderRadius.circular(30),
                    border: Border.all(color: Colors.white.withOpacity(0.65)),
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
                      AnimatedBuilder(
                        animation: animation,
                        builder: (context, child) {
                          final angle = animation.value;
                          final isBack = angle > pi / 2;

                          return Transform(
                            alignment: Alignment.center,
                            transform: Matrix4.identity()
                              ..setEntry(3, 2, 0.001)
                              ..rotateY(angle),
                            child: Transform(
                              alignment: Alignment.center,
                              transform: Matrix4.identity()
                                ..rotateY(isBack ? pi : 0),
                              child: bodyShape(front: !isBack),
                            ),
                          );
                        },
                      ),
                      const SizedBox(height: 18),
                      Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(16),
                        decoration: BoxDecoration(
                          color: const Color(0xFFF0EBDB).withOpacity(0.82),
                          borderRadius: BorderRadius.circular(18),
                        ),
                        child: Text(
                          selectedBodyPart.isEmpty
                              ? t('No body area selected', 'Body area wiya')
                              : '${t('Selected area', 'Ngurkantja')}: $selectedBodyPart',
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            color: Color(0xFF30161A),
                            fontSize: 17,
                            fontWeight: FontWeight.w900,
                          ),
                        ),
                      ),
                      const SizedBox(height: 18),
                      GestureDetector(
                        onTap: flipBody,
                        child: Container(
                          width: 260,
                          padding: const EdgeInsets.symmetric(vertical: 15),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(26),
                            gradient: const LinearGradient(
                              colors: [
                                Color(0xFF30161A),
                                Color(0xFF5A2A2F),
                              ],
                            ),
                            boxShadow: [
                              BoxShadow(
                                color: const Color(0xFF30161A)
                                    .withOpacity(0.35),
                                blurRadius: 12,
                                offset: const Offset(0, 6),
                              ),
                            ],
                          ),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const Icon(
                                Icons.flip_rounded,
                                color: Color(0xFFF0EBDB),
                              ),
                              const SizedBox(width: 10),
                              Text(
                                showFront
                                    ? t('Flip to Back', 'Back nyawa')
                                    : t('Flip to Front', 'Front nyawa'),
                                style: const TextStyle(
                                  color: Color(0xFFF0EBDB),
                                  fontWeight: FontWeight.w900,
                                  fontSize: 16,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 28),
                CustomButton(
                  text: t('Next', 'Ankula'),
                  icon: Icons.arrow_forward_rounded,
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => QuestionOnePage(
                          isEnglish: widget.isEnglish,
                          symptoms: updatedSymptoms,
                          inputText: updatedInputText,
                          voiceMode: false,
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
      actions: [
        IconButton(
          onPressed: () {
            Navigator.pushAndRemoveUntil(
              context,
              MaterialPageRoute(
                builder: (_) => InputMethodPage(
                  isEnglish: widget.isEnglish,
                ),
              ),
              (route) => false,
            );
          },
          icon: const Icon(
            Icons.home_rounded,
            color: Color(0xFF30161A),
            size: 28,
          ),
        ),
        const SizedBox(width: 10),
      ],
    );
  }
}