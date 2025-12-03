from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QWidget,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QSpacerItem
)
from PyQt6.QtCore import Qt

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