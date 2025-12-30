from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt
from backend.ssh.sshManager import SSHManager, SSHStreamWorker

class cmdPage(QWidget):
    def __init__(self, project_name):
        super().__init__()
        self.manager = SSHManager("10.80.10.96", "sam", "", 2023)
        self.initUI(project_name)

    def initUI(self, project_name):
        # Main vertical layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 20, 15, 20)
        main_layout.setSpacing(0)

        # ---- CONTAINER FOR CHAT + INPUT ----
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
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        self.chat_container = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.chat_layout.setSpacing(4)

        scroll.setWidget(self.chat_container)
        container_layout.addWidget(scroll)

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
                font-size: 16px;
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
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #53195C;
            }
        """)
        self.input_field.setFixedHeight(42)
        self.send_btn.setFixedHeight(42)

        self.clear_btn = QPushButton("Clear")
        self.clear_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B1818;
                border-radius: 5px;
                padding: 8px 20px;
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #941E1E;
            }
        """)
        self.clear_btn.setFixedHeight(42)

        self.end_btn = QPushButton("Ctrl + C")
        self.end_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.end_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #540F0F;
                        border-radius: 5px;
                        padding: 8px 20px;
                        color: white;
                        font-weight: bold;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #5B1111;
                    }
                """)
        self.end_btn.setFixedHeight(42)
        def interrupt():
            self.manager.send_interrupt()
            self.add_message(f"Successfully ended process")

        self.end_btn.clicked.connect(interrupt)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.connect_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #134419;
                        border-radius: 5px;
                        padding: 8px 20px;
                        color: white;
                        font-weight: bold;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background-color: #164E1D;
                    }
                """)
        self.connect_btn.setFixedHeight(42)
        def connect_ssh():
            self.manager.connect()
            from database.database_crud import get_project
            proj = get_project(project_name)
            self.add_message(f"Successfully connected to {proj['ssh_path']}")
        self.connect_btn.clicked.connect(connect_ssh)

        input_bar.addWidget(self.input_field)
        input_bar.addWidget(self.send_btn)
        input_bar.addWidget(self.connect_btn)
        input_bar.addWidget(self.clear_btn)
        input_bar.addWidget(self.end_btn)

        container_layout.addLayout(input_bar)

        # Connect enter key + button
        self.send_btn.clicked.connect(self.handle_send)
        self.clear_btn.clicked.connect(self.clear_console)

        self.input_field.returnPressed.connect(self.handle_send)

    def add_message(self, text):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Shared style for both user and system
        bubble.setStyleSheet("""
            color: white;
            padding: 0px;
            margin-left: 0px;
        """)

        # Wrap in HBoxLayout, left-aligned
        wrapper = QHBoxLayout()
        wrapper.setAlignment(Qt.AlignmentFlag.AlignLeft)
        wrapper.setContentsMargins(0, 0, 0, 0)
        wrapper.addWidget(bubble)

        container = QWidget()
        container.setLayout(wrapper)

        self.chat_layout.addWidget(container)

        # ---- Add horizontal line ----
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        line.setStyleSheet("color: #555555; margin-top: 4px; margin-bottom: 4px;")
        self.chat_layout.addWidget(line)

    def handle_send(self):
        text = self.input_field.text().strip()
        if not text: return
        self.input_field.clear()

        if not self.manager.is_active():
            self.add_message("Error: SSH connection not active.")
            return

        # Add the "User command" bubble first
        self.add_message(f"$ {text}")

        # Create a new bubble for the server's response
        self.current_bubble = QLabel("")
        self.current_bubble.setWordWrap(True)
        self.chat_layout.addWidget(self.current_bubble)

        # Start the background worker
        self.worker = SSHStreamWorker(self.manager, text)
        self.worker.output_received.connect(self.update_live_output)
        self.worker.finished.connect(self.on_command_finished)
        self.worker.start()

        self.send_btn.setEnabled(False)

    def update_live_output(self, raw_text):
        # Clean ANSI (colors) and trailing prompts
        text = self.strip_ansi_codes(raw_text)
        self.current_bubble.setText(text)


    def on_command_finished(self):
        self.send_btn.setEnabled(True)
        self.add_separator()
        if self.current_bubble:
            current_text = self.current_bubble.text()
            self.current_bubble.setText(current_text + "\n--- Command Finished---\n")

    def strip_ansi_codes(self, text):
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)

    def add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #555555; margin: 5px 0px;")
        self.chat_layout.addWidget(line)

    def clear_console(self):
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def get_clean_output(raw_output, command_sent):
        # 1. Split into lines
        lines = raw_output.splitlines()

        # 2. Remove the First Line (The Echo)
        # We check if the first line starts with our command to be safe
        if lines and command_sent in lines[0]:
            lines.pop(0)

        # 3. Remove the Last Line (The Prompt)
        # Most Linux prompts end with $ or #
        if lines and (lines[-1].strip().endswith('$') or lines[-1].strip().endswith('#')):
            lines.pop(-1)

        return "\n".join(lines).strip()
