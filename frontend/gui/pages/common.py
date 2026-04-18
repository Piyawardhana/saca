import os

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame,
    QGraphicsDropShadowEffect, QSizePolicy
)


def asset_path(*parts: str) -> str:
    return os.path.join(*parts)


def card_shadow(widget, blur=28, x=0, y=8):
    shadow = QGraphicsDropShadowEffect(widget)
    shadow.setBlurRadius(blur)
    shadow.setOffset(x, y)
    shadow.setColor(Qt.black)
    widget.setGraphicsEffect(shadow)


class BasePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI;
            }
            QFrame#PageCard {
                background: white;
                border: 1px solid #d7e2ef;
                border-radius: 28px;
            }
            QLabel#PageTitle {
                color: #10233c;
                font-size: 30px;
                font-weight: 800;
            }
            QLabel#PageSubtitle {
                color: #5d7088;
                font-size: 14px;
            }
            QLabel#SectionTitle {
                color: #17304f;
                font-size: 16px;
                font-weight: 700;
            }
            QPushButton#PrimaryButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2663eb, stop:1 #3b82f6);
                color: white;
                border: none;
                border-radius: 14px;
                padding: 14px 18px;
                font-size: 14px;
                font-weight: 700;
                min-height: 22px;
            }
            QPushButton#PrimaryButton:hover {
                background: #1f56d8;
            }
            QPushButton#SecondaryButton {
                background: white;
                color: #17304f;
                border: 1px solid #cbd8e7;
                border-radius: 14px;
                padding: 14px 18px;
                font-size: 14px;
                font-weight: 700;
                min-height: 22px;
            }
            QPushButton#SecondaryButton:hover {
                background: #f5f8fc;
            }
        """)


class ImageCardButton(QPushButton):
    clicked_value = Signal(str)

    def __init__(self, title: str, image_path: str, value: str, subtitle: str = ""):
        super().__init__()
        self.value = value
        self.setCursor(Qt.PointingHandCursor)
        self.setCheckable(False)
        self.setMinimumSize(250, 280)
        self.setMaximumWidth(420)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setStyleSheet("""
            QPushButton {
                background: white;
                border: 2px solid #d8e3ef;
                border-radius: 20px;
                text-align: left;
            }
            QPushButton:hover {
                border: 2px solid #3b82f6;
                background: #f7fbff;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(180)
        image_label.setStyleSheet("""
            QLabel {
                background: #f8fbff;
                border: 2px solid #e4edf7;
                border-radius: 16px;
            }
        """)

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(
                pixmap.scaled(
                    170, 170,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            image_label.setText("Image not found")

        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setStyleSheet("font-size: 18px; font-weight: 800; color: #10233c; background: transparent; border: none;")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet("font-size: 12px; color: #607489; background: transparent; border: none;")

        layout.addWidget(image_label)
        layout.addWidget(title_label)
        if subtitle:
            layout.addWidget(subtitle_label)
        layout.addStretch(1)

        self.clicked.connect(lambda: self.clicked_value.emit(self.value))


class HeaderBar(QFrame):
    def __init__(self, title: str, subtitle: str, show_back: bool = True):
        super().__init__()
        self.setObjectName("HeaderBar")
        self.setStyleSheet("""
            QFrame#HeaderBar {
                background: transparent;
                border: none;
            }
        """)

        from PySide6.QtWidgets import QHBoxLayout

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.back_button = QPushButton("← Back")
        self.back_button.setObjectName("SecondaryButton")
        self.back_button.setVisible(show_back)
        self.back_button.setFixedWidth(120)

        text_wrap = QVBoxLayout()
        title_label = QLabel(title)
        title_label.setObjectName("PageTitle")

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("PageSubtitle")
        subtitle_label.setWordWrap(True)

        text_wrap.addWidget(title_label)
        text_wrap.addWidget(subtitle_label)

        layout.addWidget(self.back_button, 0, Qt.AlignTop)
        layout.addSpacing(12)
        layout.addLayout(text_wrap, 1)