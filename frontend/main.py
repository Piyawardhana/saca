import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.append(CURRENT_DIR)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase, QFont

from gui.main_window import MainWindow


def load_fonts(app):
    font_path = os.path.join(
        CURRENT_DIR,
        "assets",
        "fonts",
        "Marcellus-Regular.ttf"
    )

    if os.path.exists(font_path):
        font_id = QFontDatabase.addApplicationFont(font_path)
        families = QFontDatabase.applicationFontFamilies(font_id)

        if families:
            app.setFont(QFont(families[0]))
            return

    app.setFont(QFont("Georgia"))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Medical Triage Assistant")

    load_fonts(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()