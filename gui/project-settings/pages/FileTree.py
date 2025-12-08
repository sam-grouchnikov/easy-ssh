from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class FileTreePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("file tree page"))
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)