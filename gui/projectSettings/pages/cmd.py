from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QScrollArea, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt


class cmdPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
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

        input_bar.addWidget(self.input_field)
        input_bar.addWidget(self.send_btn)
        input_bar.addWidget(self.clear_btn)

        container_layout.addLayout(input_bar)

        # Connect enter key + button
        self.send_btn.clicked.connect(self.handle_send)
        self.clear_btn.clicked.connect(self.clear_console)

        self.input_field.returnPressed.connect(self.handle_send)

    # ---- Add message to chat ----
    def add_message(self, text, sender):
        bubble = QLabel(text)
        bubble.setWordWrap(True)
        bubble.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Shared style for both user and system
        bubble.setStyleSheet("""
            color: white;
            padding: 0px;
            margin-left: 0px;
            font-size: 14px;
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


    # ---- Handle user sending a message ----
    def handle_send(self):
        text = self.input_field.text().strip()
        if not text:
            return

        self.add_message(text, "user")

        self.add_message("Simulated output for: " + text, "system")

        spacer = QWidget()
        spacer.setFixedHeight(5)
        self.chat_layout.addWidget(spacer)
        self.input_field.clear()

    def clear_console(self):
        while self.chat_layout.count():
            item = self.chat_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()