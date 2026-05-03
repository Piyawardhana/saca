import os

from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect
)

from .common import BasePage, ActionCardButton, PRIMARY_DARK, CREAM


class LanguagePage(BasePage):
    back_requested = Signal()
    home_requested = Signal()
    language_selected = Signal(str)

    def __init__(self):
        super().__init__()

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
        home_icon_path = os.path.join(base_dir, "assets", "icons", "home.png")

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

        self.home_button = QPushButton()
        self.home_button.setCursor(Qt.PointingHandCursor)
        self.home_button.setFixedSize(56, 56)
        self.home_button.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                border: none;
                border-radius: 14px;
            }}
            QPushButton:hover {{ background: #4a252b; }}
            QPushButton:pressed {{ background: #1f0e11; }}
        """)

        if os.path.exists(home_icon_path):
            self.home_button.setIcon(QIcon(home_icon_path))
            self.home_button.setIconSize(QSize(28, 28))

        self.home_button.clicked.connect(self.home_requested.emit)

        # optional shadow for premium feel
        home_shadow = QGraphicsDropShadowEffect(self.home_button)
        home_shadow.setBlurRadius(18)
        home_shadow.setOffset(0, 4)
        home_shadow.setColor(QColor(0, 0, 0, 90))
        self.home_button.setGraphicsEffect(home_shadow)

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        top_row.addWidget(self.home_button, 0, Qt.AlignRight)

        shell_layout.addLayout(top_row)

        center = QVBoxLayout()
        center.setSpacing(40)
        center.addStretch(1)

        title = QLabel("Choose Language")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 64px;
                font-weight: 900;
                color: {PRIMARY_DARK};
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(title)
        title_shadow.setBlurRadius(45)
        title_shadow.setOffset(0, 6)
        title_shadow.setColor(QColor(0, 0, 0, 120))
        title.setGraphicsEffect(title_shadow)

        english = ActionCardButton("English", "", "English", min_width=380, min_height=110)
        pitjantjatjara = ActionCardButton("Pitjantjatjara", "", "Pitjantjatjara", min_width=380, min_height=110)

        for btn in (english, pitjantjatjara):
            btn.layout().itemAt(1).widget().setStyleSheet(f"""
                font-family: Marcellus;
                font-size: 30px;
                font-weight: 900;
                color: {CREAM};
            """)

        english.clicked_value.connect(self.language_selected.emit)
        pitjantjatjara.clicked_value.connect(self.language_selected.emit)

        row1 = QHBoxLayout()
        row1.addStretch(1)
        row1.addWidget(english)
        row1.addStretch(1)

        row2 = QHBoxLayout()
        row2.addStretch(1)
        row2.addWidget(pitjantjatjara)
        row2.addStretch(1)

        center.addWidget(title)
        center.addLayout(row1)
        center.addLayout(row2)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)