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
from PyQt6.QtGui import QColor, QCursor, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QLabel, QHBoxLayout, QWidget, QFrame, QVBoxLayout,
    QLineEdit, QPushButton, QGraphicsDropShadowEffect, QSizePolicy
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
            base = here.parent  # fallback
    return str(base / relative_path)

class SignUpWidget(QWidget):
    def __init__(self, fb, nav):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.fb = fb
        self.nav = nav

        self.outer_container = QWidget()
        self.outer_container_layout = QVBoxLayout(self.outer_container)
        self.outer_container_layout.setContentsMargins(30, 25, 30, 35)
        self.outer_container.setFixedSize(450, 520)
        self.outer_container.setObjectName("outer_container")



        self.create_label = QLabel()

        self.outer_container_layout.addWidget(self.create_label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.outer_container_layout.addSpacing(1)

        self.desc_label = QLabel()

        self.outer_container_layout.addWidget(self.desc_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.outer_container_layout.addSpacing(15)

        self.email_label = QWidget()
        self.email_label_layout = QHBoxLayout(self.email_label)
        self.email_label_layout.setContentsMargins(10,0,0,3)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(22, 22)

        self.email_label_layout.addWidget(self.icon_label)
        self.email_label_layout.addSpacing(2)
        self.email_text_label = QLabel("Email")

        self.email_label_layout.addWidget(self.email_text_label)

        self.outer_container_layout.addWidget(self.email_label)
        self.email_input = QLineEdit()
        self.email_input.setFixedHeight(40)
        self.email_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(8)
        shadow2.setXOffset(0)
        shadow2.setYOffset(0)
        shadow2.setColor(QColor(0, 0, 0, 80))
        self.email_input.setGraphicsEffect(shadow2)
        self.outer_container_layout.addWidget(self.email_input)

        self.outer_container_layout.addSpacing(15)

        # --- Password Label and Icon ---
        self.psw_label_container = QWidget()
        self.psw_label_layout = QHBoxLayout(self.psw_label_container)
        self.psw_label_layout.setContentsMargins(5,0,0,3)

        self.psw_icon_label = QLabel()
        self.psw_icon_label.setFixedSize(22, 22)
        # Ensure you have a 'lock.png' or similar at this path

        self.psw_label_layout.addSpacing(3)
        self.psw_label_layout.addWidget(self.psw_icon_label)
        self.psw_label_layout.addSpacing(2)

        self.psw_text_label = QLabel("Password")

        self.psw_label_layout.addWidget(self.psw_text_label)
        self.outer_container_layout.addWidget(self.psw_label_container)

        # --- Password Input ---
        self.psw_input = QLineEdit()
        self.psw_input.setFixedHeight(40)
        self.psw_input.setEchoMode(QLineEdit.EchoMode.Password)  # Hides text as dots
        self.psw_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


        # Unique shadow for password input
        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(8)
        shadow3.setXOffset(0)
        shadow3.setYOffset(0)
        shadow3.setColor(QColor(0, 0, 0, 80))
        self.psw_input.setGraphicsEffect(shadow3)

        self.outer_container_layout.addWidget(self.psw_input)
        self.outer_container_layout.addSpacing(30)

        self.action_btn = QPushButton()
        self.action_btn.setFixedHeight(40)
        self.action_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.action_btn.clicked.connect(self.account_managing)

        self.action_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.outer_container_layout.addWidget(self.action_btn)
        self.outer_container_layout.addSpacing(12)


        self.alt_actions = QWidget()
        self.alt_actions_layout = QHBoxLayout(self.alt_actions)
        self.alt_actions_layout.setContentsMargins(7, 0, 0, 0)
        self.alt_actions_layout.setSpacing(0)
        self.alt_desc = QLabel()
        self.alt_desc.setContentsMargins(0,0,0,0)

        self.alt_actions_layout.addWidget(self.alt_desc)
        self.alt_actions_layout.addSpacing(3)
        self.switch_btn = QPushButton()
        self.switch_btn.setContentsMargins(2,0,0,0)

        self.switch_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.switch_btn.clicked.connect(self.toggle_mode)
        self.alt_actions_layout.addWidget(self.switch_btn)
        self.alt_actions_layout.addStretch(1)
        self.outer_container_layout.addWidget(self.alt_actions)


        self.back = QPushButton("Back to Home")
        self.back.clicked.connect(lambda _, p="home": nav(p))
        self.back.setStyleSheet("""
                                color: #6F83DC;
                                font-size: 14px;
                                font-weight: 510;
                                padding: 0px;
                                margin: 0px;
                                text-decoration: underline;
                                margin-left:4px;
                                background:transparent;
                                border:none;
                        """)
        self.back.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.outer_container_layout.addStretch(1)

        self.outer_container_layout.addWidget(self.back, alignment = Qt.AlignmentFlag.AlignLeft)





        self.main_layout.addWidget(self.outer_container, alignment = Qt.AlignmentFlag.AlignCenter)

        self.set_to_sign_up()
        self.mode = "signup"

    def toggle_mode(self):
        if self.mode == "signup":
            self.set_to_sign_in()
        else:
            self.set_to_sign_up()

    def account_managing(self):
        print("Mode: ", self.mode)
        if self.mode == "signup":
            try:
                session = self.fb.sign_up(self.email_input.text(), self.psw_input.text())
                uid = self.fb.uid()
                print(f"\n Signed up successfully")
                doc_path = f"users/{uid}/config/main"

                DEFAULT_CONFIG = {
                    "email": f"{self.email_input.text()}",
                    "ssh_user": "",
                    "ssh_ip": "",
                    "ssh_psw": "",
                    "ssh_port": 22,
                    "git_url": "",
                    "git_pat": "",
                    "wandb_user": "",
                    "wandb_proj": "",
                    "wandb_api": ""
                }
                self.email_input.setText("")
                self.psw_input.setText("")
                self.fb.set_doc(doc_path, DEFAULT_CONFIG)
                self.nav("project", uid=uid)

            except Exception as e:
                print("\n Sign-up failed")
                print(e)
                raise SystemExit(1)
        else:
            try:
                print("C1")
                session = self.fb.sign_in(self.email_input.text(), self.psw_input.text())
                print("C2")
                uid_ind = self.fb.uid()
                print("C3")
                print(f"\n Signed in successfully")
                self.nav("project", uid = uid_ind)
                print(f"UID: {uid_ind}")
                self.email_input.setText("")
                self.psw_input.setText("")
            except Exception as e:
                print("\n Sign-in failed")
                print(e)
                raise SystemExit(1)

    def set_to_sign_up(self):
        self.mode = "signup"
        self.create_label.setText("Create an Account")
        self.desc_label.setText("Sign up with your email and a password")
        self.action_btn.setText("Get Started")
        self.alt_desc.setText("Already have an account?")
        self.switch_btn.setText("Sign In")

    def set_to_sign_in(self):
        self.mode = "signin"
        self.create_label.setText("Welcome Back!")
        self.desc_label.setText("Sign in with your email and password")
        self.action_btn.setText("Sign In")
        self.alt_desc.setText("Don't have an account?")
        self.switch_btn.setText("Sign Up")


    def set_light_mode(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.outer_container.setGraphicsEffect(shadow)
        self.outer_container.setStyleSheet("""
                    QWidget#outer_container{
                        border-radius: 25px;
                        border: 1px solid #7a757f;
                        background-color: #F8F2FA;
                    }
                """)
        self.create_label.setStyleSheet("""
                   font-weight: 520;
                   font-size: 28px;
                   color: #1D1B20;
               """)
        self.desc_label.setStyleSheet("""
                           font-weight: normal;
                           font-size: 15px;
                           color: #7A757F;
                       """)
        self.pix = QPixmap(str(resource_path("gui/createProject/mail.png")))

        self.icon_label.setPixmap(self.pix.scaled(
            19, 19,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.email_text_label.setStyleSheet("""
                    font-weight: 510;
                    font-size: 16px;
                    color: #49454E;
                """)
        self.email_input.setStyleSheet("""
                    background-color: #F8F2FA;
                    border-radius: 10px;
                    border: 1px solid #7a757f;
                    padding: 2px 8px;
                    color: #49454E;
                    font-size: 15px;
                """)
        self.psw_pix = QPixmap(str(resource_path("gui/createProject/lock.png")))

        self.psw_icon_label.setPixmap(self.psw_pix.scaled(
            19, 19,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.psw_text_label.setStyleSheet("""
                    font-weight: 510;
                    font-size: 16px;
                    color: #49454E;
                """)
        self.psw_input.setStyleSheet("""
                    background-color: #F8F2FA;
                    border-radius: 10px;
                    border: 1px solid #7a757f;
                    padding-left: 10px;
                    padding: 2px 8px;
                    color: #49454E;
                    font-size: 15px;
                """)
        self.action_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #65558F;
                        border: 1px solid #65558F;
                        color: #fff;
                        border-radius: 20px;
                        font-size: 19px;
                        font-weight: 515;
                    }
                    QPushButton:hover {
                        background-color: #75659E
                    }
                    QPushButton:pressed {
                    background-color: #65558F
                    }
                """)
        self.alt_desc.setStyleSheet("""
                    color: #7A757F;
                    font-size: 14px;
                    font-weight: 510;
                """)
        self.switch_btn.setStyleSheet("""
                        color: #6F83DC;
                        font-size: 14px;
                        font-weight: 510;
                        padding: 0px;
                        margin: 0px;
                        text-decoration: underline;
                        background: transparent;
                """)
    def set_dark_mode(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(12)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor("#999"))
        self.outer_container.setGraphicsEffect(shadow)
        self.outer_container.setStyleSheet("""
                            QWidget#outer_container{
                                border-radius: 25px;
                                border: 1px solid #484848;
                                background-color: #2C292F;
                            }
                        """)
        self.create_label.setStyleSheet("""
                           font-weight: 520;
                           font-size: 28px;
                           color: #D3BCFD;
                       """)
        self.desc_label.setStyleSheet("""
                                   font-weight: normal;
                                   font-size: 15px;
                                   color: #948F99;
                               """)
        self.pix = QPixmap(str(resource_path("gui/createProject/mail_dark.png")))

        self.icon_label.setPixmap(self.pix.scaled(
            19, 19,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.email_text_label.setStyleSheet("""
                            font-weight: 510;
                            font-size: 16px;
                            color: #D3BCFD;
                        """)
        self.email_input.setStyleSheet("""
                            background-color: #2C292F;
                            border-radius: 10px;
                            border: 1.5px solid #4B454D;
                            padding: 2px 8px;
                            color: #D3D3D3;
                            font-size: 15px;
                        """)
        self.psw_pix = QPixmap(str(resource_path("gui/createProject/padlock_dark.png")))

        self.psw_icon_label.setPixmap(self.psw_pix.scaled(
            19, 19,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        ))
        self.psw_text_label.setStyleSheet("""
                            font-weight: 510;
                            font-size: 16px;
                            color: #D3BCFD;
                        """)
        self.psw_input.setStyleSheet("""
                            background-color: #2C292F;
                            border-radius: 10px;
                            border: 1.5px solid #4B454D;
                            padding-left: 10px;
                            padding: 2px 8px;
                            color: #D3D3D3;
                            font-size: 15px;
                        """)
        self.action_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #D3BCFD;
                                border: 1px solid #D3BCFD;
                                color: #39265C;
                                border-radius: 20px;
                                font-size: 19px;
                                font-weight: 515;
                            }
                            QPushButton:hover {
                                background-color: #CAACFF
                            }
                            QPushButton:pressed {
                            background-color: #D3BCFD
                            }
                        """)
        self.alt_desc.setStyleSheet("""
                            color: #7A757F;
                            font-size: 14px;
                            font-weight: 510;
                        """)
        self.switch_btn.setStyleSheet("""
                                color: #6F83DC;
                                font-size: 14px;
                                font-weight: 510;
                                padding: 0px;
                                border: none;
                                margin: 0px;
                                text-decoration: underline;
                                background:transparent;
                        """)