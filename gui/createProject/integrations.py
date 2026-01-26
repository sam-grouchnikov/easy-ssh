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


class IntegrationsWidget(QWidget):
    def __init__(self, create, parent=None):
        super().__init__(parent)

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)

        # --- 1. PROGRESS BAR SECTION ---
        self.progress_bar = QWidget()
        self.progress_layout = QHBoxLayout(self.progress_bar)

        self.status_dot_pi = QLabel()
        self.status_dot_pi.setFixedSize(16, 16)
        self.pi_label = QLabel("Profile Information")
        self.line1 = QFrame()
        self.line1.setFixedSize(120, 2)
        self.status_dot_cs = QLabel()
        self.status_dot_cs.setFixedSize(16, 16)
        self.cs_label = QLabel("Connection Settings")
        self.line2 = QFrame()
        self.line2.setFixedSize(120, 2)
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
        self.main_layout.addSpacing(25)

        # --- GITHUB SECTION ---
        self.github_container = QWidget()
        self.github_container.setFixedSize(665, 35)
        self.github_vbox = QVBoxLayout(self.github_container)
        self.github_vbox.setContentsMargins(0, 0, 0, 0)
        self.github_label = QLabel("GitHub")
        self.github_vbox.addWidget(self.github_label, alignment=Qt.AlignmentFlag.AlignBottom)
        self.main_layout.addWidget(self.github_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # GitHub Rows
        self.row1_widget = QWidget()
        self.row1_layout = QHBoxLayout(self.row1_widget)
        self.row1_layout.setSpacing(25)

        self.repo_url_input = QLineEdit()
        self.repo_url_input.setFixedSize(665, 40)
        self.repo_url_lbl = QLabel("Repository URL")
        v1 = QVBoxLayout()
        v1.setSpacing(5)
        v1.addWidget(self.repo_url_lbl)
        v1.addWidget(self.repo_url_input)

        self.row1_layout.addLayout(v1)
        self.main_layout.addWidget(self.row1_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        self.pat_input = QLineEdit()
        self.pat_input.setFixedSize(665, 35)
        self.pat_lbl = QLabel("Personal Access Token")
        self.row2_widget = QWidget()
        v3 = QVBoxLayout(self.row2_widget)
        v3.addWidget(self.pat_lbl)
        v3.addWidget(self.pat_input)

        self.main_layout.addWidget(self.row2_widget, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- WEIGHTS & BIASES SECTION ---
        self.wandb_container = QWidget()
        self.wandb_container.setFixedSize(665, 40)
        self.wandb_vbox = QVBoxLayout(self.wandb_container)
        self.wandb_vbox.setContentsMargins(0, 0, 0, 0)
        self.wandb_label = QLabel("Weights & Biases")
        self.wandb_vbox.addWidget(self.wandb_label)

        self.main_layout.addSpacing(15)
        self.main_layout.addWidget(self.wandb_container, alignment=Qt.AlignmentFlag.AlignCenter)

        # W&B Row 1 (Username & Project Name)
        self.wandb_row1 = QWidget()

        self.wandb_row1_layout = QHBoxLayout(self.wandb_row1)
        self.wandb_row1_layout.setSpacing(25)
        self.wandb_user_input = QLineEdit()
        self.wandb_user_input.setFixedSize(320, 40)
        self.wandb_user_lbl = QLabel("W&B Username")

        wv1 = QVBoxLayout()
        wv1.addWidget(self.wandb_user_lbl)
        wv1.addWidget(self.wandb_user_input)
        wv1.setSpacing(5)


        self.wandb_project_input = QLineEdit()
        self.wandb_project_input.setFixedSize(320, 40)
        self.wandb_project_lbl = QLabel("Project Name")
        wv2 = QVBoxLayout()
        wv2.addWidget(self.wandb_project_lbl)
        wv2.addWidget(self.wandb_project_input)
        wv2.setSpacing(5)

        self.wandb_row1_layout.addLayout(wv1)

        self.wandb_row1_layout.addLayout(wv2)
        self.main_layout.addWidget(self.wandb_row1, alignment=Qt.AlignmentFlag.AlignCenter)

        # W&B Row 2 (API Key)
        self.wandb_api_input = QLineEdit()
        self.wandb_api_input.setFixedSize(665, 40)
        self.wandb_api_lbl = QLabel("API Key")
        self.wandb_row2 = QWidget()
        wv3 = QVBoxLayout(self.wandb_row2)
        wv3.addWidget(self.wandb_api_lbl)
        wv3.addWidget(self.wandb_api_input)
        self.main_layout.addWidget(self.wandb_row2, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- BUTTONS ---
        self.row3_widget = QWidget()
        self.row3_widget.setFixedWidth(695)
        self.row3_layout = QHBoxLayout(self.row3_widget)
        self.back_btn = QPushButton("Back")
        self.back_btn.setFixedSize(140, 40)
        self.back_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.continue_btn = QPushButton("Continue")
        self.continue_btn.setFixedSize(225, 40)
        self.continue_btn.clicked.connect(create)
        self.continue_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.row3_layout.addWidget(self.back_btn)
        self.row3_layout.addStretch(1)
        self.row3_layout.addWidget(self.continue_btn)
        self.main_layout.addSpacing(20)
        self.main_layout.addWidget(self.row3_widget, alignment=Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addStretch(1)

    def set_light_mode(self):
        # Header Labels
        style_header = "color: black; font-weight: bold; font-size: 23px;"
        self.github_label.setStyleSheet(style_header)
        self.wandb_label.setStyleSheet(style_header)

        # Field Labels
        style_lbl = "color: black; font-weight: bold; font-size: 19px;"
        for lbl in [self.repo_url_lbl, self.pat_lbl, self.wandb_user_lbl, self.wandb_project_lbl,
                    self.wandb_api_lbl]:
            lbl.setStyleSheet(style_lbl)

        # Inputs
        style_input = "background-color: #F7F2FA; border: 1px solid black; border-radius: 10px; padding-left: 10px; color: black; font-size: 18px;"
        for inp in [self.repo_url_input, self.pat_input, self.wandb_user_input, self.wandb_project_input,
                    self.wandb_api_input]:
            inp.setStyleSheet(style_input)

        self.status_dot_pi.setStyleSheet("background-color: #EAEAEA; border: 1px solid black; border-radius: 8px;")
        self.pi_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.line1.setStyleSheet("background-color: black")
        self.status_dot_cs.setStyleSheet("background-color: #EAEAEA; border: 1px solid black; border-radius: 8px;")
        self.cs_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.line2.setStyleSheet("background-color: black")
        self.status_dot_int.setStyleSheet("background-color: #A459FF; border: 1px solid black; border-radius: 8px;")
        self.int_label.setStyleSheet("color: black; font-weight: bold; font-size:16.5px;")
        self.continue_btn.setStyleSheet(
            "background-color: black; color: white; border-radius: 13px; font-weight: bold; font-size: 19px;")
        self.back_btn.setStyleSheet(
            "QPushButton{ background-color: #D9CBFF; color: black; font-weight: bold; font-size: 19px; border-radius: 13px;}"
            "QPushButton:hover{background-color: #D3C3FF;}"
            "QPushButton:pressed{background-color: #D9CBFF}")

    def set_dark_mode(self):
        # Header Labels
        style_header = "color: #FFFFFF; font-weight: bold; font-size: 23px;"
        self.github_label.setStyleSheet(style_header)
        self.wandb_label.setStyleSheet(style_header)

        # Field Labels
        style_lbl = "color: #D0C4FF; font-weight: bold; font-size: 19px;"
        for lbl in [self.repo_url_lbl, self.pat_lbl, self.wandb_user_lbl, self.wandb_project_lbl,
                    self.wandb_api_lbl]:
            lbl.setStyleSheet(style_lbl)

        # Inputs
        style_input = "background-color: #222126; border: 1px solid #5B5B5B; border-radius: 10px; padding-left: 10px; color: white; font-size: 18px;"
        for inp in [self.repo_url_input, self.pat_input, self.wandb_user_input, self.wandb_project_input,
                    self.wandb_api_input]:
            inp.setStyleSheet(style_input)

        self.status_dot_pi.setStyleSheet("background-color: #222126; border: 1px solid #888; border-radius: 8px;")
        self.pi_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.line1.setStyleSheet("background-color: #FFFFFF")
        self.status_dot_cs.setStyleSheet("background-color: #222126; border: 1px solid #888; border-radius: 8px;")
        self.cs_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.line2.setStyleSheet("background-color: #FFFFFF")
        self.status_dot_int.setStyleSheet("background-color: #9250E4; border: 1px solid #888; border-radius: 8px;")
        self.int_label.setStyleSheet("color: #FFFFFF; font-weight: bold; font-size:16.5px;")
        self.continue_btn.setStyleSheet(
            "background-color: #CDBAFF; color: black; border-radius: 13px; font-weight: bold; font-size: 19px;")
        self.back_btn.setStyleSheet(
            "QPushButton{ background-color: #2B2838; color: white; font-weight: bold; font-size: 19px; border-radius: 13px;}"
            "QPushButton:hover{background-color: #363344;}"
            "QPushButton:pressed{background-color: #2B2838}")