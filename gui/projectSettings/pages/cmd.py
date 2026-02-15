#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.2.1
Email: sam.grouchnikov@gmail.com
Status: Development
"""

import re

from PyQt6.QtCore import Qt, QTimer, QSize, QPoint
from PyQt6.QtGui import QCursor, QIcon, QColor, QAction
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QGraphicsDropShadowEffect, QMenu, QSizePolicy
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


class cmdPage(QWidget):
    def __init__(self, shared_manager, run_func, connect_func, setup_env):
        super().__init__()
        # Use the manager and function passed from content.py
        self.manager = shared_manager
        self.run_func = run_func
        self.connect_func = connect_func
        self.is_dark = False
        self.setup_env = setup_env
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)
        # 1. Remove the top margin of the main layout to let the bar touch the top
        self.main_layout.setContentsMargins(200, 25, 200, 20)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ---- TOP BAR -----
        self.top_bar = QWidget()
        self.top_bar.setObjectName('top_bar')

        self.top_bar.setFixedHeight(40)

        self.top_tab_layout = QHBoxLayout(self.top_bar)
        self.top_tab_layout.setContentsMargins(20, 3, 20, 3)
        self.top_tab_layout.setSpacing(10)

        self.dir_label = QLabel("Current Directory: None")
        self.dir_label.setFixedHeight(20)

        self.status_label = QLabel("Status: Disconnected")

        self.status_container = QWidget()
        self.status_container.setFixedHeight(20)
        self.status_container.setStyleSheet("border: none;")

        self.status_layout = QHBoxLayout(self.status_container)
        self.status_layout.setContentsMargins(0, 0, 0, 0)
        self.status_layout.setSpacing(8)  # Space between dot and directory text

        # 1. The Dot
        self.status_dot = QLabel()
        self.status_size = 12
        self.status_dot.setFixedSize(self.status_size, self.status_size)
        self.status_dot.setStyleSheet("background-color: #ff4444; border-radius: 6px;")  # Default red

        # 2. The Directory Label (Assuming you've initialized this elsewhere)
        # If not initialized yet, add: self.dir_label = QLabel("Not Connected")
        self.dir_label.setStyleSheet("font-weight: 500; color: #5f6368;")

        # 3. Add only the dot and the directory label
        self.status_layout.addWidget(self.status_dot)
        self.status_layout.addWidget(self.dir_label)

        # 4. Shrink-to-fit logic
        # Set size policy so it doesn't try to take up extra space
        self.status_container.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.status_container.adjustSize()

        # 5. Add to top layout centered
        self.top_tab_layout.addWidget(self.status_container, alignment=Qt.AlignmentFlag.AlignHCenter)

        # self.status_layout.addWidget(self.status_label)

        self.top_tab_layout.addWidget(self.status_container)

        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addSpacing(8)

        # ---- CONTAINER ----
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 5, 10, 10)
        self.container_layout.setSpacing(10)
        self.container.setObjectName("MainOuterContainer")

        self.main_layout.addWidget(self.container)

        # ---- CHAT SCROLL AREA ----
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(4)
        self.chat_container.setContentsMargins(30, 0, 20, 0)

        self.scroll.setWidget(self.chat_container)
        self.container_layout.addWidget(self.scroll)

        # ---- INPUT BAR ----
        self.input_bar = QHBoxLayout()
        self.input_bar.setSpacing(18)
        self.input_bar.setContentsMargins(5, 0, 7, 5)

        self.input_field = QLineEdit()
        shadow1 = QGraphicsDropShadowEffect()
        shadow1.setBlurRadius(8)
        shadow1.setXOffset(0)
        shadow1.setYOffset(0)
        shadow1.setColor(QColor(0, 0, 0, 80))

        self.input_wrapper = QFrame()
        self.input_wrapper.setObjectName("InputWrapper")

        # Apply shadow to the whole wrapper, not just the text field
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(2)
        shadow.setColor(QColor(0, 0, 0, 40))
        self.input_wrapper.setGraphicsEffect(shadow)

        # --- 2. Master Layout inside the Wrapper ---
        self.master_input_layout = QVBoxLayout(self.input_wrapper)
        self.master_input_layout.setContentsMargins(20, 15, 20, 10)
        self.master_input_layout.setSpacing(4)

        # --- 3. Initialize Row 1: The Input Field ---
        self.input_field = QLineEdit()
        self.input_field.setContentsMargins(10, 0, 0, 0)
        self.input_field.setPlaceholderText("Enter command...")
        self.input_field.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.input_field.setStyleSheet("border: none; background: transparent; font-size: 16px;"
                                       "padding-top: 8px; padding-bottom: 8px; padding-left: 25px;")

        # --- 4. Initialize Row 2: Buttons ---
        self.button_row_layout = QHBoxLayout()
        self.button_row_layout.setSpacing(10)

        self.tools_btn = QPushButton(" Tools")

        self.actions_btn = QPushButton(" Actions")

        # --- Right Side Buttons ---
        self.connect_btn = QPushButton("  Connect")

        self.send_btn = QPushButton("  Run")

        self.actions_menu = QMenu(self)
        self.tools_menu = QMenu(self)

        # Make the Run button a bit more prominent
        self.send_btn.setStyleSheet("""
            QPushButton { 
                background-color: #1a73e8; 
                color: white; 
                border-radius: 12px; 
                padding: 5px 15px; 
            }
            QPushButton:hover { background-color: #1557b0; }
        """)

        # --- 5. Assemble the Layout ---
        # Add top row
        self.master_input_layout.addWidget(self.input_field)

        # Build bottom row
        self.button_row_layout.addWidget(self.tools_btn)
        self.button_row_layout.addWidget(self.actions_btn)
        self.button_row_layout.addStretch()  # This pushes the next buttons to the far right
        self.button_row_layout.addWidget(self.connect_btn)
        self.button_row_layout.addWidget(self.send_btn)

        # Add bottom row to master
        self.master_input_layout.addSpacing(5)
        self.master_input_layout.addLayout(self.button_row_layout)

        # --- 6. Final Placement & Logic ---
        # Add the wrapper to your main window's layout
        self.container_layout.addWidget(self.input_wrapper)

        # Setup Menus and Connections
        self.setup_actions_menu()
        self.setup_tools_menu()

        self.tools_btn.clicked.connect(self.show_tools_menu_above)
        self.actions_btn.clicked.connect(self.show_actions_menu_above)
        self.send_btn.clicked.connect(self.handle_send)
        self.input_field.returnPressed.connect(self.handle_send)
        self.connect_btn.clicked.connect(self.handle_connect)
        # Note: Re-linked actions_btn to handle_interrupt as per your code
        self.actions_btn.clicked.connect(self.handle_interrupt)

    def setup_tools_menu(self):
        self.tools_menu.setObjectName("toolsMenu")
        self.tools_menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.tools_menu.setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        actions = [
            ("Auto Environment Setup", self.setup_env),
            # ("Scan Dependency Imports", self.dummy_func),
            # ("System Health Check", self.dummy_func),
            # ("Clean Up Zombie Processes", self.dummy_func)
        ]

        for text, slot in actions:
            action = QAction(text, self)
            action.triggered.connect(slot)
            self.tools_menu.addAction(action)

    def show_tools_menu_above(self):
        menu_width = self.tools_menu.sizeHint().width()
        menu_height = self.tools_menu.sizeHint().height()
        btn_width = self.tools_btn.width()

        btn_pos = self.tools_btn.mapToGlobal(QPoint(0, 0))
        x = btn_pos.x() + btn_width - menu_width

        y = btn_pos.y() - menu_height - 15

        self.tools_menu.exec(QPoint(x, y))

    def setup_actions_menu(self):
        self.actions_menu.setObjectName("actionsMenu")
        self.actions_menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.actions_menu.setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        actions = [
            ("Clear Console", self.clear_console),
            ("Terminate Run", self.handle_interrupt),
            ("Disconnect", lambda: self.run_func("exit")),
        ]

        for text, slot in actions:
            action = QAction(text, self)
            action.triggered.connect(slot)
            self.actions_menu.addAction(action)

    def show_actions_menu_above(self):
        menu_width = self.actions_menu.sizeHint().width()
        menu_height = self.actions_menu.sizeHint().height()
        btn_width = self.actions_btn.width()

        btn_pos = self.actions_btn.mapToGlobal(QPoint(0, 0))
        x = btn_pos.x() + btn_width - menu_width

        y = btn_pos.y() - menu_height - 15

        self.actions_menu.exec(QPoint(x, y))

    def dummy_func(self):
        print("Action: Auto Environment Setup triggered")

    def set_busy(self, busy):
        self.send_btn.setEnabled(not busy)
        self.input_field.setEnabled(not busy)
        if busy:
            self.send_btn.setText("Running...")
        else:
            self.send_btn.setText("  Run")

    def handle_connect(self):
        self.connect_func()

    def handle_send(self):
        text = self.input_field.text().strip()
        if not text: return
        self.input_field.clear()
        self.run_func(text)

    def handle_interrupt(self):
        self.manager.send_interrupt()

    def create_new_output_bubble(self):
        self.current_bubble = QLabel("")
        self.current_bubble.setWordWrap(True)
        if self.is_dark:
            self.current_bubble.setStyleSheet(
                "color: #fff; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px;"
                "font-size: 15px;")
        else:
            self.current_bubble.setStyleSheet(
                "color: #000; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px;"
                "font-size: 15px;")

        self.chat_layout.addSpacing(10)
        self.chat_layout.addWidget(self.current_bubble)
        self.chat_layout.addSpacing(10)

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
            self.status_dot.setStyleSheet(f"""
                background-color: #A3D671;
                border-radius: {self.status_size // 2}px;
            """)
        else:
            self.status_label.setText("Status: Disconnected")
            self.status_dot.setStyleSheet(f"""
                            background-color: #E58181;
                            border-radius: {self.status_size // 2}px;
                        """)

    def add_message(self, text):
        print(self.is_dark)
        lbl = MessageBubble(text)
        lbl.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        lbl.adjustSize()

        if not self.is_dark:
            lbl.set_light_mode()
        else:
            lbl.set_dark_mode()

        self.chat_layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignLeft)
        self.scroll.verticalScrollBar().setValue(
            self.scroll.verticalScrollBar().maximum()
        )

    def add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        if self.is_dark:
            line.setStyleSheet("color: #bbb; margin: 2px 0px;")
        else:
            line.setStyleSheet("color: #444; margin: 2px 0px;")
        # self.chat_layout.addSpacing(10)

        # self.chat_layout.addWidget(line)
        self.chat_layout.addSpacing(25)

    def clear_console(self):
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def strip_ansi_codes(self, text):
        # Disclaimer: This function was written by AI for accurate regex use.
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def set_light_mode(self):
        # self.top_bar.setStyleSheet("""
        #             QWidget{
        #                 background-color: #F2E9F9; font-size: 18px; color: #7D7D7D; border-radius: 7px; border: 1px solid #909090
        #             }
        #         """)
        self.top_bar.setStyleSheet("""
                            QWidget{
                                background: transparent; font-size: 18px; color: #7D7D7D; border-radius: 7px; border: none
                            }
                        """)
        self.dir_label.setStyleSheet("color: #3B3B3B; font-weight: 500; border: none;")
        self.status_label.setStyleSheet("color: #3B3B3B; font-weight: 500;")
        if self.status_label.text() == "Status: Disconnected":
            self.status_dot.setStyleSheet(f"""
                                background-color: #E58181;
                                border-radius: {self.status_size // 2}px;
                            """)
        else:
            self.status_dot.setStyleSheet(f"""
                                        background-color: #A3D671;
                                        border-radius: {self.status_size // 2}px;
                                    """)
        # self.container.setStyleSheet("""
        #             QWidget#MainOuterContainer {
        #                 background-color: #F3F3FA;
        #                 border: 1px solid #555555;
        #                 border-radius: 10px;
        #                 font-size: 16px;
        #             }
        #         """)
        self.scroll.setStyleSheet("""
                    QScrollArea {
                        border: none;
                        background-color: transparent;
                    }
                    QScrollBar {
                                            border: none;
                                            background: #E9E9E9;
                                            width: 0px;
                                            margin: 0px 0px 0px 0px;
                                            border-radius: 5px;
                                        }

                            QScrollBar::handle {
                                            background: #D7D7D7;
                                            min-height: 20px;
                                            border-radius: 8px;
                                            margin: 2px;
                                        }

                            QScrollBar::handle:hover {
                                            background: #CBCBCB;
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

        self.input_wrapper.setStyleSheet("""
                    #InputWrapper {
                        background-color: #ffffff;
                        border: 1px solid #dadce0;
                        border-radius: 24px;
                    }
                """)

        self.input_field.setStyleSheet("""
                    QLineEdit {
                        background: transparent;
                        color: #444;
                        border-radius: 10px;
                        padding: 8px;
                        font-size: 17px;
                        font-weight: 503;
                    }
                    
                """)
        self.send_btn.setStyleSheet("""
                    QPushButton {
                        background: transparent;
                        border-radius: 15px;
                        padding: 8px 20px;
                        color: #7c757e;
                        font-size: 17px;
                        font-weight: 510;
                        spacing: 10px;
                    }
                    QPushButton:hover { background-color: #E3CDF7; color: #222 }
                    QPushButton:pressed {background-color: #f3ebf3;}
                    """)
        self.send_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(8)
        # shadow.setXOffset(0)
        # shadow.setYOffset(0)
        # shadow.setColor(QColor(0, 0, 0, 80))

        # self.connect_btn.setGraphicsEffect(shadow)

        btn_style_sheet = """QPushButton {
                        background: transparent;
                        border-radius: 15px;
                        padding: 4px 15px;      /* Reduced horizontal padding */
                        color: #7c757e;
                        font-size: 17px;
                        font-weight: 510;
                        text-align: left;       /* Helps anchor the icon and text */
                        spacing: 15px;
                    }
                    QPushButton:hover { background-color: #f3ebf3; }
                    QPushButton:pressed{background-color: #f3ebf3;}
                    QPushButton::menu-indicator {
                                image: none;
                                width: 0px;
                            }
                    """
        # Set heights
        for btn in [self.tools_btn, self.actions_btn, self.connect_btn]:
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(btn_style_sheet)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            # shadow = QGraphicsDropShadowEffect()
            # shadow.setBlurRadius(8)
            # shadow.setXOffset(0)
            # shadow.setYOffset(0)
            # shadow.setColor(QColor(0, 0, 0, 80))
            #
            # btn.setGraphicsEffect(shadow)
            # btn.setGraphicsEffect(shadow)

        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            widget = item.widget()

            if widget is not None:
                if hasattr(widget, "set_light_mode"):
                    widget.set_light_mode()
                else:
                    widget.setStyleSheet(
                        "color: #000; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px;"
                        "font-size: 15px;")

        self.is_dark = False
        self.tools_btn.setStyleSheet(self.tools_btn.styleSheet() + """
                    QPushButton::menu-indicator {
                        image: none;
                        width: 0px;
                    }
                """)
        menu_ss = """
                QMenu {
                    background-color: #EDEBF3; 
                    border-radius: 10px;
                    padding: 8px 0px;
                    margin: -1px;
                }
                QMenu::item {
                    padding: 10px 20px;
                    font-size: 13.5px;
                    font-weight: 510;
                    color: #5D5D5D;
                    background-color: transparent;
                    margin: 2px 8px; 
                    border-radius: 6px;
                    cursor: pointer;
                }
                QMenu::item:selected {
                    background-color: #E5E2ED;
                    cursor: pointer;
                }
                QMenu::separator {
                    height: 1px;
                    background: #484848;
                    margin: 5px 15px;
                }
            """
        self.tools_menu.setStyleSheet(menu_ss)
        self.actions_menu.setStyleSheet(menu_ss)

        self.tools_btn.setIcon(QIcon(resource_path("gui/icons/wrench.png")))

        self.tools_btn.setIconSize(QSize(20, 20))
        self.actions_btn.setIcon(QIcon(resource_path("gui/icons/action.png")))
        self.actions_btn.setIconSize(QSize(20, 20))
        self.connect_btn.setIcon(QIcon(resource_path("gui/icons/link.png")))
        self.connect_btn.setIconSize(QSize(19, 19))
        self.send_btn.setIcon(QIcon(resource_path("gui/icons/send.png")))
        self.send_btn.setIconSize(QSize(19, 19))

    def set_dark_mode(self):
        self.is_dark = True
        print("Set dark: ", self.is_dark)
        self.top_bar.setStyleSheet("""
                                    QWidget{
                                        background: transparent; font-size: 18px; color: #AAA3AD; border-radius: 7px; border: none
                                    }
                                """)
        self.dir_label.setStyleSheet("color: #AAA3AD; font-weight: 500; border: none;")
        self.status_label.setStyleSheet("color: #AAA3AD; font-weight: 500;")
        if self.status_label.text() == "Status: Disconnected":
            self.status_dot.setStyleSheet(f"""
                                        background-color: #E58181;
                                        border-radius: {self.status_size // 2}px;
                                    """)
        else:
            self.status_dot.setStyleSheet(f"""
                                                background-color: #A3D671;
                                                border-radius: {self.status_size // 2}px;
                                            """)
        # self.container.setStyleSheet("""
        #             QWidget#MainOuterContainer {
        #                 background-color: #F3F3FA;
        #                 border: 1px solid #555555;
        #                 border-radius: 10px;
        #                 font-size: 16px;
        #             }
        #         """)
        self.input_wrapper.setStyleSheet("""
                    #InputWrapper {
                        background-color: #231E23;
                        border: 1px solid #231E23;
                        border-radius: 24px;
                    }
                """)
        self.scroll.setStyleSheet("""
                            QScrollArea {
                                border: none;
                                background-color: transparent;
                            }
                            QScrollBar {
                                                    border: none;
                                                    background: #E9E9E9;
                                                    width: 0px;
                                                    margin: 0px 0px 0px 0px;
                                                    border-radius: 5px;
                                                }

                                    QScrollBar::handle {
                                                    background: #D7D7D7;
                                                    min-height: 20px;
                                                    border-radius: 8px;
                                                    margin: 2px;
                                                }

                                    QScrollBar::handle:hover {
                                                    background: #CBCBCB;
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

        self.input_field.setStyleSheet("""
                            QLineEdit {
                                background: transparent;
                                color: #eee;
                                border-radius: 10px;
                                padding: 8px;
                                font-size: 17px;
                                font-weight: 503;
                            }

                        """)
        self.send_btn.setStyleSheet("""
                            QPushButton {
                                background: transparent;
                                border-radius: 15px;
                                padding: 8px 20px;
                                color: #978E97;
                                font-size: 17px;
                                font-weight: 510;
                                spacing: 10px;
                            }
                            QPushButton:hover { background-color: #3B2D48; color: #ddd }
                            QPushButton:pressed {background-color: #231E23;}
                            """)
        self.send_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        # shadow = QGraphicsDropShadowEffect()
        # shadow.setBlurRadius(8)
        # shadow.setXOffset(0)
        # shadow.setYOffset(0)
        # shadow.setColor(QColor(0, 0, 0, 80))

        # self.connect_btn.setGraphicsEffect(shadow)

        btn_style_sheet = """QPushButton {
                                background: transparent;
                                border-radius: 15px;
                                padding: 4px 15px;      /* Reduced horizontal padding */
                                color: #978E97;
                                font-size: 17px;
                                font-weight: 510;
                                text-align: left;       /* Helps anchor the icon and text */
                                spacing: 15px;
                            }
                            QPushButton:hover { background-color: #302C32; }
                            QPushButton:pressed{background-color: #231E23;}
                            QPushButton::menu-indicator {
                                        image: none;
                                        width: 0px;
                                    }
                            """
        # Set heights
        for btn in [self.tools_btn, self.actions_btn, self.connect_btn]:
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(btn_style_sheet)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            widget = item.widget()

            if widget is not None:
                if hasattr(widget, "set_dark_mode"):
                    widget.set_dark_mode()
                else:
                    widget.setStyleSheet(
                        "color: #eee; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px;"
                        "font-size: 15px; font-weight: 500;")

        self.tools_btn.setStyleSheet(self.tools_btn.styleSheet() + """
                            QPushButton::menu-indicator {
                                image: none;
                                width: 0px;
                            }
                        """)
        menu_ss = """
                        QMenu {
                            background-color: #231E23; 
                            border-radius: 10px;
                            border: 1.7px solid #111;
                            padding: 8px 0px;
                            margin: -1px;
                        }
                        QMenu::item {
                            padding: 10px 20px;
                            font-size: 13.5px;
                            font-weight: 510;
                            color: #AAA3AD;
                            background-color: transparent;
                            margin: 2px 8px; 
                            border-radius: 6px;
                            cursor: pointer;
                        }
                        QMenu::item:selected {
                            background-color: #302C32;
                            cursor: pointer;
                        }
                        QMenu::separator {
                            height: 1px;
                            background: #484848;
                            margin: 5px 15px;
                        }
                    """
        self.tools_menu.setStyleSheet(menu_ss)
        self.actions_menu.setStyleSheet(menu_ss)

        self.tools_btn.setIcon(QIcon(resource_path("gui/icons/wrench_dark.png")))
        self.tools_btn.setIconSize(QSize(20, 20))
        self.actions_btn.setIcon(QIcon(resource_path("gui/icons/action_dark.png")))
        self.actions_btn.setIconSize(QSize(20, 20))
        self.connect_btn.setIcon(QIcon(resource_path("gui/icons/link_dark.png")))
        self.connect_btn.setIconSize(QSize(19, 19))
        self.send_btn.setIcon(QIcon(resource_path("gui/icons/send_dark.png")))
        self.send_btn.setIconSize(QSize(19, 19))


class MessageBubble(QLabel):
    def __init__(self, parent=None):
        super(QLabel, self).__init__(parent)

    def set_light_mode(self):
        self.setStyleSheet("color: #111; padding: 2px; font-family: 'Consolas', 'Monospace', 'Courier New';"
                           "background-color: #F2ECF4; padding: 10px 10px; border-radius: 15px;"
                           "font-size: 16px; font-weight: 500;")

    def set_dark_mode(self):
        self.setStyleSheet("color: #eee; padding: 2px; font-family: 'Consolas', 'Monospace', 'Courier New';"
                           "background-color: #2D282E; padding: 10px 10px; border-radius: 15px;"
                           "font-size: 16px; font-weight: 500;")
