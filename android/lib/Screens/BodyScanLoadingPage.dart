import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Screens/ResultPage.dart';

class BodyScanLoadingPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String duration;
  final bool takingMedication;
  final String severity;
  final String inputText;

  const BodyScanLoadingPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.duration,
    required this.takingMedication,
    required this.severity,
    required this.inputText,
  });

  @override
  State<BodyScanLoadingPage> createState() => _BodyScanLoadingPageState();
}

class _BodyScanLoadingPageState extends State<BodyScanLoadingPage>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scanAnimation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 2),
    );

    _scanAnimation = Tween<double>(begin: 0, end: 1).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.easeInOut,
      ),
    );

    _controller.forward();

    Future.delayed(const Duration(seconds: 3), () {
      if (!mounted) return;

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (_) => ResultPage(
            isEnglish: widget.isEnglish,
            symptoms: widget.symptoms,
            duration: widget.duration,
            takingMedication: widget.takingMedication,
            severity: widget.severity,
            inputText: widget.inputText,
          ),
        ),
      );
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  PreferredSizeWidget _appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.white.withOpacity(0.92),
      elevation: 0,
      surfaceTintColor: Colors.transparent,
      automaticallyImplyLeading: false,
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: Center(
          child: Container(
            width: 520,
            padding: const EdgeInsets.all(30),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.92),
              borderRadius: BorderRadius.circular(28),
              border: Border.all(color: Colors.white.withOpacity(0.7)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.10),
                  blurRadius: 20,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  widget.isEnglish
                      ? 'Scanning your symptoms'
                      : 'Pika tjuta nyanganyi',
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.w800,
                    color: Color(0xFF0F172A),
                  ),
                ),
                const SizedBox(height: 24),

                // Body scan animation
                SizedBox(
                  width: 180,
                  height: 300,
                  child: Stack(
                    alignment: Alignment.center,
                    children: [
                      Icon(
                        Icons.accessibility_new_rounded,
                        size: 210,
                        color: const Color(0xFF2563EB).withOpacity(0.25),
                      ),
                      AnimatedBuilder(
                        animation: _scanAnimation,
                        builder: (context, child) {
                          return Positioned(
                            top: 20 + (_scanAnimation.value * 230),
                            child: Container(
                              width: 170,
                              height: 8,
                              decoration: BoxDecoration(
                                borderRadius: BorderRadius.circular(20),
                                gradient: const LinearGradient(
                                  colors: [
                                    Color(0xFF06B6D4),
                                    Color(0xFF2563EB),
                                  ],
                                ),
                                boxShadow: [
                                  BoxShadow(
                                    color: const Color(0xFF2563EB)
                                        .withOpacity(0.45),
                                    blurRadius: 16,
                                    spreadRadius: 3,
                                  ),
                                ],
                              ),
                            ),
                          );
                        },
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 18),
                Text(
                  widget.isEnglish
                      ? 'Please wait while SACA prepares your result...'
                      : 'SACA nyangatja palyalkatinya...',
                  textAlign: TextAlign.center,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w500,
                    color: Colors.black54,
                  ),
                ),
                const SizedBox(height: 22),
                const CircularProgressIndicator(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}