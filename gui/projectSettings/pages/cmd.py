#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.0.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""

import re

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame
)


class cmdPage(QWidget):
    def __init__(self, shared_manager, run_func, connect_func):
        super().__init__()
        # Use the manager and function passed from content.py
        self.manager = shared_manager
        self.run_func = run_func
        self.connect_func = connect_func
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)
        # 1. Remove the top margin of the main layout to let the bar touch the top
        main_layout.setContentsMargins(10, 0, 10, 20)
        main_layout.setSpacing(10)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ---- TOP BAR -----
        top_bar = QWidget()
        # 2. Match the background color (#1F1F1F) and font
        top_bar.setStyleSheet(
            "background-color: #1B1A24; font-size: 18px; color: #7D7D7D; border-radius: 5px"
        )
        top_bar.setFixedHeight(40)

        # 3. Fix the internal layout margins (Remove the bottom 10px margin)
        top_tab_layout = QHBoxLayout(top_bar)
        top_tab_layout.setContentsMargins(15, 0, 15, 0)  # Match the 15px side padding
        top_tab_layout.setSpacing(10)

        self.dir_label = QLabel("Current Directory: None")
        self.dir_label.setStyleSheet("color: #AAA")
        top_tab_layout.addWidget(self.dir_label)

        # Status Container
        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_layout.setSpacing(5)

        self.status_label = QLabel("Status: Disconnected")
        self.icon_label = QLabel()

        self.green_icon = QPixmap("gui/icons/green_circle.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio,
                                                                       Qt.TransformationMode.SmoothTransformation)
        self.red_icon = QPixmap("gui/icons/red-circle.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio,
                                                                   Qt.TransformationMode.SmoothTransformation)
        self.icon_label.setPixmap(self.red_icon)

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.icon_label)

        top_tab_layout.addStretch()
        top_tab_layout.addWidget(status_container)

        main_layout.addWidget(top_bar)

        # ---- CONTAINER ----
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 20, 10, 10)
        container_layout.setSpacing(10)
        container.setObjectName("MainOuterContainer")
        container.setStyleSheet("""
            QWidget#MainOuterContainer {
                background-color: #18181F;
                border: 1px solid #555555;
                border-radius: 10px;
                font-size: 16px;
            }
        """)
        main_layout.addWidget(container)

        # ---- CHAT SCROLL AREA ----
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
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

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(4)
        self.chat_container.setStyleSheet("""
                background-color: #18181F;
                font-size: 16px;
        """)

        self.scroll.setWidget(self.chat_container)
        container_layout.addWidget(self.scroll)

        # ---- INPUT BAR ----
        input_bar = QHBoxLayout()
        input_bar.setSpacing(10)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter command...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #18181F;
                color: white;
                border-radius: 5px;
                border: 1px solid #555;
                padding: 8px;
                font-size: 16px;
            }
            QLineEdit:disabled {
                background-color: #0c0c0f;
                color: #555;
            }
        """)

        self.send_btn = QPushButton("Run")
        self.send_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #18181F;
                border-radius: 8px;
                padding: 8px 20px;
                color: white;
                font-size: 16px;
                border: 2px solid #00417A;
            }
            QPushButton:hover { background-color: #20202A; }
            QPushButton:disabled {
                border: 2px solid #444;

            }
        """)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #18181F;
                color: white; border-radius: 8px;
                padding: 8px 20px;
                font-size: 16px;
                border: 2px solid #8C1B1B;
            }
            QPushButton:hover { background-color: #20202A; }
            QPushButton:disabled {
                background-color: #2A2A2A;
                color: #666;
            }
         """)

        self.end_btn = QPushButton("Ctrl + C")
        self.end_btn.setStyleSheet("""
            QPushButton {
                 background-color: #18181F;
               color: white; border-radius: 8px;
                padding: 8px 20px;
                font-size: 16px;
                border: 2px solid #8C1B1B;
            }
            QPushButton:hover { background-color: #20202A; }
            QPushButton:disabled {
                background-color: #2A2A2A;
                color: #666;
            }
         """)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #18181F;
                color: white; border-radius: 8px;
                padding: 8px 20px;
                font-size: 16px;
                border: 2px solid #18521F;
            }
            QPushButton:hover { background-color: #20202A; }
            QPushButton:disabled {
                border: 2px solid #444;

            }
         """)

        # Set heights
        for btn in [self.send_btn, self.clear_btn, self.end_btn, self.connect_btn, self.input_field]:
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        input_bar.addWidget(self.input_field)
        input_bar.addWidget(self.send_btn)
        input_bar.addWidget(self.end_btn)
        input_bar.addWidget(self.clear_btn)
        input_bar.addWidget(self.connect_btn)
        container_layout.addLayout(input_bar)

        # Connections
        self.send_btn.clicked.connect(self.handle_send)
        self.input_field.returnPressed.connect(self.handle_send)
        self.clear_btn.clicked.connect(self.clear_console)
        self.end_btn.clicked.connect(self.handle_interrupt)
        self.connect_btn.clicked.connect(self.handle_connect)

    def set_busy(self, busy):
        self.send_btn.setEnabled(not busy)
        self.input_field.setEnabled(not busy)
        if busy:
            self.send_btn.setText("Running...")
        else:
            self.send_btn.setText("Run")

    def handle_connect(self):
        self.connect_func()

    def handle_send(self):
        text = self.input_field.text().strip()
        if not text: return
        self.input_field.clear()
        # Trigger the global shared logic
        self.run_func(text)

    def handle_interrupt(self):
        self.manager.send_interrupt()

    def create_new_output_bubble(self):
        """Prepare the bubble for incoming stream data."""
        self.current_bubble = QLabel("")
        self.current_bubble.setWordWrap(True)
        self.current_bubble.setStyleSheet(
            "color: #EEE; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px")
        self.chat_layout.addWidget(self.current_bubble)

    def update_live_output(self, raw_text):
        if not hasattr(self, 'current_bubble') or self.current_bubble is None:
            return

        if "SYNC_DIR:" in raw_text:
            try:
                # Split the text to find the path
                parts = raw_text.split("SYNC_DIR:")
                path_line = parts[1].splitlines()[0].strip()
                print(path_line)
                if path_line:
                    self.update_directory_display(path_line)

                # Remove the SYNC_DIR line from the output so user doesn't see it
                raw_text = parts[0] + "\n".join(parts[1].splitlines()[1:])
            except Exception as e:
                print(f"Sync Error: {e}")

        if not raw_text.strip():
            return

        clean_text = self.strip_ansi_codes(raw_text)
        if not clean_text:
            return

        # 1. BROADEN indicators for both Training and Testing
        # Added "loss", "%", and bar symbols like #, =, and block characters
        progress_indicators = ["it/s", "%", "step", "epoch", "loss", "v_num", "val_", "train_"]

        is_progress_bar = any(x in clean_text.lower() for x in progress_indicators)

        # 2. DECIDE: Overwrite or Append?
        try:
            if '\r' in clean_text:
                # Most training bars use \r. Take the latest segment.
                parts = clean_text.split('\r')
                latest = parts[-1].strip()
                if latest:
                    self.current_bubble.setText(latest)

            elif is_progress_bar:
                # For Testing or Training lines that use \n but are clearly bars
                val = clean_text.strip()
                if val:
                    self.current_bubble.setText(val)

            else:
                # Everything else (Normal Logs/Prints) -> APPEND
                current_val = self.current_bubble.text()
                self.current_bubble.setText(current_val + clean_text)

            # 3. SCROLL
            QTimer.singleShot(10, lambda: self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            ))

        except RuntimeError:
            self.current_bubble = None
        QTimer.singleShot(10, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        ))

    def on_command_finished(self, add_bubble=True):
        self.set_busy(False)
        if add_bubble:
            self.add_separator()

            self.input_field.setFocus()
        QTimer.singleShot(30, lambda: self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        ))

    def update_directory_display(self, path):
        clean_path = path.strip()
        print("Updating to ", clean_path)
        self.dir_label.setText(f"Current Directory: {clean_path}")

    def update_connection_status(self, connected: bool):
        if connected:
            self.status_label.setText("Status: Connected")
            self.icon_label.setPixmap(self.green_icon)
        else:
            self.status_label.setText("Status: Disconnected")
            self.icon_label.setPixmap(self.red_icon)

    def add_message(self, text):
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        lbl.setStyleSheet("color: white; padding: 2px; font-family: 'Consolas', 'Monospace', 'Courier New';")
        self.chat_layout.addWidget(lbl)
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #444; margin: 2px 0px;")
        self.chat_layout.addSpacing(10)

        self.chat_layout.addWidget(line)
        self.chat_layout.addSpacing(10)

    def clear_console(self):
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def strip_ansi_codes(self, text):
        # Disclaimer: This function was written by AI for accurate regex use.
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
