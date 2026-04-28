import 'package:flutter/material.dart';

class QuestionTile extends StatelessWidget {
  final String question;
  final bool? value;
  final ValueChanged<bool?> onChanged;

  const QuestionTile({
    super.key,
    required this.question,
    required this.value,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.55),
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: Colors.white.withOpacity(0.35)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            question,
            style: const TextStyle(
              fontSize: 17,
              fontWeight: FontWeight.w600,
              color: Color(0xFF1F2937),
            ),
          ),
          const SizedBox(height: 14),
          Row(
            children: [
              Expanded(
                child: RadioListTile<bool>(
                  contentPadding: EdgeInsets.zero,
                  title: const Text("Yes"),
                  value: true,
                  groupValue: value,
                  onChanged: onChanged,
                ),
              ),
              Expanded(
                child: RadioListTile<bool>(
                  contentPadding: EdgeInsets.zero,
                  title: const Text("No"),
                  value: false,
                  groupValue: value,
                  onChanged: onChanged,
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}