import sys

from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame, QSizePolicy, QSpacerItem, QGridLayout
)
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtSignal


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)


class NavItem(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, text: str, icon_path: str):
        super().__init__()
        self.index = index

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(8)

        # Icon
        icon = QLabel()
        pix = QPixmap(icon_path).scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio)
        icon.setPixmap(pix)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        # Label
        label = QLabel(text)
        label.setStyleSheet("font-size: 17px; color: white;")
        layout.addWidget(label)

        # Entire widget clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            NavItem:hover { background-color: rgba(255,255,255,0.08); }
        """)

    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)
        return super().mousePressEvent(e)


def navbar():
    nb_container = QWidget()
    container_layout = QVBoxLayout(nb_container)
    container_layout.setContentsMargins(0, 0, 0, 0)
    container_layout.setSpacing(0)

    nb = QWidget()
    nb_layout = QHBoxLayout(nb)
    nb_layout.setContentsMargins(0, 10, 0, 10)
    nb_layout.setSpacing(20)

    items = [
        ("File Tree",       "C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\code-fork.png"),
        ("cmd",             "C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\command.png"),
        ("Simple-SSH",      "C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\loading.png"),
        ("Graphs",          "C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\line-graph.png"),
        ("Settings",        "C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\setting.png"),
    ]

    # Create NavItem widgets
    nav_items = []
    for index, (text, icon_path) in enumerate(items):
        item = NavItem(index, text, icon_path)
        item.setFixedHeight(50)
        item.setStyleSheet("background-color: transparent;")
        nb_layout.addWidget(item)
        nav_items.append(item)

    nb_layout.addStretch()
    container_layout.addWidget(nb)

    # Bottom border
    border = QFrame()
    border.setFrameShape(QFrame.Shape.HLine)
    border.setFixedHeight(1)
    border.setStyleSheet("color: #969696;")
    container_layout.addWidget(border)

    # Make the navbar return both container and nav_items
    nb_container.nav_items = nav_items
    return nb_container



def filetree():
    contents = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(10, 5, 10, 5)
    layout.setSpacing(5)
    contents.setLayout(layout)

    icon = QLabel()
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\code-fork.png")
    icon.setPixmap(pixmap.scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
    layout.addWidget(icon)

    label = ClickableLabel("File Tree")
    label.setCursor(Qt.CursorShape.PointingHandCursor)
    label.setStyleSheet("font-size: 17px; color: white;")
    layout.addWidget(label)

    return contents


def cmd():
    contents = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    contents.setLayout(layout)

    icon = QLabel()
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\command.png")
    icon.setPixmap(pixmap.scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
    layout.addWidget(icon)

    label = ClickableLabel("cmd")
    label.setCursor(Qt.CursorShape.PointingHandCursor)
    label.setStyleSheet("margin-left: 0px; font-size: 17px; color: white;")
    layout.addWidget(label)
    layout.setSpacing(0)

    return contents

def simple_ssh():
    contents = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    contents.setLayout(layout)

    icon = QLabel()
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\loading.png")
    icon.setPixmap(pixmap.scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
    layout.addWidget(icon)

    label = ClickableLabel("Simple-SSH")
    label.setCursor(Qt.CursorShape.PointingHandCursor)
    label.setStyleSheet("margin-left: 0px; font-size: 17px; color: white;")
    layout.addWidget(label)
    layout.setSpacing(0)

    return contents

def graphs():
    contents = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    contents.setLayout(layout)

    icon = QLabel()
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\line-graph.png")
    icon.setPixmap(pixmap.scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
    layout.addWidget(icon)

    label = ClickableLabel("Graphs")
    label.setCursor(Qt.CursorShape.PointingHandCursor)
    label.setStyleSheet("margin-left: 0px; font-size: 17px; color: white;")
    layout.addWidget(label)
    layout.setSpacing(0)

    return contents

def proj_settings():
    contents = QWidget()
    layout = QHBoxLayout()
    layout.setContentsMargins(0, 0, 0, 0)
    contents.setLayout(layout)

    icon = QLabel()
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\setting.png")
    icon.setPixmap(pixmap.scaled(25, 25, Qt.AspectRatioMode.KeepAspectRatio))
    layout.addWidget(icon)

    label = ClickableLabel("Project Settings")
    label.setCursor(Qt.CursorShape.PointingHandCursor)
    label.setStyleSheet("margin-left: 0px; font-size: 17px; color: white;")
    layout.addWidget(label)
    layout.setSpacing(0)

    return contents
