import sys

from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel
)
from PyQt6.QtCore import Qt, pyqtSignal


class NavItem(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, text: str, icon_path: str):
        super().__init__()
        self.index = index
        self._selected = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 6, 12, 6)
        layout.setSpacing(8)

        icon = QLabel()
        icon.setProperty("role", "navIcon")
        icon.setStyleSheet("background: transparent; border: none;")

        pix = QPixmap(icon_path).scaled(
            22, 22,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        icon.setPixmap(pix)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        self.label = QLabel(text)
        self.label.setProperty("role", "navLabel")
        self.label.setStyleSheet(
            "background: transparent; border: none; color: white; font-size: 17px;"
        )
        layout.addWidget(self.label)

        self.setFixedHeight(52)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.update_style()

    def setSelected(self, selected: bool):
        self._selected = selected
        self.update_style()

    def update_style(self):
        self.setStyleSheet("""
            NavItem {
                background-color: transparent;
                border-bottom: 3px solid transparent;
            }
            NavItem[selected="true"] {
                border-bottom: 3px solid #4A42D4;
            }
           }
        """)
        self.setProperty("selected", self._selected)
        self.style().polish(self)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(event)


def select_nav_item(items, selected_index):
    for item in items:
        item.setSelected(item.index == selected_index)


def navbar():
    nb_container = QWidget()
    container_layout = QVBoxLayout(nb_container)
    container_layout.setContentsMargins(0, 0, 16, 0)
    container_layout.setSpacing(0)

    nb = QWidget()
    nb_layout = QHBoxLayout(nb)
    nb_layout.setContentsMargins(8, 0, 0, 10)
    nb_layout.setSpacing(18)

    items = [
        ("File Tree",  "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/code-fork.png"),
        ("Terminal",   "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/command.png"),
        ("Simple-SSH", "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/loading.png"),
        ("Graphs",     "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/line-graph.png"),
        ("Settings",   "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/setting.png"),
    ]

    nav_items = []

    for index, (text, icon_path) in enumerate(items):
        item = NavItem(index, text, icon_path)
        nb_layout.addWidget(item)
        nav_items.append(item)

        # Safe connection (no late-binding bug)
        item.clicked.connect(
            lambda _, i=index: select_nav_item(nav_items, i)
        )

    nb_layout.addStretch()
    container_layout.addWidget(nb)

    # Default selection
    select_nav_item(nav_items, 0)

    nb_container.nav_items = nav_items
    return nb_container



