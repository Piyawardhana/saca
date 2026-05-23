import 'dart:convert';
import 'package:http/http.dart' as http;

class PredictionService {
  static const String baseUrl = 'http://127.0.0.1:8000';

  static Future<Map<String, dynamic>> predict({
    required String text,
    required List<String> symptoms,
    required String severity,
    required String duration,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/predict'),
      headers: {
        'Content-Type': 'application/json',
      },
      body: jsonEncode({
        'text': text.trim().isEmpty ? symptoms.join(', ') : text.trim(),
        'pain_score': _painScore(severity),
        'duration_days': _durationDays(duration),
        'body_part': null,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    throw Exception('API Error: ${response.body}');
  }

  static int _painScore(String severity) {
    final value = severity.toLowerCase().trim();

    if (value.contains('high')) return 8;
    if (value.contains('moderate')) return 5;
    if (value.contains('low')) return 2;

    return 5;
  }

  static int _durationDays(String duration) {
    final value = duration.toLowerCase().trim();

    if (value.contains('10 day')) return 10;
    if (value.contains('9 day')) return 9;
    if (value.contains('8 day')) return 8;
    if (value.contains('7 day')) return 7;
    if (value.contains('6 day')) return 6;
    if (value.contains('5 day')) return 5;
    if (value.contains('4 day')) return 4;
    if (value.contains('3 day')) return 3;
    if (value.contains('2 day')) return 2;
    if (value.contains('1 day')) return 1;

    if (value.contains('1 week')) return 7;
    if (value.contains('3 week')) return 21;
    if (value.contains('1 month')) return 30;
    if (value.contains('more')) return 31;

    return 0;
  }
}