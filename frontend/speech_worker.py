import speech_recognition as sr
from PySide6.QtCore import QObject, Signal, Slot


class SpeechWorker(QObject):
    finished = Signal(str)
    error = Signal(str)
    status = Signal(str)

    @Slot()
    def run(self):
        recognizer = sr.Recognizer()

        try:
            self.status.emit("Listening...")

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)

            self.status.emit("Transcribing...")

            text = recognizer.recognize_google(audio)
            self.finished.emit(text)

        except sr.WaitTimeoutError:
            self.error.emit("No speech detected in time.")
        except sr.UnknownValueError:
            self.error.emit("Could not understand the audio.")
        except sr.RequestError as e:
            self.error.emit(f"Speech service error: {e}")
        except Exception as e:
            self.error.emit(str(e))