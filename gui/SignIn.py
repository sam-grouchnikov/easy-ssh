import sys

from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt

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

        self.sign_in_form = self.create_sign_in_form()
        self.sign_up_form = self.create_sign_up_form()
        self.stacked_layout.addWidget(self.sign_in_form)
        self.stacked_layout.addWidget(self.sign_up_form)

    def create_sign_in_form(self):
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(20)
        widget.setLayout(main_layout)

        input_width = 400
        input_height = 45
        label_input_spacing = 5

        username_group = QVBoxLayout()
        username_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        username_group.setSpacing(label_input_spacing)

        username_label = QLabel("Username")
        username_label.setStyleSheet("font-size: 14px; color: black;")
        username_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        username_label.setFixedWidth(input_width)
        username_group.addWidget(username_label)

        self.si_username = QLineEdit()
        self.si_username.setFixedWidth(input_width)
        self.si_username.setFixedHeight(input_height)
        self.si_username.setStyleSheet("""
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: black;
        """)
        username_group.addWidget(self.si_username)

        main_layout.addLayout(username_group)

        password_group = QVBoxLayout()
        password_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        password_group.setSpacing(label_input_spacing)

        password_label = QLabel("Password")
        password_label.setStyleSheet("font-size: 14px; color: black;")
        password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        password_label.setFixedWidth(input_width)
        password_group.addWidget(password_label)

        self.si_password = QLineEdit()
        self.si_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.si_password.setFixedWidth(input_width)
        self.si_password.setFixedHeight(input_height)
        self.si_password.setStyleSheet("""
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 5px;
            font-size: 14px;
            color: black;
        """)
        password_group.addWidget(self.si_password)

        main_layout.addLayout(password_group)

        self.si_submit = QPushButton("Sign In")

        self.si_submit.setFixedWidth(input_width)
        self.si_submit.setFixedHeight(45)
        self.si_submit.setStyleSheet("""
            font-size: 14px;
            background-color: #000000;
            color: white;
            border-radius: 10px;
            padding: 5px;
        }
        QPushButton:pressed {
            background-color: #333333;
        }
        """)
        self.si_submit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        extra_spacing = QSpacerItem(0, 10)
        main_layout.addItem(extra_spacing)
        main_layout.addWidget(self.si_submit, alignment=Qt.AlignmentFlag.AlignCenter)

        return widget

    def create_sign_up_form(self):
        widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setSpacing(20)
        widget.setLayout(main_layout)

        input_width = 400
        input_height = 45
        label_input_spacing = 5

        name_style = """
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: black;
            """
        label_style = "font-size: 14px; color: black;"

        name_input_spacing = 10

        username_group = QVBoxLayout()
        username_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        username_group.setSpacing(label_input_spacing)

        username_label = QLabel("Username")
        username_label.setStyleSheet(label_style)
        username_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        username_label.setFixedWidth(input_width)
        username_group.addWidget(username_label)

        self.su_username = QLineEdit()
        self.su_username.setFixedWidth(input_width)
        self.su_username.setFixedHeight(input_height)
        self.su_username.setStyleSheet(name_style)
        username_group.addWidget(self.su_username)
        main_layout.addLayout(username_group)

        password_group = QVBoxLayout()
        password_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        password_group.setSpacing(label_input_spacing)

        password_label = QLabel("Password")
        password_label.setStyleSheet(label_style)
        password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        password_label.setFixedWidth(input_width)
        password_group.addWidget(password_label)

        self.su_password = QLineEdit()
        self.su_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.su_password.setFixedWidth(input_width)
        self.su_password.setFixedHeight(input_height)
        self.su_password.setStyleSheet(name_style)
        password_group.addWidget(self.su_password)
        main_layout.addLayout(password_group)

        confirm_password_group = QVBoxLayout()
        confirm_password_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        confirm_password_group.setSpacing(label_input_spacing)

        confirm_password_label = QLabel("Confirm Password")
        confirm_password_label.setStyleSheet(label_style)
        confirm_password_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        confirm_password_label.setFixedWidth(input_width)
        confirm_password_group.addWidget(confirm_password_label)

        self.su_confirm_password = QLineEdit()
        self.su_confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.su_confirm_password.setFixedWidth(input_width)
        self.su_confirm_password.setFixedHeight(input_height)
        self.su_confirm_password.setStyleSheet(name_style)
        confirm_password_group.addWidget(self.su_confirm_password)
        main_layout.addLayout(confirm_password_group)

        self.su_submit = QPushButton("Sign Up")
        self.su_submit.setFixedWidth(input_width)
        self.su_submit.setFixedHeight(input_height)
        self.su_submit.setStyleSheet("""
                font-size: 14px;
                background-color: #000000;
                color: white;
                border-radius: 10px;
                padding: 5px;
            }
            QPushButton:pressed {
                background-color: #333333;
            }
            """)
        self.su_submit.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        extra_spacing = QSpacerItem(0, 10)
        main_layout.addItem(extra_spacing)

        main_layout.addWidget(self.su_submit, alignment=Qt.AlignmentFlag.AlignCenter)

        return widget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthWindow()
    window.show()
    sys.exit(app.exec())