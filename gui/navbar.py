#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.0.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)


class NavItem(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, text: str, icon_path: str):
        super().__init__()
        self.index = index
        self._selected = False

        layout = QHBoxLayout(self)
        layout.setContentsMargins(22, 6, 22, 6)
        layout.setSpacing(8)

        icon = QLabel()
        pix = QPixmap(icon_path).scaled(
            22, 22,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        icon.setPixmap(pix)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon)

        self.label = QLabel(text)
        self.label.setStyleSheet("color: white; font-size: 17px;")
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
                border-bottom: 1px solid #4A42D4;
            }

            NavItem[selected="true"] {
                border-bottom: 4px solid #4A42D4;
                background-color: transparent;
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
    container_layout.setContentsMargins(0, 0, 0, 0)
    container_layout.setSpacing(0)

    nb = QWidget()
    nb_layout = QHBoxLayout(nb)
    nb_layout.setContentsMargins(8, 0, 30, 0)
    nb_layout.setSpacing(0)

    items = [
        ("Terminal", "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/command.png"),
        ("Simple-SSH", "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/loading.png"),
        ("File Tree", "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/code-fork.png"),
        ("Graphs", "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/line-graph.png"),
        ("Project Settings", "C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/setting.png"),
    ]

    nav_items = []

    for index, (text, icon_path) in enumerate(items):
        item = NavItem(index, text, icon_path)
        nb_layout.addWidget(item)
        nav_items.append(item)

        item.clicked.connect(
            lambda _, i=index: select_nav_item(nav_items, i)
        )

    filler = QWidget()
    filler.setFixedHeight(52)
    filler.setStyleSheet("""
            background-color: transparent;
            border-bottom: 1px solid #4A42D4;
    """)
    filler.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
    nb_layout.addWidget(filler)

    container_layout.addWidget(nb)

    select_nav_item(nav_items, 0)

    nb_container.nav_items = nav_items
    return nb_container
