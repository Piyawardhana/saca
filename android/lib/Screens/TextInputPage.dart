import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
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
  final TextEditingController _controller = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: Center(
          child: Container(
            width: 640,
            padding: const EdgeInsets.all(28),
            decoration: _cardDecoration(),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      widget.isEnglish
                          ? 'What is your problem?'
                          : 'Nyaa pika nyuntumpa?',
                      style: const TextStyle(
                        fontSize: 28,
                        fontWeight: FontWeight.w800,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                    const SizedBox(width: 10),
                    const Icon(Icons.mic_none_rounded, color: Color(0xFF2563EB)),
                  ],
                ),
                const SizedBox(height: 22),
                Container(
                  padding: const EdgeInsets.all(20),
                  decoration: BoxDecoration(
                    color: const Color(0xFFF8FAFC),
                    borderRadius: BorderRadius.circular(22),
                  ),
                  child: Column(
                    children: [
                      Text(
                        widget.isEnglish
                            ? 'Enter symptoms'
                            : 'Pika tjuta walkatjura',
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                      const SizedBox(height: 14),
                      TextField(
                        controller: _controller,
                        maxLines: 6,
                        style: const TextStyle(fontSize: 16),
                        decoration: InputDecoration(
                          hintText: widget.isEnglish
                              ? 'e.g. headache, fever, stomach pain...'
                              : 'kata pika, mapalku pika, tjuni pika...',
                          filled: true,
                          fillColor: Colors.white,
                          contentPadding: const EdgeInsets.all(18),
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(18),
                            borderSide: BorderSide.none,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 26),
                CustomButton(
                  text: widget.isEnglish ? 'Next' : 'Ankula',
                  icon: Icons.arrow_forward_rounded,
                  onPressed: () {
                    final symptoms = _controller.text
                        .split(',')
                        .map((e) => e.trim())
                        .where((e) => e.isNotEmpty)
                        .toList();

                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (_) => QuestionOnePage(
                          isEnglish: widget.isEnglish,
                          symptoms: symptoms,
                          inputText: _controller.text,
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

  BoxDecoration _cardDecoration() {
    return BoxDecoration(
      color: Colors.white.withOpacity(0.90),
      borderRadius: BorderRadius.circular(28),
      border: Border.all(color: Colors.white.withOpacity(0.7)),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withOpacity(0.10),
          blurRadius: 20,
          offset: const Offset(0, 10),
        ),
      ],
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