import os

from PySide6.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QMessageBox,
    QLabel,
    QPushButton,
    QTextEdit,
    QLineEdit,
    QPlainTextEdit,
)

from api_client import APIClient

from .translations import (
    DEFAULT_LANGUAGE,
    normalise_language,
    translate_text,
)

from .pages.welcome_page import WelcomePage
from .pages.language_page import LanguagePage
from .pages.input_method_page import InputMethodPage
from .pages.description_page import DescriptionPage
from .pages.voice_page import VoicePage
from .pages.body_part_page import BodyPartPage
from .pages.disease_page import DiseasePage
from .pages.duration_page import DurationPage
from .pages.pain_page import PainPage
from .pages.food_allergy_page import FoodAllergyPage
from .pages.medication_page import MedicationPage
from .pages.review_page import ReviewPage
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

        self.selected_language = DEFAULT_LANGUAGE
        self.selected_input_method = None

        self.selected_body_part = None
        self.selected_disease = None
        self.entered_text = ""
        self.voice_text = ""
        self.selected_duration = None
        self.selected_pain_score = None
        self.selected_food_allergies = None
        self.takes_medication = None

        self.return_to_review_after_edit = False

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
        self.food_allergy_page = FoodAllergyPage()
        self.medication_page = MedicationPage()
        self.review_page = ReviewPage()
        self.result_page = ResultPage()

        self.pages = [
            self.welcome_page,
            self.language_page,
            self.input_method_page,
            self.description_page,
            self.voice_page,
            self.body_part_page,
            self.disease_page,
            self.duration_page,
            self.pain_page,
            self.food_allergy_page,
            self.medication_page,
            self.review_page,
            self.result_page,
        ]

        self.voice_sensitive_pages = [
            self.duration_page,
            self.pain_page,
            self.food_allergy_page,
            self.medication_page,
        ]

        for page in self.pages:
            self.stack.addWidget(page)

        self.connect_signals()
        self.show_page(self.welcome_page)

    # ============================================================
    # Translation system
    # ============================================================

    def translate_widget_tree(self, root_widget):
        widgets = [root_widget]
        widgets.extend(root_widget.findChildren(QLabel))
        widgets.extend(root_widget.findChildren(QPushButton))
        widgets.extend(root_widget.findChildren(QTextEdit))
        widgets.extend(root_widget.findChildren(QPlainTextEdit))
        widgets.extend(root_widget.findChildren(QLineEdit))

        for widget in widgets:
            if isinstance(widget, QLabel):
                old_text = widget.text()
                new_text = translate_text(
                    old_text,
                    self.selected_language,
                    widget_type="label"
                )
                if old_text != new_text:
                    widget.setText(new_text)

            elif isinstance(widget, QPushButton):
                old_text = widget.text()
                new_text = translate_text(
                    old_text,
                    self.selected_language,
                    widget_type="button"
                )
                if old_text != new_text:
                    widget.setText(new_text)

            elif isinstance(widget, QTextEdit):
                old_text = widget.placeholderText()
                new_text = translate_text(
                    old_text,
                    self.selected_language,
                    widget_type="label"
                )
                if old_text != new_text:
                    widget.setPlaceholderText(new_text)

            elif isinstance(widget, QPlainTextEdit):
                old_text = widget.placeholderText()
                new_text = translate_text(
                    old_text,
                    self.selected_language,
                    widget_type="label"
                )
                if old_text != new_text:
                    widget.setPlaceholderText(new_text)

            elif isinstance(widget, QLineEdit):
                old_text = widget.placeholderText()
                new_text = translate_text(
                    old_text,
                    self.selected_language,
                    widget_type="label"
                )
                if old_text != new_text:
                    widget.setPlaceholderText(new_text)

    def translate_all_pages(self):
        for page in self.pages:
            self.translate_widget_tree(page)

    # ============================================================
    # Voice mode control
    # ============================================================

    def voice_mode_enabled(self) -> bool:
        method = str(self.selected_input_method or "").strip().lower()
        return method in ("voice", "speak", "speech")

    def apply_voice_mode(self, page):
        if hasattr(page, "set_voice_mode_enabled"):
            page.set_voice_mode_enabled(self.voice_mode_enabled())

    def apply_voice_mode_to_all_pages(self):
        for page in self.voice_sensitive_pages:
            self.apply_voice_mode(page)

    def show_page(self, page):
        self.apply_voice_mode(page)
        self.translate_widget_tree(page)
        self.stack.setCurrentWidget(page)

    def show_duration_page(self):
        self.show_page(self.duration_page)

    def show_pain_page(self):
        self.show_page(self.pain_page)

    def show_food_allergy_page(self):
        self.show_page(self.food_allergy_page)

    def show_medication_page(self):
        self.show_page(self.medication_page)

    def show_review_page(self):
        self.return_to_review_after_edit = False

        self.review_page.set_review_data(
            input_method=self.selected_input_method,
            entered_text=self.entered_text,
            voice_text=self.voice_text,
            body_part=self.selected_body_part,
            disease=self.selected_disease,
            duration=self.selected_duration,
            pain_score=self.selected_pain_score,
            food_allergies=self.selected_food_allergies,
            medication=self.takes_medication,
        )

        self.show_page(self.review_page)

    # ============================================================
    # Review edit helpers
    # ============================================================

    def edit_from_review(self, page_function):
        self.return_to_review_after_edit = True
        page_function()

    def edit_input_from_review(self):
        self.return_to_review_after_edit = True

        if self.selected_input_method == "text":
            self.show_page(self.description_page)
        elif self.selected_input_method == "voice":
            self.show_page(self.voice_page)
        elif self.selected_input_method == "image":
            self.show_page(self.body_part_page)
        else:
            self.show_page(self.input_method_page)

    def back_from_edit_or_normal(self, normal_page_function):
        if self.return_to_review_after_edit:
            self.show_review_page()
        else:
            normal_page_function()

    # ============================================================
    # Signals
    # ============================================================

    def connect_signals(self):
        self.welcome_page.next_requested.connect(
            lambda: self.show_page(self.language_page)
        )

        self.language_page.back_requested.connect(
            lambda: self.show_page(self.welcome_page)
        )
        self.language_page.home_requested.connect(self.go_home)
        self.language_page.language_selected.connect(self.on_language_selected)

        self.input_method_page.back_requested.connect(
            lambda: self.show_page(self.language_page)
        )
        self.input_method_page.home_requested.connect(self.go_home)
        self.input_method_page.method_selected.connect(self.on_input_method_selected)

        self.description_page.back_requested.connect(
            lambda: self.back_from_edit_or_normal(
                lambda: self.show_page(self.input_method_page)
            )
        )
        self.description_page.home_requested.connect(self.go_home)
        self.description_page.next_requested.connect(self.on_description_submitted)

        self.voice_page.back_requested.connect(
            lambda: self.back_from_edit_or_normal(
                lambda: self.show_page(self.input_method_page)
            )
        )
        self.voice_page.home_requested.connect(self.go_home)
        self.voice_page.next_requested.connect(self.on_voice_submitted)

        self.body_part_page.back_requested.connect(
            lambda: self.back_from_edit_or_normal(
                lambda: self.show_page(self.input_method_page)
            )
        )
        if hasattr(self.body_part_page, "home_requested"):
            self.body_part_page.home_requested.connect(self.go_home)
        self.body_part_page.body_part_selected.connect(self.on_body_part_selected)

        self.disease_page.back_requested.connect(
            lambda: self.back_from_edit_or_normal(
                lambda: self.show_page(self.body_part_page)
            )
        )
        if hasattr(self.disease_page, "home_requested"):
            self.disease_page.home_requested.connect(self.go_home)
        self.disease_page.disease_selected.connect(self.on_disease_selected)

        self.duration_page.back_requested.connect(
            lambda: self.back_from_edit_or_normal(self.go_back_to_previous_input_page)
        )
        self.duration_page.home_requested.connect(self.go_home)
        self.duration_page.duration_selected.connect(self.on_duration_selected)

        self.pain_page.back_requested.connect(
            lambda: self.back_from_edit_or_normal(self.show_duration_page)
        )
        self.pain_page.home_requested.connect(self.go_home)
        self.pain_page.pain_selected.connect(self.on_pain_selected)

        self.food_allergy_page.back_requested.connect(
            lambda: self.back_from_edit_or_normal(self.show_pain_page)
        )
        self.food_allergy_page.home_requested.connect(self.go_home)
        self.food_allergy_page.allergies_submitted.connect(
            self.on_food_allergies_submitted
        )

        self.medication_page.back_requested.connect(
            lambda: self.back_from_edit_or_normal(self.show_food_allergy_page)
        )
        self.medication_page.home_requested.connect(self.go_home)
        self.medication_page.medication_selected.connect(self.on_medication_selected)

        self.review_page.back_requested.connect(self.show_medication_page)
        self.review_page.home_requested.connect(self.go_home)
        self.review_page.confirm_requested.connect(self.run_analysis)

        self.review_page.edit_input_requested.connect(self.edit_input_from_review)

        self.review_page.edit_body_part_requested.connect(
            lambda: self.edit_from_review(lambda: self.show_page(self.body_part_page))
        )

        self.review_page.edit_disease_requested.connect(
            lambda: self.edit_from_review(self.show_disease_from_review)
        )

        self.review_page.edit_duration_requested.connect(
            lambda: self.edit_from_review(self.show_duration_page)
        )

        self.review_page.edit_pain_requested.connect(
            lambda: self.edit_from_review(self.show_pain_page)
        )

        self.review_page.edit_food_allergy_requested.connect(
            lambda: self.edit_from_review(self.show_food_allergy_page)
        )

        self.review_page.edit_medication_requested.connect(
            lambda: self.edit_from_review(self.show_medication_page)
        )

        self.result_page.back_requested.connect(self.show_review_page)
        self.result_page.home_requested.connect(self.go_home)

    # ============================================================
    # Page flow
    # ============================================================

    def on_language_selected(self, language: str):
        self.selected_language = normalise_language(language)
        print("Selected language:", self.selected_language)

        self.translate_all_pages()
        self.show_page(self.input_method_page)

    def on_input_method_selected(self, method: str):
        self.selected_input_method = str(method or "").strip().lower()
        print("Selected input method:", self.selected_input_method)
        print("Voice mode enabled:", self.voice_mode_enabled())

        self.apply_voice_mode_to_all_pages()

        if self.selected_input_method == "text":
            self.show_page(self.description_page)
        elif self.selected_input_method in ("voice", "speak", "speech"):
            self.show_page(self.voice_page)
        elif self.selected_input_method == "image":
            self.show_page(self.body_part_page)
        else:
            QMessageBox.warning(
                self,
                "Input Method Error",
                f"Unknown input method: {method}"
            )
            self.show_page(self.input_method_page)

    def on_description_submitted(self, text: str):
        self.entered_text = text.strip()

        if not self.entered_text:
            QMessageBox.warning(
                self,
                translate_text("Missing Input", self.selected_language, "label"),
                translate_text(
                    "Please enter a description.",
                    self.selected_language,
                    "label"
                )
            )
            return

        if self.return_to_review_after_edit:
            self.show_review_page()
        else:
            self.show_duration_page()

    def on_voice_submitted(self, text: str):
        self.voice_text = text.strip()

        if not self.voice_text:
            QMessageBox.warning(
                self,
                translate_text("Missing Input", self.selected_language, "label"),
                translate_text(
                    "Please record symptoms first.",
                    self.selected_language,
                    "label"
                )
            )
            return

        if self.return_to_review_after_edit:
            self.show_review_page()
        else:
            self.show_duration_page()

    def on_body_part_selected(self, body_part: str):
        self.selected_body_part = body_part

        self.disease_page.load_diseases(body_part)
        self.translate_widget_tree(self.disease_page)

        if self.return_to_review_after_edit:
            self.show_review_page()
        else:
            self.show_page(self.disease_page)

    def show_disease_from_review(self):
        if self.selected_body_part:
            self.disease_page.load_diseases(self.selected_body_part)
            self.translate_widget_tree(self.disease_page)
            self.show_page(self.disease_page)
        else:
            self.show_page(self.body_part_page)

    def on_disease_selected(self, disease: str):
        self.selected_disease = disease

        if self.return_to_review_after_edit:
            self.show_review_page()
        else:
            self.show_duration_page()

    def go_back_to_previous_input_page(self):
        if self.selected_input_method == "text":
            self.show_page(self.description_page)
        elif self.selected_input_method in ("voice", "speak", "speech"):
            self.show_page(self.voice_page)
        elif self.selected_input_method == "image":
            self.show_page(self.disease_page)
        else:
            self.show_page(self.input_method_page)

    def on_duration_selected(self, duration: str):
        self.selected_duration = duration

        if self.return_to_review_after_edit:
            self.show_review_page()
        else:
            self.show_pain_page()

    def on_pain_selected(self, pain_score: int):
        self.selected_pain_score = pain_score

        if self.return_to_review_after_edit:
            self.show_review_page()
        else:
            self.show_food_allergy_page()

    def on_food_allergies_submitted(self, allergies: str):
        allergies = allergies.strip() if allergies else ""

        if not allergies:
            allergies = "Not specified"

        self.selected_food_allergies = allergies

        if self.return_to_review_after_edit:
            self.show_review_page()
        else:
            self.show_medication_page()

    def on_medication_selected(self, takes_medication: str):
        self.takes_medication = takes_medication
        self.show_review_page()

    # ============================================================
    # Backend prediction
    # ============================================================

    def build_text_for_prediction(self) -> str:
        parts = []

        if self.selected_input_method == "text":
            if self.entered_text:
                parts.append(self.entered_text)

        elif self.selected_input_method in ("voice", "speak", "speech"):
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

        if self.selected_food_allergies:
            parts.append(f"Food allergies: {self.selected_food_allergies}")

        if self.takes_medication:
            parts.append(f"Takes medication: {self.takes_medication}")

        return ". ".join(parts)

    def run_analysis(self):
        try:
            input_text = self.build_text_for_prediction()

            if not input_text.strip():
                QMessageBox.warning(
                    self,
                    translate_text("Missing Input", self.selected_language, "label"),
                    translate_text(
                        "Please provide symptoms before continuing.",
                        self.selected_language,
                        "label"
                    )
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
                    translate_text("Prediction Error", self.selected_language, "label"),
                    response["error"]
                )
                return

            result = response["data"]

            try:
                self.result_page.set_result(
                    result=result,
                    language=self.selected_language,
                    input_method=self.selected_input_method,
                    body_part=self.selected_body_part,
                    disease=self.selected_disease,
                    duration=self.selected_duration,
                    pain_score=self.selected_pain_score,
                    food_allergies=self.selected_food_allergies,
                    medication=self.takes_medication,
                    entered_text=None,
                )
            except TypeError:
                self.result_page.set_result(
                    result=result,
                    language=self.selected_language,
                    input_method=self.selected_input_method,
                    body_part=self.selected_body_part,
                    disease=self.selected_disease,
                    duration=self.selected_duration,
                    pain_score=self.selected_pain_score,
                    medication=self.takes_medication,
                    entered_text=None,
                )

            self.translate_widget_tree(self.result_page)
            self.show_page(self.result_page)

        except Exception as e:
            QMessageBox.critical(
                self,
                translate_text("Prediction Error", self.selected_language, "label"),
                str(e)
            )

    # ============================================================
    # Reset
    # ============================================================

    def go_home(self):
        self.selected_language = DEFAULT_LANGUAGE
        self.selected_input_method = None

        self.selected_body_part = None
        self.selected_disease = None
        self.entered_text = ""
        self.voice_text = ""
        self.selected_duration = None
        self.selected_pain_score = None
        self.selected_food_allergies = None
        self.takes_medication = None

        self.return_to_review_after_edit = False

        for page in self.pages:
            if hasattr(page, "reset"):
                page.reset()

        self.apply_voice_mode_to_all_pages()

        self.translate_all_pages()
        self.show_page(self.welcome_page)