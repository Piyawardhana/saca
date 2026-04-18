import os

from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame

from .common import BasePage, ImageCardButton, HeaderBar, card_shadow


class GenderPage(BasePage):
    gender_selected = Signal(str)

    def __init__(self, assets_dir: str):
        super().__init__()
        self.assets_dir = assets_dir

        root = QVBoxLayout(self)
        root.setContentsMargins(36, 28, 36, 28)

        page_card = QFrame()
        page_card.setObjectName("PageCard")
        card_shadow(page_card)

        layout = QVBoxLayout(page_card)
        layout.setContentsMargins(34, 30, 34, 30)
        layout.setSpacing(24)

        header = HeaderBar(
            title="Select Profile",
            subtitle="Choose the patient profile to continue.",
            show_back=False
        )

        row = QHBoxLayout()
        row.setSpacing(24)

        male_card = ImageCardButton(
            title="Male",
            subtitle="Continue with male profile",
            image_path=os.path.join(self.assets_dir, "male.png"),
            value="Male"
        )
        female_card = ImageCardButton(
            title="Female",
            subtitle="Continue with female profile",
            image_path=os.path.join(self.assets_dir, "female.png"),
            value="Female"
        )

        male_card.clicked_value.connect(self.gender_selected.emit)
        female_card.clicked_value.connect(self.gender_selected.emit)

        row.addWidget(male_card)
        row.addWidget(female_card)

        layout.addWidget(header)
        layout.addLayout(row, 1)

        root.addWidget(page_card)