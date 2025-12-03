import sys

from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt
from SignIn import create_sign_in_form
from SignUp import create_sign_up_form

class AuthWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentication")
        self.setGeometry(100, 100, 600, 400)
        self.setMinimumWidth(400)
        self.setMinimumHeight(400)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            background: qlineargradient(
                x1: 0, y1: 0, x2: 1, y2: 1, 
                stop: 0 #7F4DF4, 
                stop: 1 #772FBB
            );
        """)
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        central_widget.setLayout(main_layout)


        box = QFrame()
        box.setMinimumWidth(100)
        box.setMaximumWidth(600)
        box.setMinimumHeight(80)
        box.setMaximumHeight(500)
        box.setFrameShape(QFrame.Shape.StyledPanel)
        box_layout = QVBoxLayout()
        box_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        box_layout.setContentsMargins(0, 20, 0, 0)
        box.setLayout(box_layout)
        box.setStyleSheet("background-color: #ffffff;"
                          "border-radius: 10px;")
        main_layout.addWidget(box)

        toggle_layout = QHBoxLayout()
        toggle_layout.setSpacing(0)
        toggle_layout.setContentsMargins(50, 10, 50, 10)
        self.sign_in_btn = QPushButton("Sign In")
        self.sign_in_btn.setCheckable(True)
        self.sign_in_btn.setStyleSheet("""
            font-size: 14px;
            background-color: #D9D9D9;
            color: #000000;
            border-top-left-radius: 10px;
            border-bottom-left-radius: 10px;
            border-top-right-radius: 0px;
            border-bottom-right-radius: 0px;
        }
        QPushButton:checked {
            background-color: #B9B9B9;
        }
        """)
        self.sign_in_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


        self.sign_up_btn = QPushButton("Sign Up")
        self.sign_up_btn.setCheckable(True)
        self.sign_up_btn.setStyleSheet("""
            font-size: 14px;
            background-color: #D9D9D9;
            color: #000000;
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
            border-top-right-radius: 10px;
            border-bottom-right-radius: 10px;
        }
        QPushButton:checked {
            background-color: #B9B9B9;
        }
        QPushButton:hover {
            cursor: pointing hand;
        }
        """)
        self.sign_up_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


        self.sign_in_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.sign_up_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.sign_in_btn.setMinimumHeight(45)
        self.sign_up_btn.setMinimumHeight(45)
        toggle_layout.addWidget(self.sign_in_btn)
        toggle_layout.addWidget(self.sign_up_btn)
        toggle_layout.setStretch(0, 1)
        toggle_layout.setStretch(1, 1)
        box_layout.addLayout(toggle_layout)

        self.sign_in_btn.setChecked(True)
        self.sign_in_btn.clicked.connect(lambda: self.sign_up_btn.setChecked(False))
        self.sign_up_btn.clicked.connect(lambda: self.sign_in_btn.setChecked(False))
        self.sign_in_btn.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(0))
        self.sign_up_btn.clicked.connect(lambda: self.stacked_layout.setCurrentIndex(1))

        self.stacked_layout = QStackedLayout()
        box_layout.addLayout(self.stacked_layout)

        self.sign_in_form = create_sign_in_form(self)
        self.sign_up_form = create_sign_up_form(self)
        self.stacked_layout.addWidget(self.sign_in_form)
        self.stacked_layout.addWidget(self.sign_up_form)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())