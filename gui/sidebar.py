import sys

from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, QPropertyAnimation


def setupSidebar(layout: QVBoxLayout):
    top_widget = QWidget()
    top_layout = QHBoxLayout()
    top_layout.setContentsMargins(10, 10, 25, 15)
    top_layout.setSpacing(10)
    top_widget.setLayout(top_layout)

    app_icon = QLabel()
    app_icon.setPixmap(QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\terminal.png").scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio,
                                                            Qt.TransformationMode.SmoothTransformation))
    top_layout.addWidget(app_icon)

    app_name = QLabel("Easy-SSH")
    app_name.setStyleSheet("color: white; font-size: 25px; font-weight: bold;")
    top_layout.addWidget(app_name)

    layout.addWidget(top_widget)
    layout.addSpacing(20)

    status_widget = QWidget()
    status_layout = QHBoxLayout()
    status_layout.setContentsMargins(15, 0, 15, 15)
    status_layout.setSpacing(10)
    status_widget.setLayout(status_layout)

    status_icon = QLabel()
    status_icon.setPixmap(QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\remote.png").scaled(26, 26, Qt.AspectRatioMode.KeepAspectRatio,
                                                                  Qt.TransformationMode.SmoothTransformation))
    status_layout.addWidget(status_icon)

    status_label = QLabel("Status: 1 active")
    status_label.setStyleSheet("color: white; font-size: 17px;")
    status_layout.addWidget(status_label)

    status_layout.addStretch()
    end_icon = QLabel()
    end_icon.setPixmap(QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\green_circle.png").scaled(17, 17, Qt.AspectRatioMode.KeepAspectRatio,
                                                             Qt.TransformationMode.SmoothTransformation))
    status_layout.addWidget(end_icon)

    layout.addWidget(status_widget)
    layout.addSpacing(20)

    recent_widget = QWidget()
    recent_layout = QHBoxLayout()
    recent_layout.setContentsMargins(20, 0, 20, 5)  # left, top, right, bottom
    recent_layout.setSpacing(0)
    recent_widget.setLayout(recent_layout)

    recent_label = QLabel("Recent Projects")
    recent_label.setStyleSheet("color: white; font-size: 17px; font-weight: bold")
    recent_layout.addWidget(recent_label)

    layout.addWidget(recent_widget)

    for project_name in ["Project1", "Project2", "Project3"]:
        project_widget = QWidget()
        project_layout = QHBoxLayout()
        project_layout.setContentsMargins(20, 5, 0, 0)
        project_layout.setSpacing(10)
        project_widget.setLayout(project_layout)

        project_icon = QLabel()
        project_icon.setPixmap(QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\files.png").scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio,
                                                                        Qt.TransformationMode.SmoothTransformation))
        project_layout.addWidget(project_icon)

        project_label = QLabel(project_name)
        project_label.setStyleSheet("color: white; font-size: 15px; padding-left: 2px;")
        project_layout.addWidget(project_label)
        project_layout.addStretch()

        layout.addWidget(project_widget)

    layout.addStretch()

    bottom_items = [
        ("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\dark-mode.png", "Dark Mode"),
        ("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\setting.png", "Settings"),
        ("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\home.png", "Home"),
    ]

    for icon_path, text in bottom_items:
        item_widget = QWidget()
        item_layout = QHBoxLayout()
        item_layout.setContentsMargins(20, 5, 0, 0)
        item_layout.setSpacing(10)
        item_widget.setLayout(item_layout)

        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                                       Qt.TransformationMode.SmoothTransformation))
        item_layout.addWidget(icon_label)

        text_label = QLabel(text)
        text_label.setStyleSheet("color: white; font-size: 15px; padding-left: 2px;")
        text_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        if text == "Home":
            item_layout.setContentsMargins(20, 5, 0, 18)
        item_layout.addWidget(text_label)

        item_widget.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        layout.addWidget(item_widget)

    btn_widget = QWidget()
    btn_layout = QHBoxLayout()
    btn_layout.setContentsMargins(20, 5, 20, 20)  # left, top, right, bottom margins
    btn_widget.setLayout(btn_layout)

    disconnect_btn = QPushButton("Disconnect All")
    disconnect_btn.setStyleSheet(
        "color: white; background-color: #6C1616; border: none; padding: 4px 8px; border-radius: 10px;"
        "font-size: 15px;"
    )
    disconnect_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    disconnect_btn.setFixedHeight(35)

    btn_layout.addWidget(disconnect_btn)

    layout.addWidget(btn_widget)