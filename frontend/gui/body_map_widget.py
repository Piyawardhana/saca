from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap


class BodyMapWidget(QLabel):
    body_part_selected = Signal(str)

    def __init__(self, image_path=None):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setMinimumSize(250, 500)

        if image_path:
            pixmap = QPixmap(image_path)
            self.setPixmap(pixmap.scaled(
                250, 500,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))

    def mousePressEvent(self, event):
        x = event.position().x()
        y = event.position().y()

        body_part = self.map_click_to_body_part(x, y)
        self.body_part_selected.emit(body_part)

    def map_click_to_body_part(self, x, y):
        # Adjust these ranges based on your actual image size
        if 80 <= x <= 170 and 20 <= y <= 90:
            return "head"
        elif 70 <= x <= 180 and 90 <= y <= 180:
            return "chest"
        elif 70 <= x <= 180 and 180 <= y <= 270:
            return "abdomen"
        elif 20 <= x <= 70 and 100 <= y <= 230:
            return "left arm"
        elif 180 <= x <= 230 and 100 <= y <= 230:
            return "right arm"
        elif 70 <= x <= 110 and 270 <= y <= 450:
            return "left leg"
        elif 140 <= x <= 180 and 270 <= y <= 450:
            return "right leg"
        else:
            return "unknown"