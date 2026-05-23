import 'dart:ui';
import 'package:flutter/material.dart';

class AppBackground extends StatelessWidget {
  final Widget child;

  const AppBackground({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox.expand(
      child: Stack(
        fit: StackFit.expand,
        children: [
          Image.asset(
            'assets/images/mobile_bg.png',
            fit: BoxFit.cover,
          ),
          Container(
            color: Colors.white.withOpacity(0.08),
          ),
          BackdropFilter(
            filter: ImageFilter.blur(sigmaX: 1.2, sigmaY: 1.2),
            child: Container(color: Colors.transparent),
          ),
          child,
        ],
      ),
    );
  }
}