import os

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QVBoxLayout, QFrame, QGridLayout, QLabel, QWidget,
    QSizePolicy, QSpacerItem
)

from .common import BasePage, ImageCardButton, HeaderBar, card_shadow


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
        self.current_body_part = None

        root = QVBoxLayout(self)
        root.setContentsMargins(36, 28, 36, 28)

        page_card = QFrame()
        page_card.setObjectName("PageCard")
        card_shadow(page_card)

        layout = QVBoxLayout(page_card)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(22)

        self.header = HeaderBar(
            title="Select Matching Symptom",
            subtitle="Choose the image that best matches the reported condition."
        )
        self.header.back_button.clicked.connect(self.back_requested.emit)

        self.context_label = QLabel("Body Area: -")
        self.context_label.setStyleSheet("""
            QLabel {
                background: #f6f9fd;
                color: #27476b;
                border: 1px solid #d5e1ef;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 700;
                max-width: 220px;
            }
        """)

        self.grid_host = QWidget()
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(0, 0, 0, 0)
        self.grid.setHorizontalSpacing(18)
        self.grid.setVerticalSpacing(18)

        layout.addWidget(self.header)
        layout.addWidget(self.context_label)
        layout.addWidget(self.grid_host, 1)

        root.addWidget(page_card)

    def load_diseases(self, body_part: str):
        self.current_body_part = body_part
        self.context_label.setText(f"Body Area: {body_part.title()}")
        self._clear_grid()

        items = BODY_PART_DISEASES.get(body_part, [])

        for index, (symptom_name, filename) in enumerate(items):
            row = index // 3
            col = index % 3

            card = ImageCardButton(
                title=symptom_name,
                subtitle="Select to continue",
                image_path=os.path.join(self.assets_dir, "diseases", filename),
                value=symptom_name
            )
            card.setMinimumSize(240, 280)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            card.clicked_value.connect(self.disease_selected.emit)

            self.grid.addWidget(card, row, col)

        # keep columns evenly spaced
        for col in range(3):
            self.grid.setColumnStretch(col, 1)

        # push cards to top instead of weird stretching/overlap feel
        last_row = max(0, (len(items) - 1) // 3 + 1)
        self.grid.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding),
            last_row,
            0,
            1,
            3
        )

    def _clear_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)

    def _clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()
            if widget is not None:
                widget.deleteLater()
            elif child_layout is not None:
                self._clear_layout(child_layout)

    def reset(self):
        self.current_body_part = None
        self.context_label.setText("Body Area: -")
        self._clear_grid()