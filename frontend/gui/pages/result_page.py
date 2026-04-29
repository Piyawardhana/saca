from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame

from .common import BasePage


class ResultPage(BasePage):
    back_requested = Signal()
    home_requested = Signal()

    def __init__(self):
        super().__init__()

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        shell = self.build_shell()
        shell_layout = QVBoxLayout(shell)
        shell_layout.setContentsMargins(20, 20, 20, 20)
        shell_layout.setSpacing(0)

        top_row = QHBoxLayout()
        self.back_button = self.build_back_button()
        self.back_button.clicked.connect(self.back_requested.emit)
        top_row.addWidget(self.back_button, 0, Qt.AlignLeft)
        top_row.addStretch(1)

        shell_layout.addLayout(top_row)

        center = QVBoxLayout()
        center.setSpacing(22)
        center.addStretch(1)

        title = QLabel("Results")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 34px; font-weight: 900; color: #2d2d2d;")

        self.severity_line = QLabel("Severity - High")
        self.severity_line.setAlignment(Qt.AlignCenter)
        self.severity_line.setStyleSheet("font-size: 24px; font-weight: 900; color: #2d2d2d;")

        self.red_dot = QLabel("●")
        self.red_dot.setStyleSheet("font-size: 34px; color: red;")

        sev_row = QHBoxLayout()
        sev_row.addStretch(1)
        sev_row.addWidget(self.severity_line)
        sev_row.addSpacing(10)
        sev_row.addWidget(self.red_dot)
        sev_row.addStretch(1)

        advice_box = QFrame()
        advice_box.setObjectName("ContentCard")
        advice_box.setFixedWidth(540)

        advice_layout = QVBoxLayout(advice_box)
        advice_layout.setContentsMargins(24, 24, 24, 24)

        self.recommendation_label = QLabel(
            "Advice:\n• Drink water\n• Rest\n• Take basic medication\n• See doctor if symptoms worsen"
        )
        self.recommendation_label.setWordWrap(True)
        self.recommendation_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: 800;
                color: #111;
                background: transparent;
            }
        """)

        advice_layout.addWidget(self.recommendation_label)

        advice_row = QHBoxLayout()
        advice_row.addStretch(1)
        advice_row.addWidget(advice_box)
        advice_row.addStretch(1)

        self.ambulance_btn = QPushButton("Contact Ambulance  🚑")
        self.ambulance_btn.setObjectName("PrimaryButton")
        self.ambulance_btn.setFixedSize(280, 56)

        self.doctor_btn = QPushButton("Contact Doctor  🧑‍⚕️")
        self.doctor_btn.setObjectName("PrimaryButton")
        self.doctor_btn.setFixedSize(280, 56)
        self.doctor_btn.clicked.connect(self.home_requested.emit)

        action_row = QHBoxLayout()
        action_row.addStretch(1)
        action_row.addWidget(self.ambulance_btn)
        action_row.addSpacing(40)
        action_row.addWidget(self.doctor_btn)
        action_row.addStretch(1)

        center.addWidget(title)
        center.addLayout(sev_row)
        center.addLayout(advice_row)
        center.addLayout(action_row)
        center.addStretch(2)

        shell_layout.addLayout(center, 1)
        root.addWidget(shell)

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
        prediction = (result.get("prediction") or "-").strip().lower()
        recommendation = result.get("recommendation") or "Drink water\nRest\nTake basic medication\nSee doctor if symptoms worsen"

        if prediction == "mild":
            sev_text = "Severity - Mild"
            dot_color = "#22C55E"
        elif prediction == "moderate":
            sev_text = "Severity - Moderate"
            dot_color = "#FACC15"
        else:
            sev_text = "Severity - High"
            dot_color = "#FF0000"

        self.severity_line.setText(sev_text)
        self.red_dot.setStyleSheet(f"font-size: 34px; color: {dot_color};")

        advice_lines = recommendation.split(". ")
        formatted = "Advice:\n"
        for line in advice_lines:
            line = line.strip()
            if line:
                formatted += f"• {line}\n"
        self.recommendation_label.setText(formatted.strip())

    def reset(self):
        self.severity_line.setText("Severity - High")
        self.red_dot.setStyleSheet("font-size: 34px; color: red;")
        self.recommendation_label.setText(
            "Advice:\n• Drink water\n• Rest\n• Take basic medication\n• See doctor if symptoms worsen"
        )