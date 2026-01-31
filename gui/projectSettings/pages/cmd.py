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

from PyQt6.QtCore import Qt, QTimer, QSize, QPoint
from PyQt6.QtGui import QPixmap, QCursor, QIcon, QColor, QAction
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QGraphicsDropShadowEffect, QMenu
)


class cmdPage(QWidget):
    def __init__(self, shared_manager, run_func, connect_func):
        super().__init__()
        # Use the manager and function passed from content.py
        self.manager = shared_manager
        self.run_func = run_func
        self.connect_func = connect_func
        self.is_dark = False
        self.initUI()

    def initUI(self):
        self.main_layout = QVBoxLayout(self)
        # 1. Remove the top margin of the main layout to let the bar touch the top
        self.main_layout.setContentsMargins(40, 40, 80, 55)
        self.main_layout.setSpacing(10)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ---- TOP BAR -----
        self.top_bar = QWidget()
        self.top_bar.setObjectName('top_bar')

        self.top_bar.setFixedHeight(40)

        # 3. Fix the internal layout margins (Remove the bottom 10px margin)
        self.top_tab_layout = QHBoxLayout(self.top_bar)
        self.top_tab_layout.setContentsMargins(20, 3, 20, 3)
        self.top_tab_layout.setSpacing(10)

        self.dir_label = QLabel("Current Directory: None")
        self.dir_label.setFixedHeight(20)
        self.top_tab_layout.addWidget(self.dir_label)
        self.top_tab_layout.addStretch(1)

        # Status Container
        self.status_container = QWidget()
        self.status_container.setFixedHeight(20)
        self.status_container.setStyleSheet("border: none;")
        self.status_layout = QHBoxLayout(self.status_container)
        self.status_layout.setContentsMargins(0, 0, 0, 0)
        self.status_layout.setSpacing(5)

        self.status_label = QLabel("Status: Disconnected")
        self.status_dot = QLabel()

        self.status_dot = QLabel()
        self.status_size = 12
        self.status_dot.setFixedSize(self.status_size, self.status_size)




        self.status_layout.addWidget(self.status_label)
        self.status_layout.addWidget(self.status_dot)

        self.top_tab_layout.addStretch()
        self.top_tab_layout.addWidget(self.status_container)

        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addSpacing(8)

        # ---- CONTAINER ----
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 20, 10, 10)
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

        self.input_field.setGraphicsEffect(shadow1)
        self.input_field.setPlaceholderText("Enter command...")
        self.input_field.setCursor(QCursor(Qt.CursorShape.IBeamCursor))


        self.send_btn = QPushButton("Run")
        self.connect_btn = QPushButton("Connect")
        self.actions_btn = QPushButton("Actions")
        self.actions_menu = QMenu(self)

        self.setup_actions_menu()

        self.tools_btn = QPushButton("Tools")
        self.tools_menu = QMenu(self)
        self.setup_tools_menu()

        # Connect the click to our custom positioning function
        self.tools_btn.clicked.connect(self.show_tools_menu_above)
        self.actions_btn.clicked.connect(self.show_actions_menu_above)







        self.input_bar.addWidget(self.input_field)
        self.input_bar.addWidget(self.send_btn)
        self.input_bar.addWidget(self.actions_btn)
        self.input_bar.addWidget(self.tools_btn)
        self.input_bar.addWidget(self.connect_btn)
        self.container_layout.addLayout(self.input_bar)

        # Connections
        self.send_btn.clicked.connect(self.handle_send)
        self.input_field.returnPressed.connect(self.handle_send)
        self.actions_btn.clicked.connect(self.handle_interrupt)
        self.connect_btn.clicked.connect(self.handle_connect)

    def setup_tools_menu(self):
        self.tools_menu.setObjectName("toolsMenu")
        self.tools_menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.tools_menu.setWindowFlags(
            Qt.WindowType.Popup |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.NoDropShadowWindowHint
        )
        actions = [
            ("Auto Environment Setup", self.dummy_func),
            ("Scan Dependency Imports", self.dummy_func),
            ("System Health Check", self.dummy_func),
            ("Clean Up Zombie Processes", self.dummy_func)
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
            ("Clear all Server Files", self.dummy_func),
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
        self.current_bubble = QLabel("")
        self.current_bubble.setWordWrap(True)
        if self.is_dark:
            self.current_bubble.setStyleSheet(
                "color: #fff; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px")
        else:
            self.current_bubble.setStyleSheet(
                "color: #000; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px")

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
        lbl = QLabel(text)
        lbl.setWordWrap(True)
        if self.is_dark:
            lbl.setStyleSheet("color: white; padding: 2px; font-family: 'Consolas', 'Monospace', 'Courier New';")
        else:
            lbl.setStyleSheet("color: black; padding: 2px; font-family: 'Consolas', 'Monospace', 'Courier New';")

        self.chat_layout.addWidget(lbl)
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

    def set_light_mode(self):
        self.top_bar.setStyleSheet("""
                    QWidget{
                        background-color: #F2E9F9; font-size: 18px; color: #7D7D7D; border-radius: 7px; border: 1px solid #909090
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
        self.container.setStyleSheet("""
                    QWidget#MainOuterContainer {
                        background-color: #F3F3FA;
                        border: 1px solid #555555;
                        border-radius: 10px;
                        font-size: 16px;
                    }
                """)
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
        self.chat_container.setStyleSheet("""
                        background-color: #F3F3FA;
                        font-size: 16px;
                """)
        self.input_field.setStyleSheet("""
                    QLineEdit {
                        background-color: #FAFAFF;
                        color: #535353;
                        border-radius: 10px;
                        border: 1px solid #909090;
                        padding: 8px;
                        font-size: 16px;
                    }
                    
                """)
        self.connect_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #D7E9B8;
                        border-radius: 10px;
                        padding: 8px 20px;
                        color: #324F34;
                        font-size: 18px;
                        font-weight: 520;
                    }
                    QPushButton:hover { background-color: #CCE2A7; }
                    QPushButton:pressed {background-color: #D7E9B8;}
                    """)
        self.connect_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))

        self.connect_btn.setGraphicsEffect(shadow)

        btn_style_sheet = """QPushButton {
                        background-color: #D6E3FF;
                        border-radius: 10px;
                        padding: 8px 20px;
                        color: #5A3583;
                        font-size: 18px;
                        font-weight: 520;
                    }
                    QPushButton:hover { background-color: #C6D8FF; }
                    QPushButton:pressed{background-color: #D6E3FF;}
                    QPushButton::menu-indicator {
                                image: none;
                                width: 0px;
                            }
                    """
        # Set heights
        for btn in [self.send_btn, self.tools_btn, self.actions_btn]:
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(btn_style_sheet)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QColor(0, 0, 0, 80))

            btn.setGraphicsEffect(shadow)
            btn.setGraphicsEffect(shadow)

        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            widget = item.widget()

            if widget is not None:
                # Apply your style here
                widget.setStyleSheet("color: #000; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px")

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

    def set_dark_mode(self):
        self.top_bar.setStyleSheet("""
                            QWidget{
                                background-color: #24222E; font-size: 18px; color: #D3D3D3; border-radius: 7px; border: 1px solid #484848
                            }
                        """)
        self.dir_label.setStyleSheet("color: #DFC5FF; font-weight: 500; border: none;")
        self.status_label.setStyleSheet("color: #DFC5FF; font-weight: 500;")
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
        self.container.setStyleSheet("""
                            QWidget#MainOuterContainer {
                                background-color: #1A1921;
                                border: 1px solid #484848;
                                border-radius: 10px;
                                font-size: 16px;
                            }
                        """)
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
        self.chat_container.setStyleSheet("""
                                background-color: #1A1921;
                                font-size: 16px;
                        """)
        self.input_field.setStyleSheet("""
                            QLineEdit {
                                background-color: #282632;
                                color: #9F9F9F;
                                border-radius: 10px;
                                border: 1px solid #525252;
                                padding: 8px;
                                font-size: 16px;
                            }
                            
                        """)
        self.connect_btn.setStyleSheet("""
                            QPushButton {
                                background-color: #313137;
                                border-radius: 10px;
                                padding: 8px 20px;
                                color: #A1FF92;
                                font-size: 18px;
                                font-weight: 510;
                            }
                            QPushButton:hover { background-color: #3C3C43; }
                            QPushButton:pressed{background-color: #313137;}
                            )
                            """)
        self.connect_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))

        self.connect_btn.setGraphicsEffect(shadow)
        btn_style_sheet = """QPushButton {
                                background-color: #313137;
                                border-radius: 10px;
                                padding: 8px 20px;
                                color: #C392FF;
                                font-size: 18px;
                                font-weight: 510;
                            }
                            QPushButton:hover { background-color: #3C3C43; }
                            QPushButton:pressed{background-color: #313137;}
                            QPushButton::menu-indicator {
                                image: none;
                                width: 0px;
                            }
                            """
        # Set heights
        for btn in [self.send_btn, self.tools_btn, self.actions_btn]:
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(btn_style_sheet)
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(8)
            shadow.setXOffset(0)
            shadow.setYOffset(0)
            shadow.setColor(QColor(0, 0, 0, 0))

            btn.setGraphicsEffect(shadow)
            btn.setGraphicsEffect(shadow)

        for i in range(self.chat_layout.count()):
            item = self.chat_layout.itemAt(i)
            widget = item.widget()

            if widget is not None:
                # Apply your style here
                widget.setStyleSheet("color: #fff; font-family: 'Consolas', 'Monospace', 'Courier New'; margin-left:2px")
        self.is_dark = True
        menu_ss = """
        QMenu {
            background-color: #24222E; 
            border-radius: 12px;
            padding: 8px 0px;
            margin: -1px;
        }
        QMenu::item {
            padding: 10px 20px;
            font-size: 13.5px;
            font-weight: 510;
            color: #D3D3D3;
            background-color: transparent;
            margin: 2px 8px; 
            border-radius: 6px;
            cursor: pointer;
        }
        QMenu::item:selected {
            background-color: #353340;
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
