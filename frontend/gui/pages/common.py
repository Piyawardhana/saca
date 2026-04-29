import os

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout,
    QSizePolicy, QGraphicsDropShadowEffect
)


PRIMARY_DARK = "#30161a"
CREAM = "#f0ebdb"
TEXT_DARK = PRIMARY_DARK


class BackgroundWidget(QWidget):
    def __init__(self, image_path: str):
        super().__init__()
        self.pixmap = QPixmap(image_path)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        if not self.pixmap.isNull():
            scaled = self.pixmap.scaled(
                self.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            painter.fillRect(self.rect(), QColor(CREAM))


def card_shadow(widget, blur=40, x=0, y=12):
    effect = QGraphicsDropShadowEffect(widget)
    effect.setBlurRadius(blur)
    effect.setOffset(x, y)
    effect.setColor(QColor(0, 0, 0, 90))
    widget.setGraphicsEffect(effect)


class BasePage(QWidget):
    def __init__(self):
        super().__init__()

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )
        self.bg_path = os.path.join(base_dir, "assets", "welcome_bg.png")

        self.setStyleSheet(f"""
            QWidget {{
                font-family: Marcellus, Georgia, serif;
                color: {TEXT_DARK};
                background: transparent;
            }}

            QLabel#PageTitle {{
                font-size: 46px;
                font-weight: 900;
                color: {TEXT_DARK};
                background: transparent;
            }}

            QLabel#CardTitle {{
                font-size: 24px;
                font-weight: 900;
                color: {TEXT_DARK};
                background: transparent;
            }}

            QLabel#SmallText {{
                font-size: 18px;
                color: {TEXT_DARK};
                background: transparent;
            }}

            QFrame#ContentCard {{
                background: rgba(240, 235, 219, 235);
                border: none;
                border-radius: 24px;
            }}

            QPushButton#PrimaryButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 16px;
                padding: 16px 24px;
                font-size: 21px;
                font-weight: 900;
                min-width: 250px;
                min-height: 34px;
            }}

            QPushButton#PrimaryButton:hover {{
                background: #4a252b;
                border: none;
            }}

            QPushButton#PrimaryButton:pressed {{
                background: #1f0e11;
                border: none;
            }}

            QPushButton#SecondaryButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 14px;
                padding: 12px 18px;
                font-size: 18px;
                font-weight: 900;
            }}

            QPushButton#SecondaryButton:hover {{
                background: #4a252b;
                border: none;
            }}

            QPushButton#SecondaryButton:pressed {{
                background: #1f0e11;
                border: none;
            }}

            QTextEdit, QLineEdit {{
                background: rgba(240, 235, 219, 238);
                border: none;
                border-radius: 18px;
                padding: 18px;
                font-size: 19px;
                color: {TEXT_DARK};
                selection-background-color: #ddb231;
            }}

            QScrollArea {{
                background: transparent;
                border: none;
            }}

            QScrollBar:vertical {{
                background: transparent;
                width: 10px;
            }}

            QScrollBar::handle:vertical {{
                background: rgba(48, 22, 26, 180);
                border-radius: 5px;
            }}

            QScrollBar::handle:vertical:hover {{
                background: {PRIMARY_DARK};
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
                background: none;
                border: none;
            }}
        """)

    def build_shell(self):
        return BackgroundWidget(self.bg_path)

    def build_back_button(self):
        btn = QPushButton("Back")
        btn.setObjectName("SecondaryButton")
        btn.setFixedSize(116, 54)
        card_shadow(btn, blur=20, y=5)
        return btn


class ActionCardButton(QPushButton):
    clicked_value = Signal(str)

    def __init__(
        self,
        title: str,
        subtitle: str,
        value: str,
        min_height: int = 82,
        min_width: int = 330
    ):
        super().__init__()
        self.value = value

        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumHeight(min_height)
        self.setMinimumWidth(min_width)
        self.setMaximumWidth(min_width)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                border: none;
                border-radius: 18px;
            }}

            QPushButton:hover {{
                background: #4a252b;
                border: none;
            }}

            QPushButton:pressed {{
                background: #1f0e11;
                border: none;
            }}
        """)

        card_shadow(self, blur=22, y=7)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus, Georgia, serif;
                font-size: 22px;
                font-weight: 900;
                color: {CREAM};
                background: transparent;
                border: none;
            }}
        """)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus, Georgia, serif;
                font-size: 15px;
                color: {CREAM};
                background: transparent;
                border: none;
            }}
        """)

        layout.addStretch(1)
        layout.addWidget(title_label)

        if subtitle:
            layout.addWidget(subtitle_label)

        layout.addStretch(1)

        self.clicked.connect(lambda: self.clicked_value.emit(self.value))


class ImageCardButton(QPushButton):
    clicked_value = Signal(str)

    def __init__(
        self,
        title: str,
        image_path: str,
        value: str,
        subtitle: str = ""
    ):
        super().__init__()
        self.value = value

        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(220, 265)
        self.setMaximumWidth(340)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setStyleSheet(f"""
            QPushButton {{
                background: rgba(240, 235, 219, 240);
                border: none;
                border-radius: 24px;
            }}

            QPushButton:hover {{
                background: rgba(240, 235, 219, 255);
                border: none;
            }}

            QPushButton:pressed {{
                background: rgba(221, 178, 49, 210);
                border: none;
            }}
        """)

        card_shadow(self, blur=22, y=7)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(8)

        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setFixedHeight(160)
        image_label.setStyleSheet("""
            QLabel {
                background: transparent;
                border: none;
            }
        """)

        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            image_label.setPixmap(
                pixmap.scaled(
                    150,
                    150,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            image_label.setText("")

        title_label = QLabel(title)
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus, Georgia, serif;
                font-size: 22px;
                font-weight: 900;
                color: {TEXT_DARK};
                background: transparent;
                border: none;
            }}
        """)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setWordWrap(True)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus, Georgia, serif;
                font-size: 15px;
                color: {TEXT_DARK};
                background: transparent;
                border: none;
            }}
        """)

        layout.addWidget(image_label)
        layout.addWidget(title_label)

        if subtitle:
            layout.addWidget(subtitle_label)

        layout.addStretch(1)

        self.clicked.connect(lambda: self.clicked_value.emit(self.value))