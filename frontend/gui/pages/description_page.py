import os

from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QTextEdit, QPushButton, QGraphicsDropShadowEffect
)

from .common import BasePage, card_shadow, PRIMARY_DARK, CREAM


class DescriptionPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()
    next_requested = Signal(str)

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

        shadow = QGraphicsDropShadowEffect(self.home_button)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.home_button.setGraphicsEffect(shadow)

        self.home_button.clicked.connect(self.home_requested.emit)

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        top_row.addWidget(self.home_button, 0, Qt.AlignRight)

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
        card.setFixedWidth(560)
        card_shadow(card, blur=26, y=8)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(34, 30, 34, 30)
        card_layout.setSpacing(20)

        card_title = QLabel("Enter symptoms")
        card_title.setAlignment(Qt.AlignCenter)
        card_title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 28px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("e.g. headache, fever, stomach pain...")
        self.text_edit.setFixedHeight(180)
        self.text_edit.setStyleSheet(f"""
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

        card_layout.addWidget(card_title)
        card_layout.addWidget(self.text_edit)

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

    def submit(self):
        self.next_requested.emit(self.text_edit.toPlainText())

    def reset(self):
        self.text_edit.clear()