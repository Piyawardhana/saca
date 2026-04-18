import os

from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox

from api_client import APIClient
from .pages.gender_page import GenderPage
from .pages.input_page import InputPage
from .pages.disease_page import DiseasePage
from .pages.pain_page import PainPage
from .pages.result_page import ResultPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Triage Assistant")
        self.resize(1320, 860)
        self.setMinimumSize(1180, 760)

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.base_dir, "assets")

        self.client = APIClient()

        self.selected_gender = None
        self.selected_body_part = None
        self.selected_disease = None
        self.selected_pain_score = None
        self.entered_text = ""

        self.setStyleSheet("""
            QMainWindow {
                background: #eef4fb;
            }
        """)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.gender_page = GenderPage(self.assets_dir)
        self.input_page = InputPage(self.assets_dir)
        self.disease_page = DiseasePage(self.assets_dir)
        self.pain_page = PainPage()
        self.result_page = ResultPage()

        self.stack.addWidget(self.gender_page)
        self.stack.addWidget(self.input_page)
        self.stack.addWidget(self.disease_page)
        self.stack.addWidget(self.pain_page)
        self.stack.addWidget(self.result_page)

        self.gender_page.gender_selected.connect(self.on_gender_selected)

        self.input_page.back_requested.connect(self.go_to_gender_page)
        self.input_page.text_submitted.connect(self.on_text_submitted)
        self.input_page.body_part_selected.connect(self.on_body_part_selected)

        self.disease_page.back_requested.connect(self.go_to_input_page)
        self.disease_page.disease_selected.connect(self.on_disease_selected)

        self.pain_page.back_requested.connect(self.go_to_disease_page)
        self.pain_page.pain_selected.connect(self.on_pain_selected)

        self.result_page.back_requested.connect(self.go_back_from_result)
        self.result_page.new_assessment_requested.connect(self.restart_assessment)

        self.stack.setCurrentWidget(self.gender_page)

    def on_gender_selected(self, gender: str):
        self.selected_gender = gender
        self.input_page.set_selected_gender(gender)
        self.stack.setCurrentWidget(self.input_page)

    def go_to_gender_page(self):
        self.stack.setCurrentWidget(self.gender_page)

    def go_to_input_page(self):
        self.stack.setCurrentWidget(self.input_page)

    def go_to_disease_page(self):
        self.stack.setCurrentWidget(self.disease_page)

    def on_text_submitted(self, text: str):
        self.entered_text = text.strip()
        if not self.entered_text:
            QMessageBox.warning(self, "Missing Input", "Please enter symptoms or use the microphone.")
            return
        self.run_text_analysis()

    def on_body_part_selected(self, body_part: str):
        self.selected_body_part = body_part
        self.disease_page.load_diseases(body_part)
        self.stack.setCurrentWidget(self.disease_page)

    def on_disease_selected(self, disease_name: str):
        self.selected_disease = disease_name
        self.pain_page.set_context(self.selected_body_part, self.selected_disease)
        self.stack.setCurrentWidget(self.pain_page)

    def on_pain_selected(self, pain_score: int):
        self.selected_pain_score = pain_score
        self.run_image_analysis()

    def run_text_analysis(self):
        try:
            result = self.client.predict(
                text=self.entered_text,
                gender=self.selected_gender
            )
            self.result_page.set_result(
                result=result,
                mode_label="Text / Voice Submission",
                body_part=None,
                symptom_label=self.entered_text
            )
            self.stack.setCurrentWidget(self.result_page)
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", str(e))

    def run_image_analysis(self):
        try:
            result = self.client.predict(
                text=self.selected_disease,
                gender=self.selected_gender,
                body_part=self.selected_body_part,
                pain_score=self.selected_pain_score
            )
            self.result_page.set_result(
                result=result,
                mode_label="Visual Selection",
                body_part=self.selected_body_part,
                symptom_label=self.selected_disease,
                pain_score=self.selected_pain_score
            )
            self.stack.setCurrentWidget(self.result_page)
        except Exception as e:
            QMessageBox.critical(self, "Prediction Error", str(e))

    def go_back_from_result(self):
        if self.selected_disease and self.selected_body_part:
            self.stack.setCurrentWidget(self.pain_page)
        else:
            self.stack.setCurrentWidget(self.input_page)

    def restart_assessment(self):
        self.selected_body_part = None
        self.selected_disease = None
        self.selected_pain_score = None
        self.entered_text = ""

        self.input_page.reset(keep_gender=True)
        self.disease_page.reset()
        self.pain_page.reset()
        self.result_page.reset()

        self.stack.setCurrentWidget(self.input_page)