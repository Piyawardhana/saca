import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Screens/QuestionThreePage.dart';
import 'package:saca_project/Screens/QuestionOnePage.dart';

class TextInputPage extends StatefulWidget {
  final bool isEnglish;

  const TextInputPage({
    super.key,
    required this.isEnglish,
  });

  @override
  State<TextInputPage> createState() => _TextInputPageState();
}

class _TextInputPageState extends State<TextInputPage> {
  TextEditingController symptomController =
    TextEditingController();

  String t(String en, String pit) {
    return widget.isEnglish ? en : pit;
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
            child: Center(
              child: Container(
                width: 700,
                padding: const EdgeInsets.all(30),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.38),
                  borderRadius: BorderRadius.circular(28),
                  border: Border.all(
                    color: Colors.white.withOpacity(0.45),
                  ),
                ),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      t(
                        'What is your problem?',
                        'Nyaa pika nyuntumpa?',
                      ),
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 30,
                        fontWeight: FontWeight.w900,
                        color: Color(0xFF30161A),
                      ),
                    ),
                    const SizedBox(height: 16),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(14),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF0EBDB).withOpacity(0.75),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Text(
                        t(
                          'Hint: Enter all symptoms in one sentence.\nExample: I have headache, fever, chest pain and vomiting.',
                          'Nyuntu pika nyangatja write ngalya.',
                        ),
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          color: Color(0xFF30161A),
                          fontSize: 15,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ),
                    const SizedBox(height: 24),
                    TextField(
                      controller:symptomController,
                      maxLines: 7,
                      style: const TextStyle(
                        color: Color(0xFF30161A),
                        fontSize: 17,
                        fontWeight: FontWeight.w600,
                      ),
                      decoration: InputDecoration(
                        hintText: t(
                          'e.g. I have headache, fever and stomach pain...',
                          'Pika write ngalya...',
                        ),
                        hintStyle: TextStyle(
                          color: Colors.grey.shade600,
                        ),
                        filled: true,
                        fillColor: Colors.white.withOpacity(0.88),
                        contentPadding: const EdgeInsets.all(22),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(22),
                          borderSide: BorderSide.none,
                        ),
                      ),
                    ),
                    const SizedBox(height: 30),
                    CustomButton(
                      text: t('Next', 'Ankula'),
                      icon: Icons.arrow_forward_rounded,
                      onPressed: () {
                        final text = symptomController.text.trim();

                        final symptoms = text
                            .split(',')
                            .map((e) => e.trim())
                            .where((e) => e.isNotEmpty)
                            .toList();

                        Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => QuestionOnePage(
      isEnglish: widget.isEnglish,
      symptoms: [symptomController.text.trim()],
      inputText: symptomController.text.trim(),
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
        ),
      ),
    );
  }
}