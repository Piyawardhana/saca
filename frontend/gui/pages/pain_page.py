import os
import re

from PySide6.QtCore import Signal, Qt, QSize, QThread
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QMessageBox
)

from .common import BasePage, card_shadow, PRIMARY_DARK, CREAM


class VoiceListenThread(QThread):
    recognised = Signal(str)
    failed = Signal(str)

    def run(self):
        try:
            import speech_recognition as sr

            recognizer = sr.Recognizer()

            recognizer.dynamic_energy_threshold = True
            recognizer.energy_threshold = 300
            recognizer.pause_threshold = 0.8
            recognizer.non_speaking_duration = 0.4

            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=1.0)
                audio = recognizer.listen(
                    source,
                    timeout=6,
                    phrase_time_limit=5
                )

            result = recognizer.recognize_google(
                audio,
                language="en-AU",
                show_all=True
            )

            text = self.extract_best_transcript(result)

            if text:
                self.recognised.emit(text)
            else:
                self.failed.emit("Sorry, I could not understand that. Please try again.")

        except ImportError:
            self.failed.emit(
                "SpeechRecognition or PyAudio is not installed. Please install them first."
            )
        except Exception as e:
            error_name = e.__class__.__name__

            if error_name == "WaitTimeoutError":
                self.failed.emit("No speech detected. Please try again.")
            elif error_name == "UnknownValueError":
                self.failed.emit("Sorry, I could not understand that. Please try again.")
            elif error_name == "RequestError":
                self.failed.emit(
                    "Speech service is unavailable. Please check your internet connection."
                )
            else:
                self.failed.emit(str(e))

    def extract_best_transcript(self, result):
        if isinstance(result, str):
            return result.strip()

        if not isinstance(result, dict):
            return ""

        alternatives = result.get("alternative", [])

        if not alternatives:
            return ""

        best_text = ""

        for item in alternatives:
            transcript = item.get("transcript", "").strip()
            if transcript:
                best_text = transcript
                break

        return best_text


class PainPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()
    pain_selected = Signal(int)

    def __init__(self, voice_mode_enabled=False):
        super().__init__()

        self.selected_score = None
        self.buttons = []
        self.page_title = "How bad is the pain?"
        self.voice_mode_enabled = voice_mode_enabled
        self.voice_thread = None

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

        icon_dir = os.path.join(base_dir, "assets", "icons")

        home_icon_path = os.path.join(icon_dir, "home.png")
        speaker_icon_path = os.path.join(icon_dir, "speaker.png")
        microphone_icon_path = os.path.join(icon_dir, "voice.png")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        shell = self.build_shell()
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(30, 30, 30, 30)
        shell_layout.setSpacing(0)

        top_row = QHBoxLayout()

        self.back_button = self.build_back_button()
        self.back_button.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 14px;
                font-family: Marcellus;
                font-size: 20px;
                font-weight: 900;
                padding: 6px 16px;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
            QPushButton:pressed {{
                background: #1f0e11;
            }}
        """)
        self.back_button.clicked.connect(self.back_requested.emit)

        self.home_button = self.icon_button(home_icon_path)
        self.home_button.clicked.connect(self.home_requested.emit)

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        top_row.addWidget(self.home_button, 0, Qt.AlignRight)

        shell_layout.addLayout(top_row)

        center = QVBoxLayout()
        center.setSpacing(32)
        center.addStretch(1)

        title = QLabel(self.page_title)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 64px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(title)
        title_shadow.setBlurRadius(45)
        title_shadow.setOffset(0, 6)
        title_shadow.setColor(QColor(0, 0, 0, 120))
        title.setGraphicsEffect(title_shadow)

        self.speaker_button = self.icon_button(speaker_icon_path)
        self.speaker_button.clicked.connect(self.speak_title)

        title_row = QHBoxLayout()
        title_row.addStretch(1)
        title_row.addWidget(title)
        title_row.addSpacing(18)
        title_row.addWidget(self.speaker_button, 0, Qt.AlignVCenter)
        title_row.addStretch(1)

        card = QFrame()
        card.setObjectName("ContentCard")
        card.setFixedWidth(860)
        card_shadow(card, blur=28, y=9)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(22)

        self.voice_panel = QFrame()
        self.voice_panel.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)

        voice_panel_layout = QVBoxLayout(self.voice_panel)
        voice_panel_layout.setContentsMargins(0, 0, 0, 4)
        voice_panel_layout.setSpacing(12)

        self.voice_status_label = QLabel(
            "Tap the microphone and say a pain score from 1 to 10."
        )
        self.voice_status_label.setWordWrap(True)
        self.voice_status_label.setAlignment(Qt.AlignCenter)
        self.voice_status_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 20px;
                font-weight: 700;
                color: {PRIMARY_DARK};
                background: transparent;
            }}
        """)

        self.voice_input_button = self.voice_button(microphone_icon_path)
        self.voice_input_button.clicked.connect(self.start_voice_input)

        voice_row = QHBoxLayout()
        voice_row.addStretch(1)
        voice_row.addWidget(self.voice_input_button)
        voice_row.addStretch(1)

        voice_panel_layout.addWidget(self.voice_status_label)
        voice_panel_layout.addLayout(voice_row)

        card_layout.addWidget(self.voice_panel)

        score_row = QHBoxLayout()
        score_row.setSpacing(14)
        score_row.addStretch(1)

        for i in range(1, 11):
            btn = QPushButton(str(i))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(self.default_score_style())
            btn.clicked.connect(
                lambda checked=False, score=i: self.select_score(score)
            )
            self.buttons.append(btn)
            score_row.addWidget(btn)

        score_row.addStretch(1)

        colour_bar = QFrame()
        colour_bar.setFixedHeight(24)
        colour_bar.setStyleSheet("""
            QFrame {
                border: none;
                border-radius: 12px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #22C55E,
                    stop:0.5 #FACC15,
                    stop:1 #EF4444
                );
            }
        """)

        bar_row = QHBoxLayout()
        bar_row.setContentsMargins(58, 0, 58, 0)
        bar_row.addWidget(colour_bar)

        label_row = QHBoxLayout()
        label_row.setContentsMargins(58, 0, 58, 0)

        low_label = QLabel("Low")
        moderate_label = QLabel("Moderate")
        high_label = QLabel("High")

        for label in (low_label, moderate_label, high_label):
            label.setStyleSheet(f"""
                QLabel {{
                    font-family: Marcellus;
                    font-size: 20px;
                    font-weight: 900;
                    color: {PRIMARY_DARK};
                    background: transparent;
                    border: none;
                }}
            """)

        label_row.addWidget(low_label, 0, Qt.AlignLeft)
        label_row.addStretch(1)
        label_row.addWidget(moderate_label, 0, Qt.AlignCenter)
        label_row.addStretch(1)
        label_row.addWidget(high_label, 0, Qt.AlignRight)

        next_btn = QPushButton("Next")
        next_btn.setCursor(Qt.PointingHandCursor)
        next_btn.setFixedSize(240, 68)
        next_btn.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 16px;
                font-family: Marcellus;
                font-size: 22px;
                font-weight: 900;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
            QPushButton:pressed {{
                background: #1f0e11;
            }}
        """)
        card_shadow(next_btn, blur=22, y=7)
        next_btn.clicked.connect(self.submit)

        next_row = QHBoxLayout()
        next_row.addStretch(1)
        next_row.addWidget(next_btn)
        next_row.addStretch(1)

        card_layout.addLayout(score_row)
        card_layout.addLayout(bar_row)
        card_layout.addLayout(label_row)
        card_layout.addLayout(next_row)

        card_row = QHBoxLayout()
        card_row.addStretch(1)
        card_row.addWidget(card)
        card_row.addStretch(1)

        center.addLayout(title_row)
        center.addLayout(card_row)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)

        self.set_voice_mode_enabled(self.voice_mode_enabled)

    def set_voice_mode_enabled(self, enabled: bool):
        self.voice_mode_enabled = enabled

        self.speaker_button.setVisible(enabled)
        self.voice_panel.setVisible(enabled)
        self.voice_input_button.setEnabled(enabled)

        if enabled:
            self.voice_status_label.setText(
                "Tap the microphone and say a pain score from 1 to 10."
            )

    def icon_button(self, icon_path: str):
        button = QPushButton()
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedSize(56, 56)

        button.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                border: none;
                border-radius: 14px;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
            QPushButton:pressed {{
                background: #1f0e11;
            }}
        """)

        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(30, 30))

        card_shadow(button, blur=18, y=4)
        return button

    def voice_button(self, icon_path: str):
        button = QPushButton()
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedSize(72, 72)
        button.setToolTip("Speak your answer")

        button.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 36px;
                font-size: 32px;
                font-weight: 900;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
            QPushButton:pressed {{
                background: #1f0e11;
            }}
            QPushButton:disabled {{
                background: #8a7679;
                color: #f0ebdb;
            }}
        """)

        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(38, 38))
        else:
            button.setText("🎤")

        card_shadow(button, blur=20, y=5)
        return button

    def default_score_style(self):
        return f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 14px;
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
        """

    def selected_score_style(self):
        return """
            QPushButton {
                background: #ddb231;
                color: #30161a;
                border: none;
                border-radius: 14px;
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
            }
        """

    def select_score(self, score: int):
        self.selected_score = score

        for index, btn in enumerate(self.buttons, start=1):
            if index == score:
                btn.setStyleSheet(self.selected_score_style())
            else:
                btn.setStyleSheet(self.default_score_style())

    def speak_title(self):
        if not self.voice_mode_enabled:
            return

        try:
            import pyttsx3

            engine = pyttsx3.init()
            engine.setProperty("rate", 145)
            engine.say(self.page_title)
            engine.say("Please say a number from one to ten.")
            engine.runAndWait()

        except Exception as e:
            QMessageBox.warning(self, "Speaker Error", str(e))

    def start_voice_input(self):
        if not self.voice_mode_enabled:
            return

        self.voice_input_button.setEnabled(False)
        self.voice_status_label.setText(
            "Listening... please say one number from 1 to 10."
        )

        self.voice_thread = VoiceListenThread()
        self.voice_thread.recognised.connect(self.handle_voice_text)
        self.voice_thread.failed.connect(self.handle_voice_error)
        self.voice_thread.finished.connect(
            lambda: self.voice_input_button.setEnabled(True)
        )
        self.voice_thread.start()

    def handle_voice_text(self, spoken_text: str):
        score = self.match_score_from_voice(spoken_text)

        if score is not None:
            self.select_score(score)
            self.voice_status_label.setText(
                f'Heard: "{spoken_text}"\nSelected pain score: {score}. Press Next to continue.'
            )
        else:
            self.voice_status_label.setText(
                f'Heard: "{spoken_text}"\nPlease say only a number from 1 to 10.'
            )

    def handle_voice_error(self, message: str):
        self.voice_status_label.setText(message)
        QMessageBox.warning(self, "Voice Input Error", message)

    def match_score_from_voice(self, spoken_text: str):
        text = spoken_text.lower().strip()

        text = text.replace("-", " ")
        text = text.replace("_", " ")
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        number_match = re.search(r"\b(10|[1-9])\b", text)
        if number_match:
            return int(number_match.group(1))

        phrase_to_number = {
            "zero one": 1,
            "number one": 1,
            "score one": 1,
            "pain one": 1,
            "one": 1,
            "won": 1,
            "first": 1,

            "number two": 2,
            "score two": 2,
            "pain two": 2,
            "two": 2,
            "too": 2,
            "to": 2,
            "second": 2,

            "number three": 3,
            "score three": 3,
            "pain three": 3,
            "three": 3,
            "tree": 3,
            "free": 3,
            "third": 3,

            "number four": 4,
            "score four": 4,
            "pain four": 4,
            "four": 4,
            "for": 4,
            "fore": 4,
            "fourth": 4,

            "number five": 5,
            "score five": 5,
            "pain five": 5,
            "five": 5,
            "fifth": 5,

            "number six": 6,
            "score six": 6,
            "pain six": 6,
            "six": 6,
            "sex": 6,
            "sixth": 6,

            "number seven": 7,
            "score seven": 7,
            "pain seven": 7,
            "seven": 7,
            "seventh": 7,

            "number eight": 8,
            "score eight": 8,
            "pain eight": 8,
            "eight": 8,
            "ate": 8,
            "eighth": 8,

            "number nine": 9,
            "score nine": 9,
            "pain nine": 9,
            "nine": 9,
            "ninth": 9,

            "number ten": 10,
            "score ten": 10,
            "pain ten": 10,
            "ten": 10,
            "tin": 10,
            "tenth": 10,
        }

        sorted_phrases = sorted(
            phrase_to_number.keys(),
            key=len,
            reverse=True
        )

        for phrase in sorted_phrases:
            if re.search(rf"\b{re.escape(phrase)}\b", text):
                return phrase_to_number[phrase]

        compact_text = text.replace(" ", "")

        compact_map = {
            "oneoutoften": 1,
            "twooutoften": 2,
            "threeoutoften": 3,
            "fouroutoften": 4,
            "fiveoutoften": 5,
            "sixoutoften": 6,
            "sevenoutoften": 7,
            "eightoutoften": 8,
            "nineoutoften": 9,
            "tenoutoften": 10,
        }

        if compact_text in compact_map:
            return compact_map[compact_text]

        return None

    def submit(self):
        if self.selected_score is not None:
            self.pain_selected.emit(self.selected_score)
        else:
            QMessageBox.warning(
                self,
                "Pain Score Required",
                "Please select a pain score before continuing."
            )

    def reset(self):
        self.selected_score = None

        for btn in self.buttons:
            btn.setStyleSheet(self.default_score_style())

        if self.voice_mode_enabled:
            self.voice_status_label.setText(
                "Tap the microphone and say a pain score from 1 to 10."
            )
            self.voice_input_button.setEnabled(True)