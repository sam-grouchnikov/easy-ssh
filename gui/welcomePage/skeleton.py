import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame, QSizePolicy, QSpacerItem
)
from gui.sidebar import setupSidebar
from gui.projectSettings.content import setupContent

class HomepageSkeleton(QMainWindow):
    def __init__(self, navigate):
        super().__init__()
        self.project_name = None
        self.setWindowTitle("Homepage")


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            background-color: qradialgradient(
                cx:0.5, cy:0.5, radius:0.8, fx:0.5, fy:0.5,
                stop:0 #1D1B28, 
                stop:1 #0D0C12
            );
        """)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        main_layout.addStretch(1)

        welcome_box = QWidget()
        welcome_box.setStyleSheet("border: 1px solid #A4A4A4; border-radius: 10px; background-color: #18181F")

        box_layout = QVBoxLayout(welcome_box)
        box_layout.setSpacing(15)
        box_layout.setContentsMargins(50, 70, 50, 70)
        welcome_label = QLabel("Welcome to Easy-SSH")
        welcome_label.setStyleSheet("""color: white; font-size: 40px; border: none;""")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_layout.addWidget(welcome_label)

        desc_label = QLabel("Your one stop shop for AI model training.")
        desc_label.setStyleSheet("color: #A4A4A4; font-size: 22px; border: none;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_layout.addWidget(desc_label)
        box_layout.addSpacing(15)

        self.start_btn = QPushButton("Get Started")
        self.start_btn.setFixedSize(200, 50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                /* Left to Right: Blue (#00dbde) to Purple (#fc00ff) */
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                                  stop:0 #0068C3, stop:1 #6F00B9);
                color: white;
                font-size: 20px;
                border-radius: 10px;
                border: none;
            }

            QPushButton:hover {
                /* Slightly shift the colors or brighten on hover */
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                                  stop:0 #0075DB, stop:1 #0022CD);
                                                  cursor: pointer;
            }

            QPushButton:pressed {
                /* Darken slightly when clicked to give feedback */
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                                                  stop:0 #0068C3, stop:1 #6F00B9);
            }
        """)
        self.start_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.start_btn.clicked.connect(lambda _, p="create": navigate(p))
        box_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        h_container = QHBoxLayout()
        h_container.addStretch(1)
        h_container.addWidget(welcome_box)
        h_container.addStretch(1)

        main_layout.addLayout(h_container)

        main_layout.addStretch(1)




