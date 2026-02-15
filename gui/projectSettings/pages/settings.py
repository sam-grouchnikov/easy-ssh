#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.2.1
Email: sam.grouchnikov@gmail.com
Status: Development
"""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCursor, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QGridLayout, QMessageBox, QFrame, QSizePolicy, QScrollArea, QGraphicsDropShadowEffect
)


class SettingsPage(QWidget):
    def __init__(self, config, reload, fb):
        super().__init__()
        self.inputs = {}
        self.config = config
        self.doc_path = None
        self.fb = fb
        self.reload = reload

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(85,30,90,25)
        self.setLayout(self.layout)
        self.row1 = QWidget()
        self.row1_layout = QHBoxLayout(self.row1)
        self.row1_layout.setContentsMargins(20, 0, 42, 0)
        self.page_title = QLabel("Manage your account settings and integrations")
        self.row1_layout.addWidget(self.page_title, alignment=Qt.AlignmentFlag.AlignVCenter)


        self.save_btn = QPushButton("Save Changes")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.save_btn.setGraphicsEffect(shadow)
        self.save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.save_btn.clicked.connect(self.save_changes)

        self.row1_layout.addStretch()
        self.row1_layout.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.layout.addWidget(self.row1)
        self.layout.addSpacing(15)
        self.line1 = Line(2)
        self.layout.addWidget(self.line1)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)


        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)


        self.connection_row = ConnectionRowWidget()
        self.connection_row.setContentsMargins(10, 0, 0, 0)
        self.scroll_layout.addWidget(self.connection_row)

        self.line3 = Line(2)
        self.scroll_layout.addWidget(self.line3)

        self.integrations_row = IntegrationsRowWidget()
        self.integrations_row.setContentsMargins(10,0,0,0)
        self.scroll_layout.addWidget(self.integrations_row)

        self.scroll_area.setWidget(self.scroll_content)

        self.layout.addWidget(self.scroll_area)

    def update_config(self, new, path):
        self.config = new
        self.doc_path = path

    def load_parts(self, config):
        # self.profile_row.password_input.input.setText("placeholder")
        # self.profile_row.email_input.input.setText(str(config.get("email")))

        self.connection_row.username.input.setText(str(config.get("ssh_user")))
        self.connection_row.ip.input.setText(str(config.get("ssh_ip")))
        self.connection_row.password.input.setText(str(config.get("ssh_psw")))
        self.connection_row.port.input.setText(str(config.get("ssh_port")))

        self.integrations_row.gitblock.git_url.input.setText(str(config.get("git_url")))
        self.integrations_row.gitblock.git_pat.input.setText(str(config.get("git_pat")))
        self.integrations_row.wandbblock.username.input.setText(str(config.get("wandb_user")))
        self.integrations_row.wandbblock.proj.input.setText(str(config.get("wandb_proj")))
        self.integrations_row.wandbblock.api_key.input.setText(str(config.get("wandb_api")))

    def save_changes(self):
        original_text = self.save_btn.text()

        self.save_btn.setText("Saved ✓")
        self.save_btn.setEnabled(False)
        self.config["ssh_user"] = self.connection_row.username.input.text()
        self.config["ssh_ip"] = self.connection_row.ip.input.text()
        self.config["ssh_port"] = self.connection_row.port.input.text()
        self.config["ssh_psw"] = self.connection_row.password.input.text()
        self.config["git_url"] = self.integrations_row.gitblock.git_url.input.text()
        self.config["git_pat"] = self.integrations_row.gitblock.git_pat.input.text()
        self.config["wandb_user"] = self.integrations_row.wandbblock.username.input.text()
        self.config["wandb_proj"] = self.integrations_row.wandbblock.proj.input.text()
        self.config["wandb_api"] = self.integrations_row.wandbblock.api_key.input.text()
        print(self.config)
        self.fb.set_doc(self.doc_path, self.config)

        QTimer.singleShot(1800, lambda: self.revert_save_button(original_text))
        self.reload()

    def revert_save_button(self, original_text):
        self.save_btn.setText(original_text)
        self.save_btn.setEnabled(True)


    def set_light_mode(self):
        self.line1.set_light_mode()
        # self.profile_row.set_light_mode()
        # self.line2.set_light_mode()
        self.connection_row.set_light_mode()
        self.line3.set_light_mode()
        self.integrations_row.set_light_mode()
        self.page_title.setStyleSheet("font-weight: 510; font-size: 21px; color: #343434")
        self.save_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #e9ddff;
                        border-radius: 19px;
                        color: #4e3d75;
                        font-size: 17px;
                        font-weight: normal;
                        padding: 8px 25px;
                    }
                    QPushButton:hover {
                        background-color: #DDCAFF;
                    }
                    QPushButton:pressed {
                        background-color: #e9ddff;
                    }
                """)


        self.scroll_area.setStyleSheet("""
                            QScrollArea{ 
                                border: none; background-color: transparent; 
                            }
                            QScrollBar {
                                            border: none;
                                            background: #E9E9E9;
                                            width: 13px;
                                            margin: 0px 0px 0px 0px;
                                        }

                            QScrollBar::handle {
                                            background: #D7D7D7;
                                            min-height: 20px;
                                            border-radius: 5px;
                                            margin: 2px;
                                        }

                            QScrollBar::handle:hover {
                                            background: #CBCBCB;
                                        }

                            QScrollBar::add-line, QScrollBar::sub-line {
                                            height: 0px;
                                        }

                            QScrollBar::add-page, QScrollBar::sub-page {
                                     background: none;
                            }
                """)
    def set_dark_mode(self):
        self.line1.set_dark_mode()
        # self.profile_row.set_dark_mode()
        # self.line2.set_dark_mode()
        self.connection_row.set_dark_mode()
        self.line3.set_dark_mode()
        self.integrations_row.set_dark_mode()
        self.page_title.setStyleSheet("font-weight: 510; font-size: 21px; color: #B1B1B1")
        self.save_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #4E3D75;
                                border-radius: 19px;
                                color: #E9DDFF;
                                font-size: 17px;
                                font-weight: normal;
                                padding: 8px 25px;
                            }
                            QPushButton:hover {
                                background-color: #5A4786;
                            }
                            QPushButton:pressed {
                                background-color: #4E3D75;
                            }
                        """)

        self.scroll_area.setStyleSheet("""
                                    QScrollArea{ 
                                        border: none; background-color: transparent; 
                                    }
                                    QScrollBar {
                                                    border: none;
                                                    background: #312D39;
                                                    width: 13px;
                                                    margin: 0px 0px 0px 0px;
                                                }

                                    QScrollBar::handle {
                                                    background: #211E29;
                                                    min-height: 20px;
                                                    border-radius: 5px;
                                                    margin: 2px;
                                                }

                                    QScrollBar::handle:hover {
                                                    background: #1A1723;
                                                }

                                    QScrollBar::add-line, QScrollBar::sub-line {
                                                    height: 0px;
                                                }

                                    QScrollBar::add-page, QScrollBar::sub-page {
                                             background: none;
                                    }
                        """)




class Line(QWidget):
    def __init__(self, height):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.line = QFrame()
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFixedHeight(height)
        self.line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.layout.addWidget(self.line)

    def set_light_mode(self):
        self.line.setStyleSheet("background-color: #D1D1D1; border: none;")

    def set_dark_mode(self):
        self.line.setStyleSheet("background-color: #4F4756; border: none;")





class FormItem(QWidget):
    def __init__(self, label, width):
        super().__init__()
        self.layout=QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(label)
        self.layout.addWidget(self.label)

        self.layout.addSpacing(2)

        self.input = QLineEdit()
        self.input.setFixedSize(width, 37)
        self.layout.addWidget(self.input)

        if label in ["Password", "Personal Access Token", "API Key"]:
            self.input.setEchoMode(QLineEdit.EchoMode.Password)

    def set_light_mode(self):
        self.label.setStyleSheet("color: #434343; font-size: 18px; font-weight: 520; padding-left: 1px;")
        self.input.setStyleSheet("padding-left: 8px; border: 1px solid #A381B1; border-radius: 10px;"
                                 "color: black; font-weight: 500; font-size: 16px;")

    def set_dark_mode(self):
        self.label.setStyleSheet("color: #A590CB; font-size: 18px; font-weight: 520; padding-left: 1px;")
        self.input.setStyleSheet("padding-left: 8px; border: 1px solid #5d5d5d; border-radius: 10px;"
                                 "color: #C4C4C4; font-weight: 500; font-size: 16px;")



class TwoRowLabel(QWidget):
    def __init__(self, l1, l2):
        super().__init__()
        main_layout = QVBoxLayout(self)

        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 18, 0, 0)

        self.l1 = QLabel(l1)
        main_layout.addWidget(self.l1)

        main_layout.addSpacing(2)

        self.l2 = QLabel(l2)
        main_layout.addWidget(self.l2)

    def set_light_mode(self):
        self.l1.setStyleSheet("color: #434343; font-size: 23px; font-weight: 520")
        self.l2.setStyleSheet("color: #656565; font-size: 17px; font-weight: 510")

    def set_dark_mode(self):
        self.l1.setStyleSheet("color: #C4C4C4; font-size: 23px; font-weight: 520")
        self.l2.setStyleSheet("color: #9D9D9D; font-size: 17px; font-weight: 510")



class ProfileRowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.label_side = TwoRowLabel("Profile", "Set your account details")
        self.label_side.setFixedWidth(300)
        self.layout.addWidget(self.label_side)
        self.layout.addStretch()

        self.inputs_vbox = QWidget()
        self.inputs_vbox_layout = QVBoxLayout(self.inputs_vbox)
        self.inputs_r1 = QHBoxLayout()
        self.inputs_r1.setSpacing(10)
        self.email_input = FormItem("Email", 600)
        self.inputs_r1.addWidget(self.email_input)
        self.inputs_vbox_layout.addLayout(self.inputs_r1)
        self.inputs_r2 = QHBoxLayout()
        self.password_input = FormItem("Password", 600)
        self.inputs_r2.addWidget(self.password_input)
        self.inputs_vbox_layout.addLayout(self.inputs_r2)

        self.layout.addWidget(self.inputs_vbox)

    def set_light_mode(self):
        self.label_side.set_light_mode()
        self.email_input.set_light_mode()
        self.password_input.set_light_mode()

    def set_dark_mode(self):
        self.label_side.set_dark_mode()
        self.email_input.set_dark_mode()
        self.password_input.set_dark_mode()

class ConnectionRowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.label_side = TwoRowLabel("Connection", "Configure SSH connection details")
        self.label_side.setFixedWidth(300)
        self.layout.addWidget(self.label_side)
        self.layout.addStretch()

        self.inputs_vbox = QWidget()
        self.inputs_vbox_layout = QVBoxLayout(self.inputs_vbox)
        self.inputs_r1 = QHBoxLayout()
        self.inputs_r1.setSpacing(10)
        self.username = FormItem("Server Username", 285)
        self.ip = FormItem("Server IP", 285)
        self.inputs_r1.addWidget(self.username)
        self.inputs_r1.addWidget(self.ip)
        self.inputs_vbox_layout.addLayout(self.inputs_r1)
        self.inputs_r2 = QHBoxLayout()
        self.inputs_r2.setSpacing(10)

        self.password = FormItem("Password", 365)
        self.port = FormItem("Port", 205)
        self.inputs_r2.addWidget(self.password)
        self.inputs_r2.addWidget(self.port)
        self.inputs_vbox_layout.addLayout(self.inputs_r2)

        self.layout.addWidget(self.inputs_vbox)

    def set_light_mode(self):
        self.label_side.set_light_mode()
        self.username.set_light_mode()
        self.ip.set_light_mode()
        self.password.set_light_mode()
        self.port.set_light_mode()

    def set_dark_mode(self):
        self.label_side.set_dark_mode()
        self.username.set_dark_mode()
        self.ip.set_dark_mode()
        self.password.set_dark_mode()
        self.port.set_dark_mode()

class IntegrationsRowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.label_side = TwoRowLabel("Integrations", "Set up repo and log integrations")
        self.label_side.setFixedWidth(300)
        self.layout.addWidget(self.label_side)
        self.layout.addStretch()

        self.gitblock = GitBlock()
        self.wandbblock = WandbBlock()

        self.part2 = QVBoxLayout()
        self.part2.addWidget(self.gitblock)
        self.part2.addWidget(self.wandbblock)
        self.layout.addLayout(self.part2)

    def set_light_mode(self):
        self.label_side.set_light_mode()
        self.gitblock.set_light_mode()
        self.wandbblock.set_light_mode()

    def set_dark_mode(self):
        self.label_side.set_dark_mode()
        self.gitblock.set_dark_mode()
        self.wandbblock.set_dark_mode()

class GitBlock(QWidget):
    def __init__(self):
        super().__init__()
        self.inputs_vbox_layout = QVBoxLayout(self)
        self.github_label = QLabel("GitHub")
        self.inputs_vbox_layout.addWidget(self.github_label)
        self.inputs_r1 = QHBoxLayout()
        self.inputs_r1.setSpacing(10)
        self.git_url = FormItem("Repository URL", 600)
        self.inputs_r1.addWidget(self.git_url)
        self.inputs_vbox_layout.addLayout(self.inputs_r1)
        self.inputs_r2 = QHBoxLayout()
        self.git_pat = FormItem("Personal Access Token", 600)
        self.inputs_r2.addWidget(self.git_pat)
        self.inputs_vbox_layout.addLayout(self.inputs_r2)

    def set_light_mode(self):
        self.github_label.setStyleSheet("color: #434343; font-size: 22px; font-weight: 520; padding-left: 2px;")
        self.git_url.set_light_mode()
        self.git_pat.set_light_mode()

    def set_dark_mode(self):
        self.github_label.setStyleSheet("color: #C4C4C4; font-size: 22px; font-weight: 520; padding-left: 2px;")
        self.git_url.set_dark_mode()
        self.git_pat.set_dark_mode()


class WandbBlock(QWidget):
    def __init__(self):
        super().__init__()
        self.inputs_vbox_layout = QVBoxLayout(self)
        self.github_label = QLabel("Weights & Biases")
        self.inputs_vbox_layout.addWidget(self.github_label)
        self.inputs_r1 = QHBoxLayout()
        self.inputs_r1.setSpacing(10)
        self.username = FormItem("W&B Username", 285)
        self.proj = FormItem("Project Name", 285)
        self.inputs_r1.addWidget(self.username)
        self.inputs_r1.addWidget(self.proj)
        self.inputs_vbox_layout.addLayout(self.inputs_r1)
        self.inputs_r2 = QHBoxLayout()
        self.api_key = FormItem("API Key", 600)
        self.inputs_r2.addWidget(self.api_key)
        self.inputs_vbox_layout.addLayout(self.inputs_r2)

    def set_light_mode(self):
        self.github_label.setStyleSheet("color: #434343; font-size: 22px; font-weight: 520; padding-left: 2px;")
        self.username.set_light_mode()
        self.proj.set_light_mode()
        self.api_key.set_light_mode()

    def set_dark_mode(self):
        self.github_label.setStyleSheet("color: #C4C4C4; font-size: 22px; font-weight: 520; padding-left: 2px;")
        self.username.set_dark_mode()
        self.proj.set_dark_mode()
        self.api_key.set_dark_mode()

