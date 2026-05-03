import os

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox

from api_client import APIClient

from .pages.welcome_page import WelcomePage
from .pages.language_page import LanguagePage
from .pages.input_method_page import InputMethodPage
from .pages.description_page import DescriptionPage
from .pages.voice_page import VoicePage
from .pages.body_part_page import BodyPartPage
from .pages.disease_page import DiseasePage
from .pages.duration_page import DurationPage
from .pages.pain_page import PainPage
from .pages.medication_page import MedicationPage
from .pages.result_page import ResultPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Triage Assistant")
        self.resize(1360, 860)
        self.setMinimumSize(1180, 760)

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.client = APIClient()

        self.selected_language = None
        self.selected_input_method = None
        self.selected_body_part = None
        self.selected_disease = None
        self.entered_text = ""
        self.voice_text = ""
        self.selected_duration = None
        self.selected_pain_score = None
        self.takes_medication = None

        self.setStyleSheet("""
            QMainWindow {
                background: #eef5fb;
            }
        """)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.welcome_page = WelcomePage()
        self.language_page = LanguagePage()
        self.input_method_page = InputMethodPage()
        self.description_page = DescriptionPage()
        self.voice_page = VoicePage()
        self.body_part_page = BodyPartPage(self.assets_dir)
        self.disease_page = DiseasePage(self.assets_dir)
        self.duration_page = DurationPage()
        self.pain_page = PainPage()
        self.medication_page = MedicationPage()
        self.result_page = ResultPage()

        for page in [
            self.welcome_page,
            self.language_page,
            self.input_method_page,
            self.description_page,
            self.voice_page,
            self.body_part_page,
            self.disease_page,
            self.duration_page,
            self.pain_page,
            self.medication_page,
            self.result_page,
        ]:
            self.stack.addWidget(page)

        self.connect_signals()
        self.stack.setCurrentWidget(self.welcome_page)

    def connect_signals(self):
        self.welcome_page.next_requested.connect(
            lambda: self.stack.setCurrentWidget(self.language_page)
        )

        self.language_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.welcome_page)
        )
        self.language_page.language_selected.connect(self.on_language_selected)

        self.input_method_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.language_page)
        )
        self.input_method_page.method_selected.connect(self.on_input_method_selected)

        self.description_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.input_method_page)
        )
        self.description_page.next_requested.connect(self.on_description_submitted)

        self.voice_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.input_method_page)
        )
        self.voice_page.next_requested.connect(self.on_voice_submitted)

        self.body_part_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.input_method_page)
        )
        self.body_part_page.body_part_selected.connect(self.on_body_part_selected)

        self.disease_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.body_part_page)
        )
        self.disease_page.disease_selected.connect(self.on_disease_selected)

        self.duration_page.back_requested.connect(self.go_back_to_previous_input_page)
        self.duration_page.duration_selected.connect(self.on_duration_selected)

        self.pain_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.duration_page)
        )
        self.pain_page.pain_selected.connect(self.on_pain_selected)

        self.medication_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.pain_page)
        )
        self.medication_page.medication_selected.connect(self.on_medication_selected)

        self.result_page.back_requested.connect(
            lambda: self.stack.setCurrentWidget(self.medication_page)
        )
        self.result_page.home_requested.connect(self.go_home)

        self.language_page.home_requested.connect(self.go_home)
        self.input_method_page.home_requested.connect(self.go_home)
        self.description_page.home_requested.connect(self.go_home)
        self.duration_page.home_requested.connect(self.go_home)
        self.pain_page.home_requested.connect(self.go_home)
        self.medication_page.home_requested.connect(self.go_home)

    def on_language_selected(self, language: str):
        self.selected_language = language
        self.stack.setCurrentWidget(self.input_method_page)

    def on_input_method_selected(self, method: str):
        self.selected_input_method = method

        if method == "text":
            self.stack.setCurrentWidget(self.description_page)
        elif method == "voice":
            self.stack.setCurrentWidget(self.voice_page)
        elif method == "image":
            self.stack.setCurrentWidget(self.body_part_page)

    def on_description_submitted(self, text: str):
        self.entered_text = text.strip()
        if not self.entered_text:
            QMessageBox.warning(self, "Missing Input", "Please enter a description.")
            return
        self.stack.setCurrentWidget(self.duration_page)

    def on_voice_submitted(self, text: str):
        self.voice_text = text.strip()
        if not self.voice_text:
            QMessageBox.warning(self, "Missing Input", "Please record symptoms first.")
            return
        self.stack.setCurrentWidget(self.duration_page)

    def on_body_part_selected(self, body_part: str):
        self.selected_body_part = body_part
        self.disease_page.load_diseases(body_part)
        self.stack.setCurrentWidget(self.disease_page)

    def on_disease_selected(self, disease: str):
        self.selected_disease = disease
        self.stack.setCurrentWidget(self.duration_page)

    def go_back_to_previous_input_page(self):
        if self.selected_input_method == "text":
            self.stack.setCurrentWidget(self.description_page)
        elif self.selected_input_method == "voice":
            self.stack.setCurrentWidget(self.voice_page)
        elif self.selected_input_method == "image":
            self.stack.setCurrentWidget(self.disease_page)

    def on_duration_selected(self, duration: str):
        self.selected_duration = duration
        self.stack.setCurrentWidget(self.pain_page)

    def on_pain_selected(self, pain_score: int):
        self.selected_pain_score = pain_score
        self.stack.setCurrentWidget(self.medication_page)

    def on_medication_selected(self, takes_medication: str):
        self.takes_medication = takes_medication
        self.run_analysis()

    def build_text_for_prediction(self) -> str:
        if self.selected_input_method == "text":
            return self.entered_text

        if self.selected_input_method == "voice":
            return self.voice_text

        if self.selected_input_method == "image":
            parts = []
            if self.selected_disease:
                parts.append(self.selected_disease)
            if self.selected_duration:
                parts.append(f"Duration: {self.selected_duration}")
            if self.takes_medication:
                parts.append(f"Medication: {self.takes_medication}")
            return " | ".join(parts)

        return ""

    def run_analysis(self):
        try:
            input_text = self.build_text_for_prediction()

            if not input_text.strip():
                QMessageBox.warning(
                    self,
                    "Missing Input",
                    "Please provide symptoms before continuing."
                )
                return

            response = self.client.predict(
                text=input_text,
                pain_score=self.selected_pain_score,
                body_part=self.selected_body_part,
                age=None,
                gender=None,
            )

            if not response["success"]:
                QMessageBox.critical(
                    self,
                    "Prediction Error",
                    response["error"]
                )
                return

            result = response["data"]

            self.result_page.set_result(
                result=result,
                language=self.selected_language,
                input_method=self.selected_input_method,
                body_part=self.selected_body_part,
                disease=self.selected_disease,
                duration=self.selected_duration,
                pain_score=self.selected_pain_score,
                medication=self.takes_medication,
                entered_text=input_text
            )

            self.stack.setCurrentWidget(self.result_page)

        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", str(e))

    def go_home(self):
        self.selected_language = None
        self.selected_input_method = None
        self.selected_body_part = None
        self.selected_disease = None
        self.entered_text = ""
        self.voice_text = ""
        self.selected_duration = None
        self.selected_pain_score = None
        self.takes_medication = None

        self.description_page.reset()
        self.voice_page.reset()
        self.disease_page.reset()
        self.duration_page.reset()
        self.pain_page.reset()
        self.medication_page.reset()
        self.result_page.reset()

        self.stack.setCurrentWidget(self.welcome_page)

    def build_text_for_prediction(self) -> str:
        parts = []

        if self.selected_input_method == "text":
            if self.entered_text:
                parts.append(self.entered_text)

        elif self.selected_input_method == "voice":
            if self.voice_text:
                parts.append(self.voice_text)

        elif self.selected_input_method == "image":
            if self.selected_body_part:
                parts.append(f"Body part: {self.selected_body_part}")

            if self.selected_disease:
                parts.append(f"Symptom or condition selected: {self.selected_disease}")

        if self.selected_duration:
            parts.append(f"Duration: {self.selected_duration}")

        if self.selected_pain_score is not None:
            parts.append(f"Pain score: {self.selected_pain_score} out of 10")

        if self.takes_medication:
            parts.append(f"Takes medication: {self.takes_medication}")

        return ". ".join(parts)