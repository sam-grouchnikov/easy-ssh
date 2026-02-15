#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.2.1
Email: sam.grouchnikov@gmail.com
Status: Development
"""

import sys
from PyQt6.QtCore import Qt, QSize, QPointF
from PyQt6.QtGui import QPixmap, QColor, QCursor, QIcon, QPainter, QLinearGradient, QBrush
from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QApplication,
    QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from pathlib import Path
import sys

def resource_path(relative_path: str) -> str:
    # PyInstaller onefile
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        # Walk upward until we find the project root marker(s)
        here = Path(__file__).resolve()
        for p in [here] + list(here.parents):
            if (p / "application.py").exists() or (p / "pyproject.toml").exists() or (p / ".git").exists():
                base = p
                break
        else:
            base = here.parent
    return str(base / relative_path)

class HomepageSkeleton(QMainWindow):
    def __init__(self, navigate, toggle_theme_func):
        super().__init__()
        self.setWindowTitle("Homepage")
        self.resize(1000, 700)

        # Use our custom smooth background frame
        self.central_widget = QFrame()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setObjectName("mainContainer")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 40, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)

        self.top_bar = QWidget()
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setContentsMargins(35, 10, 25, 10)
        self.top_bar.setObjectName("top_bar")
        self.top_bar.setFixedHeight(75)
        self.top_bar.setLayout(self.top_bar_layout)
        self.top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.top_bar_layout.setSpacing(20)

        # 1: Mode Toggle Button
        self.mode_button = QPushButton()
        self.mode_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_button.clicked.connect(toggle_theme_func)
        self.top_bar_layout.addWidget(self.mode_button)

        self.docs = QPushButton("Docs")
        self.docs.setFixedSize(150,50)
        self.top_bar_layout.addWidget(self.docs)
        self.docs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.github = QPushButton("GitHub")
        self.github.setFixedSize(150, 50)
        self.top_bar_layout.addWidget(self.github)
        self.github.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sign_in_btn = QPushButton("Sign in")
        self.sign_in_btn.setFixedSize(150, 50)
        self.sign_in_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sign_in_btn.clicked.connect(lambda _, p="create": navigate(p, signin = "true"))
        self.top_bar_layout.addWidget(self.sign_in_btn)

        self.main_layout.addWidget(self.top_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(125)

        self.easyssh = QLabel("Easy-SSH")
        self.main_layout.addWidget(self.easyssh, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(30)

        self.description = QLabel("Your one stop shop for AI model training.")
        self.main_layout.addWidget(self.description, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(45)

        self.get_started_btn = QPushButton("Get Started")
        self.get_started_btn.setFixedSize(250, 50)
        self.get_started_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.get_started_btn.clicked.connect(lambda _, p="create": navigate(p, signin = "false"))

        self.main_layout.addWidget(self.get_started_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addStretch(1)

        self.is_dark = False
        self.set_light_mode()

    def toggle_mode(self):
        if self.is_dark:
            self.set_light_mode()
        else:
            self.set_dark_mode()
        self.is_dark = not self.is_dark

    def set_light_mode(self):
        self.central_widget.setStyleSheet("""
        QFrame#mainContainer{
            background-color: qlineargradient(
                x1: 1, y1: 0, 
                x2: 0, y2: 1, 
                stop: 0 #A992FF, 
                stop: 0.70 #D6C7FE, 
                stop: 1 #DBCEFF
            );
            }
        """)

        # UI Elements
        self.top_bar.setStyleSheet("QWidget#top_bar { background-color: #F4E1FF; border-radius: 10px; }")
        self.mode_button.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; padding: 5px; }
            QPushButton:hover { background-color: rgba(0, 0, 0, 20); border-radius: 15px; }
        """)
        self.docs.setStyleSheet("""
                           QPushButton { background:transparent; font-size: 23px; font-weight: bold; border-radius: 15px; color:black; }
                           QPushButton:hover { background-color: rgba(0, 0, 0, 20); }
                           QPushButton:pressed {background-color: #D4C4FF; }
                       """)
        self.github.setStyleSheet("""
                           QPushButton { background:transparent; font-size: 23px; font-weight: bold; border-radius: 15px; color:black; }
                           QPushButton:hover { background-color: rgba(0, 0, 0, 20); }
                           QPushButton:pressed {background-color: #D4C4FF; }
                       """)

        self.sign_in_btn.setStyleSheet("""
            QPushButton { background-color: #D4C4FF; font-size: 23px; font-weight: bold; border-radius: 15px; color:black; }
            QPushButton:hover { background-color: #DACCFF; }
            QPushButton:pressed {background-color: #D4C4FF; }
        """)

        self.easyssh.setStyleSheet("font-size: 65px; color: #000000; font-weight: bold;")
        self.description.setStyleSheet("font-size: 35px; color: #000000; font-weight: bold;")
        self.get_started_btn.setStyleSheet("""
        QPushButton{background-color: black; color: white; font-size: 23px; border-radius: 25px; font-weight: 650px;}
        QPushButton:hover{background-color: #222}"""
        )

        path = resource_path("gui/icons/light mode.png")
        print("ICON PATH:", path)
        print("EXISTS:", Path(path).exists())
        self.mode_button.setIcon(QIcon(resource_path("gui/icons/light mode.png")))

        self.mode_button.setIconSize(QSize(40, 40))

    def set_dark_mode(self):
        # Update smooth gradient colors
        self.central_widget.setStyleSheet("""
            QFrame#mainContainer{
                background-color: #141318
            }
        """)

        self.top_bar.setStyleSheet("QWidget#top_bar { background-color: #2B2838; border-radius: 10px; }")
        self.mode_button.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; padding: 5px; }
            QPushButton:hover { background-color: #39354A; border-radius: 15px; }
            
        """)
        self.docs.setStyleSheet("""
                            QPushButton { 
                                background-color: #2B2838; 
                                border: none;
                                font-size: 23px; 
                                font-weight: bold; 
                                border-radius: 15px; 
                                color: white; 
                            }
                            QPushButton:hover { background-color: #39354A; }
                            QPushButton:pressed { background-color: #494266; }
                        """)

        self.github.setStyleSheet("""
                            QPushButton { 
                                background-color: #2B2838; 
                                border: none;
                                font-size: 23px; 
                                font-weight: bold; 
                                border-radius: 15px; 
                                color: white; 
                            }
                            QPushButton:hover { background-color: #39354A; }
                            QPushButton:pressed { background-color: #494266; }
                        """)

        self.sign_in_btn.setStyleSheet("""
            QPushButton { background-color: #3E375B; font-size: 23px; font-weight: bold; color: #FFFFFF; border-radius: 15px; }
            QPushButton:hover { background-color: #494266; }
            QPushButton:pressed { background-color: #3E375B; }
        """)

        self.easyssh.setStyleSheet("font-size: 65px; color: #C392FF; font-weight: bold;")
        self.description.setStyleSheet("font-size: 35px; color: #C392FF; font-weight: bold;")
        self.get_started_btn.setStyleSheet("""
            QPushButton{background-color: #D0C4FF; color: #141318; font-size: 23px; border-radius: 25px; font-weight: 650px;}
            QPushButton:hover{background-color: #B7A3FF}
        """)

        self.mode_button.setIcon(QIcon(resource_path("gui/icons/dark mode.png")))

        self.mode_button.setIconSize(QSize(40, 40))
