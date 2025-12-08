from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel


class SimpleSSHPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("simple ssh page"))
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)