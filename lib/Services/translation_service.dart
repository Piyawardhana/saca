class TranslationService {
  static final Map<String, String> pitToEnglish = {
    'kata pika': 'headache',
    'chest pika': 'chest pain',
    'tjuni pika': 'stomach pain',
    'tjana pika': 'leg pain',
    'mara pika': 'hand pain',
    'fever': 'fever',
    'cough': 'cough',
    'vomiting': 'vomiting',
    'diarrhea': 'diarrhea',
    'breathing wiya': 'breathing difficulty',
  };

  static final Map<String, String> englishToPit = {
    'Unknown': 'Wiya ninti',
    'Prediction unavailable': 'Prediction wiya',
    'Low': 'Low',
    'Moderate': 'Moderate',
    'High': 'High',
    'Please consult a doctor if symptoms continue.':
        'Pika alatji nyinanyi, doctor nyawa.',
    'Backend connection failed. Please check the API server.':
        'Backend connection wiya. API server check palya.',
  };

  static Future<String> toEnglish(String text) async {
    String translated = text.toLowerCase();

    pitToEnglish.forEach((pit, en) {
      translated = translated.replaceAll(pit, en);
    });

    return translated;
  }

  static Future<String> toPitjantjatjara(String text) async {
    String translated = text;

    englishToPit.forEach((en, pit) {
      translated = translated.replaceAll(en, pit);
    });

    return translated;
  }
}