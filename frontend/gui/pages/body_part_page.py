import os

from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel,
    QGridLayout, QFrame, QGraphicsDropShadowEffect
)

from .common import BasePage, ImageCardButton, card_shadow, PRIMARY_DARK, CREAM


class BodyPartPage(BasePage):
    back_requested = Signal()
    body_part_selected = Signal(str)

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
        center.setSpacing(28)
        center.addStretch(1)

        title = QLabel("Select Body Part")
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
        card.setFixedWidth(980)
        card.setFixedHeight(620)
        card_shadow(card, blur=28, y=9)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(34, 30, 34, 30)
        card_layout.setSpacing(0)

        grid = QGridLayout()
        grid.setContentsMargins(0, 0, 0, 0)
        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)

        items = [
            ("Head", "head", "bodyparts/head.png"),
            ("Chest", "chest", "bodyparts/chest.png"),
            ("Abdomen", "abdomen", "bodyparts/abdomen.png"),
            ("Back", "back", "bodyparts/back.png"),
            ("Arm", "arm", "bodyparts/arm.png"),
            ("Leg", "leg", "bodyparts/leg.png"),
        ]

        for index, (title_text, key, rel_path) in enumerate(items):
            row = index // 3
            col = index % 3

            card_btn = ImageCardButton(
                title=title_text,
                subtitle="",
                image_path=os.path.join(self.assets_dir, rel_path),
                value=key
            )
            card_btn.setFixedSize(280, 250)
            card_btn.clicked_value.connect(self.body_part_selected.emit)

            grid.addWidget(card_btn, row, col, Qt.AlignCenter)

        for i in range(3):
            grid.setColumnStretch(i, 1)

        for i in range(2):
            grid.setRowStretch(i, 1)

        card_layout.addLayout(grid)

        card_row = QHBoxLayout()
        card_row.addStretch(1)
        card_row.addWidget(card)
        card_row.addStretch(1)

        center.addWidget(title)
        center.addLayout(card_row)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)