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
from PyQt6.QtCore import Qt, QSize, QPointF
from PyQt6.QtGui import QPixmap, QColor, QCursor, QIcon, QPainter, QLinearGradient, QBrush
from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QApplication,
    QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget
)

from .signIn import SignInWidget
from .signUp import SignUpWidget


class CreateSkeleton(QMainWindow):
    def __init__(self, navigate, toggle_theme_func, fb):
        super().__init__()
        self.setWindowTitle("Homepage")
        self.resize(1000, 700)
        self.fb = fb
        self.navigate = navigate

        # Use our custom smooth background frame
        self.central_widget = QFrame()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setObjectName("mainContainer")
        self.central_widget.setMinimumSize(800, 600)


        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)

        self.stack = QStackedWidget(self)
        self.signUpWidget = SignUpWidget(self.fb, self.navigate)
        self.stack.addWidget(self.signUpWidget)
        self.stack.setCurrentIndex(0)

        self.main_layout.addWidget(self.stack)
        self.is_dark = False

        self.set_light_mode()

    def setSignIn(self):
        self.signUpWidget.set_to_sign_in()

    def set_light_mode(self):
        self.signUpWidget.set_light_mode()
        self.central_widget.setStyleSheet("""
                QFrame#mainContainer {
                    background-color: qlineargradient(
                        x1: 1, y1: 0, 
                        x2: 0, y2: 1, 
                        stop: 0 #FDF7FF,
                        stop: 0.5 #F8EBFF,
                        stop: 1 #F3DEFF
                    );
                }
                """)

    def set_dark_mode(self):
        self.signUpWidget.set_dark_mode()
        self.central_widget.setStyleSheet("""
                    QFrame#mainContainer{
                        background-color: #141318
                    }
                """)
