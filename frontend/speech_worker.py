import speech_recognition as sr
from PySide6.QtCore import QObject, Signal, Slot


class SpeechWorker(QObject):
    finished = Signal(str)
    error = Signal(str)
    status = Signal(str)

    @Slot()
    def run(self):
        recognizer = sr.Recognizer()

        recognizer.energy_threshold = 250
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.8

        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.1)

                self.status.emit("Listening...")

                audio = recognizer.listen(
                    source,
                    timeout=6,
                    phrase_time_limit=10
                )

            self.status.emit("Processing...")

            try:
                text = recognizer.recognize_google(audio, language="en-AU")
            except:
                text = recognizer.recognize_google(audio, language="en-US")

            text = text.strip()

            if not text:
                self.error.emit("No speech detected.")
                return

            self.finished.emit(text)

        except sr.WaitTimeoutError:
            self.error.emit("No speech detected. Try again.")
        except sr.UnknownValueError:
            self.error.emit("Could not understand. Speak clearly.")
        except sr.RequestError:
            self.error.emit("Network error. Check connection.")
        except Exception as e:
            self.error.emit(str(e))