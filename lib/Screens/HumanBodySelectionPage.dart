import 'package:flutter/material.dart';
import 'package:saca_project/Components/AppBackground.dart';
import 'package:saca_project/Components/CustomButton.dart';
import 'package:saca_project/Components/HeadingWithMic.dart';
import 'package:saca_project/Screens/QuestionOnePage.dart';

class HumanBodySelectionPage extends StatefulWidget {
  final bool isEnglish;
  final List<String> symptoms;
  final String inputText;

  const HumanBodySelectionPage({
    super.key,
    required this.isEnglish,
    required this.symptoms,
    required this.inputText,
  });

  @override
  State<HumanBodySelectionPage> createState() => _HumanBodySelectionPageState();
}

class _HumanBodySelectionPageState extends State<HumanBodySelectionPage> {
  bool showFront = true;
  final Set<String> selectedParts = {};

  final Map<String, List<String>> bodyPartSymptoms = {
    'Head': ['Headache', 'Dizziness', 'Blurred Vision', 'Fever'],
    'Chest': ['Chest Pain', 'Shortness of Breath', 'Cough', 'Wheezing'],
    'Abdomen': ['Stomach Pain', 'Vomiting', 'Nausea', 'Diarrhea'],
    'Back Head': ['Back Head Pain', 'Neck Pain', 'Dizziness'],
    'Upper Back': ['Upper Back Pain', 'Shoulder Pain', 'Neck Pain'],
    'Lower Back': ['Lower Back Pain', 'Leg Pain', 'Hip Pain'],
    'Left Shoulder': ['Left Shoulder Pain', 'Left Arm Pain'],
    'Right Shoulder': ['Right Shoulder Pain', 'Right Arm Pain'],
    'Left Back Leg': ['Left Leg Pain', 'Left Knee Pain'],
    'Right Back Leg': ['Right Leg Pain', 'Right Knee Pain'],
  };

  String t(String en, String pit) => widget.isEnglish ? en : pit;

  String partText(String en) {
    if (widget.isEnglish) return en;

    final map = {
      'Head': 'Kata',
      'Chest': 'Pirlpirrpa pika',
      'Abdomen': 'Tjuni pika',
      'Left Hand': 'Left mara pika',
      'Right Hand': 'Right mara pika',
      'Left Foot': 'Left tjina pika',
      'Right Foot': 'Right tjina pika',
      'Back Head': 'Kata back pika',
      'Upper Back': 'Wirtapi pika',
      'Lower Back': 'Lower wirtapi pika',
      'Left Shoulder': 'Left alipiri pika',
      'Right Shoulder': 'Right alipiri pika',
      'Left Back Leg': 'Left tjarlpa pika',
      'Right Back Leg': 'Right tjarlpa pika',
      'Headache': 'Kata pika',
      'Dizziness': 'Kata wiru wiya',
      'Blurred Vision': 'Nyaanytjaku wiya',
      'Fever': 'Fever',
      'Chest Pain': 'Pirlpirrpa pika',
      'Shortness of Breath': 'Breathing wiya',
      'Cough': 'Cough',
      'Wheezing': 'Wheezing',
      'Stomach Pain': 'Tjuni pika',
      'Vomiting': 'Vomiting',
      'Nausea': 'Nausea',
      'Diarrhea': 'Diarrhea',
      'Neck Pain': 'Ngurnti pika',
      'Upper Back Pain': 'Upper tjarna pika',
      'Lower Back Pain': 'Lower tjarna pika',
      'Shoulder Pain': 'Alipiri pika',
      'Leg Pain': 'Tjina pika',
      'Hip Pain': 'Marna pika',
      'Left Arm Pain': 'Left arm pika',
      'Right Arm Pain': 'Right arm pika',
      'Left Knee Pain': 'Left murti pika',
      'Right Knee Pain': 'Right murti pika',
      'Left Thumb Pain': 'Left mara mama pika',
      'Left Index Finger Pain': 'Left index miltji pika',
      'Left Middle Finger Pain': 'Left middle miltji pika',
      'Left Ring Finger Pain': 'Left ring miltji pika',
      'Left Little Finger Pain': 'Left mara ngal pika',
      'Left Palm Pain': 'Left palm pika',
      'Left Wrist Pain': 'Left wrist pika',
      'Right Thumb Pain': 'Right mara mama pika',
      'Right Index Finger Pain': 'Right index miltji pika',
      'Right Middle Finger Pain': 'Right middle miltji pika',
      'Right Ring Finger Pain': 'Right ring miltji pika',
      'Right Little Finger Pain': 'Right mara ngal pika',
      'Right Palm Pain': 'Right palm pika',
      'Right Wrist Pain': 'Right wrist pika',
      'Left Toe Pain': 'Left miltji pika',
      'Left Top Foot Pain': 'Left tjina pika',
      'Left Ankle Pain': 'Left tari pika',
      'Right Toe Pain': 'Right miltji pika',
      'Right Top Foot Pain': 'Right tjina pika',
      'Right Ankle Pain': 'Right tari pika',
    };

    return map[en] ?? en;
  }

  void togglePart(String part) {
    setState(() {
      selectedParts.contains(part)
          ? selectedParts.remove(part)
          : selectedParts.add(part);
    });
  }

  Future<void> openSymptomSelector(String bodyPart) async {
    final symptoms = bodyPartSymptoms[bodyPart] ?? [];

    await showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, dialogSetState) {
            return Dialog(
              backgroundColor: Colors.transparent,
              insetPadding: const EdgeInsets.all(18),
              child: Container(
                width: 520,
                padding: const EdgeInsets.all(22),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.97),
                  borderRadius: BorderRadius.circular(28),
                ),
                child: SingleChildScrollView(
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Row(
                        children: [
                          const SizedBox(width: 40),
                          Expanded(
                            child: Text(
                              '${partText(bodyPart)} ${t("Symptoms", "Pika tjuta")}',
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                color: Color(0xFF30161A),
                                fontSize: 24,
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                          ),
                          _closeButton(context),
                        ],
                      ),
                      const SizedBox(height: 18),
                      for (final symptom in symptoms)
                        _symptomOption(symptom, dialogSetState),
                      const SizedBox(height: 10),
                      CustomButton(
                        text: t('Done', 'Palya'),
                        icon: Icons.check_rounded,
                        onPressed: () => Navigator.pop(context),
                      ),
                    ],
                  ),
                ),
              ),
            );
          },
        );
      },
    );
  }

Widget _symptomOption(
  String symptom,
  void Function(void Function()) dialogSetState,
) {
  final selected = selectedParts.contains(symptom);

  String imagePath = _getSymptomImage(symptom);

  return GestureDetector(
    onTap: () {
      dialogSetState(() {
        selectedParts.contains(symptom)
            ? selectedParts.remove(symptom)
            : selectedParts.add(symptom);
      });

      setState(() {});
    },
    child: AnimatedContainer(
      duration: const Duration(milliseconds: 220),
      width: double.infinity,
      margin: const EdgeInsets.only(bottom: 14),
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: selected
            ? const Color(0xFFF0EBDB)
            : Colors.white.withOpacity(0.96),
        borderRadius: BorderRadius.circular(22),
        border: Border.all(
          color: selected
              ? const Color(0xFF30161A)
              : Colors.grey.withOpacity(0.18),
          width: 2,
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            width: 62,
            height: 62,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(18),
            ),
            child: Padding(
              padding: const EdgeInsets.all(8),
              child: Image.asset(
                imagePath,
                fit: BoxFit.contain,
              ),
            ),
          ),

          const SizedBox(width: 14),

          Expanded(
            child: Text(
              partText(symptom),
              style: const TextStyle(
                color: Color(0xFF30161A),
                fontSize: 18,
                fontWeight: FontWeight.w900,
              ),
            ),
          ),

          AnimatedContainer(
            duration: const Duration(milliseconds: 200),
            width: selected ? 34 : 28,
            height: selected ? 34 : 28,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              color: selected
                  ? Colors.red
                  : Colors.transparent,
              border: Border.all(
                color: const Color(0xFF30161A),
                width: 2,
              ),
            ),
            child: selected
                ? const Icon(
                    Icons.check,
                    color: Colors.white,
                    size: 18,
                  )
                : null,
          ),
        ],
      ),
    ),
  );
}

String _getSymptomImage(String symptom) {
  final s = symptom.toLowerCase();

  if (s.contains('head')) {
    return 'assets/diseases/headache.png';
  }

  if (s.contains('dizziness')) {
    return 'assets/diseases/dizziness.png';
  }

  if (s.contains('blurred')) {
    return 'assets/diseases/dizziness.png';
  }

  if (s.contains('fever')) {
    return 'assets/diseases/fever.png';
  }

  if (s.contains('chest')) {
    return 'assets/diseases/chest_pain.png';
  }

  if (s.contains('breathing')) {
    return 'assets/diseases/breathing trouble.png';
  }

  if (s.contains('cough')) {
    return 'assets/diseases/cough.png';
  }

  if (s.contains('wheezing')) {
    return 'assets/diseases/breathing trouble.png';
  }

  if (s.contains('stomach')) {
    return 'assets/diseases/stomach_pain.png';
  }

  if (s.contains('vomiting')) {
    return 'assets/diseases/vomiting.png';
  }

  if (s.contains('diarrhea')) {
    return 'assets/diseases/diarrhea.png';
  }

  if (s.contains('arm')) {
    return 'assets/diseases/arm_pain.png';
  }

  if (s.contains('leg')) {
    return 'assets/diseases/leg_pain.jpg';
  }

  if (s.contains('swelling')) {
    return 'assets/diseases/leg_swelling.jpg';
  }

  if (s.contains('back')) {
    return 'assets/diseases/back_pain.png';
  }

  if (s.contains('injury')) {
    return 'assets/diseases/injury.png';
  }

  return 'assets/diseases/muscle_pain.png';
}
  Future<void> openDetailSelector({
    required String title,
    required String image,
    required List<String> options,
  }) async {
    await showDialog(
      context: context,
      barrierDismissible: false,
      builder: (context) {
        return StatefulBuilder(
          builder: (context, dialogSetState) {
            return Dialog(
              backgroundColor: Colors.transparent,
              insetPadding: const EdgeInsets.all(18),
              child: Container(
                width: 560,
                padding: const EdgeInsets.all(22),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.97),
                  borderRadius: BorderRadius.circular(28),
                ),
                child: SingleChildScrollView(
                  child: Column(
                    children: [
                      Row(
                        children: [
                          const SizedBox(width: 40),
                          Expanded(
                            child: Text(
                              title,
                              textAlign: TextAlign.center,
                              style: const TextStyle(
                                color: Color(0xFF30161A),
                                fontSize: 25,
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                          ),
                          _closeButton(context),
                        ],
                      ),
                      const SizedBox(height: 18),
                      _detailView(
                        imagePath: image,
                        options: options,
                        dialogSetState: dialogSetState,
                      ),
                      const SizedBox(height: 12),
                      CustomButton(
                        text: t('Done', 'Palya'),
                        icon: Icons.check_rounded,
                        onPressed: () => Navigator.pop(context),
                      ),
                    ],
                  ),
                ),
              ),
            );
          },
        );
      },
    );
  }

  Widget _closeButton(BuildContext context) {
    return GestureDetector(
      onTap: () => Navigator.pop(context),
      child: Container(
        width: 38,
        height: 38,
        decoration: BoxDecoration(
          color: Colors.red.withOpacity(0.12),
          shape: BoxShape.circle,
        ),
        child: const Icon(
          Icons.close_rounded,
          color: Colors.red,
          size: 24,
        ),
      ),
    );
  }

  Widget _detailView({
    required String imagePath,
    required List<String> options,
    required void Function(void Function()) dialogSetState,
  }) {
    return LayoutBuilder(
      builder: (context, constraints) {
        const detailHeight = 420.0;
        final detailWidth =
            constraints.maxWidth < 520 ? constraints.maxWidth : 520.0;

        double px(double value) => detailWidth * value;
        double py(double value) => detailHeight * value;

        return SizedBox(
          height: detailHeight,
          width: detailWidth,
          child: Stack(
            alignment: Alignment.center,
            children: [
              Image.asset(
                imagePath,
                fit: BoxFit.contain,
                height: detailHeight * 0.92,
              ),
              for (final item in options)
                _detailMarker(
                  label: item,
                  x: px(_detailPosition(item).dx),
                  y: py(_detailPosition(item).dy),
                  dialogSetState: dialogSetState,
                ),
            ],
          ),
        );
      },
    );
  }

  Offset _detailPosition(String label) {
    final l = label.toLowerCase();

    if (l.contains('left little')) return const Offset(0.70, 0.21);
    if (l.contains('left ring')) return const Offset(0.59, 0.08);
    if (l.contains('left middle')) return const Offset(0.47, 0.06);
    if (l.contains('left index')) return const Offset(0.37, 0.08);
    if (l.contains('left thumb')) return const Offset(0.22, 0.37);
    if (l.contains('left palm')) return const Offset(0.47, 0.58);
    if (l.contains('left wrist')) return const Offset(0.47, 0.87);

    if (l.contains('right little')) return const Offset(0.25, 0.20);
    if (l.contains('right ring')) return const Offset(0.35, 0.09);
    if (l.contains('right middle')) return const Offset(0.45, 0.04);
    if (l.contains('right index')) return const Offset(0.55, 0.09);
    if (l.contains('right thumb')) return const Offset(0.68, 0.35);
    if (l.contains('right palm')) return const Offset(0.47, 0.54);
    if (l.contains('right wrist')) return const Offset(0.47, 0.82);

    if (l.contains('left toe')) return const Offset(0.50, 0.10);
    if (l.contains('left top foot')) return const Offset(0.50, 0.45);
    if (l.contains('left ankle')) return const Offset(0.50, 0.80);

    if (l.contains('right toe')) return const Offset(0.50, 0.10);
    if (l.contains('right top foot')) return const Offset(0.50, 0.45);
    if (l.contains('right ankle')) return const Offset(0.50, 0.80);

    return const Offset(0.50, 0.50);
  }

  Widget _detailMarker({
    required String label,
    required double x,
    required double y,
    required void Function(void Function()) dialogSetState,
  }) {
    final selected = selectedParts.contains(label);

    return Positioned(
      left: x,
      top: y,
      child: GestureDetector(
        onTap: () {
          dialogSetState(() {
            selectedParts.contains(label)
                ? selectedParts.remove(label)
                : selectedParts.add(label);
          });
          setState(() {});
        },
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 220),
              width: selected ? 42 : 36,
              height: selected ? 42 : 36,
              decoration: BoxDecoration(
                color: selected ? Colors.red : const Color(0xFF00AFCB),
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.add_rounded,
                color: Colors.white,
                size: 24,
              ),
            ),
            if (selected) ...[
              _connectorLine(),
              _markerLabel(label),
            ],
          ],
        ),
      ),
    );
  }

  Widget _markerLabel(String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 5),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.92),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        partText(label),
        style: const TextStyle(
          color: Color(0xFF30161A),
          fontSize: 11,
          fontWeight: FontWeight.w900,
        ),
      ),
    );
  }

  Widget _connectorLine() {
    return Container(
      width: 18,
      height: 2,
      color: const Color(0xFF30161A).withOpacity(0.45),
    );
  }

  Widget bodyMarker({
    required String label,
    required double x,
    required double y,
    required VoidCallback onTap,
    bool labelRight = true,
  }) {
    final selected = selectedParts.contains(label);

    return Positioned(
      left: x,
      top: y,
      child: GestureDetector(
        onTap: onTap,
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (!labelRight) _markerLabel(label),
            if (!labelRight) _connectorLine(),
            AnimatedContainer(
              duration: const Duration(milliseconds: 220),
              width: selected ? 42 : 36,
              height: selected ? 42 : 36,
              decoration: BoxDecoration(
                color: selected ? Colors.red : const Color(0xFF00AFCB),
                shape: BoxShape.circle,
              ),
              child: const Icon(
                Icons.add_rounded,
                color: Colors.white,
                size: 24,
              ),
            ),
            if (labelRight) _connectorLine(),
            if (labelRight) _markerLabel(label),
          ],
        ),
      ),
    );
  }

  Widget bodyView() {
    return SizedBox(
      height: 620,
      width: 560,
      child: Stack(
        alignment: Alignment.center,
        children: [
          Image.asset(
            showFront
                ? 'assets/bodyarea/front_body.png'
                : 'assets/bodyarea/back_body.png',
            height: 590,
            fit: BoxFit.contain,
          ),
          if (showFront) ...[
            bodyMarker(
              label: 'Head',
              x: 255,
              y: 60,
              labelRight: true,
              onTap: () {
               // togglePart('Head');
                openSymptomSelector('Head');
              },
            ),
            bodyMarker(
              label: 'Chest',
              x: 260,
              y: 170,
              labelRight: true,
              onTap: () {
                //togglePart('Chest');
                openSymptomSelector('Chest');
              },
            ),
            bodyMarker(
              label: 'Abdomen',
              x: 260,
              y: 245,
              labelRight: true,
              onTap: () {
               // togglePart('Abdomen');
                openSymptomSelector('Abdomen');
              },
            ),
            bodyMarker(
              label: 'Left Hand',
              x: 60,
              y: 310,
              labelRight: false,
              onTap: () {
              //  togglePart('Left Hand');
                openDetailSelector(
                  title: t('Left Hand Pain Area', 'Left hand pika area'),
                  image: 'assets/bodyarea/left_hand_back.png',
                  options: const [
                    'Left Thumb Pain',
                    'Left Index Finger Pain',
                    'Left Middle Finger Pain',
                    'Left Ring Finger Pain',
                    'Left Little Finger Pain',
                    'Left Palm Pain',
                    'Left Wrist Pain',
                  ],
                );
              },
            ),
            bodyMarker(
              label: 'Right Hand',
              x: 360,
              y: 310,
              labelRight: true,
              onTap: () {
              //  togglePart('Right Hand');
                openDetailSelector(
                  title: t('Right Hand Pain Area', 'Right hand pika area'),
                  image: 'assets/bodyarea/right_hand_back.png',
                  options: const [
                    'Right Thumb Pain',
                    'Right Index Finger Pain',
                    'Right Middle Finger Pain',
                    'Right Ring Finger Pain',
                    'Right Little Finger Pain',
                    'Right Palm Pain',
                    'Right Wrist Pain',
                  ],
                );
              },
            ),
            bodyMarker(
              label: 'Left Foot',
              x: 100,
              y: 525,
              labelRight: false,
              onTap: () {
              //  togglePart('Left Foot');
                openDetailSelector(
                  title: t('Left Foot Pain Area', 'Left foot pika area'),
                  image: 'assets/bodyarea/left_foot.png',
                  options: const [
                    'Left Toe Pain',
                    'Left Top Foot Pain',
                    'Left Ankle Pain',
                  ],
                );
              },
            ),
            bodyMarker(
              label: 'Right Foot',
              x: 305,
              y: 525,
              labelRight: true,
              onTap: () {
              //  togglePart('Right Foot');
                openDetailSelector(
                  title: t('Right Foot Pain Area', 'Right foot pika area'),
                  image: 'assets/bodyarea/right_foot.png',
                  options: const [
                    'Right Toe Pain',
                    'Right Top Foot Pain',
                    'Right Ankle Pain',
                  ],
                );
              },
            ),
          ] else ...[
            bodyMarker(
              label: 'Back Head',
              x: 268,
              y: 65,
              labelRight: true,
              onTap: () {
              //  togglePart('Back Head');
                openSymptomSelector('Back Head');
              },
            ),
            bodyMarker(
              label: 'Upper Back',
              x: 270,
              y: 185,
              labelRight: true,
              onTap: () {
              //  togglePart('Upper Back');
                openSymptomSelector('Upper Back');
              },
            ),
            bodyMarker(
              label: 'Lower Back',
              x: 270,
              y: 275,
              labelRight: true,
              onTap: () {
              //  togglePart('Lower Back');
                openSymptomSelector('Lower Back');
              },
            ),
            bodyMarker(
              label: 'Left Shoulder',
              x: 105,
              y: 145,
              labelRight: false,
              onTap: () {
              //  togglePart('Left Shoulder');
                openSymptomSelector('Left Shoulder');
              },
            ),
            bodyMarker(
              label: 'Right Shoulder',
              x: 320,
              y: 145,
              labelRight: true,
              onTap: () {
              //  togglePart('Right Shoulder');
                openSymptomSelector('Right Shoulder');
              },
            ),
            bodyMarker(
              label: 'Left Back Leg',
              x: 110,
              y: 435,
              labelRight: false,
              onTap: () {
              //  togglePart('Left Back Leg');
                openSymptomSelector('Left Back Leg');
              },
            ),
            bodyMarker(
              label: 'Right Back Leg',
              x: 300,
              y: 435,
              labelRight: true,
              onTap: () {
              //  togglePart('Right Back Leg');
                openSymptomSelector('Right Back Leg');
              },
            ),
          ],
        ],
      ),
    );
  }

  void goNext() {
    if (showFront) {
      setState(() => showFront = false);
      return;
    }

    final updatedSymptoms = [
      ...widget.symptoms,
      ...selectedParts,
    ];

    final updatedInputText = [
      widget.inputText,
      selectedParts.join(', '),
    ].where((e) => e.trim().isNotEmpty).join(', ');

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
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _appBar(context),
      body: AppBackground(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(22),
          child: Column(
            children: [
              HeadingWithMic(
                text: t('Select Pain Area', 'Pika ngurkantja'),
                speakText:
                    'Select the pain area. Tap the plus sign near the body part where you feel pain.',
              ),
              const SizedBox(height: 12),
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
                padding: const EdgeInsets.all(22),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.72),
                  borderRadius: BorderRadius.circular(30),
                ),
                child: Column(
                  children: [
                    bodyView(),
                    const SizedBox(height: 14),

TextButton.icon(
  onPressed: () {
    setState(() {
      showFront = !showFront;
    });
  },
  icon: const Icon(
    Icons.flip_rounded,
    color: Color(0xFF30161A),
  ),
  label: Text(
    showFront
        ? t('View Back Body', 'Back body nyawa')
        : t('View Front Body', 'Front body nyawa'),
    style: const TextStyle(
      color: Color(0xFF30161A),
      fontWeight: FontWeight.w900,
      fontSize: 15,
    ),
  ),
),
                    const SizedBox(height: 16),
                    Container(
                      width: double.infinity,
                      padding: const EdgeInsets.all(15),
                      decoration: BoxDecoration(
                        color: const Color(0xFFF0EBDB).withOpacity(0.82),
                        borderRadius: BorderRadius.circular(18),
                      ),
                      child: Text(
                        selectedParts.isEmpty
                            ? t(
                                'Selected: No body area selected',
                                'Ngurkantja: wiya',
                              )
                            : '${t('Selected', 'Ngurkantja')}: ${selectedParts.map(partText).join(', ')}',
                        textAlign: TextAlign.center,
                        style: const TextStyle(
                          color: Color(0xFF30161A),
                          fontSize: 16,
                          fontWeight: FontWeight.w900,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 28),

if (!showFront)
  CustomButton(
    text: t('Continue', 'Ankula'),
    icon: Icons.arrow_forward_rounded,
    onPressed: goNext,
  ),
            ],
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
}