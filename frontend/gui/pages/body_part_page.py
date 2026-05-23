import os

from PySide6.QtCore import Signal, Qt, QPoint
from PySide6.QtGui import QColor, QPixmap, QPainter, QPen
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QGraphicsDropShadowEffect,
    QWidget,
    QFrame,
)

from .common import BasePage, card_shadow, PRIMARY_DARK, CREAM
from ..translations import text, normalise_language


class BodyDiagramWidget(QWidget):
    body_part_selected = Signal(str)

    def __init__(self, assets_dir: str, view: str):
        super().__init__()

        self.assets_dir = assets_dir
        self.view = view
        self.current_pixmap = QPixmap()
        self.buttons = {}

        if self.view == "front":
            self.setFixedSize(760, 560)

            self.image_x = 275
            self.image_y = 8
            self.image_w = 275
            self.image_h = 525

            self.create_label_button("head", "Head", 20, 35, 120, 38)
            self.create_label_button("chest", "Chest", 20, 125, 120, 38)
            self.create_label_button("left_hand", "Left Hand", 20, 205, 150, 38)
            self.create_label_button("abdomen", "Abdomen", 20, 285, 150, 38)
            self.create_label_button("left_leg", "Left Leg", 20, 430, 135, 38)

            self.create_label_button("right_hand", "Right Hand", 595, 205, 150, 38)
            self.create_label_button("right_leg", "Right Leg", 595, 430, 135, 38)

        else:
            self.setFixedSize(430, 560)

            self.image_x = 70
            self.image_y = 8
            self.image_w = 255
            self.image_h = 525

            # Only the Back selector is shown on the back image
            self.create_label_button("back", "Back", 315, 150, 100, 38)

        self.load_image()

    # ============================================================
    # Buttons
    # ============================================================

    def create_label_button(self, key: str, label: str, x: int, y: int, w: int, h: int):
        btn = QPushButton(label, self)
        btn.setGeometry(x, y, w, h)
        btn.setCursor(Qt.PointingHandCursor)

        btn.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 11px;
                font-family: Marcellus;
                font-size: 16px;
                font-weight: 900;
                padding: 3px 8px;
                text-align: center;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
            QPushButton:pressed {{
                background: #1f0e11;
            }}
        """)

        card_shadow(btn, blur=8, y=2)

        btn.clicked.connect(
            lambda checked=False, value=key: self.emit_body_part(value)
        )

        self.buttons[key] = btn

    def emit_body_part(self, key: str):
        mapping = {
            "head": "head",
            "chest": "chest",
            "abdomen": "abdomen",
            "left_hand": "arm",
            "right_hand": "arm",
            "left_leg": "leg",
            "right_leg": "leg",
            "back": "back",
        }

        self.body_part_selected.emit(mapping.get(key, key))

    # ============================================================
    # Image
    # ============================================================

    def load_image(self):
        image_name = "front.png" if self.view == "front" else "back.png"
        image_path = os.path.join(self.assets_dir, "bodyparts", image_name)

        if os.path.exists(image_path):
            self.current_pixmap = QPixmap(image_path)
        else:
            self.current_pixmap = QPixmap()

        self.update()

    # ============================================================
    # Geometry helpers
    # ============================================================

    def button_right_middle(self, key: str):
        btn = self.buttons[key]
        return QPoint(
            btn.x() + btn.width(),
            btn.y() + btn.height() // 2
        )

    def button_left_middle(self, key: str):
        btn = self.buttons[key]
        return QPoint(
            btn.x(),
            btn.y() + btn.height() // 2
        )

    def body_point_from_ratio(self, real_x, real_y, real_w, real_h, x_ratio, y_ratio):
        return QPoint(
            int(real_x + real_w * x_ratio),
            int(real_y + real_h * y_ratio)
        )

    # ============================================================
    # Paint
    # ============================================================

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self.current_pixmap.isNull():
            scaled = self.current_pixmap.scaled(
                self.image_w,
                self.image_h,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            real_x = self.image_x + (self.image_w - scaled.width()) // 2
            real_y = self.image_y + (self.image_h - scaled.height()) // 2
            real_w = scaled.width()
            real_h = scaled.height()

            painter.drawPixmap(real_x, real_y, scaled)

        else:
            painter.setPen(QPen(QColor(PRIMARY_DARK), 2))
            painter.drawText(
                self.image_x,
                self.image_y + 220,
                f"Missing image: {self.view}.png"
            )
            return

        painter.setPen(QPen(QColor(PRIMARY_DARK), 3))
        painter.setBrush(QColor(PRIMARY_DARK))

        if self.view == "front":
            connectors = [
                (
                    self.button_right_middle("head"),
                    self.body_point_from_ratio(real_x, real_y, real_w, real_h, 0.50, 0.085),
                    "left"
                ),
                (
                    self.button_right_middle("chest"),
                    self.body_point_from_ratio(real_x, real_y, real_w, real_h, 0.50, 0.285),
                    "left"
                ),
                (
                    self.button_right_middle("left_hand"),
                    self.body_point_from_ratio(real_x, real_y, real_w, real_h, 0.17, 0.445),
                    "left"
                ),
                (
                    self.button_right_middle("abdomen"),
                    self.body_point_from_ratio(real_x, real_y, real_w, real_h, 0.50, 0.385),
                    "left"
                ),
                (
                    self.button_right_middle("left_leg"),
                    self.body_point_from_ratio(real_x, real_y, real_w, real_h, 0.39, 0.785),
                    "left"
                ),
                (
                    self.button_left_middle("right_hand"),
                    self.body_point_from_ratio(real_x, real_y, real_w, real_h, 0.83, 0.445),
                    "right"
                ),
                (
                    self.button_left_middle("right_leg"),
                    self.body_point_from_ratio(real_x, real_y, real_w, real_h, 0.61, 0.785),
                    "right"
                ),
            ]

        else:
            connectors = [
                (
                    self.button_left_middle("back"),
                    self.body_point_from_ratio(real_x, real_y, real_w, real_h, 0.50, 0.30),
                    "right"
                ),
            ]

        for label_point, body_dot, side in connectors:
            self.draw_connector(painter, label_point, body_dot, side)

    def draw_connector(self, painter: QPainter, label_point: QPoint, body_dot: QPoint, side: str):
        dot_radius = 5
        painter.drawEllipse(body_dot, dot_radius, dot_radius)

        if side == "left":
            mid_x = body_dot.x() - 42
        else:
            mid_x = body_dot.x() + 42

        elbow_1 = QPoint(mid_x, body_dot.y())
        elbow_2 = QPoint(mid_x, label_point.y())

        painter.drawLine(body_dot, elbow_1)
        painter.drawLine(elbow_1, elbow_2)
        painter.drawLine(elbow_2, label_point)


class BodyPartPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()
    body_part_selected = Signal(str)

    def __init__(self, assets_dir: str):
        super().__init__()

        self.assets_dir = assets_dir
        self.current_language = "English"

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        shell = self.build_shell()
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(24, 10, 24, 10)
        shell_layout.setSpacing(2)

        # ========================================================
        # Top row
        # ========================================================

        top_row = QHBoxLayout()

        self.back_button = self.build_back_button()
        self.back_button.setText(text("back", self.current_language))
        self.back_button.setFixedSize(92, 42)
        self.back_button.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 13px;
                font-family: Marcellus;
                font-size: 18px;
                font-weight: 900;
                padding: 5px 14px;
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

        # ========================================================
        # Title
        # ========================================================

        self.title_label = QLabel(text("select_body_part", self.current_language))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(74)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 58px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                padding: 0px;
                margin: 0px;
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(self.title_label)
        title_shadow.setBlurRadius(28)
        title_shadow.setOffset(0, 4)
        title_shadow.setColor(QColor(0, 0, 0, 85))
        self.title_label.setGraphicsEffect(title_shadow)

        shell_layout.addWidget(self.title_label, 0, Qt.AlignTop)

        # Gap between title and card
        shell_layout.addSpacing(40)

        # ========================================================
        # Responsive middle card
        # ========================================================

        self.content_card = QFrame()
        self.content_card.setObjectName("ContentCard")

        card_shadow(self.content_card, blur=24, y=6)

        self.content_card.setStyleSheet("""
            QFrame#ContentCard {
                background: rgba(240, 235, 219, 0.88);
                border-radius: 24px;
                border: 1px solid rgba(48, 22, 26, 0.10);
            }
        """)

        card_layout = QVBoxLayout(self.content_card)
        card_layout.setContentsMargins(18, 6, 18, 8)
        card_layout.setSpacing(0)

        # ========================================================
        # Headings
        # ========================================================

        headings_row = QHBoxLayout()
        headings_row.setContentsMargins(0, 0, 0, 0)
        headings_row.setSpacing(0)

        self.front_label = QLabel("Front")
        self.front_label.setAlignment(Qt.AlignCenter)
        self.front_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 22px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
            }}
        """)

        self.back_label = QLabel("Back")
        self.back_label.setAlignment(Qt.AlignCenter)
        self.back_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 22px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
            }}
        """)

        headings_row.addWidget(self.front_label, 7)
        headings_row.addWidget(self.back_label, 4)

        card_layout.addLayout(headings_row)

        # ========================================================
        # Diagrams
        # ========================================================

        diagram_row = QHBoxLayout()
        diagram_row.setContentsMargins(0, 0, 0, 0)
        diagram_row.setSpacing(8)

        self.front_diagram = BodyDiagramWidget(self.assets_dir, "front")
        self.front_diagram.body_part_selected.connect(self.body_part_selected.emit)

        self.back_diagram = BodyDiagramWidget(self.assets_dir, "back")
        self.back_diagram.body_part_selected.connect(self.body_part_selected.emit)

        diagram_row.addWidget(self.front_diagram, 7, Qt.AlignTop)
        diagram_row.addWidget(self.back_diagram, 4, Qt.AlignTop)

        card_layout.addLayout(diagram_row)

        card_row = QHBoxLayout()
        card_row.setContentsMargins(0, 0, 0, 0)
        card_row.addStretch(1)
        card_row.addWidget(self.content_card, 0, Qt.AlignTop)
        card_row.addStretch(1)

        shell_layout.addLayout(card_row, 0)
        shell_layout.addStretch(1)

        root.addWidget(shell)

        self.update_responsive_sizes()

    # ============================================================
    # Responsive card sizing
    # ============================================================

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_responsive_sizes()

    def update_responsive_sizes(self):
        window_w = self.width()
        window_h = self.height()

        # Keep the big monitor layout, but shrink just enough on laptop.
        card_w = min(1280, int(window_w * 0.86))
        card_h = min(640, int(window_h * 0.68))

        # Do not let the card become tiny.
        card_w = max(1120, card_w)
        card_h = max(520, card_h)

        # Safety for smaller displays.
        available_w = max(900, window_w - 80)
        available_h = max(500, window_h - 160)

        card_w = min(card_w, available_w)
        card_h = min(card_h, available_h)

        self.content_card.setFixedSize(card_w, card_h)

        # Larger title
        title_size = max(46, min(62, int(window_w * 0.034)))

        # More vertical room for larger title
        self.title_label.setFixedHeight(
            max(64, min(82, int(window_h * 0.085)))
        )

        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: {title_size}px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                padding: 0px;
                margin: 0px;
            }}
        """)

    def apply_language(self, language: str | None):
        self.current_language = normalise_language(language)
        self.back_button.setText(text("back", self.current_language))
        self.title_label.setText(text("select_body_part", self.current_language))

    def reset(self):
        pass