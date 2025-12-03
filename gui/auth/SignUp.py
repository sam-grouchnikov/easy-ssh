from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QSpacerItem
)
from PyQt6.QtCore import Qt

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