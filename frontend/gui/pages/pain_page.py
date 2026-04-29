from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect
)

from .common import BasePage, card_shadow, PRIMARY_DARK, CREAM


class PainPage(BasePage):
    back_requested = Signal()
    pain_selected = Signal(int)

    def __init__(self):
        super().__init__()
        self.selected_score = None
        self.buttons = []

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
        center.setSpacing(36)
        center.addStretch(1)

        title = QLabel("How bad is the pain?")
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
        card.setFixedWidth(860)
        card_shadow(card, blur=28, y=9)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 34, 40, 34)
        card_layout.setSpacing(26)

        score_row = QHBoxLayout()
        score_row.setSpacing(14)
        score_row.addStretch(1)

        for i in range(1, 11):
            btn = QPushButton(str(i))
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(60, 60)
            btn.setStyleSheet(self.default_score_style())
            btn.clicked.connect(lambda checked=False, score=i: self.select_score(score))
            self.buttons.append(btn)
            score_row.addWidget(btn)

        score_row.addStretch(1)

        emoji_row = QHBoxLayout()
        emoji_row.addStretch(1)

        low = QLabel("😕")
        mid = QLabel("😣")
        high = QLabel("😫")

        for lbl in (low, mid, high):
            lbl.setStyleSheet("font-size: 54px; background: transparent;")
            lbl.setAlignment(Qt.AlignCenter)

        emoji_row.addWidget(low)
        emoji_row.addStretch(1)
        emoji_row.addWidget(mid)
        emoji_row.addStretch(1)
        emoji_row.addWidget(high)
        emoji_row.addStretch(1)

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

        card_layout.addLayout(score_row)
        card_layout.addLayout(emoji_row)
        card_layout.addLayout(next_row)

        card_row = QHBoxLayout()
        card_row.addStretch(1)
        card_row.addWidget(card)
        card_row.addStretch(1)

        center.addWidget(title)
        center.addLayout(card_row)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)

    def default_score_style(self):
        return f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 14px;
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
        """

    def selected_score_style(self):
        return """
            QPushButton {
                background: #ddb231;
                color: #30161a;
                border: none;
                border-radius: 14px;
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
            }
        """

    def select_score(self, score: int):
        self.selected_score = score

        for index, btn in enumerate(self.buttons, start=1):
            if index == score:
                btn.setStyleSheet(self.selected_score_style())
            else:
                btn.setStyleSheet(self.default_score_style())

    def submit(self):
        if self.selected_score is not None:
            self.pain_selected.emit(self.selected_score)

    def reset(self):
        self.selected_score = None
        for btn in self.buttons:
            btn.setStyleSheet(self.default_score_style())