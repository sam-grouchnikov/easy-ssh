#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.1.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""

from pathlib import Path

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QCursor, QIcon
from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QApplication,
    QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)

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
        self.main_layout.setContentsMargins(0, 28, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)

        self.top_bar = QWidget()
        self.top_bar_layout = QHBoxLayout()
        self.top_bar_layout.setContentsMargins(20, 12, 20, 12)
        self.top_bar.setObjectName("top_bar")
        self.top_bar.setFixedHeight(82)
        self.top_bar.setFixedWidth(860)
        self.top_bar.setLayout(self.top_bar_layout)
        self.top_bar_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.top_bar_layout.setSpacing(20)

        # 1: Mode Toggle Button
        self.mode_button = QPushButton()
        self.mode_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mode_button.clicked.connect(toggle_theme_func)
        self.top_bar_layout.addWidget(self.mode_button)

        self.docs = QPushButton("Docs")
        self.docs.setFixedSize(150, 48)
        self.top_bar_layout.addWidget(self.docs)
        self.docs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.github = QPushButton("GitHub")
        self.github.setFixedSize(150, 48)
        self.top_bar_layout.addWidget(self.github)
        self.github.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.sign_in_btn = QPushButton("Sign in")
        self.sign_in_btn.setFixedSize(150, 48)
        self.sign_in_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.sign_in_btn.clicked.connect(lambda _, p="create": navigate(p, signin = "true"))
        self.top_bar_layout.addWidget(self.sign_in_btn)

        self.main_layout.addWidget(self.top_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(110)

        self.easyssh = QLabel("Easy-SSH")
        self.main_layout.addWidget(self.easyssh, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(24)

        self.description = QLabel("Your one stop shop for AI model training.")
        self.main_layout.addWidget(self.description, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(40)

        self.get_started_btn = QPushButton("Get Started")
        self.get_started_btn.setFixedSize(260, 52)
        self.get_started_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.get_started_btn.clicked.connect(lambda _, p="create": navigate(p, signin = "false"))

        self.main_layout.addWidget(self.get_started_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addStretch(1)

        self.is_dark = False
        self._icons_dir = Path(__file__).resolve().parents[1] / "icons"
        self.set_light_mode()

    def toggle_mode(self):
        if self.is_dark:
            self.set_light_mode()
        else:
            self.set_dark_mode()
        self.is_dark = not self.is_dark

    def set_light_mode(self):
        self.central_widget.setStyleSheet("""
        QFrame#mainContainer {
            background-color: qlineargradient(
                x1: 0, y1: 0,
                x2: 1, y2: 1,
                stop: 0 #F7F2FF,
                stop: 0.48 #EEE4FF,
                stop: 1 #E1D3FF
            );
        }
        """)

        # UI Elements
        self.top_bar.setStyleSheet("QWidget#top_bar { background-color: rgba(255, 255, 255, 0.56); border-radius: 16px; border: 1px solid rgba(120, 99, 176, 0.23); }")
        self.mode_button.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; padding: 5px; }
            QPushButton:hover { background-color: rgba(0, 0, 0, 20); border-radius: 15px; }
        """)
        self.docs.setStyleSheet("""
                           QPushButton { background:transparent; font-size: 19px; font-weight: 600; border-radius: 12px; color:#231B33; }
                           QPushButton:hover { background-color: rgba(49, 31, 80, 0.08); }
                           QPushButton:pressed {background-color: rgba(49, 31, 80, 0.16); }
                       """)
        self.github.setStyleSheet("""
                           QPushButton { background:transparent; font-size: 19px; font-weight: 600; border-radius: 12px; color:#231B33; }
                           QPushButton:hover { background-color: rgba(49, 31, 80, 0.08); }
                           QPushButton:pressed {background-color: rgba(49, 31, 80, 0.16); }
                       """)

        self.sign_in_btn.setStyleSheet("""
            QPushButton { background-color: #6F59B5; font-size: 18px; font-weight: 600; border-radius: 12px; color:white; border: none; }
            QPushButton:hover { background-color: #7D66C4; }
            QPushButton:pressed {background-color: #654EAA; }
        """)

        self.easyssh.setStyleSheet("font-size: 70px; color: #1B1230; font-weight: 700;")
        self.description.setStyleSheet("font-size: 30px; color: #312050; font-weight: 500;")
        self.get_started_btn.setStyleSheet("""
        QPushButton{background-color: #241242; color: white; font-size: 20px; border-radius: 26px; font-weight: 600; border: none;}
        QPushButton:hover{background-color: #301A53;}
        QPushButton:pressed{background-color: #21103C;}"""
        )



        # Update Icon to "Light Mode" icon
        icon_path = str(self._icons_dir / "light mode.png")
        self.mode_button.setIcon(QIcon(icon_path))
        self.mode_button.setIconSize(QSize(28, 28))

    def set_dark_mode(self):
        # Update smooth gradient colors
        self.central_widget.setStyleSheet("""
            QFrame#mainContainer{
                background-color: qlineargradient(
                    x1: 0, y1: 0,
                    x2: 1, y2: 1,
                    stop: 0 #121116,
                    stop: 0.6 #161422,
                    stop: 1 #1B1730
                )
            }
        """)

        self.top_bar.setStyleSheet("QWidget#top_bar { background-color: rgba(43, 40, 56, 0.92); border-radius: 16px; border: 1px solid #3E3953; }")
        self.mode_button.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; padding: 5px; }
            QPushButton:hover { background-color: #39354A; border-radius: 15px; }
            
        """)
        self.docs.setStyleSheet("""
                            QPushButton { 
                                background-color: #2B2838; 
                                border: none;
                                font-size: 19px; 
                                font-weight: 600; 
                                border-radius: 12px; 
                                color: white; 
                            }
                            QPushButton:hover { background-color: #39354A; }
                            QPushButton:pressed { background-color: #494266; }
                        """)

        self.github.setStyleSheet("""
                            QPushButton { 
                                background-color: #2B2838; 
                                border: none;
                                font-size: 19px; 
                                font-weight: 600; 
                                border-radius: 12px; 
                                color: white; 
                            }
                            QPushButton:hover { background-color: #39354A; }
                            QPushButton:pressed { background-color: #494266; }
                        """)

        self.sign_in_btn.setStyleSheet("""
            QPushButton { background-color: #8D7AE0; font-size: 18px; font-weight: 600; color: #161225; border-radius: 12px; border: none; }
            QPushButton:hover { background-color: #494266; }
            QPushButton:pressed { background-color: #7F6FD4; }
        """)

        self.easyssh.setStyleSheet("font-size: 70px; color: #D4C0FF; font-weight: 700;")
        self.description.setStyleSheet("font-size: 30px; color: #B7A8DC; font-weight: 500;")
        self.get_started_btn.setStyleSheet("""
            QPushButton{background-color: #D0C4FF; color: #141318; font-size: 20px; border-radius: 26px; font-weight: 600; border: none;}
            QPushButton:hover{background-color: #B7A3FF}
            QPushButton:pressed{background-color: #A58BFA}
        """)

        # Update Icon to "Dark Mode" icon
        icon_path = str(self._icons_dir / "dark mode.png")
        self.mode_button.setIcon(QIcon(icon_path))
        self.mode_button.setIconSize(QSize(28, 28))
