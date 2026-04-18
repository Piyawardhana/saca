from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton
)

from .common import BasePage, HeaderBar, card_shadow


class ResultPage(BasePage):
    back_requested = Signal()
    new_assessment_requested = Signal()

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(36, 28, 36, 28)

        page_card = QFrame()
        page_card.setObjectName("PageCard")
        card_shadow(page_card)

        layout = QVBoxLayout(page_card)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(22)

        self.header = HeaderBar(
            title="Assessment Result",
            subtitle="Review the prediction and recommended next step."
        )
        self.header.back_button.clicked.connect(self.back_requested.emit)

        self.mode_label = QLabel("Mode: -")
        self.mode_label.setStyleSheet("""
            QLabel {
                background: #f6f9fd;
                color: #27476b;
                border: 1px solid #d5e1ef;
                border-radius: 12px;
                padding: 10px 14px;
                font-size: 13px;
                font-weight: 700;
            }
        """)

        self.severity_badge = QLabel("Severity: -")
        self.severity_badge.setAlignment(Qt.AlignCenter)
        self.severity_badge.setMinimumHeight(92)
        self.severity_badge.setStyleSheet("""
            QLabel {
                border-radius: 22px;
                background: #eef2f7;
                color: #10233c;
                font-size: 30px;
                font-weight: 900;
                padding: 18px;
            }
        """)

        self.summary_label = QLabel("Summary: -")
        self.summary_label.setWordWrap(True)
        self.summary_label.setStyleSheet("""
            QLabel {
                background: #fbfdff;
                border: 1px solid #d7e2ef;
                border-radius: 18px;
                padding: 18px;
                font-size: 14px;
                color: #21384f;
            }
        """)

        self.recommendation_label = QLabel("Recommendation: -")
        self.recommendation_label.setWordWrap(True)
        self.recommendation_label.setStyleSheet("""
            QLabel {
                background: #f8fbff;
                border: 1px solid #cfe0fb;
                border-radius: 18px;
                padding: 18px;
                font-size: 15px;
                font-weight: 700;
                color: #173b73;
            }
        """)

        buttons = QHBoxLayout()
        buttons.setSpacing(12)

        self.new_btn = QPushButton("New Assessment")
        self.new_btn.setObjectName("PrimaryButton")
        self.new_btn.clicked.connect(self.new_assessment_requested.emit)

        buttons.addStretch(1)
        buttons.addWidget(self.new_btn)

        layout.addWidget(self.header)
        layout.addWidget(self.mode_label)
        layout.addWidget(self.severity_badge)
        layout.addWidget(self.summary_label)
        layout.addWidget(self.recommendation_label)
        layout.addStretch(1)
        layout.addLayout(buttons)

        root.addWidget(page_card)

    def set_result(
        self,
        result: dict,
        mode_label: str,
        body_part: str | None = None,
        symptom_label: str | None = None,
        pain_score: int | None = None
    ):
        prediction = (result.get("prediction") or "-").strip()
        recommendation = result.get("recommendation") or "-"
        symptoms = result.get("symptoms") or []
        severity_words = result.get("severity_words") or []

        badge_style = self._severity_style(prediction)
        self.severity_badge.setStyleSheet(badge_style)
        self.severity_badge.setText(f"Severity: {prediction.title()}")

        pieces = [f"Mode: {mode_label}"]
        if symptom_label:
            pieces.append(f"Input: {symptom_label}")
        if body_part:
            pieces.append(f"Body Area: {body_part.title()}")
        if pain_score is not None:
            pieces.append(f"Pain Score: {pain_score}/10")
        if symptoms:
            pieces.append(f"Symptoms Found: {', '.join(symptoms)}")
        if severity_words:
            pieces.append(f"Severity Words: {', '.join(severity_words)}")

        self.mode_label.setText(f"Mode: {mode_label}")
        self.summary_label.setText("Summary: " + "  •  ".join(pieces))
        self.recommendation_label.setText(f"Recommendation: {recommendation}")

    def _severity_style(self, prediction: str) -> str:
        p = prediction.lower()
        if p == "mild":
            bg = "#e9f8ee"
            border = "#bfe7c9"
            fg = "#146c36"
        elif p == "moderate":
            bg = "#fff8e6"
            border = "#f0dfab"
            fg = "#8a6500"
        elif p == "severe":
            bg = "#ffe9e9"
            border = "#efbaba"
            fg = "#b42318"
        else:
            bg = "#eef2f7"
            border = "#d7e2ef"
            fg = "#10233c"

        return f"""
            QLabel {{
                border-radius: 22px;
                background: {bg};
                border: 1px solid {border};
                color: {fg};
                font-size: 30px;
                font-weight: 900;
                padding: 18px;
            }}
        """

    def reset(self):
        self.mode_label.setText("Mode: -")
        self.severity_badge.setText("Severity: -")
        self.summary_label.setText("Summary: -")
        self.recommendation_label.setText("Recommendation: -")