import os

from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QColor, QPixmap, QIcon
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QGraphicsDropShadowEffect
)

from .common import BasePage, PRIMARY_DARK, CREAM, card_shadow


class IconButton(QPushButton):
    def __init__(self, icon_path: str):
        super().__init__()

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(56, 56)

        self.setStyleSheet(f"""
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

        if os.path.exists(icon_path):
            self.setIcon(QIcon(icon_path))
            self.setIconSize(QSize(30, 30))

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(0, 0, 0, 100))
        self.setGraphicsEffect(shadow)


class MethodButton(QPushButton):
    clicked_value = Signal(str)

    def __init__(self, text: str, value: str, icon_path: str):
        super().__init__()
        self.value = value

        self.setCursor(Qt.PointingHandCursor)
        self.setFixedSize(460, 110)

        self.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                border: none;
                border-radius: 18px;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
            QPushButton:pressed {{
                background: #1f0e11;
            }}
        """)

        card_shadow(self, blur=24, y=8)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(28, 0, 28, 0)
        main_layout.setSpacing(0)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 28px;
                font-weight: 900;
                color: {CREAM};
                background: transparent;
                border: none;
            }}
        """)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(54, 54)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("background: transparent; border: none;")

        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            self.icon_label.setPixmap(
                pixmap.scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )

        content_layout.addWidget(self.text_label)
        content_layout.addWidget(self.icon_label)

        main_layout.addStretch(1)
        main_layout.addLayout(content_layout)
        main_layout.addStretch(1)

        self.clicked.connect(lambda: self.clicked_value.emit(self.value))


class InputMethodPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()
    method_selected = Signal(str)

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

        self.home_button = IconButton(os.path.join(icon_dir, "home.png"))
        self.home_button.clicked.connect(self.home_requested.emit)

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        top_row.addWidget(self.home_button, 0, Qt.AlignRight)

        shell_layout.addLayout(top_row)

        center = QVBoxLayout()
        center.setSpacing(38)
        center.addStretch(1)

        title = QLabel("How do you want to tell us?")
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

        text_btn = MethodButton("Text", "text", os.path.join(icon_dir, "text.png"))
        voice_btn = MethodButton("Speak", "voice", os.path.join(icon_dir, "voice.png"))
        image_btn = MethodButton("Select Symptom", "image", os.path.join(icon_dir, "image.png"))

        text_btn.clicked_value.connect(self.method_selected.emit)
        voice_btn.clicked_value.connect(self.method_selected.emit)
        image_btn.clicked_value.connect(self.method_selected.emit)

        center.addWidget(title)

        for btn in (text_btn, voice_btn, image_btn):
            row = QHBoxLayout()
            row.addStretch(1)
            row.addWidget(btn)
            row.addStretch(1)
            center.addLayout(row)

        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)