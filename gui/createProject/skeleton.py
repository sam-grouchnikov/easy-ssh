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
from .profileInfo import ProfileInfoWidget
from .connSettings import ConnectionSettingsWidget
from.integrations import IntegrationsWidget


class CreateSkeleton(QMainWindow):
    def __init__(self, navigate, toggle_theme_func, config):
        super().__init__()
        self.setWindowTitle("Homepage")
        self.resize(1000, 700)
        self.config = config

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
        self.docs.setFixedSize(150, 50)
        self.top_bar_layout.addWidget(self.docs)
        self.docs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.github = QPushButton("GitHub")
        self.github.setFixedSize(150, 50)
        self.top_bar_layout.addWidget(self.github)
        self.github.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.home_btn = QPushButton("Home")
        self.home_btn.setFixedSize(150, 50)
        self.home_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self.top_bar_layout.addWidget(self.home_btn)

        self.main_layout.addWidget(self.top_bar, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stack = QStackedWidget()
        self.profile_info_widget = ProfileInfoWidget(mode=0)
        self.conn_settings_widget = ConnectionSettingsWidget(mode=0)
        self.integrations_widget = IntegrationsWidget(self.create_account)
        self.stack.addWidget(self.profile_info_widget)
        self.stack.addWidget(self.conn_settings_widget)
        self.stack.addWidget(self.integrations_widget)
        self.profile_info_widget.continue_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.conn_settings_widget.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.conn_settings_widget.continue_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.integrations_widget.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        self.home_btn.clicked.connect(lambda: (self.stack.setCurrentIndex(0), navigate("home")))
        self.main_layout.addWidget(self.stack, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addStretch(1)

        self.is_dark = False
        self.set_light_mode()
        self.navigate = navigate

    def create_account(self):
        self.profile_user = self.profile_info_widget.first_input.text()
        self.profile_psw = self.profile_info_widget.psw_input.text()
        self.profile_email = self.profile_info_widget.email_input.text()

        self.server_user = self.conn_settings_widget.server_username_input.text()
        self.server_psw = self.conn_settings_widget.password_input.text()
        self.server_ip = self.conn_settings_widget.server_ip_input.text()
        self.server_port = self.conn_settings_widget.port_input.text()

        self.git_url = self.integrations_widget.repo_url_input.text()
        self.git_pat = self.integrations_widget.pat_input.text()

        self.wandb_user = self.integrations_widget.wandb_user_input.text()
        self.wandb_proj = self.integrations_widget.wandb_project_input.text()
        self.wandb_api = self.integrations_widget.wandb_api_input.text()

        self.config.set("user", self.profile_user)
        self.config.set("psw", self.profile_psw)
        self.config.set("email", self.profile_email)
        self.config.set("ssh_user", self.server_user)
        self.config.set("ssh_psw", self.server_psw)
        self.config.set("ssh_ip", self.server_ip)
        self.config.set("ssh_port", self.server_port)
        self.config.set("git_url", self.git_url)
        self.config.set("git_pat", self.git_pat)
        self.config.set("wandb_user", self.wandb_user)
        self.config.set("wandb_proj", self.wandb_proj)
        self.config.set("wandb_api", self.wandb_api)

        self.navigate("project")



    def set_light_mode(self):
        self.profile_info_widget.set_light_mode()
        self.conn_settings_widget.set_light_mode()
        self.integrations_widget.set_light_mode()
        self.central_widget.setStyleSheet("""
        QFrame#mainContainer{
            background-color: qlineargradient(
                x1: 1, y1: 0, 
                x2: 0, y2: 1, 
                stop: 0 #FDF7FF, 
                stop: 0.5 #F8EBFF
                stop: 1 #F3DEFF
            );
            }
        """)

        # UI Elements
        self.top_bar.setStyleSheet("QWidget#top_bar { background-color: #E2D8FF; border-radius: 10px; }")
        self.mode_button.setStyleSheet("""
            QPushButton { background-color: transparent; border: none; padding: 5px; }
            QPushButton:hover { background-color: #D2C2FF; border-radius: 15px; }
        """)
        self.docs.setStyleSheet("font-size: 23px; color: #000000; font-weight: bold;")
        self.github.setStyleSheet("font-size: 23px; color: #000000; font-weight: bold;")

        self.home_btn.setStyleSheet("""
            QPushButton { background-color: #CDBAFF; font-size: 23px; font-weight: bold; border-radius: 15px; color:black; }
            QPushButton:hover { background-color: #D2C2FF; }
            QPushButton:pressed {background-color: #D4C4FF; }
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



        # Update Icon to "Light Mode" icon
        icon_path = "C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\light mode.png"
        self.mode_button.setIcon(QIcon(icon_path))
        self.mode_button.setIconSize(QSize(40, 40))

    def set_dark_mode(self):
        self.profile_info_widget.set_dark_mode()
        self.conn_settings_widget.set_dark_mode()
        self.integrations_widget.set_dark_mode()
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

        self.home_btn.setStyleSheet("""
                    QPushButton { background-color: #3E375B; font-size: 23px; font-weight: bold; color: #FFFFFF; border-radius: 15px; }
                    QPushButton:hover { background-color: #494266; }
                    QPushButton:pressed { background-color: #3E375B; }
                """)

        icon_path = "C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\dark mode.png"
        self.mode_button.setIcon(QIcon(icon_path))
        self.mode_button.setIconSize(QSize(40, 40))
