import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  static const String baseUrl = 'https://saca-render-backend.onrender.com';

  static Future<bool> healthCheck() async {
    final response = await http.get(
      Uri.parse('$baseUrl/health'),
    );

    return response.statusCode == 200;
  }

  static Future<Map<String, dynamic>> predict({
    required String text,
    int? painScore,
    String? bodyPart,
    int? age,
    String? gender,
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/predict'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'text': text,
        'pain_score': painScore,
        'body_part': bodyPart,
        'age': age,
        'gender': gender,
      }),
    );

    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }

    throw Exception('API error: ${response.body}');
  }
}