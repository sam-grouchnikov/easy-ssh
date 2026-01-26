#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.1.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""

import re

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCursor
from PyQt6.QtGui import QTextCursor, QTextCharFormat, QColor
from PyQt6.QtWidgets import QPlainTextEdit, QInputDialog
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QPushButton


class ActionButtonMenu(QWidget):
    def __init__(self, console, run_func=None, connect_func=None):
        super().__init__()
        self.run_func = run_func
        self.connect_func = connect_func
        self.console = console
        self.init_ui()

    def init_ui(self):
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        self.wrapper = QFrame()
        self.wrapper.setObjectName("MainWrapper")
        self.wrapper.setStyleSheet("""
            #MainWrapper {
                border: 2px solid #3B3B3B; 
                border-radius: 10px;
            }
        """)

        self.main_layout = QVBoxLayout(self.wrapper)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(6)

        # --- TITLE ---
        title = QLabel("Actions")
        title.setStyleSheet("color: #AAAAAA; font-size: 21px; border: none; padding: 0px")
        self.main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop)

        self.add_divider("#FFFFFF", 1)

        # --- SECTIONS ---
        self.main_layout.addLayout(self.create_connection_section())
        self.main_layout.addSpacing(3)
        self.main_layout.addLayout(self.create_navigation_section())
        self.main_layout.addSpacing(3)
        self.main_layout.addLayout(self.create_commands_section())

        self.main_layout.addStretch()

        self.outer_layout.addWidget(self.wrapper)

    def add_divider(self, color, height, top_spacing=0, bottom_spacing=0):
        if top_spacing: self.main_layout.addSpacing(top_spacing)
        line = QFrame()
        line.setFixedHeight(height)
        line.setStyleSheet(f"background-color: #3B3B3B; border: none;")
        self.main_layout.addWidget(line)
        if bottom_spacing: self.main_layout.addSpacing(bottom_spacing)

    def create_connection_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("Connection/Environment")
        title.setStyleSheet("color: #A0A0A0; font-size: 17px; border: none")
        layout.addWidget(title)

        # Buttons
        row1 = QHBoxLayout()
        self.ssh_con_btn = self.make_btn("Connect to SSH", "#1D5F1F")
        self.ssh_con_btn.clicked.connect(self.connect_func)
        self.run_curr_btn = self.make_btn("Run Select File", "#1D5F1F")
        self.run_curr_btn.clicked.connect(self.open_run_dialog)
        row1.addWidget(self.ssh_con_btn)
        row1.addWidget(self.run_curr_btn)
        row1.addStretch()

        row2 = QHBoxLayout()
        self.term_con_btn = self.make_btn("Terminate Connection", "#5F1D1D")
        self.term_con_btn.clicked.connect(lambda: self.run_func("exit"))
        self.term_run_btn = self.make_btn("Terminate Run", "#5F1D1D")
        self.term_run_btn.clicked.connect(lambda: self.run_func("Ctrl+C"))
        row2.addWidget(self.term_con_btn)
        row2.addWidget(self.term_run_btn)
        row2.addStretch()

        row3 = QHBoxLayout()
        self.create_venv_btn = self.make_btn("Create Virtual Environment", "#1D405F")

        def create_venv():
            self.run_func("python3 -m venv venv")
            self.run_func(". venv/bin/activate")

        self.create_venv_btn.clicked.connect(create_venv)

        row3.addWidget(self.create_venv_btn)
        row3.addStretch()

        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        return layout

    def open_run_dialog(self):
        file, ok = QInputDialog.getText(
            self,
            "Run File",
            "Enter file name:",
        )

        if ok and file:
            command = f"python3 {file}"
            print(f"Running command (1): {command}")
            if not file.endswith(".py") and not '.' in file:
                command += f".py"
            print("Running command:", command)
            self.run_func(command)

    def create_navigation_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        title = QLabel("Quick Navigation")
        title.setStyleSheet("color: #A0A0A0; font-size: 17px; border: none")
        layout.addWidget(title)

        row = QHBoxLayout()
        self.cd_btn = self.make_btn("Change Directory", "#1D405F")
        self.cd_btn.clicked.connect(self.open_cd_dialog)
        self.rd_btn = self.make_btn("Reset Directory", "#1D405F")
        self.rd_btn.clicked.connect(lambda: self.run_func("cd ~"))
        row.addWidget(self.cd_btn)
        row.addWidget(self.rd_btn)
        row.addStretch()
        layout.addLayout(row)
        return layout

    def open_cd_dialog(self):

        path, ok = QInputDialog.getText(
            self,
            "Change Directory",
            "Enter remote path:",
        )

        if ok and path:
            command = f"cd {path}"
            self.run_func(command)

    def open_packages_dialog(self):

        packages, ok = QInputDialog.getText(
            self,
            "Install Packages",
            "Enter package names (seperated by a single space):",
        )

        if ok and packages:
            command = f"pip install {packages}"
            self.run_func(command)

    def open_git_dialogue(self):

        branch, ok = QInputDialog.getText(
            self,
            "Pull Latest Changes",
            "Enter active branch name (ex. main, master):",
        )

        if ok and branch:
            command = f"git pull origin {branch}"
            self.run_func(command)

    def create_commands_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        title = QLabel("Quick Commands")
        title.setStyleSheet("color: #A0A0A0; font-size: 17px; border: none")
        layout.addWidget(title)

        r1 = QHBoxLayout()
        self.inst_pack_btn = self.make_btn("Install Packages", "#1D405F")
        self.inst_pack_btn.clicked.connect(self.open_packages_dialog)
        r1.addWidget(self.inst_pack_btn)

        r1.addStretch()

        r2 = QHBoxLayout()
        self.dir_btn = self.make_btn("Directory Files List", "#1D405F")
        self.dir_btn.clicked.connect(lambda: self.run_func("ls"))
        r2.addWidget(self.dir_btn)
        self.status_btn = self.make_btn("GPU Status", "#1D405F")
        self.status_btn.clicked.connect(lambda: self.run_func("nvidia-smi"))
        r2.addWidget(self.status_btn)
        r2.addStretch()

        r3 = QHBoxLayout()
        self.pull_btn = self.make_btn("Pull Latest Changes", "#1D405F")
        self.pull_btn.clicked.connect(self.open_git_dialogue)
        r3.addWidget(self.pull_btn)
        self.clear_btn = self.make_btn("Clear Console", "#5F1D1D")
        self.clear_btn.clicked.connect(self.console.clear)
        r3.addWidget(self.clear_btn)
        r3.addStretch()

        layout.addLayout(r2)
        layout.addLayout(r3)
        layout.addLayout(r1)

        return layout

    def make_btn(self, text, border_color):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                color: #808080; 
                background: none; 
                border: 1px solid {border_color}; 
                padding: 4px 20px; 
                border-radius: 10px;
                font-size: 15px;
            }}
            QPushButton:hover {{
                background-color: #1E1E1E;
            }}
            QPushButton:disabled {{
                border: 2px solid #444;
            }}
        """)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setFixedHeight(35)

        return btn


class ConsoleOutput(QWidget):
    def __init__(self, on_path_found=None):
        super().__init__()
        self.on_path_found = on_path_found
        self.initUI()

    def initUI(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.main_container = QWidget()
        self.main_container.setObjectName("ConsoleBackground")
        self.main_container.setStyleSheet("""
            QWidget#ConsoleBackground {
                background-color: #18181F;
                border: 1px solid #555555;
                border-radius: 10px;
                font-size: 16px;
            }
        """)

        content_layout = QVBoxLayout(self.main_container)
        content_layout.setContentsMargins(20, 15, 20, 15)
        content_layout.setSpacing(6)

        title = QLabel("Console Output")
        title.setStyleSheet("color: #AAAAAA; font-size: 21px; border: none; background: transparent;")
        content_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop)

        border = QFrame()
        border.setFixedHeight(2)
        border.setStyleSheet("background-color: #3B3B3B; border: none;")
        content_layout.addWidget(border)

        self.text_display = QPlainTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("""
        QPlainTextEdit {
            background: transparent; border: none; color: #DDD;
            font-family: 'Consolas', 'Monospace', 'Courier New'; font-size:16px
        }
        QScrollBar:vertical {
                border: none;
                background: #18181F;
                width: 13px;
                margin: 0px 0px 0px 0px;
            }
        
            /* The Scrollbar Handle */
            QScrollBar::handle:vertical {
                background: #3E3E42;
                min-height: 20px;
                border-radius: 5px;
                margin: 2px;
            }
        
            /* Handle color when hovering */
            QScrollBar::handle:vertical:hover {
                background: #505050;
            }
        
            /* Remove the buttons (arrows) at the top and bottom */
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        
            /* Remove the background area above and below the handle */
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        content_layout.addWidget(self.text_display)

        outer_layout.addWidget(self.main_container)

    def apply_line_spacing(self):
        """Helper to ensure all text in the widget uses 150% line height."""
        cursor = self.text_display.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        block_format = cursor.blockFormat()
        block_format.setLineHeight(150, 1)
        cursor.setBlockFormat(block_format)

    def add_command_line(self, command):
        """Adds the command with a $ prefix without excessive spacing."""
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        if self.text_display.toPlainText() == "Waiting for command...":
            self.text_display.setPlainText("")

        cursor.insertText(f"$ {command}\n")

        self.apply_line_spacing()

    def update_output(self, raw_text):
        if "SYNC_DIR:" in raw_text:
            try:
                parts = raw_text.split("SYNC_DIR:")
                path_line = parts[1].splitlines()[0].strip()
                if path_line and self.on_path_found:
                    self.on_path_found(path_line)
                raw_text = parts[0] + "\n".join(parts[1].splitlines()[1:])
            except Exception as e:
                print(f"Sync Error: {e}")

        # 1. Clean ANSI codes
        # Disclaimer: This chunk (next two lines) were generated by AI for accurate regex use.
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_text = ansi_escape.sub('', raw_text)

        if not clean_text:
            return

        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        white = QTextCharFormat()
        white.setForeground(QColor("#FFFFFF"))
        cursor.setCharFormat(white)
        # Define progress keywords and symbols for replacement
        progress_indicators = ["it/s", "%", "step", "epoch", "loss", "v_num", "val_", "train_", "testing", "validation"]
        bar_symbols = ["#", "=", "█", "░", "│"]

        is_progress = any(x in clean_text.lower() for x in progress_indicators) or \
                      any(s in clean_text for s in bar_symbols)

        # 2. Handle Carriage Returns (\r)
        if '\r' in clean_text:
            parts = clean_text.split('\r')
            final_text = parts[-1].strip()

            if final_text:
                # Select the current line and replace it
                cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor)
                cursor.insertText(final_text)

        # 3. Handle "Testing" and "Training" lines that use \n but should be replaced
        elif is_progress:
            # Move to start of line to see if there's existing progress text to replace
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor)
            cursor.insertText(clean_text.strip())

        # 4. Standard Append for regular logs
        else:
            cursor.insertText(clean_text)

        self.text_display.setTextCursor(cursor)
        self.text_display.ensureCursorVisible()

    def finish_command(self, add_bubble=True, single=False, add_sep=True):
        """Appends the finish marker in a light gray color."""
        if add_bubble:
            cursor = self.text_display.textCursor()
            cursor.movePosition(QTextCursor.MoveOperation.End)

            # 1. Create a format for the gray text
            gray_format = QTextCharFormat()
            gray_format.setForeground(QColor("#444444"))
            white = QTextCharFormat()
            white.setForeground(QColor("#FFFFFF"))

            # 2. Store the original format to reset it later
            original_format = cursor.charFormat()

            # 3. Apply gray and insert text
            cursor.setCharFormat(gray_format)
            if not single:
                if add_sep:
                    cursor.insertText(f"\n\n{'-' * 65}\n\n")
            else:
                if add_sep:
                    cursor.insertText(f"{'-' * 65}\n\n")

            cursor.setCharFormat(white)

            # 4. Reset to original format so next command is white again
            cursor.setCharFormat(original_format)

            self.text_display.setTextCursor(cursor)
            self.apply_line_spacing()

    def clear(self):
        self.text_display.setPlainText("")
