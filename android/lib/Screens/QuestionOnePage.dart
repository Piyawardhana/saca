import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'QuestionTwoPage.dart';

class QuestionOnePage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;

  const QuestionOnePage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
  });

  @override
  State<QuestionOnePage> createState() => _QuestionOnePageState();
}

class _QuestionOnePageState extends State<QuestionOnePage> {
  String selectedDuration = '1 Day';

  @override
  Widget build(BuildContext context) {
    final options = widget.isEnglish
        ? ['1 Day', '1-2 Days', '1 Week', 'More than a week']
        : ['1 Tjiṉṯu', '1-2 Tjiṉṯu', '1 Wiiki', 'Wiiki alatji alatji'];

    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            children: [
              _pageTitle(),
              const SizedBox(height: 24),

              _card(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      widget.isEnglish
                          ? '1. How long have you had the pain?'
                          : '1. Pika nyanga yaaltji-yaaltji nyinangi?',
                      style: const TextStyle(
                        fontSize: 23,
                        fontWeight: FontWeight.w800,
                        color: Color(0xFF0F172A),
                      ),
                    ),
                    const SizedBox(height: 22),

                    Wrap(
                      spacing: 14,
                      runSpacing: 14,
                      children: options.map((item) {
                        final selected = selectedDuration == item;

                        return ChoiceChip(
                          label: Text(item),
                          selected: selected,
                          selectedColor: const Color(0xFF2563EB).withOpacity(0.15),
                          backgroundColor: Colors.white.withOpacity(0.9),
                          side: BorderSide(
                            color: selected
                                ? const Color(0xFF2563EB)
                                : Colors.grey.shade300,
                            width: 1.5,
                          ),
                          labelStyle: TextStyle(
                            color: selected
                                ? const Color(0xFF1D4ED8)
                                : const Color(0xFF334155),
                            fontWeight: FontWeight.w800,
                            fontSize: 16,
                          ),
                          avatar: selected
                              ? const Icon(
                                  Icons.check_rounded,
                                  size: 18,
                                  color: Color(0xFF1D4ED8),
                                )
                              : null,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 14,
                            vertical: 12,
                          ),
                          onSelected: (_) {
                            setState(() {
                              selectedDuration = item;
                            });
                          },
                        );
                      }).toList(),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 28),

              CustomButton(
                text: widget.isEnglish ? 'Next' : 'Ankula',
                icon: Icons.arrow_forward_rounded,
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => QuestionTwoPage(
                        isEnglish: widget.isEnglish,
                        symptoms: widget.symptoms,
                        inputText: widget.inputText,
                        duration: selectedDuration,
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

  Widget _pageTitle() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Text(
          widget.isEnglish ? 'Questions' : 'Kulintjaku tjuta',
          style: const TextStyle(
            fontSize: 30,
            fontWeight: FontWeight.w900,
            color: Color(0xFF0F172A),
          ),
        ),
        const SizedBox(width: 10),
        const Icon(Icons.mic_none_rounded, color: Color(0xFF2563EB)),
      ],
    );
  }

  Widget _card({required Widget child}) {
    return Container(
      width: 780,
      padding: const EdgeInsets.all(28),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.93),
        borderRadius: BorderRadius.circular(28),
        border: Border.all(color: Colors.white.withOpacity(0.75)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.08),
            blurRadius: 16,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: child,
    );
  }

  PreferredSizeWidget _appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white.withOpacity(0.94),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      leading: IconButton(
        onPressed: () => Navigator.pop(context),
        icon: const Icon(Icons.arrow_back_ios_new_rounded),
      ),
      title: const Row(
        children: [
          Icon(Icons.favorite_rounded, color: Color(0xFF2563EB)),
          SizedBox(width: 10),
          Text(
            'SACA',
            style: TextStyle(
              color: Color(0xFF0F172A),
              fontWeight: FontWeight.w800,
            ),
          ),
        ],
      ),
    );
  }
}