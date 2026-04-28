import 'package:flutter/material.dart';

class CustomButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final IconData? icon;
  final List<Color>? gradientColors;
  final double width;
  final double height;

  const CustomButton({
    super.key,
    required this.text,
    required this.onPressed,
    this.icon,
    this.gradientColors,
    this.width = 240,
    this.height = 56,
  });

  @override
  Widget build(BuildContext context) {
    final colors = gradientColors ??
        const [
          Color(0xFF1D4ED8),
          Color(0xFF2563EB),
        ];

    return SizedBox(
      width: width,
      height: height,
      child: DecoratedBox(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(18),
          gradient: LinearGradient(
            colors: colors,
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          boxShadow: [
            BoxShadow(
              color: colors.last.withOpacity(0.30),
              blurRadius: 18,
              offset: const Offset(0, 8),
            ),
          ],
        ),
        child: ElevatedButton.icon(
          onPressed: onPressed,
          icon: icon != null
              ? Icon(icon, color: Colors.white, size: 18)
              : const SizedBox.shrink(),
          label: Text(
            text,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w700,
              color: Colors.white,
            ),
          ),
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.transparent,
            shadowColor: Colors.transparent,
            surfaceTintColor: Colors.transparent,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(18),
            ),
          ),
        ),
      ),
    );
  }
}