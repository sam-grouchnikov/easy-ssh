#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.2.1
Email: sam.grouchnikov@gmail.com
Status: Development
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtWidgets import (
    QLabel, QHBoxLayout, QWidget, QFrame, QVBoxLayout,
    QLineEdit, QPushButton, QGraphicsDropShadowEffect, QSizePolicy
)


class SignInWidget(QWidget):
    def __init__(self, fb, nav):
        super().__init__()
        self.main_layout = QVBoxLayout(self)

        self.outer_container = QWidget()
        self.outer_container_layout = QVBoxLayout(self.outer_container)
        self.outer_container_layout.addWidget(QLabel("Test"))

        self.main_layout.addWidget(self.outer_container)

    def set_light_mode(self):
        pass

    def set_dark_mode(self):
        pass