from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QSizePolicy, QStackedWidget
)
from PyQt6.QtCore import Qt
from gui.navbar import navbar
from gui.projectSettings.pages.FileTree import FileTreePage
from gui.projectSettings.pages.graphs import GraphsPage
from gui.projectSettings.pages.settings import SettingsPage
from gui.projectSettings.pages.SimpleSSH import SimpleSSHPage
from gui.projectSettings.pages.cmd import cmdPage
from backend.ssh.sshManager import SSHStreamWorker, SSHManager

PAGE_NAMES = [
    "File Tree",
    "Terminal",
    "Simple SSH",
    "Logged Metrics",
    "Project Settings"
]


def setupContent(self, layout: QVBoxLayout, project_name):
    # 1. Initialize the SHARED SSH Manager
    self.ssh_manager = SSHManager("10.80.10.96", "sam", "vera1986", 2023)

    # 2. Define the SHARED Logic for running commands
    def global_run_command(command):
        # 1. Don't run if already busy
        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            return

        # 2. Basic UI Updates
        self.cmd_page.set_busy(True)
        self.simple_ssh_page.set_busy(True)
        self.cmd_page.add_message(f"$ {command}")
        self.cmd_page.create_new_output_bubble()
        self.simple_ssh_page.console.add_command_line(command)

        # 3. Create Worker (Assigned to self to prevent crash)
        self.worker = SSHStreamWorker(self.ssh_manager, command)

        self.worker.output_received.connect(
            self.cmd_page.update_live_output,
            Qt.ConnectionType.QueuedConnection
        )
        self.worker.output_received.connect(
            self.simple_ssh_page.console.update_output,
            Qt.ConnectionType.QueuedConnection
        )
        self.worker.finished.connect(
            global_finished,
            Qt.ConnectionType.QueuedConnection
        )

        self.worker.start()

    def global_finished():
        self.cmd_page.on_command_finished()

        self.simple_ssh_page.console.finish_command()
        self.simple_ssh_page.on_command_finished()

    # ---- UI Setup ----
    self.title_label = QLabel()
    self.title_label.setStyleSheet(
        "color: white; font-size: 35px; font-weight: bold; padding-left: 10px;"
    )
    layout.addWidget(self.title_label)

    nav = navbar()
    nav.setContentsMargins(10, 0, 20, 0)
    nav.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    layout.addWidget(nav)

    self.stack = QStackedWidget(self)

    # 3. Create the pages with the shared dependencies
    self.cmd_page = cmdPage(project_name, self.ssh_manager, global_run_command)
    self.simple_ssh_page = SimpleSSHPage(global_run_command)

    # Add pages to the stack
    self.stack.addWidget(FileTreePage("/gui/projectSettings"))  # Index 0
    self.stack.addWidget(self.cmd_page)  # Index 1
    self.stack.addWidget(self.simple_ssh_page)  # Index 2
    self.stack.addWidget(GraphsPage(project_name))  # Index 3
    self.stack.addWidget(SettingsPage(project_name))  # Index 4

    self.stack.setContentsMargins(10, 0, 25, 20)
    layout.addWidget(self.stack)

    # ---- Navigation Logic ----
    def update_title(index: int):
        self.title_label.setText(f"{project_name} - {PAGE_NAMES[index]}")

    for index, item in enumerate(nav.nav_items):
        item.clicked.connect(
            lambda _, i=index: self.stack.setCurrentIndex(i)
        )

    self.stack.currentChanged.connect(update_title)
    self.stack.setCurrentIndex(0)
    update_title(0)