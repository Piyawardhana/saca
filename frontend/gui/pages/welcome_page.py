from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QGraphicsDropShadowEffect
)

from .common import BasePage, PRIMARY_DARK, CREAM


class WelcomePage(BasePage):
    next_requested = Signal()

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        shell = self.build_shell()
        layout = QVBoxLayout(shell)
        layout.setContentsMargins(40, 40, 40, 40)

        layout.addStretch(1)

        title = QLabel("Adaptive Clinical Assistant\n(SACA)")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                color: {PRIMARY_DARK};
                font-family: Marcellus, Georgia, serif;
                font-size: 72px;
                font-weight: 900;
                background: transparent;
                border: none;
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(title)
        title_shadow.setBlurRadius(40)  # softness
        title_shadow.setOffset(0, 6)  # vertical shadow
        title_shadow.setColor(QColor(0, 0, 0, 120))  # subtle dark shadow
        title.setGraphicsEffect(title_shadow)

        layout.addWidget(title)
        layout.addSpacing(36)

        button_row = QHBoxLayout()
        button_row.addStretch(1)

        get_started_btn = QPushButton("Get Started")
        get_started_btn.setCursor(Qt.PointingHandCursor)
        get_started_btn.setFixedSize(240, 68)
        get_started_btn.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 16px;
                font-family: Marcellus, Georgia, serif;
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

        shadow = QGraphicsDropShadowEffect(get_started_btn)
        shadow.setBlurRadius(22)
        shadow.setOffset(0, 7)
        shadow.setColor(QColor(0, 0, 0, 90))
        get_started_btn.setGraphicsEffect(shadow)

        get_started_btn.clicked.connect(self.next_requested.emit)

        button_row.addWidget(get_started_btn)
        button_row.addStretch(1)

        layout.addLayout(button_row)
        layout.addStretch(1)

        root.addWidget(shell)