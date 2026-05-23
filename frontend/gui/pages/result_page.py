from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QGraphicsDropShadowEffect,
    QScrollArea,
    QWidget,
)

from .common import BasePage, card_shadow, PRIMARY_DARK, CREAM
from ..translations import (
    text,
    disease_label,
    normalise_language,
)


class ResultPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()

    def __init__(self):
        super().__init__()

        self.current_language = "English"

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        shell = self.build_shell()
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(30, 25, 30, 25)
        shell_layout.setSpacing(8)

        top_row = QHBoxLayout()

        self.back_button = self.build_back_button()
        self.back_button.setText(text("back", self.current_language))
        self.back_button.setStyleSheet(f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 14px;
                font-family: Marcellus;
                font-size: 18px;
                font-weight: 900;
                padding: 8px 20px;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
        """)
        self.back_button.clicked.connect(self.back_requested.emit)

        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)

        shell_layout.addLayout(top_row)

        self.title_label = QLabel(text("results", self.current_language))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFixedHeight(75)
        self.title_label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 54px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(self.title_label)
        title_shadow.setBlurRadius(35)
        title_shadow.setOffset(0, 5)
        title_shadow.setColor(QColor(0, 0, 0, 100))
        self.title_label.setGraphicsEffect(title_shadow)

        shell_layout.addWidget(self.title_label)

        main_row = QHBoxLayout()
        main_row.addStretch(1)

        self.main_card = QFrame()
        self.main_card.setObjectName("ContentCard")
        self.main_card.setFixedWidth(960)
        self.main_card.setMaximumHeight(600)
        card_shadow(self.main_card, blur=30, y=10)

        main_card_layout = QVBoxLayout(self.main_card)
        main_card_layout.setContentsMargins(38, 28, 38, 28)
        main_card_layout.setSpacing(16)

        severity_card = QFrame()
        severity_card.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 220);
                border-radius: 20px;
                border: none;
            }
        """)
        card_shadow(severity_card, blur=16, y=4)

        severity_layout = QHBoxLayout(severity_card)
        severity_layout.setContentsMargins(28, 18, 28, 18)
        severity_layout.setSpacing(14)

        self.severity_title = QLabel(text("severity_level", self.current_language))
        self.severity_title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 25px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
            }}
        """)

        self.severity_value = QLabel(text("not_available", self.current_language))
        self.severity_value.setAlignment(Qt.AlignCenter)
        self.severity_value.setMinimumWidth(190)
        self.severity_value.setStyleSheet("""
            QLabel {
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
                color: white;
                background: #999999;
                border-radius: 16px;
                padding: 10px 28px;
            }
        """)

        self.severity_glow = QGraphicsDropShadowEffect(self.severity_value)
        self.severity_glow.setOffset(0, 0)
        self.severity_glow.setBlurRadius(20)
        self.severity_glow.setColor(QColor("#777777"))
        self.severity_value.setGraphicsEffect(self.severity_glow)

        self.glow_animation = QPropertyAnimation(self.severity_glow, b"blurRadius")
        self.glow_animation.setDuration(1000)
        self.glow_animation.setStartValue(14)
        self.glow_animation.setEndValue(42)
        self.glow_animation.setLoopCount(-1)
        self.glow_animation.setEasingCurve(QEasingCurve.InOutSine)
        self.glow_animation.start()

        severity_layout.addWidget(self.severity_title)
        severity_layout.addStretch(1)
        severity_layout.addWidget(self.severity_value)

        main_card_layout.addWidget(severity_card)

        content_row = QHBoxLayout()
        content_row.setSpacing(16)

        self.conditions_card = self.make_section_card()
        self.conditions_layout = QVBoxLayout(self.conditions_card)
        self.conditions_layout.setContentsMargins(24, 20, 24, 20)
        self.conditions_layout.setSpacing(10)

        self.conditions_title = self.make_section_title(
            text("possible_conditions", self.current_language)
        )

        self.conditions_scroll = QScrollArea()
        self.conditions_scroll.setWidgetResizable(True)
        self.conditions_scroll.setFrameShape(QFrame.NoFrame)
        self.conditions_scroll.setMinimumHeight(190)
        self.conditions_scroll.setMaximumHeight(230)
        self.conditions_scroll.setStyleSheet(self.scroll_style())

        conditions_content = QWidget()
        conditions_content_layout = QVBoxLayout(conditions_content)
        conditions_content_layout.setContentsMargins(0, 0, 0, 0)

        self.conditions_text = self.make_text_label()
        conditions_content_layout.addWidget(self.conditions_text)
        conditions_content_layout.addStretch(1)

        self.conditions_scroll.setWidget(conditions_content)

        self.conditions_layout.addWidget(self.conditions_title)
        self.conditions_layout.addWidget(self.conditions_scroll)

        self.advice_card = self.make_section_card()
        self.advice_layout = QVBoxLayout(self.advice_card)
        self.advice_layout.setContentsMargins(24, 20, 24, 20)
        self.advice_layout.setSpacing(10)

        self.advice_title = self.make_section_title(
            text("recommendation", self.current_language)
        )

        self.advice_scroll = QScrollArea()
        self.advice_scroll.setWidgetResizable(True)
        self.advice_scroll.setFrameShape(QFrame.NoFrame)
        self.advice_scroll.setMinimumHeight(190)
        self.advice_scroll.setMaximumHeight(230)
        self.advice_scroll.setStyleSheet(self.scroll_style())

        advice_content = QWidget()
        advice_content_layout = QVBoxLayout(advice_content)
        advice_content_layout.setContentsMargins(0, 0, 0, 0)

        self.advice_text = self.make_text_label()
        advice_content_layout.addWidget(self.advice_text)
        advice_content_layout.addStretch(1)

        self.advice_scroll.setWidget(advice_content)

        self.advice_layout.addWidget(self.advice_title)
        self.advice_layout.addWidget(self.advice_scroll)

        content_row.addWidget(self.conditions_card, 1)
        content_row.addWidget(self.advice_card, 1)

        main_card_layout.addLayout(content_row)

        self.disclaimer_label = QLabel(text("disclaimer", self.current_language))
        self.disclaimer_label.setWordWrap(True)
        self.disclaimer_label.setAlignment(Qt.AlignCenter)
        self.disclaimer_label.setStyleSheet("""
            QLabel {
                color: #7a2e2e;
                font-size: 14px;
                font-weight: bold;
                background: transparent;
                border: none;
                padding: 4px;
            }
        """)

        main_card_layout.addWidget(self.disclaimer_label)

        action_row = QHBoxLayout()
        action_row.setSpacing(28)
        action_row.addStretch(1)

        self.ambulance_btn = QPushButton(text("contact_ambulance", self.current_language))
        self.ambulance_btn.setCursor(Qt.PointingHandCursor)
        self.ambulance_btn.setFixedSize(300, 58)
        self.ambulance_btn.setStyleSheet(self.action_button_style())
        card_shadow(self.ambulance_btn, blur=18, y=5)

        self.start_again_btn = QPushButton(text("start_again", self.current_language))
        self.start_again_btn.setCursor(Qt.PointingHandCursor)
        self.start_again_btn.setFixedSize(300, 58)
        self.start_again_btn.setStyleSheet(self.action_button_style())
        self.start_again_btn.clicked.connect(self.home_requested.emit)
        card_shadow(self.start_again_btn, blur=18, y=5)

        action_row.addWidget(self.ambulance_btn)
        action_row.addWidget(self.start_again_btn)
        action_row.addStretch(1)

        main_card_layout.addLayout(action_row)

        main_row.addWidget(self.main_card)
        main_row.addStretch(1)

        shell_layout.addLayout(main_row, 1)
        root.addWidget(shell)

        self.reset()

    def scroll_style(self):
        return """
            QScrollArea {
                background: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #9b8a7a;
                border-radius: 5px;
            }
        """

    def make_section_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: rgba(240, 235, 219, 245);
                border: none;
                border-radius: 20px;
            }
        """)
        card_shadow(card, blur=15, y=4)
        return card

    def make_section_title(self, title_text):
        label = QLabel(title_text)
        label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 22px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)
        return label

    def make_text_label(self, font_size=18):
        label = QLabel(text("not_available", self.current_language))
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        label.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: {font_size}px;
                font-weight: 800;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
                line-height: 130%;
            }}
        """)
        return label

    def action_button_style(self):
        return f"""
            QPushButton {{
                background: {PRIMARY_DARK};
                color: {CREAM};
                border: none;
                border-radius: 17px;
                font-family: Marcellus;
                font-size: 20px;
                font-weight: 900;
            }}
            QPushButton:hover {{
                background: #4a252b;
            }}
            QPushButton:pressed {{
                background: #1f0e11;
            }}
        """

    def apply_language(self, language: str | None):
        self.current_language = normalise_language(language)

        self.back_button.setText(text("back", self.current_language))
        self.title_label.setText(text("results", self.current_language))
        self.severity_title.setText(text("severity_level", self.current_language))
        self.conditions_title.setText(text("possible_conditions", self.current_language))
        self.advice_title.setText(text("recommendation", self.current_language))
        self.ambulance_btn.setText(text("contact_ambulance", self.current_language))
        self.start_again_btn.setText(text("start_again", self.current_language))

    def set_result(
        self,
        result: dict,
        language: str | None = None,
        input_method: str | None = None,
        body_part: str | None = None,
        disease: str | None = None,
        duration: str | None = None,
        pain_score: int | None = None,
        medication: str | None = None,
        entered_text: str | None = None,
        food_allergies: str | None = None,
    ):
        self.apply_language(language)

        severity = (
            result.get("severity")
            or result.get("prediction")
            or result.get("predicted_label")
            or "unknown"
        )
        severity = str(severity).strip().lower()

        recommendation = (
            result.get("recommendation")
            or result.get("advice")
            or text("no_recommendation", self.current_language)
        )

        possible_diseases = (
            result.get("possible_diseases")
            or result.get("conditions")
            or []
        )

        self.render_severity(severity)
        self.render_possible_diseases(possible_diseases, disease)
        self.render_recommendation(recommendation)

        disclaimer = result.get("disclaimer") or text("disclaimer", self.current_language)
        self.disclaimer_label.setText(disclaimer)

    def render_severity(self, severity: str):
        severity = str(severity).strip().lower()

        if severity == "mild":
            self.severity_value.setText(text("mild", self.current_language))
            bg = "#22C55E"
            glow = QColor(34, 197, 94, 210)
            self.ambulance_btn.hide()

        elif severity == "moderate":
            self.severity_value.setText(text("moderate", self.current_language))
            bg = "#D99A20"
            glow = QColor(217, 154, 32, 220)
            self.ambulance_btn.hide()

        elif severity == "severe":
            self.severity_value.setText(text("severe", self.current_language))
            bg = "#DC2626"
            glow = QColor(220, 38, 38, 230)
            self.ambulance_btn.show()

        else:
            self.severity_value.setText(text("unknown", self.current_language))
            bg = "#777777"
            glow = QColor(119, 119, 119, 180)
            self.ambulance_btn.hide()

        self.severity_value.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
                color: white;
                background: {bg};
                border-radius: 16px;
                padding: 10px 28px;
            }}
        """)

        self.severity_glow.setColor(glow)

        if self.glow_animation.state() != QPropertyAnimation.Running:
            self.glow_animation.start()

    def render_possible_diseases(self, possible_diseases: list, selected_disease: str | None):
        if possible_diseases:
            lines = []

            for index, item in enumerate(possible_diseases, start=1):
                if isinstance(item, dict):
                    name = str(
                        item.get("name")
                        or item.get("condition")
                        or item.get("disease")
                        or "Unknown"
                    ).title()
                else:
                    name = str(item).title()

                name = disease_label(name, self.current_language)
                lines.append(f"{index}. {name}")

            self.conditions_text.setText("\n".join(lines))
            return

        if selected_disease:
            self.conditions_text.setText(
                f"{text('selected_condition', self.current_language)}:\n"
                f"{disease_label(selected_disease, self.current_language)}\n\n"
                f"{text('prediction_not_connected', self.current_language)}"
            )
            return

        self.conditions_text.setText(text("prediction_not_connected", self.current_language))

    def render_recommendation(self, recommendation: str):
        recommendation = str(recommendation).strip()

        if not recommendation:
            self.advice_text.setText(text("no_recommendation", self.current_language))
            return

        recommendation = recommendation.replace("\n", " ")
        parts = [p.strip() for p in recommendation.split(".") if p.strip()]

        if not parts:
            self.advice_text.setText(text("no_recommendation", self.current_language))
            return

        self.advice_text.setText("\n".join(f"• {part}" for part in parts))

    def reset(self):
        self.apply_language(self.current_language)

        self.severity_value.setText(text("not_available", self.current_language).upper())
        self.severity_value.setStyleSheet("""
            QLabel {
                font-family: Marcellus;
                font-size: 24px;
                font-weight: 900;
                color: white;
                background: #777777;
                border-radius: 16px;
                padding: 10px 28px;
            }
        """)
        self.severity_glow.setColor(QColor(119, 119, 119, 180))

        self.conditions_text.setText(text("prediction_not_connected", self.current_language))
        self.advice_text.setText(text("no_recommendation", self.current_language))
        self.disclaimer_label.setText(text("disclaimer", self.current_language))
        self.ambulance_btn.hide()