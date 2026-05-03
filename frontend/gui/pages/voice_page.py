import os

from PySide6.QtCore import Signal, QThread, Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QMessageBox, QFrame, QGraphicsDropShadowEffect
)

from .common import BasePage, card_shadow, PRIMARY_DARK, CREAM

try:
    from speech_worker import SpeechWorker
    VOICE_AVAILABLE = True
except ImportError:
    SpeechWorker = None
    VOICE_AVAILABLE = False


class RecordButton(QPushButton):
    def __init__(self, text: str, icon_path: str):
        super().__init__()

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(340, 80)

        self.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                border: none;
                border-radius: 18px;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
            QPushButton:pressed {{
                background: #1f0e11;
            }}
            QPushButton:disabled {{
                background: rgba(48, 22, 26, 150);
            }}
        """)

        card_shadow(self, blur=22, y=7)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(28, 0, 28, 0)
        layout.setSpacing(0)

        content = QHBoxLayout()
        content.setSpacing(10)

        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
                color: {CREAM};
                background: transparent;
                border: none;
            }}
        """)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(44, 44)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
            }
        """)

        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            self.icon_label.setPixmap(
                pixmap.scaled(
                    40,
                    40,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )

        content.addWidget(self.text_label)
        content.addWidget(self.icon_label)

        layout.addStretch(1)
        layout.addLayout(content)
        layout.addStretch(1)

    def set_label(self, text: str):
        self.text_label.setText(text)


class VoicePage(BasePage):
    back_requested = Signal()
    next_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.speech_thread = None
        self.speech_worker = None

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
        voice_icon_path = os.path.join(base_dir, "assets", "icons", "voice.png")

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

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        shell_layout.addLayout(top_row)

        center = QVBoxLayout()
        center.setSpacing(38)
        center.addStretch(1)

        title = QLabel("What is your problem?")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 64px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(title)
        title_shadow.setBlurRadius(45)
        title_shadow.setOffset(0, 6)
        title_shadow.setColor(QColor(0, 0, 0, 120))
        title.setGraphicsEffect(title_shadow)

        card = QFrame()
        card.setObjectName("ContentCard")
        card.setFixedWidth(580)
        card_shadow(card, blur=26, y=8)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(34, 30, 34, 30)
        card_layout.setSpacing(20)

        card_title = QLabel("Voice input")
        card_title.setAlignment(Qt.AlignCenter)
        card_title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 30px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)

        self.status_label = QLabel("Tap the button and speak")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 21px;
                font-weight: 700;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)

        self.transcript_box = QTextEdit()
        self.transcript_box.setPlaceholderText("Recorded symptoms will appear here...")
        self.transcript_box.setFixedHeight(165)
        self.transcript_box.setStyleSheet(f"""
            QTextEdit {{
                background: rgba(240, 235, 219, 240);
                color: {PRIMARY_DARK};
                border: none;
                border-radius: 18px;
                padding: 18px;
                font-family: Marcellus;
                font-size: 22px;
            }}
        """)

        self.record_btn = RecordButton("Start Recording", voice_icon_path)
        self.record_btn.clicked.connect(self.capture_voice)

        record_row = QHBoxLayout()
        record_row.addStretch(1)
        record_row.addWidget(self.record_btn)
        record_row.addStretch(1)

        card_layout.addWidget(card_title)
        card_layout.addWidget(self.status_label)
        card_layout.addWidget(self.transcript_box)
        card_layout.addLayout(record_row)

        card_row = QHBoxLayout()
        card_row.addStretch(1)
        card_row.addWidget(card)
        card_row.addStretch(1)

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

        center.addWidget(title)
        center.addLayout(card_row)
        center.addLayout(next_row)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)

        if not VOICE_AVAILABLE:
            self.record_btn.setEnabled(False)
            self.record_btn.set_label("Microphone Not Available")

    def capture_voice(self):
        if not VOICE_AVAILABLE:
            QMessageBox.warning(self, "Microphone", "Voice input is not available.")
            return

        self.transcript_box.clear()

        self.record_btn.setEnabled(False)
        self.record_btn.set_label("Listening")
        self.status_label.setText("Listening...")

        self.speech_thread = QThread()
        self.speech_worker = SpeechWorker()

        self.speech_worker.moveToThread(self.speech_thread)
        self.speech_thread.started.connect(self.speech_worker.run)

        self.speech_worker.status.connect(self.update_status)
        self.speech_worker.finished.connect(self.on_voice_finished)
        self.speech_worker.error.connect(self.on_voice_error)

        self.speech_worker.finished.connect(self.speech_thread.quit)
        self.speech_worker.error.connect(self.speech_thread.quit)

        self.speech_worker.finished.connect(self.speech_worker.deleteLater)
        self.speech_worker.error.connect(self.speech_worker.deleteLater)
        self.speech_thread.finished.connect(self.speech_thread.deleteLater)

        self.speech_thread.start()

    def update_status(self, message: str):
        self.status_label.setText(message)

    def on_voice_finished(self, text: str):
        self.transcript_box.setPlainText(text)
        self.status_label.setText("Completed")
        self.record_btn.set_label("Start Recording")
        self.record_btn.setEnabled(True)

    def on_voice_error(self, message: str):
        self.status_label.setText("Error")
        self.record_btn.set_label("Start Recording")
        QMessageBox.warning(self, "Voice Input Error", message)
        self.record_btn.setEnabled(True)

    def submit(self):
        self.next_requested.emit(self.transcript_box.toPlainText())

    def reset(self):
        self.status_label.setText("Tap the button and speak")
        self.transcript_box.clear()
        self.record_btn.set_label("Start Recording")
        if VOICE_AVAILABLE:
            self.record_btn.setEnabled(True)