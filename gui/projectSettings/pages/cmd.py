from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
import re


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
        main_layout.setContentsMargins(10, 0, 15, 20)
        main_layout.setSpacing(10)
        # ---- TOP BAR -----
        top_bar = QWidget()
        top_bar.setStyleSheet(
            "background-color: #1F1F1F; font-size: 18px; color: #7D7D7D; border-radius: 5px"
        )
        top_bar.setContentsMargins(0, 0, 0, 0)
        top_tab_layout = QHBoxLayout(top_bar)

        self.dir_label = QLabel("Current Directory: None")
        top_tab_layout.addWidget(self.dir_label)

        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)

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
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(10)
        container.setStyleSheet("""
            background-color: #18181F;
            border: 1px solid #555555;
            border-radius: 10px;
            font-size: 16px;
        """)
        main_layout.addWidget(container)

        # ---- CHAT SCROLL AREA ----
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none;")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(4)

        self.scroll.setWidget(self.chat_container)
        container_layout.addWidget(self.scroll)

        # ---- INPUT BAR ----
        input_bar = QHBoxLayout()
        input_bar.setSpacing(10)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter command...")
        self.input_field.setStyleSheet("""
            QLineEdit {
                background-color: #121217;
                color: white;
                border-radius: 5px;
                border: 1px solid #555;
                padding: 8px;
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
                background-color: #451C4B;
                border-radius: 5px;
                padding: 8px 20px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #53195C; }
            QPushButton:disabled {
                background-color: #2A2A2A;
                color: #666;
            }
        """)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setStyleSheet("background-color: #7B1818; color: white; border-radius: 5px; padding: 8px 20px;")

        self.end_btn = QPushButton("Ctrl + C")
        self.end_btn.setStyleSheet("background-color: #540F0F; color: white; border-radius: 5px; padding: 8px 20px;")

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setStyleSheet(
            "background-color: #134419; color: white; border-radius: 5px; padding: 8px 20px;")

        # Set heights
        for btn in [self.send_btn, self.clear_btn, self.end_btn, self.connect_btn, self.input_field]:
            btn.setFixedHeight(42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        input_bar.addWidget(self.input_field)
        input_bar.addWidget(self.send_btn)
        input_bar.addWidget(self.connect_btn)
        input_bar.addWidget(self.clear_btn)
        input_bar.addWidget(self.end_btn)
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
        self.add_message("System: Sent Ctrl+C (Interrupt)")

    def create_new_output_bubble(self):
        """Prepare the bubble for incoming stream data."""
        self.current_bubble = QLabel("")
        self.current_bubble.setWordWrap(True)
        self.current_bubble.setStyleSheet("color: #CCC; font-family: 'Consolas', 'Courier New';")
        self.chat_layout.addWidget(self.current_bubble)

    def update_live_output(self, raw_text):
        if not hasattr(self, 'current_bubble') or self.current_bubble is None:
            return

        try:
            clean_text = self.strip_ansi_codes(raw_text)
            if not clean_text:
                return

            # Check if this is a progress bar situation
            # We only want to overwrite (\r) if it's a known progress bar type
            is_progress_bar = any(word in clean_text.lower() for word in ["epoch", "step", "%", "it/s"])

            if '\r' in clean_text and is_progress_bar:
                # OVERWRITE MODE (Progress bars)
                parts = clean_text.split('\r')
                latest_update = parts[-1]
                if latest_update.strip():
                    self.current_bubble.setText(latest_update)
            else:
                # APPEND MODE (nvidia-smi, ls, cat, etc.)
                current = self.current_bubble.text()

                # If the current bubble is empty and we are starting a table,
                # make sure we use a monospace font for nvidia-smi alignment
                self.current_bubble.setText(current + clean_text)

            # Force scroll to bottom
            self.scroll.verticalScrollBar().setValue(
                self.scroll.verticalScrollBar().maximum()
            )

        except RuntimeError:
            self.current_bubble = None

    def on_command_finished(self):
        self.set_busy(False)
        if hasattr(self, 'current_bubble'):
            current = self.current_bubble.text()
            self.current_bubble.setText(current + "\n\n[Command Finished]")
        self.add_separator()
        self.input_field.setFocus()

    def update_directory_display(self, path):
        clean_path = path.strip()
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
        lbl.setStyleSheet("color: white; padding: 2px;")
        self.chat_layout.addWidget(lbl)
        self.add_separator()

    def add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #444; margin: 2px 0px;")
        self.chat_layout.addWidget(line)

    def clear_console(self):
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def strip_ansi_codes(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)