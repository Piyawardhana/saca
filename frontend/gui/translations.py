DEFAULT_LANGUAGE = "English"
PITJANTJATJARA = "Pitjantjatjara"


# ============================================================
# Global UI translations
# ============================================================
# NOTE:
# These translations are for assignment/demo UI support.
# For real clinical use, final Pitjantjatjara medical wording should be
# checked by a qualified Pitjantjatjara translator or Aboriginal health body.
# ============================================================


TEXT_LABEL_TRANSLATIONS = {
    # Welcome page
    "Adaptive Clinical Assistant\n(SACA)": "SACA\nAṉangu Tjukaruru",
    "Get Started": "Palyala",

    # Language page
    "Choose Language": "Wangka ngurkantala",
    "English": "English",
    "Pitjantjatjara": "Pitjantjatjara",

    # General labels
    "Home": "Ngura",
    "Next": "Mapalku",

    # Important:
    # For QLabel text, "Back" usually means the body part.
    # For QPushButton text, "Back" is handled separately below as "Kuwaripa".
    "Back": "Wirtapi",

    # Input method page
    "How do you want to tell us?": "Yaaltji-yaaltji wangkanyi?",
    "Text": "Walkatjuwa",
    "Voice": "Wangka",
    "Speak": "Wangka",
    "Language": "Wangka",
    "Image": "Munu",
    "Image Selection": "Munu ngurkantala",

    # Symptom Selection
    "Select Symptom": "Pika ngurkantala",
    "Select Matching Symptom": "Pika kutju ngurkantala",

    # Description page
    "What is your problem?": "Nyaa pika nyuntula?",
    "Enter symptoms": "Pika walkatjunanyi",
    "e.g. headache, fever, stomach pain...": "Kata pika, pika pulka, tjuni pika...",

    # Voice page
    "Voice input": "Wangka kulini",
    "Voice Input": "Wangka kulini",
    "Tap the button and speak": "Button puwa munu wangka",
    "Recorded symptoms will appear here...": "Pika wangka nyanganyi...",
    "Start Recording": "Wangka tjaratjunanyi",
    "Listening": "Kulini",
    "Listening...": "Kulini...",
    "Completed": "Palyanu",
    "Error": "Wiya palyanu",
    "Microphone": "Microphone",
    "Microphone Not Available": "Microphone wiya",
    "Voice Input Error": "Wangka wiya",
    "Voice input is not available.": "Wangka wiya mantjini.",

    # Body part page
    "Select Body Part": "Aṉangu ngurkantala",
    "Body Part": "Aṉangu",
    "Body Part:": "Aṉangu:",
    "Body Part: -": "Aṉangu: -",

    # Body parts
    "Head": "Kata",
    "Chest": "Ipi",
    "Abdomen": "Tjuni",
    "Arm": "Muḻi",
    "Leg": "Tjina",
    "Back": "Wirtapi",

    # Symptoms / disease labels
    "Headache": "Kata pika",
    "Dizziness": "Kata wampa",
    "Fever": "Pika pulka",
    "Chest Pain": "Ipi pika",
    "Cough": "Kuṉpu",
    "Breathing Trouble": "Ngaaṉytju-ngaaṉytju",
    "Stomach Pain": "Tjuni pika",
    "Vomiting": "Gumanpa",
    "Diarrhea": "Tjuṉkurpa",
    "Back Pain": "Wirtapi pika",
    "Muscle Pain": "Pika",
    "Injury": "Pika",
    "Arm Pain": "Muḻi pika",
    "Arm Swelling": "Muḻi puḻka-rianyi",
    "Leg Pain": "Tjina pika",
    "Leg Swelling": "Tjina puḻka-rianyi",

    # Duration page
    "How long have you had this?": "Tjintu yaaltji-yaaltji pika?",
    "1 Day": "Tjintu kutju",
    "1–2 Days": "Tjintu 1–2",
    "1-2 Days": "Tjintu 1–2",
    "2–3 Days": "Tjintu 2–3",
    "2-3 Days": "Tjintu 2–3",
    "3–4 Days": "Tjintu 3–4",
    "3-4 Days": "Tjintu 3–4",
    "4–5 Days": "Tjintu 4–5",
    "4-5 Days": "Tjintu 4–5",
    "1 Week": "Wiki kutju",
    "More than a week": "Wiki rawa",

    # Pain page
    "How bad is the pain?": "Yaaltji-yaaltji pika pulka?",
    "Low": "Kulunypa",
    "Moderate": "Pika",
    "High": "Pulka",

    # Medication page
    "Do you take any medications?": "Medicine mantjini?",
    "Yes": "Uwa",
    "No": "Wiya",

    # Result page
    "Results": "Nyanganyi",
    "Severity Level": "Pika pulka",
    "Not Available": "Wiya",
    "Not available": "Wiya",
    "Not available.": "Wiya.",
    "NOT AVAILABLE": "WIYA",
    "Possible Conditions": "Pika kutjupa",
    "Recommendation": "Tjukurpa",
    "Detected Information": "Tjukurpa nyangu",
    "Contact Ambulance 🚑": "Ambulance-kutu wangka 🚑",
    "Start Again 🧑‍⚕️": "Munta piṟuku 🧑‍⚕️",

    "MILD": "PIKA KULUNYPA",
    "MODERATE": "PIKA",
    "SEVERE": "PIKA PULKA",
    "UNKNOWN": "WAMPA",
    "Unknown": "Wampa",

    "Input": "Wangka",
    "Input:": "Wangka:",
    "Input method": "Ara",
    "Input method:": "Ara:",
    "Duration": "Tjintu",
    "Duration:": "Tjintu:",
    "Pain score": "Pika score",
    "Pain score:": "Pika score:",
    "Medication": "Medicine",
    "Medication:": "Medicine:",
    "Detected symptoms": "Pika nyangu",
    "Detected symptoms:": "Pika nyangu:",
    "Detected symptoms: None": "Pika nyangu: Wiya",
    "Warning signs": "Pika pulka",
    "Warning signs:": "Pika pulka:",
    "Warning signs: None": "Pika pulka: Wiya",
    "Selected symptom/condition": "Pika ngurkantanu",
    "Selected symptom/condition:": "Pika ngurkantanu:",
    "None": "Wiya",

    "No recommendation available.": "Tjukurpa wiya.",
    "Disease prediction will be added after the disease model is connected.": (
        "Disease model wiya."
    ),
    "This is not a medical diagnosis. Please consult a healthcare professional.": (
        "Nyangatja doctor diagnosis wiya. Health worker-kutu wangka."
    ),

    # Backend/internal values
    "text": "walkatjunanyi",
    "voice": "wangka",
    "image": "munu",
    "head": "kata",
    "chest": "ipi",
    "abdomen": "tjuni",
    "back": "wirtapi",
    "arm": "muḻi",
    "leg": "tjina",

    # Error dialogs
    "Missing Input": "Wangka wiya",
    "Please enter a description.": "Pika walkatjunanyi.",
    "Please record symptoms first.": "Pika wangka tjaratjunanyi.",
    "Please provide symptoms before continuing.": "Pika ngurkantala.",
    "Prediction Error": "Wiya palyanu",
}


BUTTON_TRANSLATIONS = {
    **TEXT_LABEL_TRANSLATIONS,

    # Button-specific translations
    "Back": "Malaku",
    "Home": "Ngura",
    "Next": "Mapalku",
    "Contact Ambulance 🚑": "Ambulance-kutu wangka 🚑",
    "Start Again 🧑‍⚕️": "Munta piṟuku 🧑‍⚕️",
}


def normalise_language(language: str | None) -> str:
    if not language:
        return DEFAULT_LANGUAGE

    value = str(language).strip().lower()

    if value in ["pitjantjatjara", "pitjantjatjara language"]:
        return PITJANTJATJARA

    return DEFAULT_LANGUAGE


def is_pitjantjatjara(language: str | None) -> bool:
    return normalise_language(language) == PITJANTJATJARA


def _reverse_map(mapping: dict[str, str]) -> dict[str, str]:
    reversed_items = {}
    for english, pitjantjatjara in mapping.items():
        if pitjantjatjara not in reversed_items:
            reversed_items[pitjantjatjara] = english
    return reversed_items


REVERSE_BUTTON_TRANSLATIONS = _reverse_map(BUTTON_TRANSLATIONS)
REVERSE_LABEL_TRANSLATIONS = _reverse_map(TEXT_LABEL_TRANSLATIONS)


def _normalise_to_english(value: str, widget_type: str = "label") -> str:
    if value is None:
        return value
    value = str(value)
    if not value.strip():
        return value

    mapping = (
        REVERSE_BUTTON_TRANSLATIONS
        if widget_type == "button"
        else REVERSE_LABEL_TRANSLATIONS
    )

    if value in mapping:
        return mapping[value]

    result = value
    for pit, eng in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
        if pit and pit in result:
            result = result.replace(pit, eng)
    return result


def translate_text(value: str, language: str | None, widget_type: str = "label") -> str:
    if value is None:
        return value
    value = str(value)
    if not value.strip():
        return value

    english_value = _normalise_to_english(value, widget_type)

    if not is_pitjantjatjara(language):
        return english_value

    mapping = (
        BUTTON_TRANSLATIONS
        if widget_type == "button"
        else TEXT_LABEL_TRANSLATIONS
    )

    if english_value in mapping:
        return mapping[english_value]

    result = english_value
    for eng, pit in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
        if eng and eng in result:
            result = result.replace(eng, pit)
    return result


BODY_PART_KEYS = {
    "English": {
        "head": "Head",
        "chest": "Chest",
        "abdomen": "Abdomen",
        "back": "Back",
        "arm": "Arm",
        "leg": "Leg",
    },
    "Pitjantjatjara": {
        "head": "Kata",
        "chest": "Ipi",
        "abdomen": "Tjuni",
        "back": "Wirtapi",
        "arm": "Muḻi",
        "leg": "Tjina",
    },
}


DISEASE_KEYS = {
    "English": {
        "Headache": "Headache",
        "Dizziness": "Dizziness",
        "Fever": "Fever",
        "Chest Pain": "Chest Pain",
        "Cough": "Cough",
        "Breathing Trouble": "Breathing Trouble",
        "Stomach Pain": "Stomach Pain",
        "Vomiting": "Vomiting",
        "Diarrhea": "Diarrhea",
        "Back Pain": "Back Pain",
        "Muscle Pain": "Muscle Pain",
        "Injury": "Injury",
        "Arm Pain": "Arm Pain",
        "Arm Swelling": "Arm Swelling",
        "Leg Pain": "Leg Pain",
        "Leg Swelling": "Leg Swelling",
    },
    "Pitjantjatjara": {
        "Headache": "Kata pika",
        "Dizziness": "Kata wampa",
        "Fever": "Pika pulka",
        "Chest Pain": "Ipi pika",
        "Cough": "Kuṉpu",
        "Breathing Trouble": "Ngaaṉytju-ngaaṉytju",
        "Stomach Pain": "Tjuni pika",
        "Vomiting": "Gumanpa",
        "Diarrhea": "Tjuṉkurpa",
        "Back Pain": "Wirtapi pika",
        "Muscle Pain": "Pika",
        "Injury": "Pika",
        "Arm Pain": "Muḻi pika",
        "Arm Swelling": "Muḻi puḻka-rianyi",
        "Leg Pain": "Tjina pika",
        "Leg Swelling": "Tjina puḻka-rianyi",
    },
}


INPUT_METHOD_KEYS = {
    "English": {
        "text": "Text",
        "voice": "Voice",
        "image": "Image selection",
    },
    "Pitjantjatjara": {
        "text": "Walkatjunanyi",
        "voice": "Wangka",
        "image": "Munu",
    },
}


YES_NO_KEYS = {
    "English": {
        "yes": "Yes",
        "no": "No",
    },
    "Pitjantjatjara": {
        "yes": "Uwa",
        "no": "Wiya",
    },
}


def text(key: str, language: str | None = None) -> str:
    key_map = {
        "back": "Back",
        "home": "Home",
        "next": "Next",
        "select_body_part": "Select Body Part",
        "select_symptom": "Select Symptom",
        "select_matching_symptom": "Select Matching Symptom",
        "body_part": "Body Part",
        "results": "Results",
        "severity_level": "Severity Level",
        "not_available": "Not Available",
        "possible_conditions": "Possible Conditions",
        "recommendation": "Recommendation",
        "detected_information": "Detected Information",
        "contact_ambulance": "Contact Ambulance 🚑",
        "start_again": "Start Again 🧑‍⚕️",
        "mild": "MILD",
        "moderate": "MODERATE",
        "severe": "SEVERE",
        "unknown": "UNKNOWN",
        "input": "Input",
        "input_method": "Input method",
        "language": "Language",
        "duration": "Duration",
        "pain_score": "Pain score",
        "medication": "Medication",
        "detected_symptoms": "Detected symptoms",
        "warning_signs": "Warning signs",
        "none": "None",
        "selected_condition": "Selected symptom/condition",
        "prediction_not_connected": "Disease prediction will be added after the disease model is connected.",
        "no_recommendation": "No recommendation available.",
        "disclaimer": "This is not a medical diagnosis. Please consult a healthcare professional.",
    }
    english_text = key_map.get(key, key)
    if key in {"back", "home", "next", "contact_ambulance", "start_again"}:
        return translate_text(english_text, language, widget_type="button")
    return translate_text(english_text, language, widget_type="label")


def body_part_label(body_part_key: str, language: str | None = None) -> str:
    lang = normalise_language(language)
    key = str(body_part_key).strip().lower()
    return BODY_PART_KEYS.get(lang, BODY_PART_KEYS["English"]).get(
        key, BODY_PART_KEYS["English"].get(key, key.title())
    )


def disease_label(disease_name: str, language: str | None = None) -> str:
    lang = normalise_language(language)
    key = str(disease_name).strip()
    return DISEASE_KEYS.get(lang, DISEASE_KEYS["English"]).get(
        key, DISEASE_KEYS["English"].get(key, key)
    )


def input_method_label(method: str | None, language: str | None = None) -> str:
    if not method: return ""
    lang = normalise_language(language)
    key = str(method).strip().lower()
    return INPUT_METHOD_KEYS.get(lang, INPUT_METHOD_KEYS["English"]).get(
        key, INPUT_METHOD_KEYS["English"].get(key, key.title())
    )


def yes_no_label(value: str | None, language: str | None = None) -> str:
    if not value: return ""
    lang = normalise_language(language)
    key = str(value).strip().lower()
    if key in ["yes", "uwa", "true", "1"]: key = "yes"
    elif key in ["no", "wiya", "false", "0"]: key = "no"
    return YES_NO_KEYS.get(lang, YES_NO_KEYS["English"]).get(key, value)