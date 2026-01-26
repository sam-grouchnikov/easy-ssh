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


class ConnectionSettingsWidget(QWidget):
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

        # Username Field
        self.user_container = QWidget()
        self.user_vbox = QVBoxLayout(self.user_container)
        self.server_user_lbl = QLabel("Server Username")
        self.server_user_lbl.setContentsMargins(2, 0, 0, 2)
        self.server_username_input = QLineEdit()
        self.server_username_input.setFixedSize(320, 40)
        self.user_vbox.addWidget(self.server_user_lbl)
        self.user_vbox.addWidget(self.server_username_input)

        # IP Field
        self.ip_container = QWidget()
        self.ip_vbox = QVBoxLayout(self.ip_container)
        self.server_ip_lbl = QLabel("Server IP")
        self.server_ip_lbl.setContentsMargins(2, 0, 0, 2)
        self.server_ip_input = QLineEdit()
        self.server_ip_input.setFixedSize(320, 40)
        self.ip_vbox.addWidget(self.server_ip_lbl)
        self.ip_vbox.addWidget(self.server_ip_input)

        self.row1_layout.addWidget(self.user_container)
        self.row1_layout.addWidget(self.ip_container)
        self.main_layout.addWidget(self.row1_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- 3. ROW 2: Password & Port ---
        self.row2_widget = QWidget()
        self.row2_layout = QHBoxLayout(self.row2_widget)

        # Password Field
        self.pass_container = QWidget()
        self.pass_vbox = QVBoxLayout(self.pass_container)
        self.server_psw_label = QLabel("Password")
        self.server_psw_label.setContentsMargins(2, 0, 0, 2)
        self.password_input = QLineEdit()
        self.password_input.setFixedSize(400, 40)
        self.pass_vbox.addWidget(self.server_psw_label)
        self.pass_vbox.addWidget(self.password_input)

        # Port Field
        self.port_container = QWidget()
        self.port_vbox = QVBoxLayout(self.port_container)
        self.server_port_label = QLabel("Port")
        self.server_port_label.setContentsMargins(2, 0, 0, 2)
        self.port_input = QLineEdit()
        self.port_input.setFixedSize(240, 40)
        self.port_vbox.addWidget(self.server_port_label)
        self.port_vbox.addWidget(self.port_input)

        self.row2_layout.addWidget(self.pass_container)
        self.row2_layout.addWidget(self.port_container)
        self.main_layout.addWidget(self.row2_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- 4. ROW 3: Buttons ---
        self.row3_widget = QWidget()
        self.row3_widget.setFixedWidth(695)
        self.row3_layout = QHBoxLayout(self.row3_widget)
        self.row3_layout.setContentsMargins(17, 10, 15, 10)

        self.back_btn = QPushButton("Back")
        self.back_btn.setFixedSize(140, 40)


        # Shadow Back
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(15)
        shadow1.setOffset(0, 2)
        shadow1.setColor(QColor(0, 0, 0, 80))
        self.back_btn.setGraphicsEffect(shadow1)

        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setFixedSize(225, 40)

        # Shadow Continue
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(15)
        shadow2.setOffset(0, 2)
        shadow2.setColor(QColor(0, 0, 0, 80))
        self.continue_btn.setGraphicsEffect(shadow2)

        self.back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.continue_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.row3_layout.addWidget(self.back_btn)
        self.row3_layout.addStretch(1)

        self.row3_layout.addWidget(self.continue_btn)

        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(self.row3_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(1)


    def set_light_mode(self):
        self.status_dot_pi.setStyleSheet("background-color: #EAEAEA; border: 1px solid black; border-radius: 8px;")
        self.pi_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.line1.setStyleSheet("background-color: black")
        self.status_dot_cs.setStyleSheet("background-color: #A459FF; border: 1px solid black; border-radius: 8px;")
        self.cs_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.line2.setStyleSheet("background-color: black")
        self.status_dot_int.setStyleSheet("background-color: #EAEAEA; border: 1px solid black; border-radius: 8px;")
        self.int_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.server_user_lbl.setStyleSheet("color: black; font-weight: bold; font-size: 19px;")
        self.server_username_input.setStyleSheet("background-color: #F7F2FA; border: 1px solid black; border-radius: 10px; padding-left: 10px; color: black; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.server_ip_lbl.setStyleSheet("color: black; font-weight: bold; font-size: 19px;")
        self.server_ip_input.setStyleSheet("background-color: #F7F2FA; border: 1px solid black; border-radius: 10px; padding-left: 10px; color: black; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.server_psw_label.setStyleSheet("color: black; font-weight: bold; font-size: 19px;")
        self.password_input.setStyleSheet("background-color: #F7F2FA; border: 1px solid black; border-radius: 10px; padding-left: 10px; color: black; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.server_port_label.setStyleSheet("color: black; font-weight: bold; font-size: 19px;")
        self.port_input.setStyleSheet("background-color: #F7F2FA; border: 1px solid black; border-radius: 10px; padding-left: 10px; color: black; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.back_btn.setStyleSheet(
            "QPushButton{ background-color: #D9CBFF; color: black; font-weight: bold; font-size: 19px; border-radius: 13px;}"
            "QPushButton:hover{background-color: #D3C3FF;}"
            "QPushButton:pressed{background-color: #D9CBFF}")
        self.continue_btn.setStyleSheet("QPushButton{ background-color: black; color: white; border-radius: 13px; font-weight: bold; font-size: 19px; }")

    def set_dark_mode(self):
        self.status_dot_pi.setStyleSheet("background-color: #222126; border: 1px solid #888; border-radius: 8px;")
        self.pi_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.line1.setStyleSheet("background-color: #FFFFFF")
        self.status_dot_cs.setStyleSheet("background-color: #9250E4; border: 1px solid #888; border-radius: 8px;")
        self.cs_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.line2.setStyleSheet("background-color: #FFFFFF")
        self.status_dot_int.setStyleSheet("background-color: #222126; border: 1px solid #888; border-radius: 8px;")
        self.int_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.server_user_lbl.setStyleSheet("color: #D0C4FF; font-weight: bold; font-size: 19px;")
        self.server_username_input.setStyleSheet("background-color: #222126; border: 1px solid #5B5B5B; border-radius: 10px; padding-left: 10px; color: white; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.server_ip_lbl.setStyleSheet("color: #D0C4FF; font-weight: bold; font-size: 19px;")
        self.server_ip_input.setStyleSheet("background-color: #222126; border: 1px solid #5B5B5B; border-radius: 10px; padding-left: 10px; color: white; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.server_psw_label.setStyleSheet("color: #D0C4FF; font-weight: bold; font-size: 19px;")
        self.password_input.setStyleSheet("background-color: #222126; border: 1px solid #5B5B5B; border-radius: 10px; padding-left: 10px; color: white; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.server_port_label.setStyleSheet("color: #D0C4FF; font-weight: bold; font-size: 19px;")
        self.port_input.setStyleSheet("background-color: #222126; border: 1px solid #5B5B5B; border-radius: 10px; padding-left: 10px; color: white; font-weight: bold; font-size: 18px; font-weight: 450px;")
        self.back_btn.setStyleSheet(
            "QPushButton{ background-color: #2B2838; color: white; font-weight: bold; font-size: 19px; border-radius: 13px;}"
            "QPushButton:hover{background-color: #363344;}"
            "QPushButton:pressed{background-color: #2B2838}")
        self.continue_btn.setStyleSheet("QPushButton{ background-color: #CDBAFF; color: black; border-radius: 13px; font-weight: bold; font-size: 19px; }"
                                        "QPushButton:hover{background-color: #BCA3FF}"
                                        "QPushButton:pressed{background-color: #CDBAFF}")
