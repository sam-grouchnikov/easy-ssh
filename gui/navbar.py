#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.1.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""
import sys
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
)


class NavItem(QWidget):
    clicked = pyqtSignal(int)

    def __init__(self, index: int, text: str, icon_path: str):
        super().__init__()
        self.index = index
        self._selected = False

        # PyQt6 specific Enum access
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setFixedWidth(220)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(10, 6, 15, 6)
        self.layout.setSpacing(12)

        self.icon_label = QLabel()
        self.icon_label.setFixedSize(22, 22)

        self.pix = QPixmap(icon_path)
        if not self.pix.isNull():
            self.icon_label.setPixmap(self.pix.scaled(
                22, 22,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

        self.label = QLabel(text)
        self.label.setContentsMargins(0,0,0,3)

        self.layout.addWidget(self.icon_label)
        self.layout.addWidget(self.label)
        self.layout.addStretch()

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        self.update_style()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)
        super().mousePressEvent(event)

    def setSelected(self, selected: bool):
        self._selected = selected
        self.setProperty("selected", str(selected).lower())

        # Force style refresh
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def update_style(self):
        self.setStyleSheet("""
            NavItem {
                background-color: transparent;
                border-radius: 8px;
            }
            NavItem:hover {
                background-color: #E4E4E8;
            }
            NavItem[selected="true"] {
                background-color: #E3CDF7;
            }
            NavItem QLabel {
                background-color: transparent;
                color: black;
                font-size: 15.5px;
            }
        """)

    def update_icon(self, new_path):
        self.pix = QPixmap(new_path)
        if not self.pix.isNull():
            self.icon_label.setPixmap(self.pix.scaled(
                22, 22,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

    def set_light_mode(self):
        self.setStyleSheet("""
                    NavItem {
                        background-color: transparent;
                        border-radius: 8px;
                    }
                    NavItem:hover {
                        background-color: #E4E4E8;
                    }
                    NavItem[selected="true"] {
                        background-color: #E3CDF7;
                    }
                    NavItem QLabel {
                        background-color: transparent;
                        color: black;
                        font-size: 15.5px;
                    }
                """)
    def set_dark_mode(self):
        self.setStyleSheet("""
                    NavItem {
                        background-color: transparent;
                        border-radius: 8px;
                    }
                    NavItem:hover {
                        background-color: #2F2A46;
                    }
                    NavItem[selected="true"] {
                        background-color: #3E375B;
                    }
                    NavItem QLabel {
                        background-color: transparent;
                        color: #E8E3FF;
                        font-size: 15.5px;
                    }
                """)


class SideNavBar(QWidget):
    # Use pyqtSignal for PyQt6
    itemChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)

        self.nb = QWidget()
        self.nb.setFixedWidth(300)
        self.nb_layout = QVBoxLayout(self.nb)
        self.nb_layout.setContentsMargins(0, 10, 10, 10)
        self.nb_layout.setSpacing(5)

        # Using raw strings for Windows paths
        self.light_items_data = [
            ("Terminal", r"C:\Users\samgr\PycharmProjects\easy-ssh-ui-remake\gui\icons\terminal_light.png"),
            ("File Tree", r"C:\Users\samgr\PycharmProjects\easy-ssh-ui-remake\gui\icons\code_light.png"),
            ("Graphs", r"C:\Users\samgr\PycharmProjects\easy-ssh-ui-remake\gui\icons\graph_light.png"),
            ("Project Settings", r"C:\Users\samgr\PycharmProjects\easy-ssh-ui-remake\gui\icons\settings_light.png"),
        ]

        self.dark_items_data = [
            ("Terminal", r"C:\Users\samgr\PycharmProjects\easy-ssh-ui-remake\gui\icons\terminal_dark.png"),
            ("File Tree", r"C:\Users\samgr\PycharmProjects\easy-ssh-ui-remake\gui\icons\code_dark.png"),
            ("Graphs", r"C:\Users\samgr\PycharmProjects\easy-ssh-ui-remake\gui\icons\graph-dark.png"),
            ("Project Settings", r"C:\Users\samgr\PycharmProjects\easy-ssh-ui-remake\gui\icons\settings_dark.png"),
        ]

        self.nav_items = []
        self._setup_items()
        self.container_layout.addWidget(self.nb)
        self.container_layout.addStretch()  # Push everything to the top

        # Initialize selection
        self.select_item(0)

    def _setup_items(self):
        for index, (text, icon_path) in enumerate(self.light_items_data):
            item = NavItem(index, text, icon_path)
            self.nb_layout.addWidget(item)
            self.nav_items.append(item)

            # Connect clicked signal
            item.clicked.connect(self.select_item)

    def select_item(self, target_index):
        for index, item in enumerate(self.nav_items):
            # Fixed: Changed set_active to setSelected to match your NavItem class
            item.setSelected(index == target_index)

        self.itemChanged.emit(target_index)

    def set_light_mode(self):
        for index, item in enumerate(self.nav_items):
            item.set_light_mode()
            item.update_icon(self.light_items_data[index][1])

    def set_dark_mode(self):
        for index, item in enumerate(self.nav_items):
            item.set_dark_mode()
            item.update_icon(self.dark_items_data[index][1])

