import re

def normalize_text(text: str) -> str:
    text = text.lower().strip()

    phrase_map = {
        "shortness of breath": "breathing difficulty",
        "cannot breathe": "breathing difficulty",
        "trouble breathing": "breathing difficulty",
        "chest tightness": "chest pain",
        "throwing up": "vomiting",
        "feeling dizzy": "dizziness",
        "passed out": "fainting",
        "high temperature": "fever"
    }

    for old, new in phrase_map.items():
        text = text.replace(old, new)

    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text