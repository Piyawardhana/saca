NEGATED_PATTERNS = [
    "no fever",
    "no chest pain",
    "no vomiting",
    "no dizziness",
    "not breathing difficulty",
    "without fever",
    "without vomiting"
]

DANGER_TERMS = [
    "chest pain",
    "breathing difficulty",
    "fainting",
    "unconscious",
    "seizure",
    "severe bleeding"
]


def detect_negations(text: str):
    found = []
    for phrase in NEGATED_PATTERNS:
        if phrase in text:
            found.append(phrase)
    return found


def detect_danger_terms(text: str):
    found = []
    for term in DANGER_TERMS:
        if term in text:
            found.append(term)
    return found