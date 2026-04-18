import os

from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton,
    QFrame, QGridLayout, QMessageBox, QWidget, QScrollArea
)

from .common import BasePage, ImageCardButton, HeaderBar, card_shadow

try:
    from speech_worker import SpeechWorker
    VOICE_AVAILABLE = True
except ImportError:
    SpeechWorker = None
    VOICE_AVAILABLE = False


class InputPage(BasePage):
    back_requested = Signal()
    text_submitted = Signal(str)
    body_part_selected = Signal(str)

    def __init__(self, assets_dir: str):
        super().__init__()
        self.assets_dir = assets_dir
        self.speech_thread = None
        self.speech_worker = None
        self.selected_gender = None

        root = QVBoxLayout(self)
        root.setContentsMargins(36, 28, 36, 28)

        page_card = QFrame()
        page_card.setObjectName("PageCard")
        card_shadow(page_card)

        layout = QVBoxLayout(page_card)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(22)

        self.header = HeaderBar(
            title="Describe Symptoms",
            subtitle="Use text, microphone input, or select a body area below."
        )
        self.header.back_button.clicked.connect(self.back_requested.emit)

        self.profile_label = QLabel("Profile: -")
        self.profile_label.setStyleSheet("""
            QLabel {
                background: #eef5ff;
                color: #1b4b9b;
                border: 1px solid #cfe0fb;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 700;
                max-width: 160px;
            }
        """)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText(
            "Enter symptoms here.\nExample: chest pain, cough, headache, stomach pain..."
        )
        self.text_edit.setMinimumHeight(85)
        self.text_edit.setMaximumHeight(110)
        self.text_edit.setStyleSheet("""
            QTextEdit {
                background: #fbfdff;
                border: 1px solid #d4dfec;
                border-radius: 18px;
                padding: 16px;
                font-size: 14px;
                color: #10233c;
            }
        """)

        self.voice_btn = QPushButton("Use Microphone")
        self.voice_btn.setObjectName("SecondaryButton")
        self.voice_btn.clicked.connect(self.capture_voice)

        self.analyse_btn = QPushButton("Analyse Input")
        self.analyse_btn.setObjectName("PrimaryButton")
        self.analyse_btn.clicked.connect(self.submit_text)

        self.voice_status_label = QLabel("Microphone status: Ready")
        self.voice_status_label.setStyleSheet("color: #5d7088; font-size: 13px;")

        input_buttons = QHBoxLayout()
        input_buttons.setSpacing(12)
        input_buttons.addWidget(self.voice_btn)
        input_buttons.addWidget(self.analyse_btn)

        section_label = QLabel("Select Body Area")
        section_label.setObjectName("SectionTitle")

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: #edf2f7;
                width: 12px;
                margin: 4px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #c5d4e6;
                min-height: 30px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background: #aebfd5;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
                background: none;
            }
        """)

        scroll_content = QWidget()
        body_grid = QGridLayout(scroll_content)
        body_grid.setContentsMargins(0, 0, 10, 0)
        body_grid.setHorizontalSpacing(8)
        body_grid.setVerticalSpacing(8)

        body_parts = [
            ("Head", "head", "bodyparts/head.png"),
            ("Chest", "chest", "bodyparts/chest.png"),
            ("Abdomen", "abdomen", "bodyparts/abdomen.png"),
            ("Back", "back", "bodyparts/back.png"),
            ("Arm", "arm", "bodyparts/arm.png"),
            ("Leg", "leg", "bodyparts/leg.png"),
        ]

        row = 0
        col = 0
        for title, key, rel_path in body_parts:
            card = ImageCardButton(
                title=title,
                subtitle=f"Select {title.lower()} related symptoms",
                image_path=os.path.join(self.assets_dir, rel_path),
                value=key
            )
            card.setMinimumSize(200, 220)
            card.clicked_value.connect(self.body_part_selected.emit)
            body_grid.addWidget(card, row, col)

            col += 1
            if col > 2:
                col = 0
                row += 1

        body_grid.setColumnStretch(0, 1)
        body_grid.setColumnStretch(1, 1)
        body_grid.setColumnStretch(2, 1)

        scroll.setWidget(scroll_content)
        scroll.setMinimumHeight(360)

        if not VOICE_AVAILABLE:
            self.voice_btn.setEnabled(False)
            self.voice_btn.setText("Microphone Not Available")

        top_section = QVBoxLayout()
        top_section.setSpacing(10)
        top_section.addWidget(self.profile_label, 0, Qt.AlignLeft)
        top_section.addWidget(self.text_edit)
        top_section.addLayout(input_buttons)
        top_section.addWidget(self.voice_status_label)

        bottom_section = QVBoxLayout()
        bottom_section.setSpacing(10)
        bottom_section.addWidget(section_label)
        bottom_section.addWidget(scroll)

        layout.addWidget(self.header)
        layout.addLayout(top_section, 1)
        layout.addLayout(bottom_section, 3)

        root.addWidget(page_card)

    def set_selected_gender(self, gender: str):
        self.selected_gender = gender
        self.profile_label.setText(f"Profile: {gender}")

    def submit_text(self):
        self.text_submitted.emit(self.text_edit.toPlainText())

    def reset(self, keep_gender: bool = False):
        self.text_edit.clear()
        self.voice_status_label.setText("Microphone status: Ready")
        if not keep_gender:
            self.profile_label.setText("Profile: -")

    def capture_voice(self):
        if not VOICE_AVAILABLE:
            QMessageBox.warning(
                self,
                "Microphone",
                "Voice input is not available. Install SpeechRecognition and PyAudio first."
            )
            return

        self.voice_btn.setEnabled(False)
        self.voice_status_label.setText("Microphone status: Listening...")

        self.speech_thread = QThread()
        self.speech_worker = SpeechWorker()

        self.speech_worker.moveToThread(self.speech_thread)
        self.speech_thread.started.connect(self.speech_worker.run)

        self.speech_worker.status.connect(self.update_voice_status)
        self.speech_worker.finished.connect(self.on_voice_finished)
        self.speech_worker.error.connect(self.on_voice_error)

        self.speech_worker.finished.connect(self.speech_thread.quit)
        self.speech_worker.error.connect(self.speech_thread.quit)

        self.speech_worker.finished.connect(self.speech_worker.deleteLater)
        self.speech_worker.error.connect(self.speech_worker.deleteLater)
        self.speech_thread.finished.connect(self.speech_thread.deleteLater)

        self.speech_thread.start()

    def update_voice_status(self, message: str):
        self.voice_status_label.setText(f"Microphone status: {message}")

    def on_voice_finished(self, text: str):
        current = self.text_edit.toPlainText().strip()
        if current:
            self.text_edit.setPlainText(f"{current} {text}")
        else:
            self.text_edit.setPlainText(text)

        self.voice_status_label.setText("Microphone status: Completed")
        self.voice_btn.setEnabled(True)

    def on_voice_error(self, message: str):
        self.voice_status_label.setText("Microphone status: Error")
        QMessageBox.warning(self, "Voice Input Error", message)
        self.voice_btn.setEnabled(True)