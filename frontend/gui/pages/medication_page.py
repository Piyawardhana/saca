import os

from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QPushButton, QGraphicsDropShadowEffect
)

from .common import BasePage, ActionCardButton, card_shadow, PRIMARY_DARK, CREAM


class MedicationPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()
    medication_selected = Signal(str)

    def __init__(self):
        super().__init__()

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
        icon_dir = os.path.join(base_dir, "assets", "icons")

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

        self.home_button = QPushButton()
        self.home_button.setCursor(Qt.PointingHandCursor)
        self.home_button.setFixedSize(56, 56)
        self.home_button.setStyleSheet(f"""
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

        home_icon_path = os.path.join(icon_dir, "home.png")
        if os.path.exists(home_icon_path):
            self.home_button.setIcon(QIcon(home_icon_path))
            self.home_button.setIconSize(QSize(30, 30))

        card_shadow(self.home_button, blur=18, y=4)
        self.home_button.clicked.connect(self.home_requested.emit)

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        top_row.addWidget(self.home_button, 0, Qt.AlignRight)

        shell_layout.addLayout(top_row)

        center = QVBoxLayout()
        center.setSpacing(36)
        center.addStretch(1)

        title = QLabel("Do you take any medications?")
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

        card = QFrame()
        card.setObjectName("ContentCard")
        card.setFixedWidth(540)
        card_shadow(card, blur=28, y=9)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 34, 40, 34)
        card_layout.setSpacing(24)

        yes_btn = ActionCardButton("Yes", "", "Yes", min_width=420, min_height=95)
        no_btn = ActionCardButton("No", "", "No", min_width=420, min_height=95)

        yes_btn.clicked_value.connect(self.medication_selected.emit)
        no_btn.clicked_value.connect(self.medication_selected.emit)

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

        center.addWidget(title)
        center.addLayout(card_row)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)

    def reset(self):
        pass