#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.1.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtWidgets import (
    QLabel, QHBoxLayout, QWidget, QFrame, QVBoxLayout,
    QLineEdit, QPushButton, QGraphicsDropShadowEffect, QSizePolicy
)


class ProfileInfoWidget(QWidget):
    def __init__(self, parent=None, mode=0):
        super().__init__(parent)


        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)

        # --- 1. PROGRESS BAR SECTION ---
        self.progress_bar = QWidget()
        self.progress_layout = QHBoxLayout(self.progress_bar)

        # Profile Information
        self.status_dot_pi = QLabel()
        self.status_dot_pi.setFixedSize(16, 16)
        self.pi_label = QLabel("Profile Information")

        # Line 1
        self.line1 = QFrame()
        self.line1.setFixedSize(120, 2)

        # Connection Settings
        self.status_dot_cs = QLabel()
        self.status_dot_cs.setFixedSize(16, 16)
        self.cs_label = QLabel("Connection Settings")

        # Line 2
        self.line2 = QFrame()
        self.line2.setFixedSize(120, 2)

        # Integrations
        self.status_dot_int = QLabel()
        self.status_dot_int.setFixedSize(16, 16)
        self.int_label = QLabel("Integrations")

        self.progress_layout.addWidget(self.status_dot_pi)
        self.progress_layout.addWidget(self.pi_label)
        self.progress_layout.addSpacing(5)
        self.progress_layout.addWidget(self.line1)
        self.progress_layout.addSpacing(5)
        self.progress_layout.addWidget(self.status_dot_cs)
        self.progress_layout.addWidget(self.cs_label)
        self.progress_layout.addSpacing(5)
        self.progress_layout.addWidget(self.line2)
        self.progress_layout.addSpacing(5)
        self.progress_layout.addWidget(self.status_dot_int)
        self.progress_layout.addWidget(self.int_label)

        self.main_layout.addSpacing(50)
        self.main_layout.addWidget(self.progress_bar, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addSpacing(10)

        # --- 2. ROW 1: Username & IP ---
        self.row1_widget = QWidget()
        self.row1_layout = QHBoxLayout(self.row1_widget)

        self.first_container = QWidget()
        self.first_vbox = QVBoxLayout(self.first_container)
        self.profile_user_label = QLabel("Username")
        self.profile_user_label.setContentsMargins(2, 0, 0, 2)
        self.first_input = QLineEdit()
        self.first_input.setFixedSize(320, 40)
        self.first_vbox.addWidget(self.profile_user_label)
        self.first_vbox.addWidget(self.first_input)

        self.psw_container = QWidget()
        self.psw_vbox = QVBoxLayout(self.psw_container)
        self.profile_psw_lbl = QLabel("Password")
        self.profile_psw_lbl.setContentsMargins(2, 0, 0, 2)
        self.psw_input = QLineEdit()
        self.psw_input.setFixedSize(320, 40)
        self.psw_vbox.addWidget(self.profile_psw_lbl)
        self.psw_vbox.addWidget(self.psw_input)

        self.row1_layout.addWidget(self.first_container)
        self.row1_layout.addWidget(self.psw_container)
        self.main_layout.addWidget(self.row1_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- 3. ROW 2: Password & Port ---
        self.row2_widget = QWidget()
        self.row2_layout = QHBoxLayout(self.row2_widget)

        self.email_container = QWidget()
        self.email_vbox = QVBoxLayout(self.email_container)
        self.profile_email_lbl = QLabel("Email")
        self.profile_email_lbl.setContentsMargins(2, 0, 0, 2)
        self.email_input = QLineEdit()
        self.email_input.setFixedSize(665, 40)
        self.email_vbox.addWidget(self.profile_email_lbl)
        self.email_vbox.addWidget(self.email_input)



        self.row2_layout.addWidget(self.email_container)
        self.main_layout.addWidget(self.row2_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- 4. ROW 3: Buttons ---
        self.row3_widget = QWidget()
        self.row3_widget.setFixedWidth(695)
        self.row3_layout = QHBoxLayout(self.row3_widget)
        self.row3_layout.setContentsMargins(17, 10, 15, 10)



        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setFixedSize(225, 40)

        # Shadow Continue
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(15)
        shadow2.setOffset(0, 2)
        shadow2.setColor(QColor(0, 0, 0, 80))
        self.continue_btn.setGraphicsEffect(shadow2)

        self.continue_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.row3_layout.addStretch(1)

        self.row3_layout.addWidget(self.continue_btn)

        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(self.row3_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(1)


    def set_light_mode(self):
        self.status_dot_pi.setStyleSheet("background-color: #A459FF; border: 1px solid black; border-radius: 8px;")
        self.pi_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.line1.setStyleSheet("background-color: black")
        self.status_dot_cs.setStyleSheet("background-color: #EAEAEA; border: 1px solid black; border-radius: 8px;")
        self.cs_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.line2.setStyleSheet("background-color: black")
        self.status_dot_int.setStyleSheet("background-color: #EAEAEA; border: 1px solid black; border-radius: 8px;")
        self.int_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.profile_user_label.setStyleSheet("color: black; font-weight: bold; font-size: 19px;")
        self.first_input.setStyleSheet("background-color: #F7F2FA; border: 1px solid black; border-radius: 10px; padding-left: 10px; color: black; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.profile_psw_lbl.setStyleSheet("color: black; font-weight: bold; font-size: 19px;")
        self.psw_input.setStyleSheet("background-color: #F7F2FA; border: 1px solid black; border-radius: 10px; padding-left: 10px; color: black; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.profile_email_lbl.setStyleSheet("color: black; font-weight: bold; font-size: 19px;")
        self.email_input.setStyleSheet("background-color: #F7F2FA; border: 1px solid black; border-radius: 10px; padding-left: 10px; color: black; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.continue_btn.setStyleSheet("QPushButton{ background-color: black; color: white; border-radius: 13px; font-weight: bold; font-size: 19px; }")

    def set_dark_mode(self):
        self.status_dot_pi.setStyleSheet("background-color: #9250E4; border: 1px solid #888; border-radius: 8px;")
        self.pi_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.line1.setStyleSheet("background-color: #FFFFFF")
        self.status_dot_cs.setStyleSheet("background-color: #222126; border: 1px solid #888; border-radius: 8px;")
        self.cs_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.line2.setStyleSheet("background-color: #FFFFFF")
        self.status_dot_int.setStyleSheet("background-color: #222126; border: 1px solid #888; border-radius: 8px;")
        self.int_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.profile_user_label.setStyleSheet("color: #D0C4FF; font-weight: bold; font-size: 19px;")
        self.first_input.setStyleSheet("background-color: #222126; border: 1px solid #5B5B5B; border-radius: 10px; padding-left: 10px; color: white; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.profile_psw_lbl.setStyleSheet("color: #D0C4FF; font-weight: bold; font-size: 19px;")
        self.psw_input.setStyleSheet("background-color: #222126; border: 1px solid #5B5B5B; border-radius: 10px; padding-left: 10px; color: white; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.profile_email_lbl.setStyleSheet("color: #D0C4FF; font-weight: bold; font-size: 19px;")
        self.email_input.setStyleSheet("background-color: #222126; border: 1px solid #5B5B5B; border-radius: 10px; padding-left: 10px; color: white; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.continue_btn.setStyleSheet("QPushButton{ background-color: #CDBAFF; color: black; border-radius: 13px; font-weight: bold; font-size: 19px; }"
                                        "QPushButton:hover{background-color: #BCA3FF}"
                                        "QPushButton:pressed{background-color: #CDBAFF}")
