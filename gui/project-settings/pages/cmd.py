from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class cmdPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("cmd page"))
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)