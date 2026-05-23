import os

from PySide6.QtCore import Signal, Qt, QSize, QThread
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QGraphicsDropShadowEffect, QMessageBox
)

from .common import BasePage, ActionCardButton, card_shadow, PRIMARY_DARK, CREAM


class VoiceListenThread(QThread):
    recognised = Signal(str)
    failed = Signal(str)

    def run(self):
        try:
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=4)
            text = recognizer.recognize_google(audio)
            self.recognised.emit(text)
        except ImportError:
            self.failed.emit("SpeechRecognition or PyAudio is not installed. Please install them first.")
        except Exception as e:
            error_name = e.__class__.__name__
            if error_name == "WaitTimeoutError":
                self.failed.emit("No speech detected. Please try again.")
            elif error_name == "UnknownValueError":
                self.failed.emit("Sorry, I could not understand that. Please try again.")
            elif error_name == "RequestError":
                self.failed.emit("Speech service is unavailable. Please check your internet connection.")
            else:
                self.failed.emit(str(e))


class FoodAllergyPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()
    allergies_submitted = Signal(str)

    def __init__(self, voice_mode_enabled=False):
        super().__init__()

        self.page_title = "Do you have any food allergies?"
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
            QPushButton:hover {{ background: #4a252b; }}
            QPushButton:pressed {{ background: #1f0e11; }}
        """)
        self.back_button.clicked.connect(self.back_requested.emit)

        self.home_button = self.icon_button(home_icon_path)
        self.home_button.clicked.connect(self.home_requested.emit)

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        top_row.addWidget(self.home_button, 0, Qt.AlignRight)
        shell_layout.addLayout(top_row)

        center = QVBoxLayout()
        center.setSpacing(36)
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
        card.setFixedWidth(540)
        card_shadow(card, blur=28, y=9)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 34, 40, 34)
        card_layout.setSpacing(24)

        self.voice_panel = QFrame()
        self.voice_panel.setStyleSheet("QFrame { background: transparent; border: none; }")
        voice_panel_layout = QVBoxLayout(self.voice_panel)
        voice_panel_layout.setContentsMargins(0, 0, 0, 0)
        voice_panel_layout.setSpacing(14)

        self.voice_status_label = QLabel("Tap the microphone and say yes or no.")
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

        yes_btn = ActionCardButton("Yes", "", "Yes", min_width=420, min_height=95)
        no_btn = ActionCardButton("No", "", "No", min_width=420, min_height=95)
        yes_btn.clicked_value.connect(self.allergies_submitted.emit)
        no_btn.clicked_value.connect(self.allergies_submitted.emit)

        for btn in (yes_btn, no_btn):
            row = QHBoxLayout()
            row.addStretch(1)
            row.addWidget(btn)
            row.addStretch(1)
            card_layout.addLayout(row)

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
            self.voice_status_label.setText("Tap the microphone and say yes or no.")

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
            QPushButton:hover {{ background: #4a252b; }}
            QPushButton:pressed {{ background: #1f0e11; }}
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
            QPushButton:hover {{ background: #4a252b; }}
            QPushButton:pressed {{ background: #1f0e11; }}
            QPushButton:disabled {{ background: #8a7679; color: #f0ebdb; }}
        """)
        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(38, 38))
        else:
            button.setText("🎤")
        card_shadow(button, blur=20, y=5)
        return button

    def speak_title(self):
        if not self.voice_mode_enabled:
            return
        try:
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty("rate", 155)
            engine.say(self.page_title)
            engine.say("Choose yes or no.")
            engine.runAndWait()
        except Exception as e:
            QMessageBox.warning(self, "Speaker Error", str(e))

    def start_voice_input(self):
        if not self.voice_mode_enabled:
            return
        self.voice_input_button.setEnabled(False)
        self.voice_status_label.setText("Listening... please say yes or no.")
        self.voice_thread = VoiceListenThread()
        self.voice_thread.recognised.connect(self.handle_voice_text)
        self.voice_thread.failed.connect(self.handle_voice_error)
        self.voice_thread.finished.connect(lambda: self.voice_input_button.setEnabled(True))
        self.voice_thread.start()

    def handle_voice_text(self, spoken_text: str):
        answer = self.match_yes_no(spoken_text)
        if answer:
            self.voice_status_label.setText(f'Heard: "{spoken_text}"\nSelected: {answer}')
            self.allergies_submitted.emit(answer)
        else:
            self.voice_status_label.setText(f'Heard: "{spoken_text}"\nPlease say yes or no.')

    def handle_voice_error(self, message: str):
        self.voice_status_label.setText(message)
        QMessageBox.warning(self, "Voice Input Error", message)

    def match_yes_no(self, spoken_text: str):
        text = spoken_text.lower().strip()
        yes_words = ["yes", "yeah", "yep", "i do", "i have", "have allergies", "allergies"]
        no_words = ["no", "nope", "not", "none", "i don't", "i do not", "no allergies"]
        if any(word in text for word in no_words):
            return "No"
        if any(word in text for word in yes_words):
            return "Yes"
        return None

    def reset(self):
        self.set_voice_mode_enabled(False)

    def reset_page(self):
        self.reset()
