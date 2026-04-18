SYMPTOM_TERMS = [
    "chest pain",
    "breathing difficulty",
    "fever",
    "vomiting",
    "dizziness",
    "headache",
    "cough",
    "fainting",
    "abdominal pain",
    "diarrhea",
    "sore throat",
    "fatigue",
    "weakness",
    "nausea"
]

SEVERITY_WORDS = [
    "severe",
    "mild",
    "moderate",
    "extreme",
    "worst",
    "intense"
]

DURATION_PATTERNS = [
    "today",
    "since morning",
    "for two days",
    "for one day",
    "for hours",
    "for weeks"
]

NEGATION_WORDS = [
    "no",
    "not",
    "without",
    "denies"
]


def extract_symptoms(text: str):
    found = []
    for term in SYMPTOM_TERMS:
        if term in text:
            found.append(term)
    return found


def extract_severity_words(text: str):
    found = []
    for word in SEVERITY_WORDS:
        if word in text:
            found.append(word)
    return found


def extract_duration(text: str):
    found = []
    for pattern in DURATION_PATTERNS:
        if pattern in text:
            found.append(pattern)
    return found