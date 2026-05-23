import os

from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QColor, QIcon
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGraphicsDropShadowEffect,
    QSizePolicy,
    QScrollArea,
    QWidget,
)

from .common import BasePage, card_shadow, PRIMARY_DARK, CREAM


class ReviewPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()
    confirm_requested = Signal()

    edit_input_requested = Signal()
    edit_body_part_requested = Signal()
    edit_disease_requested = Signal()
    edit_duration_requested = Signal()
    edit_pain_requested = Signal()
    edit_food_allergy_requested = Signal()
    edit_medication_requested = Signal()

    def __init__(self):
        super().__init__()

        self.page_title = "Review your details"

        base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))
            )
        )

        icon_dir = os.path.join(base_dir, "assets", "icons")
        self.edit_icon_path = os.path.join(icon_dir, "edit.png")
        self.home_icon_path = os.path.join(icon_dir, "home.png")

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        shell = self.build_shell()
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(30, 24, 30, 24)
        shell_layout.setSpacing(0)

        # ========================================================
        # Top row
        # ========================================================
        top_row = QHBoxLayout()
        top_row.setContentsMargins(0, 0, 0, 0)

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

        self.home_button = self.icon_button(self.home_icon_path)
        self.home_button.clicked.connect(self.home_requested.emit)

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)
        top_row.addWidget(self.home_button, 0, Qt.AlignRight)

        shell_layout.addLayout(top_row)

        # ========================================================
        # Center content
        # ========================================================
        center = QVBoxLayout()
        center.setSpacing(22)
        center.addStretch(1)

        title = QLabel(self.page_title)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 60px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(title)
        title_shadow.setBlurRadius(40)
        title_shadow.setOffset(0, 5)
        title_shadow.setColor(QColor(0, 0, 0, 110))
        title.setGraphicsEffect(title_shadow)

        subtitle = QLabel("Please double check your answers before continuing.")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 19px;
                font-weight: 700;
                color: {PRIMARY_DARK};
                background: transparent;
            }}
        """)

        title_block = QVBoxLayout()
        title_block.setSpacing(8)
        title_block.addWidget(title)
        title_block.addWidget(subtitle)

        # ========================================================
        # Review card
        # ========================================================
        self.card = QFrame()
        self.card.setObjectName("ContentCard")
        self.card.setFixedWidth(820)
        self.card.setMinimumHeight(440)
        self.card.setMaximumHeight(500)
        self.card.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        card_shadow(self.card, blur=28, y=9)

        self.card.setStyleSheet(f"""
            QFrame#ContentCard {{
                background-color: rgba(240, 235, 219, 0.96);
                border-radius: 28px;
            }}

            QFrame#ReviewRow {{
                background-color: rgba(255, 255, 255, 0.68);
                border-radius: 20px;
            }}

            QLabel#FieldTitle {{
                font-family: Marcellus;
                color: {PRIMARY_DARK};
                font-size: 18px;
                font-weight: 700;
                background: transparent;
            }}

            QLabel#FieldValue {{
                font-family: Marcellus;
                color: {PRIMARY_DARK};
                font-size: 17px;
                font-weight: 400;
                background: transparent;
            }}

            QPushButton#EditButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 14px;
                font-family: Marcellus;
                font-size: 20px;
                font-weight: 900;
            }}

            QPushButton#EditButton:hover {{
                background: #4a252b;
            }}

            QPushButton#EditButton:pressed {{
                background: #1f0e11;
            }}

            QScrollArea {{
                border: none;
                background: transparent;
            }}

            QScrollBar:vertical {{
                background: rgba(48, 22, 26, 0.08);
                width: 12px;
                border-radius: 6px;
                margin: 4px 4px 4px 0px;
            }}

            QScrollBar::handle:vertical {{
                background: rgba(48, 22, 26, 0.45);
                border-radius: 6px;
                min-height: 30px;
            }}

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)

        card_outer_layout = QVBoxLayout(self.card)
        card_outer_layout.setContentsMargins(22, 20, 18, 20)
        card_outer_layout.setSpacing(0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scroll_content = QWidget()
        self.card_layout = QVBoxLayout(self.scroll_content)
        self.card_layout.setContentsMargins(8, 6, 8, 6)
        self.card_layout.setSpacing(14)

        self.input_value = self.add_review_row(
            "Symptoms / Input",
            self.edit_input_requested.emit
        )

        self.body_part_value = self.add_review_row(
            "Body part",
            self.edit_body_part_requested.emit
        )

        self.disease_value = self.add_review_row(
            "Selected symptom or condition",
            self.edit_disease_requested.emit
        )

        self.duration_value = self.add_review_row(
            "Duration",
            self.edit_duration_requested.emit
        )

        self.pain_value = self.add_review_row(
            "Pain score",
            self.edit_pain_requested.emit
        )

        self.food_allergy_value = self.add_review_row(
            "Food allergies",
            self.edit_food_allergy_requested.emit
        )

        self.medication_value = self.add_review_row(
            "Medication",
            self.edit_medication_requested.emit
        )

        self.card_layout.addStretch(1)

        self.scroll_area.setWidget(self.scroll_content)
        card_outer_layout.addWidget(self.scroll_area)

        # ========================================================
        # Confirm button
        # ========================================================
        self.confirm_button = QPushButton("Confirm & Continue")
        self.confirm_button.setCursor(Qt.PointingHandCursor)
        self.confirm_button.setMinimumHeight(64)
        self.confirm_button.setMinimumWidth(450)
        self.confirm_button.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 20px;
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
                padding: 10px 34px;
            }}
            QPushButton:hover {{ background: #4a252b; }}
            QPushButton:pressed {{ background: #1f0e11; }}
        """)
        card_shadow(self.confirm_button, blur=18, y=4)
        self.confirm_button.clicked.connect(self.confirm_requested.emit)

        confirm_row = QHBoxLayout()
        confirm_row.addStretch(1)
        confirm_row.addWidget(self.confirm_button)
        confirm_row.addStretch(1)

        card_row = QHBoxLayout()
        card_row.addStretch(1)
        card_row.addWidget(self.card)
        card_row.addStretch(1)

        center.addLayout(title_block)
        center.addLayout(card_row)
        center.addLayout(confirm_row)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)

    # ============================================================
    # Shared icon button
    # ============================================================

    def icon_button(self, icon_path: str):
        button = QPushButton()
        button.setCursor(Qt.PointingHandCursor)
        button.setFixedSize(56, 56)
        button.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                border: none;
                border-radius: 14px;
            }}
            QPushButton:hover {{ background: #4a252b; }}
            QPushButton:pressed {{ background: #1f0e11; }}
        """)

        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(30, 30))
        else:
            button.setText("⌂")
            button.setStyleSheet(f"""
                QPushButton {{
                    background: {PRIMARY_DARK};
                    color: {CREAM};
                    border: none;
                    border-radius: 14px;
                    font-family: Marcellus;
                    font-size: 24px;
                    font-weight: 900;
                }}
                QPushButton:hover {{ background: #4a252b; }}
                QPushButton:pressed {{ background: #1f0e11; }}
            """)

        card_shadow(button, blur=18, y=4)
        return button

    # ============================================================
    # Row builder
    # ============================================================

    def add_review_row(self, label_text, edit_callback):
        row = QFrame()
        row.setObjectName("ReviewRow")
        row.setMinimumHeight(82)
        row.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(22, 12, 14, 12)
        row_layout.setSpacing(16)

        text_col = QVBoxLayout()
        text_col.setSpacing(6)
        text_col.setContentsMargins(0, 0, 0, 0)

        title = QLabel(label_text)
        title.setObjectName("FieldTitle")
        title.setWordWrap(True)
        title.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        value = QLabel("-")
        value.setObjectName("FieldValue")
        value.setWordWrap(True)
        value.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        value.setTextInteractionFlags(Qt.TextSelectableByMouse)

        text_col.addWidget(title)
        text_col.addWidget(value)

        row_layout.addLayout(text_col, stretch=1)

        edit_button = QPushButton()
        edit_button.setObjectName("EditButton")
        edit_button.setCursor(Qt.PointingHandCursor)
        edit_button.setFixedSize(46, 46)

        if os.path.exists(self.edit_icon_path):
            edit_button.setIcon(QIcon(self.edit_icon_path))
            edit_button.setIconSize(QSize(24, 24))
        else:
            edit_button.setText("✎")

        edit_button.clicked.connect(edit_callback)
        card_shadow(edit_button, blur=14, y=3)

        row_layout.addWidget(edit_button, 0, Qt.AlignVCenter)

        self.card_layout.addWidget(row)

        return value

    # ============================================================
    # Data setter
    # ============================================================

    def set_review_data(
        self,
        input_method=None,
        entered_text=None,
        voice_text=None,
        body_part=None,
        disease=None,
        duration=None,
        pain_score=None,
        food_allergies=None,
        medication=None,
    ):
        if input_method == "text":
            input_display = entered_text or "Not provided"
        elif input_method == "voice":
            input_display = voice_text or "Not recorded"
        elif input_method == "image":
            input_display = "Image selection"
        else:
            input_display = "Not selected"

        self.input_value.setText(str(input_display))
        self.body_part_value.setText(str(body_part) if body_part else "Not selected")
        self.disease_value.setText(str(disease) if disease else "Not selected")
        self.duration_value.setText(str(duration) if duration else "Not selected")

        if pain_score is None:
            self.pain_value.setText("Not selected")
        else:
            self.pain_value.setText(f"{pain_score} / 10")

        self.food_allergy_value.setText(
            str(food_allergies) if food_allergies else "Not specified"
        )

        self.medication_value.setText(
            str(medication) if medication else "Not answered"
        )

    # ============================================================
    # Reset
    # ============================================================

    def reset(self):
        self.input_value.setText("-")
        self.body_part_value.setText("-")
        self.disease_value.setText("-")
        self.duration_value.setText("-")
        self.pain_value.setText("-")
        self.food_allergy_value.setText("-")
        self.medication_value.setText("-")

    def reset_page(self):
        self.reset()