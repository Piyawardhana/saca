import os

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QGridLayout, QScrollArea, QSizePolicy, QSpacerItem

from .common import BasePage, ImageCardButton


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
        shell_layout.setContentsMargins(20, 20, 20, 20)
        shell_layout.setSpacing(0)

        top_row = QHBoxLayout()
        self.back_button = self.build_back_button()
        self.back_button.clicked.connect(self.back_requested.emit)
        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        shell_layout.addLayout(top_row)

        center = QVBoxLayout()
        center.setSpacing(16)

        self.title_label = QLabel("Select Matching Symptom")
        self.title_label.setObjectName("PageTitle")
        self.title_label.setAlignment(Qt.AlignCenter)

        self.context_label = QLabel("Body Part: -")
        self.context_label.setObjectName("SmallText")
        self.context_label.setAlignment(Qt.AlignCenter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent; border: none;")

        self.grid_host = QWidget()
        self.grid = QGridLayout(self.grid_host)
        self.grid.setContentsMargins(10, 10, 10, 10)
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(8)

        scroll.setWidget(self.grid_host)
        scroll.setMinimumHeight(470)

        center.addWidget(self.title_label)
        center.addWidget(self.context_label)
        center.addWidget(scroll, 1)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)

    def load_diseases(self, body_part: str):
        self.context_label.setText(f"Body Part: {body_part.title()}")
        self.reset_grid()

        items = BODY_PART_DISEASES.get(body_part, [])

        for index, (name, filename) in enumerate(items):
            row = index // 3
            col = index % 3

            card = ImageCardButton(
                title=name,
                subtitle="Select to continue",
                image_path=os.path.join(self.assets_dir, "diseases", filename),
                value=name
            )
            card.clicked_value.connect(self.disease_selected.emit)
            self.grid.addWidget(card, row, col)

        for col in range(3):
            self.grid.setColumnStretch(col, 1)

        last_row = max(0, (len(items) - 1) // 3 + 1)
        self.grid.addItem(
            QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding),
            last_row,
            0,
            1,
            3
        )

    def reset_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def reset(self):
        self.context_label.setText("Body Part: -")
        self.reset_grid()