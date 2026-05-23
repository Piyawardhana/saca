import os
from typing import List, Optional

from PySide6.QtCore import QObject, Signal, Slot, QThread


# Keep Hugging Face warning disabled in case old cached imports remain elsewhere.
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


class SpeechRecognitionSetupError(Exception):
    pass


class SpeechRecognitionRuntimeError(Exception):
    pass


def _get_recognizer():
    try:
        import speech_recognition as sr
    except ImportError as exc:
        raise SpeechRecognitionSetupError(
            "SpeechRecognition or PyAudio is not installed. Install them with: "
            "pip install SpeechRecognition PyAudio"
        ) from exc

    recognizer = sr.Recognizer()

    # Better behaviour for short medical-choice answers.
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 300
    recognizer.pause_threshold = 0.7
    recognizer.non_speaking_duration = 0.35
    recognizer.phrase_threshold = 0.25

    return sr, recognizer


def _normalise_candidates(candidates: List[str]) -> List[str]:
    cleaned = []
    seen = set()

    for candidate in candidates:
        if not candidate:
            continue

        text = " ".join(str(candidate).strip().split())
        key = text.lower()

        if text and key not in seen:
            cleaned.append(text)
            seen.add(key)

    return cleaned


def _extract_google_candidates(response) -> List[str]:
    """
    Google's show_all=True response usually looks like:
    {'alternative': [{'transcript': 'four', 'confidence': 0.92}, ...], 'final': True}
    This function safely extracts every transcript alternative.
    """
    if not response:
        return []

    alternatives = response.get("alternative", []) if isinstance(response, dict) else []
    candidates = []

    for alternative in alternatives:
        transcript = alternative.get("transcript") if isinstance(alternative, dict) else None
        if transcript:
            candidates.append(transcript)

    return _normalise_candidates(candidates)


def listen_from_microphone(
    timeout: int = 6,
    phrase_time_limit: int = 6,
    status_callback=None,
):
    sr, recognizer = _get_recognizer()

    try:
        with sr.Microphone() as source:
            if status_callback:
                status_callback("Preparing microphone...")

            # Slightly longer ambient-noise calibration improves short answers.
            recognizer.adjust_for_ambient_noise(source, duration=0.9)

            if status_callback:
                status_callback("Listening... please speak clearly.")

            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

        return sr, recognizer, audio

    except sr.WaitTimeoutError as exc:
        raise TimeoutError("No speech detected. Please try again.") from exc
    except OSError as exc:
        raise SpeechRecognitionRuntimeError(
            "Microphone is not available. Please check your microphone permissions and input device."
        ) from exc
    except Exception as exc:
        raise SpeechRecognitionRuntimeError(str(exc)) from exc


def recognise_with_google(
    recognizer,
    audio,
    language: str = "en-AU",
    include_alternatives: bool = False,
    status_callback=None,
) -> str:
    try:
        if status_callback:
            status_callback("Understanding speech...")

        response = recognizer.recognize_google(
            audio,
            language=language,
            show_all=True,
        )

        candidates = _extract_google_candidates(response)

        if not candidates:
            raise ValueError("Sorry, I could not understand that. Please try again.")

        if include_alternatives:
            # For fixed-choice pages, matching improves when all candidate transcripts are searched.
            return " | ".join(candidates)

        # For free-text pages, use the best transcript only.
        return candidates[0]

    except Exception as exc:
        error_name = exc.__class__.__name__

        if error_name == "UnknownValueError":
            raise ValueError("Sorry, I could not understand that. Please try again.") from exc

        if error_name == "RequestError":
            raise ConnectionError(
                "Speech service is unavailable. Please check your internet connection."
            ) from exc

        if isinstance(exc, (ValueError, ConnectionError)):
            raise

        raise SpeechRecognitionRuntimeError(str(exc)) from exc


def transcribe_microphone(
    timeout: int = 6,
    phrase_time_limit: int = 8,
    language: str = "en-AU",
    include_alternatives: bool = False,
    status_callback=None,
) -> str:
    """
    Enhanced Google Speech Recognition path.

    - No Whisper model loading.
    - Uses en-AU for Australian pronunciation.
    - Uses show_all=True to access alternative transcripts.
    - Fixed-choice pages can search all alternatives for better matching.
    """
    sr, recognizer, audio = listen_from_microphone(
        timeout=timeout,
        phrase_time_limit=phrase_time_limit,
        status_callback=status_callback,
    )

    return recognise_with_google(
        recognizer=recognizer,
        audio=audio,
        language=language,
        include_alternatives=include_alternatives,
        status_callback=status_callback,
    )


class SpeechWorker(QObject):
    finished = Signal(str)
    error = Signal(str)
    status = Signal(str)

    def __init__(self, timeout: int = 6, phrase_time_limit: int = 10, parent=None):
        super().__init__(parent)
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit

    @Slot()
    def run(self):
        try:
            text = transcribe_microphone(
                timeout=self.timeout,
                phrase_time_limit=self.phrase_time_limit,
                language="en-AU",
                include_alternatives=False,
                status_callback=self.status.emit,
            )
            self.finished.emit(text)

        except TimeoutError as exc:
            self.error.emit(str(exc))
        except SpeechRecognitionSetupError as exc:
            self.error.emit(str(exc))
        except SpeechRecognitionRuntimeError as exc:
            self.error.emit(str(exc))
        except ValueError as exc:
            self.error.emit(str(exc))
        except ConnectionError as exc:
            self.error.emit(str(exc))
        except Exception as exc:
            self.error.emit(str(exc))


class VoiceListenThread(QThread):
    recognised = Signal(str)
    failed = Signal(str)
    status = Signal(str)

    def __init__(self, timeout: int = 6, phrase_time_limit: int = 5, parent=None):
        super().__init__(parent)
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit

    def run(self):
        try:
            text = transcribe_microphone(
                timeout=self.timeout,
                phrase_time_limit=self.phrase_time_limit,
                language="en-AU",
                include_alternatives=True,
                status_callback=self.status.emit,
            )
            self.recognised.emit(text)

        except TimeoutError as exc:
            self.failed.emit(str(exc))
        except SpeechRecognitionSetupError as exc:
            self.failed.emit(str(exc))
        except SpeechRecognitionRuntimeError as exc:
            self.failed.emit(str(exc))
        except ValueError as exc:
            self.failed.emit(str(exc))
        except ConnectionError as exc:
            self.failed.emit(str(exc))
        except Exception as exc:
            self.failed.emit(str(exc))
