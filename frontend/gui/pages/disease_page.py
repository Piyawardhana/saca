import os

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel,
    QGridLayout, QFrame, QGraphicsDropShadowEffect
)

from .common import BasePage, ImageCardButton, card_shadow, PRIMARY_DARK, CREAM


BODY_PART_DISEASES = {
    "head": [
        ("Headache", "headache.png"),
        ("Dizziness", "dizziness.png"),
        ("Fever", "fever.png"),
    ],
    "chest": [
        ("Chest Pain", "chest_pain.png"),
        ("Cough", "cough.png"),
        ("Breathing Trouble", "breathing trouble.png"),
    ],
    "abdomen": [
        ("Stomach Pain", "stomach_pain.png"),
        ("Vomiting", "vomiting.png"),
        ("Diarrhea", "diarreha.png"),
    ],
    "back": [
        ("Back Pain", "back_pain.png"),
        ("Muscle Pain", "muscle_pain.png"),
        ("Injury", "injury.png"),
    ],
    "arm": [
        ("Arm Pain", "arm_pain.png"),
        ("Arm Swelling", "arm_swelling.jpeg"),
        ("Injury", "injury.png"),
    ],
    "leg": [
        ("Leg Pain", "leg_pain.jpg"),
        ("Leg Swelling", "leg_swelling.jpg"),
        ("Injury", "injury.png"),
    ],
}


class DiseasePage(BasePage):
    back_requested = Signal()
    disease_selected = Signal(str)

    def __init__(self, assets_dir: str):
        super().__init__()
        self.assets_dir = assets_dir

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
        center.setSpacing(22)
        center.addStretch(1)

        self.title_label = QLabel("Select Matching Symptom")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 64px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(self.title_label)
        title_shadow.setBlurRadius(45)
        title_shadow.setOffset(0, 6)
        title_shadow.setColor(QColor(0, 0, 0, 120))
        self.title_label.setGraphicsEffect(title_shadow)

        self.context_label = QLabel("Body Part: -")
        self.context_label.setAlignment(Qt.AlignCenter)
        self.context_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)

        card = QFrame()
        card.setObjectName("ContentCard")
        card.setFixedWidth(980)
        card.setFixedHeight(360)
        card_shadow(card, blur=28, y=9)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(34, 30, 34, 30)
        card_layout.setSpacing(0)

        self.grid = QGridLayout()
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(18)
        self.grid.setVerticalSpacing(18)

        card_layout.addLayout(self.grid)

        card_row = QHBoxLayout()
        card_row.addStretch(1)
        card_row.addWidget(card)
        card_row.addStretch(1)

        center.addWidget(self.title_label)
        center.addWidget(self.context_label)
        center.addLayout(card_row)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)

    def load_diseases(self, body_part: str):
        self.context_label.setText(f"Body Part: {body_part.title()}")
        self.reset_grid()

        items = BODY_PART_DISEASES.get(body_part, [])

        for index, (name, filename) in enumerate(items):
            row = index // 3
            col = index % 3

            card_btn = ImageCardButton(
                title=name,
                subtitle="",
                image_path=os.path.join(self.assets_dir, "diseases", filename),
                value=name
            )
            card_btn.setFixedSize(280, 250)
            card_btn.clicked_value.connect(self.disease_selected.emit)

            self.grid.addWidget(card_btn, row, col, Qt.AlignCenter)

        for col in range(3):
            self.grid.setColumnStretch(col, 1)

        for row in range(1):
            self.grid.setRowStretch(row, 1)

    def reset_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def reset(self):
        self.context_label.setText("Body Part: -")
        self.reset_grid()