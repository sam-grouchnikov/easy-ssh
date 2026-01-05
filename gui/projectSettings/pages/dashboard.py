from datetime import datetime

from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QGridLayout, QMessageBox, QFrame
)
from PyQt6.QtCore import Qt
import database.database_crud as db_crud


class Dashboard(QWidget):
    def __init__(self, config):
        super().__init__()
        self.inputs = {}

        layout = QVBoxLayout()
        self.conn_card = ConnectionCard(config)

        layout.addWidget(self.init_ui(config))
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.setLayout(layout)

    def init_ui(self, config):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0,0,0,0)

        # --- ROW 1 ---
        row1 = QHBoxLayout()


        row1.addWidget(self.conn_card)
        row1.addWidget(ClusterInfo())
        row1.addWidget(RecentlyEdited(config))

        main_layout.addLayout(row1)

        return main_widget

class ConnectionCard(QWidget):
    def __init__(self, config):
        super().__init__()
        self.init_ui(config)

    def init_ui(self, config):
        main_layout = QVBoxLayout(self)


        self.wrapper = QWidget()
        self.wrapper.setStyleSheet("background-color: #16161A; border-radius: 12px")

        # Set card style
        layout = QVBoxLayout(self.wrapper)
        layout.setSpacing(8)
        layout.setContentsMargins(35, 15, 35, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        title = QLabel("Connection Details")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)

        layout.addSpacing(4)
        # SSH Destination Header
        conn_static_label = QLabel(f"SSH Destination: {config.get("sshcon")}")
        conn_static_label.setStyleSheet("font-size: 15px; color: #BDBDBD")
        layout.addWidget(conn_static_label)

        layout.addSpacing(4)

        # Status Label
        self.status_label = QLabel("Status: Disconnected")
        self.status_label.setStyleSheet("font-size: 15px; color: #BDBDBD")
        layout.addWidget(self.status_label)
        layout.addSpacing(2)

        # The Border Line
        self.border = QFrame()
        self.border.setFrameShape(QFrame.Shape.HLine)
        self.border.setFixedHeight(4)
        self.border.setStyleSheet("background-color: #941E1E; border-radius: 5px")
        layout.addWidget(self.border)

        layout.addSpacing(4)

        # Last Run
        recent_runs = config.get("recentruns")
        if not recent_runs:
            self.last_run_label = QLabel(f"Last run: N/A")
        else:
            now = datetime.now()
            date = now.strftime("%B %d, %Y")
            time = now.strftime("%I:%M %p")
            self.last_run_label = QLabel(f"Last run: {date} at {time}")

        self.last_run_label.setStyleSheet("font-size: 14px; color: #D0D0D0")
        layout.addWidget(self.last_run_label)
        main_layout.addWidget(self.wrapper)

    # --- Methods to update the card dynamically ---
    def update_connection_status(self, connected: bool):
        if connected:
            self.status_label.setText("Status: Connected")
            self.border.setStyleSheet("background-color: #1E970E; border-radius: 5px")
        else:
            self.status_label.setText("Status: Disconnected")
            self.border.setStyleSheet("background-color: #941E1E; border-radius: 5px")

class ClusterInfo(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        self.wrapper = QWidget()
        self.wrapper.setStyleSheet("background-color: #16161A; border-radius: 12px")

        # Set card style
        layout = QVBoxLayout(self.wrapper)
        layout.setSpacing(8)
        layout.setContentsMargins(35, 15, 35, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)



        # Title
        title = QLabel("GPU Info")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)
        layout.addSpacing(4)

        # SSH Destination Header
        type_title = QLabel("GPU Type : Nvidia RTX 3090")
        type_title.setStyleSheet("font-size: 15px; color: #BDBDBD")
        layout.addWidget(type_title)
        layout.addSpacing(4)


        # Status Label
        self.gpu_count = QLabel("GPU Count: 3")
        self.gpu_count.setStyleSheet("font-size: 15px; color: #BDBDBD")
        layout.addWidget(self.gpu_count)
        layout.addSpacing(4)


        # Last Run
        self.available_memory = QLabel("Memory Available: 91GB")
        self.available_memory.setStyleSheet("font-size: 15px; color: #BDBDBD")
        layout.addWidget(self.available_memory)
        main_layout.addWidget(self.wrapper)

class RecentlyEdited(QWidget):
    def __init__(self, config):
        super().__init__()
        self.init_ui(config)

    def init_ui(self, config):
        recent_runs = config.get("recentruns")

        main_layout = QVBoxLayout(self)

        self.wrapper = QWidget()
        self.wrapper.setStyleSheet("background-color: #16161A; border-radius: 12px")

        # Set card style
        layout = QVBoxLayout(self.wrapper)
        layout.setSpacing(8)
        layout.setContentsMargins(35, 15, 35, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        title = QLabel("Recent Runs")
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        layout.addWidget(title)
        layout.addSpacing(4)

        self.recent_runs_widget = QWidget()
        self.recent_runs_layout = QVBoxLayout(self.recent_runs_widget)
        self.recent_runs_layout.setContentsMargins(0, 0, 0, 0)

        if recent_runs:
            for item in recent_runs[:3]:
                label = QLabel(f"{item[0]} on {item[1]} at {item[2]}")
                label.setStyleSheet("font-size: 15px; color: #BDBDBD")
                self.recent_runs_layout.addWidget(label)
                self.recent_runs_layout.addSpacing(3)
        else:
            label = QLabel("No Recent Runs")
            self.recent_runs_layout.addWidget(label)
            label.setStyleSheet("font-size: 15px; color: #BDBDBD")

        self.recent_runs_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        layout.addWidget(self.recent_runs_widget)


        main_layout.addWidget(self.wrapper)

