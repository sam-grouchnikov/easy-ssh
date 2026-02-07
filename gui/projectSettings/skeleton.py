#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.1.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""
from datetime import datetime

from PyQt6.QtCore import Qt, QCoreApplication, QSize
from PyQt6.QtGui import QIcon, QPixmap, QCursor
from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QSizePolicy, QStackedWidget, QWidget, QHBoxLayout, QFrame, QPushButton, QMainWindow
)


from backend.ssh.sshManager import SSHStreamWorker, SSHManager
from gui.navbar import SideNavBar
from gui.projectSettings.pages.FileTree import FileTreePage
from gui.projectSettings.pages.SimpleSSH import SimpleSSHPage
from gui.projectSettings.pages.cmd import cmdPage
from gui.projectSettings.pages.graphs import GraphsPage
from gui.projectSettings.pages.settings import SettingsPage

from firebase import _from_fs_value, _to_fs_value, from_fs_doc
def config_doc_path(uid: str) -> str:
    return f"users/{uid}/config/main"

class ProjectSettingsSkeleton(QMainWindow):
    def __init__(self, navigate, toggle_theme_func, fb):
        super().__init__()
        self.project_name = None
        self.setWindowTitle("Homepage")
        self.setGeometry(100, 100, 1300, 700)
        self.setMinimumSize(600, 400)
        self.cloned = False
        self.uid = None
        self.fb = fb

        self.ssh_manager = None
        self.home_dir = None
        self.current_dir = None
        self.recent_cmd = None

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Inside ProjectSettingsSkeleton.__init__
        self.main_layout = QHBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Create the right-side container
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)

        self.sidebar = QWidget()
        self.sidebar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.sidebar.setContentsMargins(15, 15, 15, 15)
        self.sidebar.setFixedWidth(270)
        self.sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(self.sidebar_layout)

        self.easy_ssh_label = QLabel("Easy-SSH")
        self.easy_ssh_label.setContentsMargins(10, 0, 0, 0)
        self.sidebar_layout.addWidget(self.easy_ssh_label)
        self.sidebar_layout.addSpacing(5)

        self.line_container = QWidget()
        self.line_layout = QHBoxLayout(self.line_container)

        self.line_layout.setContentsMargins(0, 0, 0, 0)

        self.line = QFrame()
        self.line.setFixedSize(215, 1)

        self.line_layout.addWidget(self.line)
        self.sidebar_layout.addWidget(self.line_container)

        self.pages_label = QLabel("Pages")
        self.pages_label.setContentsMargins(10, 0, 0, 0)
        self.sidebar_layout.addWidget(self.pages_label)

        self.nav = SideNavBar()
        self.nav.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.sidebar_layout.addWidget(self.nav)

        self.sidebar_layout.addStretch(1)

        self.docs_btn = QPushButton()
        self.docs_btn.setFixedSize(220, 35)

        # Create a layout inside the button
        btn_layout = QHBoxLayout(self.docs_btn)
        btn_layout.setContentsMargins(10, 0, 15, 0)
        btn_layout.setSpacing(10)

        # Create the icon
        self.icon_lbl = QLabel()
        self.icon_lbl.setPixmap(
            QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\google-docs.png").scaled(25, 25,
                                                                                                                 Qt.AspectRatioMode.KeepAspectRatio))
        self.icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.text_lbl = QLabel("Docs")
        self.text_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Add to the button's layout
        btn_layout.addWidget(self.icon_lbl)
        btn_layout.addWidget(self.text_lbl)
        btn_layout.addStretch()

        self.docs_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.sidebar_layout.addWidget(self.docs_btn)

        # --- Light Mode Button ---
        self.light_mode_btn = QPushButton()
        self.light_mode_btn.setFixedSize(220, 35)

        # Create a layout inside the button
        light_btn_layout = QHBoxLayout(self.light_mode_btn)
        light_btn_layout.setContentsMargins(9, 0, 15, 0)
        light_btn_layout.setSpacing(10)

        # Create the icon
        self.light_icon_lbl = QLabel()
        # Updated path to use "light_mode.png"
        self.light_pix = QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\light mode.png")
        self.light_icon_lbl.setPixmap(
            self.light_pix.scaled(27, 27, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.light_icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Create the text label
        self.light_text_lbl = QLabel("Light Mode")
        self.light_text_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Add to the button's layout
        light_btn_layout.addWidget(self.light_icon_lbl)
        light_btn_layout.addWidget(self.light_text_lbl)
        self.light_mode_btn.clicked.connect(toggle_theme_func)
        light_btn_layout.addStretch()

        # Apply the styles


        self.light_mode_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.sidebar_layout.addWidget(self.light_mode_btn)

        self.sidebar_layout.addSpacing(3)

        self.line_container2 = QWidget()
        self.line_layout2 = QHBoxLayout(self.line_container2)

        self.line_layout2.setContentsMargins(0, 0, 0, 0)

        self.line2 = QFrame()
        self.line2.setFixedSize(215, 1)

        self.line_layout2.addWidget(self.line2)
        self.sidebar_layout.addWidget(self.line_container2)

        # --- Profile Button (Single Row) ---
        self.profile_btn = QPushButton()
        self.profile_btn.setFixedSize(220, 48)  # Slightly taller than standard buttons

        # Main horizontal layout
        profile_btn_layout = QHBoxLayout(self.profile_btn)
        profile_btn_layout.setContentsMargins(11, 0, 15, 0)
        profile_btn_layout.setSpacing(10)

        # 1. The Profile Icon
        self.profile_icon_lbl = QLabel()
        self.profile_pix = QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\user.png")
        self.profile_icon_lbl.setPixmap(
            self.profile_pix.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.profile_icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.profile_btn.clicked.connect(lambda _, p="home": navigate(p))


        # 2. The Username Label (Single Row)
        # self.profile_name_lbl = QLabel(config.get("User"))
        self.profile_name_lbl = QLabel("")
        # Using 16px for a clean, readable look
        self.profile_name_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        # Add to the button's layout
        profile_btn_layout.addWidget(self.profile_icon_lbl)
        profile_btn_layout.addWidget(self.profile_name_lbl)
        profile_btn_layout.addStretch()

        # 3. Apply the Styles


        self.tree_data_accumulator = ""

        self.profile_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.sidebar_layout.addWidget(self.profile_btn)

        self.content_layout.addWidget(self.sidebar)

        self.stack = QStackedWidget(self)
        self.config = None

        self.cmd_page = cmdPage(self.ssh_manager, self.global_run_command, self.global_handle_connect)
        self.file_tree_page = FileTreePage(self.global_run_command, self.home_dir, self.config, self.ssh_manager)
        self.settings_page = SettingsPage(self.config, self.reload_manager, self.fb)
        self.graph_page = GraphsPage(self.config)

        # self.cmd_page = QWidget()
        # self.file_tree_page = QWidget()
        # self.settings_page = QWidget()
        # self.graph_page = QWidget()

        self.stack.addWidget(self.cmd_page)
        self.stack.addWidget(self.file_tree_page)
        self.stack.addWidget(self.graph_page)
        self.stack.addWidget(self.settings_page)
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.content)
        self.content_layout.addWidget(self.stack)

        def handle_navigation(index):
            self.stack.setCurrentIndex(index)

            # 2. Update the visual highlight for all items
            for item in self.nav.nav_items:
                item.setSelected(item.index == index)

        # Connect each item's signal to our handler
        for item in self.nav.nav_items:
            # We use the 'index' stored inside the NavItem itself
            item.clicked.connect(handle_navigation)

        # Initialize the first page and first highlight
        handle_navigation(0)
        self.set_light_mode()

    def update_uid(self, new):
        self.uid = new
        self.doc_path = config_doc_path(self.uid)
        self.doc = self.fb.get_doc(self.doc_path)
        self.config = from_fs_doc(self.doc)
        self.graph_page.update_config(self.config, self.doc_path)
        self.settings_page.update_config(self.config, self.doc_path)
        self.load_settings()

    def load_settings(self):
        self.settings_page.load_parts(self.config)
        self.profile_name_lbl.setText(self.config.get("email"))

    def reload_manager(self):
        pass

    def global_handle_connect(self):
        self.cmd_page.connect_btn.setText(" Connecting")
        QCoreApplication.processEvents()
        if self.ssh_manager is None and self.config.get("user") != "":
            server_new = self.config.get("ssh_ip")
            user_new = self.config.get("ssh_user")
            port_new = self.config.get("ssh_port")
            psw_new = self.config.get("ssh_psw")
            self.ssh_manager = SSHManager(server_new, user_new, port_new, psw_new)

        success, msg = self.ssh_manager.connect()
        self.cmd_page.add_message(f"System: {msg}")
        self.cmd_page.add_separator()
        self.cmd_page.update_connection_status(success)

        if success:
            new_path = self.ssh_manager.get_pwd_silently()
            self.home_dir = new_path
            self.current_dir = new_path

            # 2. Update UI displays
            self.file_tree_page.update_home(new_path)
            self.cmd_page.update_directory_display(new_path)
            find_cmd = "find . -not -path '*/.*' -not -path '*__pycache__*' -not -path '*venv*' -not -path '*wandb*'"
            self.global_run_command(find_cmd, is_tree_update=True)

            new_path = self.ssh_manager.get_pwd_silently()
            self.home_dir = new_path
            self.file_tree_page.update_home(new_path)
            self.current_dir = new_path
            self.cmd_page.update_directory_display(new_path)
            self.cmd_page.connect_btn.setText(" Connect")
            self.cmd_page.connect_btn.setEnabled(False)
            self.cmd_page.send_btn.setEnabled(True)
        else:
            self.cmd_page.connect_btn.setText(" Connect")

    def update_tree(self):
        find_cmd = "find . -not -path '*/.*' -not -path '*__pycache__*' -not -path '*venv*' -not -path '*wandb*'"
        self.global_run_command(find_cmd, is_tree_update=True)


    def accumulate_tree_data(self, text):
        self.tree_data_accumulator += text

    def global_run_command(self, command, is_tree_update=False, is_file_read=False, is_file_save=False, is_git_clone=False):
        self.recent_cmd = command
        self.cmd_page.send_btn.setEnabled(False)

        if command == "exit":
            self.cmd_page.add_message("$ exit\nSystem: Disconnected")
            self.cmd_page.add_separator()

            # 1. Close the backend connection
            self.ssh_manager.close()

            # 2. Update the UI Status
            self.cmd_page.update_connection_status(False)

            self.cmd_page.update_directory_display("None")

            self.cmd_page.connect_btn.setText("Connect")
            self.cmd_page.connect_btn.setEnabled(True)
            self.file_tree_page.rebuild_tree("")
            self.file_tree_page.reset_editor_text()
            self.file_tree_page.file_name_label.setText("No File Selected")
            return

        if command.startswith("python") or command.startswith("python3"):
            if "venv" not in command:
                now = datetime.now()
                date = now.strftime("%B %d, %Y")
                time = now.strftime("%I:%M %p")
                if "-m" in command:
                    file = command.split(" ")[2].split(".")[1] + ".py"
                else:
                    file = command.split(" ")[1]

        if command == "Ctrl+C":
            self.ssh_manager.send_interrupt()
            return

        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            return
        self.worker = SSHStreamWorker(self.ssh_manager, command)

        if command.startswith("cd"):
            appended = command.split(' ')[1]
            if appended == '~':
                self.current_dir = self.home_dir
            else:
                self.current_dir += f"/{appended}"
            command = f"$ {command}"

            self.cmd_page.add_message(command)
            self.worker.finished.connect(
                lambda: self.global_finished(is_tree_update, is_file_read, is_file_save, is_git_clone)
            )

            self.worker.start()
            return


        if is_tree_update:
            self.tree_data_accumulator = ""

            self.worker.output_received.connect(self.accumulate_tree_data)

            self.worker.finished.connect(
                lambda: self.file_tree_page.rebuild_tree(self.tree_data_accumulator),
                Qt.ConnectionType.QueuedConnection
            )
        elif is_file_save:
            pass
        elif is_git_clone:
            self.update_tree()
            self.graph_page.refresh_runs()
            pass

        elif is_file_read:
            # Clear the editor first
            self.file_tree_page.editor.clear()
            # Connect output DIRECTLY to the editor's append function
            self.worker.output_received.connect(self.file_tree_page.display_file_content)
        else:
            command = f"$ {command}"

            self.cmd_page.add_message(command)
            self.cmd_page.create_new_output_bubble()

            self.worker.output_received.connect(self.cmd_page.update_live_output)

        self.worker.finished.connect(
            lambda: self.global_finished(is_tree_update, is_file_read, is_file_save, is_git_clone)
        )

        self.worker.start()

    def global_finished(self, is_tree_update=False, is_file_read=False, is_file_save=False, is_git_clone=False):
        if is_tree_update or is_file_read or is_file_save or is_git_clone:
            self.cmd_page.update_directory_display(self.current_dir)
            return

        # Normal terminal finish logic
        cmd_start = self.recent_cmd.split(' ')[0]
        add_bubble = cmd_start not in ["cat", "ssh", "git", "find"]
        if self.recent_cmd.startswith("git pull"):
            add_bubble = True
        if is_git_clone:
            add_bubble = False
        self.cmd_page.on_command_finished(add_bubble)

        self.cmd_page.update_directory_display(self.current_dir)
        self.cmd_page.send_btn.setEnabled(True)

    def set_light_mode(self):
        self.nav.set_light_mode()
        self.cmd_page.set_light_mode()
        self.file_tree_page.set_light_mode()
        self.settings_page.set_light_mode()
        self.graph_page.set_light_mode()
        self.light_text_lbl.setText("Light Mode")
        self.central_widget.setStyleSheet("background-color: #F9F9FF;")
        self.sidebar.setStyleSheet("background-color:#eee6ee")
        self.easy_ssh_label.setStyleSheet("color: black; font-weight: bold; font-size: 38px")
        self.line.setStyleSheet("background-color: #555;")
        self.pages_label.setStyleSheet("color: black; font-size: 26px; font-weight: 570;")
        self.text_lbl.setStyleSheet("font-size: 15.5px; color: black; background: transparent;")
        self.docs_btn.setStyleSheet("""
                        QPushButton {
                            background-color: transparent;
                            border-radius: 8px;
                        }
                        QPushButton:hover {
                            background-color: #E4E4E8;
                        }
                        QPushButton[selected="true"] {
                            background-color: #E3CDF7;
                        }
                        QPushButton QLabel {
                            background-color: transparent;
                            color: black;
                            font-size: 14px;
                        }
                    """)
        self.light_text_lbl.setStyleSheet("font-size: 15.5px; color: black; background: transparent;")

        self.light_mode_btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        border-radius: 8px;
                    }
                    QPushButton:hover {
                        background-color: #E4E4E8;
                    }
                    QPushButton[selected="true"] {
                        background-color: #E3CDF7;
                    }
                    QPushButton QLabel {
                        background-color: transparent;
                        color: black;
                        font-size: 18px; 
                    }
                """)
        self.line2.setStyleSheet("background-color: #555;")
        self.profile_name_lbl.setStyleSheet("font-size: 16px; color: black; background: transparent;")

        self.profile_btn.setStyleSheet("""
                   QPushButton {
                       background-color: transparent;
                       border-radius: 8px;
                   }
                   QPushButton:hover {
                       background-color: #E4E4E8;
                   }
                   QPushButton[selected="true"] {
                       background-color: #E3CDF7;
                   }
                   QPushButton QLabel {
                        background-color: transparent;
                    }
               """)
        self.profile_pix = QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\user.png")
        self.profile_icon_lbl.setPixmap(
            self.profile_pix.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                    Qt.TransformationMode.SmoothTransformation))

        self.icon_lbl.setPixmap(
            QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\google-docs.png").scaled(25, 25,
                                                                                                                 Qt.AspectRatioMode.KeepAspectRatio))
        self.icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.light_pix = QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\light mode.png")
        self.light_icon_lbl.setPixmap(
            self.light_pix.scaled(27, 27, Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation))
        self.light_icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def set_dark_mode(self):
        self.nav.set_dark_mode()
        self.cmd_page.set_dark_mode()
        self.file_tree_page.set_dark_mode()
        self.settings_page.set_dark_mode()
        self.graph_page.set_dark_mode()
        self.light_text_lbl.setText("Dark Mode")
        self.central_widget.setStyleSheet("background-color: #141318;")
        self.sidebar.setStyleSheet("background-color: #1B1926")
        self.easy_ssh_label.setStyleSheet("color: #D0C4FF; font-weight: bold; font-size: 38px")
        self.line.setStyleSheet("background-color: #C392FF;")
        self.pages_label.setStyleSheet("color: #D0C4FF; font-size: 26px; font-weight: 570;")
        self.text_lbl.setStyleSheet("font-size: 15.5px; color: #E8E3FF; background: transparent;")
        self.docs_btn.setStyleSheet("""
                                QPushButton {
                                    background-color: transparent;
                                    border-radius: 8px;
                                }
                                QPushButton:hover {
                                    background-color: #2F2A46;
                                }
                                QPushButton[selected="true"] {
                                    background: transparent;
                                }
                                QPushButton QLabel {
                                    background-color: transparent;
                                    color: #E8E3FF;
                                    font-size: 14px;
                                }
                            """)
        self.light_text_lbl.setStyleSheet("font-size: 15.5px; color: #E8E3FF; background: transparent;")

        self.light_mode_btn.setStyleSheet("""
                            QPushButton {
                                background-color: transparent;
                                border-radius: 8px;
                            }
                            QPushButton:hover {
                                background-color: #2F2A46;
                            }
                            QPushButton[selected="true"] {
                                background: transparent;
                            }
                            QPushButton QLabel {
                                background-color: transparent;
                                color: white;
                                font-size: 18px; 
                            }
                        """)
        self.line2.setStyleSheet("background-color: #C392FF;")
        self.profile_name_lbl.setStyleSheet("font-size: 16px; color: #E8E3FF; background: transparent;")

        self.profile_btn.setStyleSheet("""
                           QPushButton {
                               background-color: transparent;
                               border-radius: 8px;
                           }
                           QPushButton:hover {
                               background-color: #2F2A46;
                           }
                           QPushButton[selected="true"] {
                               background-color: #3E375B;
                           }
                           QPushButton QLabel {
                            background-color: transparent;
                            }
                       """)
        self.profile_pix = QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\user_dark.png")
        self.profile_icon_lbl.setPixmap(
            self.profile_pix.scaled(24, 24, Qt.AspectRatioMode.KeepAspectRatio,
                                    Qt.TransformationMode.SmoothTransformation))

        self.icon_lbl.setPixmap(
            QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\google-docs-dark.png").scaled(25, 25,
                                                                                                                 Qt.AspectRatioMode.KeepAspectRatio))
        self.icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self.light_pix = QPixmap("C:\\Users\\samgr\\PycharmProjects\\easy-ssh-ui-remake\\gui\\icons\\dark mode.png")
        self.light_icon_lbl.setPixmap(
            self.light_pix.scaled(23, 23, Qt.AspectRatioMode.KeepAspectRatio,
                                  Qt.TransformationMode.SmoothTransformation))
        self.light_icon_lbl.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)