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
from gui.projectSettings.pages.dashboard import Dashboard
from datetime import datetime

PAGE_NAMES = [
    "Dashboard",
    "File Tree",
    "Terminal",
    "Simple SSH",
    "Logged Metrics",
    "Project Settings",
]


def setupContent(self, layout: QVBoxLayout, config):

    # 1. Initialize the SHARED SSH Manager
    if config.is_complete():
        path = config.get("sshcon")
        user = path.split('@')[0]
        server = path.split('@')[1]
        psw = config.get("sshpsw")
        port = config.get("sshport")
        self.ssh_manager = SSHManager(server, user, port, psw)
    else:
        self.ssh_manager = None

    # 2. Define the SHARED Logic for running commands
    def global_handle_connect():
        success, msg = self.ssh_manager.connect()

        self.cmd_page.add_message(f"System: {msg}")
        self.simple_ssh_page.update_connection_status(success)
        self.cmd_page.update_connection_status(success)
        self.dashboard.conn_card.update_connection_status(success)

        if success:
            # THREADED: This won't freeze the app anymore
            print("Running find")
            find_cmd = "find . -not -path '*/.*' -not -path '*__pycache__*' -not -path '*venv*' -not -path '*wandb*'"
            global_run_command(find_cmd, is_tree_update=True)

            # Keep directory sync silent
            new_path = self.ssh_manager.get_pwd_silently()
            self.simple_ssh_page.update_directory_display(new_path)
            self.cmd_page.update_directory_display(new_path)

    self.tree_data_accumulator = ""

    def accumulate_tree_data(text):
        self.tree_data_accumulator += text
    def global_run_command(command, is_tree_update=False, is_file_read=False, is_gpu_check=False, is_gpu_mem=False):
        # 1. Don't run if already busy

        if command == "exit":
            self.cmd_page.add_message("$ exit")
            self.cmd_page.add_message("System: Closing connection...")

            # 1. Close the backend connection
            self.ssh_manager.close()

            # 2. Update the UI Status
            self.simple_ssh_page.update_connection_status(False)
            self.cmd_page.update_connection_status(False)
            self.dashboard.conn_card.update_connection_status(False)
            self.cmd_page.add_message("System: Disconnected.")

            self.simple_ssh_page.update_directory_display("None")
            self.cmd_page.update_directory_display("None")
            return

        if command.startswith("python") or command.startswith("python3"):
            now = datetime.now()
            date = now.strftime("%B %d, %Y")
            time = now.strftime("%I:%M %p")
            if "-m" in command:
                file = command.split(" ")[2].split(".")[1] + ".py"
            else:
                file = command.split(" ")[1]

            config.add_run([file, date, time])

        if command == "Ctrl+C":
            self.ssh_manager.send_interrupt()
            return

        if command.startswith("cd"):
            self.cmd_page.add_message("System: Successfully changed directory")
            self.simple_ssh_page.console.update_output("System: Successfully changed directory")

        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            return

        if not any([is_tree_update, is_file_read]) and command != "exit":
            # The semicolon ensures this runs even if the first command fails
            # We use a unique marker 'SYNC_DIR:'
            actual_command = f"{command} && echo 'SYNC_DIR:'$(pwd) || echo 'SYNC_DIR:'$(pwd)"
        else:
            actual_command = command

            # 2. Create the worker with the augmented command

        self.worker = SSHStreamWorker(self.ssh_manager, actual_command)
        # 3. Create Worker
        print(f"Tree: {is_tree_update}, GPU check: {is_gpu_check}, GPU mem: {is_gpu_mem}")

        if is_tree_update:
            self.tree_data_accumulator = ""

            self.worker.output_received.connect(accumulate_tree_data)

            self.worker.finished.connect(
                lambda: self.file_tree_page.rebuild_tree(self.tree_data_accumulator),
                Qt.ConnectionType.QueuedConnection
            )
        elif is_file_read:
            # Clear the editor first
            self.file_tree_page.editor.clear()
            # Connect output DIRECTLY to the editor's append function
            self.worker.output_received.connect(self.file_tree_page.display_file_content)
        else:
            # Normal terminal behavior
            self.cmd_page.create_new_output_bubble()
            self.worker.output_received.connect(self.cmd_page.update_live_output)
            self.worker.output_received.connect(self.simple_ssh_page.console.update_output)

        self.worker.finished.connect(global_finished)

        self.worker.start()

    def global_finished():
        self.cmd_page.on_command_finished()
        self.simple_ssh_page.console.finish_command()


    # ---- UI Setup ----
    self.title_label = QLabel()
    self.title_label.setStyleSheet(
        "color: white; font-size: 35px; font-weight: bold; padding-left: 10px;"
    )
    layout.addWidget(self.title_label)

    nav = navbar()
    nav.setContentsMargins(10, 0, 0, 0)
    nav.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    layout.addWidget(nav)

    self.stack = QStackedWidget(self)

    # 3. Create the pages with the shared dependencies
    self.cmd_page = cmdPage(self.ssh_manager, global_run_command, global_handle_connect)

    self.simple_ssh_page = SimpleSSHPage(global_run_command, global_handle_connect)
    self.dashboard = Dashboard(config)
    self.file_tree_page = FileTreePage(global_run_command)

    # Add pages to the stack
    self.stack.addWidget(self.dashboard)
    self.stack.addWidget(self.file_tree_page)  # Index 0
    self.stack.addWidget(self.cmd_page)  # Index 1
    self.stack.addWidget(self.simple_ssh_page)  # Index 2
    self.stack.addWidget(GraphsPage())  # Index 3
    self.stack.addWidget(SettingsPage(config))  # Index 4

    self.stack.setContentsMargins(10, 0, 25, 20)
    layout.addWidget(self.stack)

    # ---- Navigation Logic ----
    def update_title(index: int):
        user = config.get("user")
        if user == "":
            self.title_label.setText("Welcome to Easy-SSH!")
        else:
            self.title_label.setText(f"Welcome back, {config.get("user")}")

    for index, item in enumerate(nav.nav_items):
        item.clicked.connect(
            lambda _, i=index: self.stack.setCurrentIndex(i)
        )

    self.stack.currentChanged.connect(update_title)
    self.stack.setCurrentIndex(0)
    update_title(0)