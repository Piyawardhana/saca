from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton,
    QGridLayout
)

from .common import BasePage, HeaderBar, card_shadow


class PainScoreButton(QPushButton):
    def __init__(self, score: int, label: str):
        super().__init__(f"{score}\n{label}")
        self.score = score
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(130, 120)
        self.setStyleSheet("""
            QPushButton {
                background: white;
                color: #10233c;
                border: 1px solid #d7e2ef;
                border-radius: 22px;
                font-size: 22px;
                font-weight: 800;
                padding: 8px;
            }
            QPushButton:hover {
                border: 2px solid #3b82f6;
                background: #f7fbff;
            }
        """)


class PainPage(BasePage):
    back_requested = Signal()
    pain_selected = Signal(int)

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(36, 28, 36, 28)

        page_card = QFrame()
        page_card.setObjectName("PageCard")
        card_shadow(page_card)

        layout = QVBoxLayout(page_card)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(22)

        self.header = HeaderBar(
            title="Pain Score",
            subtitle="Select the pain level that best matches the current condition."
        )
        self.header.back_button.clicked.connect(self.back_requested.emit)

        self.context_label = QLabel("Selection: -")
        self.context_label.setStyleSheet("""
            QLabel {
                background: #f6f9fd;
                color: #27476b;
                border: 1px solid #d5e1ef;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 700;
            }
        """)

        grid = QGridLayout()
        grid.setSpacing(16)

        labels = {
            1: "Very Low", 2: "Low", 3: "Mild", 4: "Noticeable", 5: "Moderate",
            6: "Strong", 7: "High", 8: "Very High", 9: "Severe", 10: "Extreme"
        }

        for i in range(1, 11):
            btn = PainScoreButton(i, labels[i])
            btn.clicked.connect(lambda checked=False, score=i: self.pain_selected.emit(score))
            grid.addWidget(btn, (i - 1) // 5, (i - 1) % 5)

        layout.addWidget(self.header)
        layout.addWidget(self.context_label)
        layout.addLayout(grid, 1)

        root.addWidget(page_card)

    def set_context(self, body_part: str, disease: str):
        self.context_label.setText(
            f"Selection: {body_part.title()}  •  {disease}"
        )

    def reset(self):
        self.context_label.setText("Selection: -")