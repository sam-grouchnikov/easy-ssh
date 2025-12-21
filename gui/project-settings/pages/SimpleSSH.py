from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QFrame, QPushButton
from PyQt6.QtGui import QPixmap, QCursor
from .actionButtonMenu import action_button_menu


def console_output():
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_widget.setStyleSheet("background-color: #18181A;"
                              "border-radius: 5px;")
    return main_widget


class SimpleSSHPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        top_bar = QWidget()
        top_bar.setAutoFillBackground(True)
        top_bar.setStyleSheet(
            "background-color: #1F1F1F;"
            "font-size: 18px;"
            "color: #7D7D7D;"
            "border-radius: 5px"
        )

        top_tab_layout = QHBoxLayout(top_bar)

        current_dir = "sudoku/sudoku-cp-ai/model/"
        l1 = QLabel(f"Current Directory: {current_dir}")

        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(5)
        l2 = QLabel("Status: Connected")
        icon_label = QLabel()
        icon_label.setStyleSheet("padding-left: 5px;"
                                 "padding-right: 5px")
        pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\green_circle.png")
        pixmap = pixmap.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        icon_label.setPixmap(pixmap)

        status_layout.addWidget(l2)
        status_layout.addWidget(icon_label)
        status_container.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        l1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        l2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)

        top_tab_layout.addWidget(l1)
        top_tab_layout.addStretch()
        top_tab_layout.addWidget(status_container)
        layout.addWidget(top_bar)

        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setContentsMargins(0, 15, 0, 0)
        row2_layout.setSpacing(20)
        action = action_button_menu()
        action.setMaximumWidth(425)
        action.setMaximumHeight(650)
        row2_layout.addWidget(action)
        console = console_output()
        # console.setMaximumWidth(500)
        row2_layout.addWidget(console)
        layout.addWidget(row2)

        self.setLayout(layout)

