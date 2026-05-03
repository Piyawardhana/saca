from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QGraphicsDropShadowEffect, QScrollArea, QWidget
)

from .common import BasePage, card_shadow, PRIMARY_DARK, CREAM


class ResultPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        shell = self.build_shell()
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(30, 25, 30, 25)
        shell_layout.setSpacing(8)

        # -----------------------------
        # Top row
        # -----------------------------
        top_row = QHBoxLayout()

        self.back_button = self.build_back_button()
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

        # -----------------------------
        # Title
        # -----------------------------
        title = QLabel("Results")
        title.setAlignment(Qt.AlignCenter)
        title.setFixedHeight(75)
        title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 54px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
                border: none;
            }}
        """)

        title_shadow = QGraphicsDropShadowEffect(title)
        title_shadow.setBlurRadius(35)
        title_shadow.setOffset(0, 5)
        title_shadow.setColor(QColor(0, 0, 0, 100))
        title.setGraphicsEffect(title_shadow)

        shell_layout.addWidget(title)

        # -----------------------------
        # Main card
        # -----------------------------
        main_row = QHBoxLayout()
        main_row.addStretch(1)

        self.main_card = QFrame()
        self.main_card.setObjectName("ContentCard")
        self.main_card.setFixedWidth(960)
        self.main_card.setMaximumHeight(690)
        card_shadow(self.main_card, blur=30, y=10)

        main_card_layout = QVBoxLayout(self.main_card)
        main_card_layout.setContentsMargins(38, 28, 38, 28)
        main_card_layout.setSpacing(16)

        # -----------------------------
        # Severity section
        # -----------------------------
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

        self.severity_title = QLabel("Severity Level")
        self.severity_title.setStyleSheet(f"""
            QLabel {{
                font-family: Marcellus;
                font-size: 25px;
                font-weight: 900;
                color: {PRIMARY_DARK};
                background: transparent;
            }}
        """)

        self.severity_value = QLabel("Not Available")
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

        # Animated severity glow
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

        # -----------------------------
        # Two-column section
        # -----------------------------
        content_row = QHBoxLayout()
        content_row.setSpacing(16)

        # Conditions
        self.conditions_card = self.make_section_card()
        self.conditions_layout = QVBoxLayout(self.conditions_card)
        self.conditions_layout.setContentsMargins(24, 20, 24, 20)
        self.conditions_layout.setSpacing(10)

        conditions_title = self.make_section_title("Possible Conditions")
        self.conditions_text = self.make_text_label()

        self.conditions_layout.addWidget(conditions_title)
        self.conditions_layout.addWidget(self.conditions_text)

        # Recommendation with scroll
        self.advice_card = self.make_section_card()
        self.advice_layout = QVBoxLayout(self.advice_card)
        self.advice_layout.setContentsMargins(24, 20, 24, 20)
        self.advice_layout.setSpacing(10)

        advice_title = self.make_section_title("Recommendation")

        self.advice_scroll = QScrollArea()
        self.advice_scroll.setWidgetResizable(True)
        self.advice_scroll.setFrameShape(QFrame.NoFrame)
        self.advice_scroll.setMinimumHeight(135)
        self.advice_scroll.setMaximumHeight(165)
        self.advice_scroll.setStyleSheet("""
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
        """)

        advice_content = QWidget()
        advice_content_layout = QVBoxLayout(advice_content)
        advice_content_layout.setContentsMargins(0, 0, 0, 0)

        self.advice_text = self.make_text_label()
        advice_content_layout.addWidget(self.advice_text)
        advice_content_layout.addStretch(1)

        self.advice_scroll.setWidget(advice_content)

        self.advice_layout.addWidget(advice_title)
        self.advice_layout.addWidget(self.advice_scroll)

        content_row.addWidget(self.conditions_card, 1)
        content_row.addWidget(self.advice_card, 1)

        main_card_layout.addLayout(content_row)

        # -----------------------------
        # Details scroll section
        # -----------------------------
        details_card = self.make_section_card()
        details_card.setMinimumHeight(190)

        details_layout = QVBoxLayout(details_card)
        details_layout.setContentsMargins(24, 20, 24, 20)
        details_layout.setSpacing(10)

        details_title = self.make_section_title("Detected Information")

        self.details_scroll = QScrollArea()
        self.details_scroll.setWidgetResizable(True)
        self.details_scroll.setFrameShape(QFrame.NoFrame)
        self.details_scroll.setMinimumHeight(130)
        self.details_scroll.setMaximumHeight(170)
        self.details_scroll.setStyleSheet("""
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
        """)

        details_content = QWidget()
        details_content_layout = QVBoxLayout(details_content)
        details_content_layout.setContentsMargins(0, 0, 0, 0)

        self.details_text = self.make_text_label(font_size=16)
        details_content_layout.addWidget(self.details_text)
        details_content_layout.addStretch(1)

        self.details_scroll.setWidget(details_content)

        details_layout.addWidget(details_title)
        details_layout.addWidget(self.details_scroll)

        main_card_layout.addWidget(details_card)

        # -----------------------------
        # Disclaimer
        # -----------------------------
        self.disclaimer_label = QLabel(
            "This is not a medical diagnosis. Please consult a healthcare professional."
        )
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

        # -----------------------------
        # Buttons
        # -----------------------------
        action_row = QHBoxLayout()
        action_row.setSpacing(28)
        action_row.addStretch(1)

        self.ambulance_btn = QPushButton("Contact Ambulance 🚑")
        self.ambulance_btn.setCursor(Qt.PointingHandCursor)
        self.ambulance_btn.setFixedSize(300, 58)
        self.ambulance_btn.setStyleSheet(self.action_button_style())
        card_shadow(self.ambulance_btn, blur=18, y=5)

        self.start_again_btn = QPushButton("Start Again 🧑‍⚕️")
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

    # ============================================================
    # UI helpers
    # ============================================================

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

    def make_section_title(self, text):
        label = QLabel(text)
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
        label = QLabel("Not available")
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

    # ============================================================
    # Data rendering
    # ============================================================

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
        entered_text: str | None = None
    ):
        severity = (
            result.get("severity")
            or result.get("prediction")
            or "unknown"
        )
        severity = str(severity).strip().lower()

        recommendation = result.get("recommendation") or "No recommendation available."
        possible_diseases = result.get("possible_diseases") or []

        symptoms = result.get("symptoms") or []
        danger_terms = result.get("danger_terms") or []
        severity_words = result.get("severity_words") or []
        negations = result.get("negations") or []
        api_duration = result.get("duration")

        self.render_severity(severity)
        self.render_possible_diseases(possible_diseases, disease)
        self.render_recommendation(recommendation)
        self.render_details(
            entered_text=entered_text,
            input_method=input_method,
            language=language,
            body_part=body_part,
            duration=duration or api_duration,
            pain_score=pain_score,
            medication=medication,
            symptoms=symptoms,
            severity_words=severity_words,
            danger_terms=danger_terms,
            negations=negations
        )

        disclaimer = result.get(
            "disclaimer",
            "This is not a medical diagnosis. Please consult a healthcare professional."
        )
        self.disclaimer_label.setText(disclaimer)

    def render_severity(self, severity: str):
        if severity == "mild":
            self.severity_value.setText("MILD")
            bg = "#22C55E"
            glow = QColor(34, 197, 94, 210)
            self.ambulance_btn.hide()

        elif severity == "moderate":
            self.severity_value.setText("MODERATE")
            bg = "#D99A20"
            glow = QColor(217, 154, 32, 220)
            self.ambulance_btn.hide()

        elif severity == "severe":
            self.severity_value.setText("SEVERE")
            bg = "#DC2626"
            glow = QColor(220, 38, 38, 230)
            self.ambulance_btn.show()

        else:
            self.severity_value.setText("UNKNOWN")
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
                name = str(item.get("name", "Unknown")).title()
                probability = item.get("probability")

                if probability is None:
                    lines.append(f"{index}. {name}")
                else:
                    try:
                        percent = float(probability) * 100
                        lines.append(f"{index}. {name}  —  {percent:.1f}%")
                    except Exception:
                        lines.append(f"{index}. {name}")

            self.conditions_text.setText("\n".join(lines))
            return

        if selected_disease:
            self.conditions_text.setText(
                f"Selected symptom/condition:\n{selected_disease}\n\n"
                "Disease prediction will be added after the disease model is connected."
            )
            return

        self.conditions_text.setText(
            "Disease prediction will be added after the disease model is connected."
        )

    def render_recommendation(self, recommendation: str):
        recommendation = str(recommendation).replace("\n", " ")
        parts = [p.strip() for p in recommendation.split(".") if p.strip()]

        if not parts:
            self.advice_text.setText("No recommendation available.")
            return

        self.advice_text.setText("\n".join(f"• {part}" for part in parts))

    def render_details(
        self,
        entered_text: str | None,
        input_method: str | None,
        language: str | None,
        body_part: str | None,
        duration: str | None,
        pain_score: int | None,
        medication: str | None,
        symptoms: list,
        severity_words: list,
        danger_terms: list,
        negations: list
    ):
        lines = []

        if entered_text:
            lines.append(f"Input: {entered_text}")

        if input_method:
            lines.append(f"Input method: {input_method}")

        if language:
            lines.append(f"Language: {language}")

        if body_part:
            lines.append(f"Body part: {body_part}")

        if duration:
            lines.append(f"Duration: {duration}")

        if pain_score is not None:
            lines.append(f"Pain score: {pain_score}/10")

        if medication:
            lines.append(f"Medication: {medication}")

        if symptoms:
            lines.append("Detected symptoms: " + ", ".join(symptoms))
        else:
            lines.append("Detected symptoms: None")

        if severity_words:
            lines.append("Severity words: " + ", ".join(severity_words))

        if danger_terms:
            lines.append("Warning signs: " + ", ".join(danger_terms))
        else:
            lines.append("Warning signs: None")

        if negations:
            lines.append("Negations: " + ", ".join(negations))

        self.details_text.setText("\n".join(f"• {line}" for line in lines))

    def reset(self):
        self.severity_value.setText("NOT AVAILABLE")
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

        self.conditions_text.setText(
            "Disease prediction will be added after the disease model is connected."
        )
        self.advice_text.setText("No recommendation available.")
        self.details_text.setText("Not available.")
        self.disclaimer_label.setText(
            "This is not a medical diagnosis. Please consult a healthcare professional."
        )
        self.ambulance_btn.hide()