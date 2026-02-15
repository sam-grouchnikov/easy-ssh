#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.2.1
Email: sam.grouchnikov@gmail.com
Status: Development
"""

from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
)


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
        main_layout.setContentsMargins(0, 0, 0, 0)

        # --- ROW 1 ---
        row1 = QHBoxLayout()

        self.cluster_info = ClusterInfo()
        row1.addWidget(self.conn_card)
        row1.addWidget(self.cluster_info)
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
        self.main_layout = QVBoxLayout(self)

        self.wrapper = QWidget()
        self.wrapper.setStyleSheet("background-color: #16161A; border-radius: 12px")

        # Set card style
        self.layout = QVBoxLayout(self.wrapper)
        self.layout.setSpacing(8)
        self.layout.setContentsMargins(35, 15, 35, 20)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Title
        self.title = QLabel("GPU Info")
        self.title.setStyleSheet("font-size: 22px; font-weight: bold;")
        self.layout.addWidget(self.title)
        self.layout.addSpacing(4)

        # SSH Destination Header
        self.type_title = QLabel("GPU Type : Fetched on connect")
        self.type_title.setStyleSheet("font-size: 15px; color: #BDBDBD")
        self.layout.addWidget(self.type_title)
        self.layout.addSpacing(4)

        # Status Label
        self.gpu_count = QLabel("GPU Count: Fetched on connect")
        self.gpu_count.setStyleSheet("font-size: 15px; color: #BDBDBD")
        self.layout.addWidget(self.gpu_count)
        self.layout.addSpacing(4)

        # Last Run
        self.available_memory = QLabel("Memory Available: Fetched on connect")
        self.available_memory.setStyleSheet("font-size: 15px; color: #BDBDBD")
        self.layout.addWidget(self.available_memory)
        self.main_layout.addWidget(self.wrapper)

    def handle_gpu_info(self, output):
        print(output)
        gpus = [line.strip() for line in output.strip().split('\n') if line.strip()]
        count = len(gpus)
        type = gpus[0]
        self.cluster_info.type_title.setText(f"GPU Type: {type}")
        self.cluster_info.gpu_count.setText(f"GPU Count: {count}")

    def handle_gpu_mem(self, output):
        print("Getting output in function")
        print("Output:", output)
        if not output.strip() or "not found" in output.lower():
            return

        try:
            mem_values = [int(line.strip()) for line in output.strip().split('\n') if line.strip().isdigit()]

            total_free_mib = sum(mem_values)
            total_free_gb = total_free_mib / 1024

            self.cluster_info.available_memory.setText(f"Memory available: {total_free_gb:.2f} GB")

        except Exception as e:
            print(f"Error parsing GPU memory: {e}")


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
            for item in reversed(recent_runs[-3:]):
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
