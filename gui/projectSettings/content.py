#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.0.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""

from datetime import datetime

from PyQt6.QtCore import Qt, QCoreApplication
from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QSizePolicy, QStackedWidget
)

from backend.ssh.sshManager import SSHStreamWorker, SSHManager
from gui.navbar import navbar
from gui.projectSettings.pages.FileTree import FileTreePage
from gui.projectSettings.pages.SimpleSSH import SimpleSSHPage
from gui.projectSettings.pages.cmd import cmdPage
from gui.projectSettings.pages.graphs import GraphsPage
from gui.projectSettings.pages.settings import SettingsPage

PAGE_NAMES = [
    "Terminal",
    "Simple SSH",
    "File Tree",
    "Logged Metrics",
    "Project Settings",
]


def setupContent(self, layout: QVBoxLayout):
    if self.config.is_complete():
        path = self.config.get("sshcon")
        user = path.split('@')[0]
        server = path.split('@')[1]
        psw = self.config.get("sshpsw")
        port = self.config.get("sshport")
        self.ssh_manager = SSHManager(server, user, port, psw)
    else:
        self.ssh_manager = None
    self.home_dir = None
    self.current_dir = None
    self.recent_cmd = None

    def global_handle_connect():
        self.simple_ssh_page.action_menu.ssh_con_btn.setText("Connecting")
        self.cmd_page.connect_btn.setText("Connecting")
        QCoreApplication.processEvents()
        self.settings_page.load_project_data()
        if self.ssh_manager is None and self.config.get("user") != "":
            path_new = self.config.get("sshcon")
            user_new = path_new.split('@')[0]
            server_new = path_new.split('@')[1]
            psw_new = self.config.get("sshpsw")
            port_new = self.config.get("sshport")
            self.ssh_manager = SSHManager(server_new, user_new, port_new, psw_new)
            print(self.ssh_manager)

        success, msg = self.ssh_manager.connect()
        self.cmd_page.add_message(f"System: {msg}")
        self.cmd_page.add_separator()
        self.simple_ssh_page.console.update_output(f"System: {msg}\n\n")
        self.simple_ssh_page.update_connection_status(success)
        self.cmd_page.update_connection_status(success)

        if success:
            # 1. Get the path first so we know where we are
            new_path = self.ssh_manager.get_pwd_silently()
            self.home_dir = new_path
            self.current_dir = new_path

            self.simple_ssh_page.console.finish_command(single=True)

            # 2. Update UI displays
            self.file_tree_page.update_home(new_path)
            self.simple_ssh_page.update_directory_display(new_path)
            self.cmd_page.update_directory_display(new_path)
            print("Start clone")
            if self.config.get("cloned") == "no":
                git_url = self.config.get("giturl")

                if git_url:
                    global_run_command(f"git clone {git_url}", is_git_clone=True)
                    self.config.set("cloned", "yes")
            print("End clone")
            find_cmd = "find . -not -path '*/.*' -not -path '*__pycache__*' -not -path '*venv*' -not -path '*wandb*'"
            print("Tree update")
            global_run_command(find_cmd, is_tree_update=True)
            print("Tree update done")

            new_path = self.ssh_manager.get_pwd_silently()
            self.home_dir = new_path
            self.file_tree_page.update_home(new_path)
            self.current_dir = new_path
            self.simple_ssh_page.update_directory_display(new_path)
            self.cmd_page.update_directory_display(new_path)
            self.cmd_page.connect_btn.setText("Connect")
            self.cmd_page.connect_btn.setEnabled(False)
            self.simple_ssh_page.action_menu.ssh_con_btn.setText("Connect to SSH")
            self.simple_ssh_page.action_menu.ssh_con_btn.setEnabled(False)
            self.simple_ssh_page.action_menu.run_curr_btn.setEnabled(True)
            self.cmd_page.send_btn.setEnabled(True)
        else:
            self.cmd_page.connect_btn.setText("Connect")

    def update_tree():
        find_cmd = "find . -not -path '*/.*' -not -path '*__pycache__*' -not -path '*venv*' -not -path '*wandb*'"
        global_run_command(find_cmd, is_tree_update=True)

    self.tree_data_accumulator = ""

    def accumulate_tree_data(text):
        self.tree_data_accumulator += text

    def global_run_command(command, is_tree_update=False, is_file_read=False, is_file_save=False, is_git_clone=False):
        # 1. Don't run if already busy
        self.recent_cmd = command
        print("Command: ", command)
        self.cmd_page.send_btn.setEnabled(False)
        self.simple_ssh_page.action_menu.run_curr_btn.setEnabled(False)

        if command == "exit":
            self.cmd_page.add_message("$ exit\nSystem: Disconnected")

            # 1. Close the backend connection
            self.ssh_manager.close()

            # 2. Update the UI Status
            self.simple_ssh_page.update_connection_status(False)
            self.cmd_page.update_connection_status(False)

            self.simple_ssh_page.update_directory_display("None")
            self.cmd_page.update_directory_display("None")

            self.cmd_page.connect_btn.setText("Connect")
            self.cmd_page.connect_btn.setEnabled(True)
            self.simple_ssh_page.action_menu.ssh_con_btn.setText("Connect to SSH")
            self.simple_ssh_page.action_menu.ssh_con_btn.setEnabled(True)
            return

        if command.startswith("python") or command.startswith("python3"):
            if "venv" not in command:
                now = datetime.now()
                date = now.strftime("%B %d, %Y")
                time = now.strftime("%I:%M %p")
                if "-m" in command:
                    file = command.split(" ")[2].split(".")[1] + ".py"
                else:
                    file = command.split(" ")[1]

                self.config.add_run([file, date, time])
        if command == "Ctrl+C":
            print("Sending interrupt")
            self.ssh_manager.send_interrupt()
            print("Sent")
            return

        if command.startswith("cd"):
            appended = command.split(' ')[1]
            if appended == '~':
                self.current_dir = self.home_dir
            else:
                self.current_dir += f"/{appended}"

        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            return
        self.worker = SSHStreamWorker(self.ssh_manager, command)
        if is_tree_update:
            self.tree_data_accumulator = ""

            self.worker.output_received.connect(accumulate_tree_data)

            self.worker.finished.connect(
                lambda: self.file_tree_page.rebuild_tree(self.tree_data_accumulator),
                Qt.ConnectionType.QueuedConnection
            )
        elif is_file_save:
            pass
        elif is_git_clone:
            update_tree()
            print("Updated tree")
            self.graph_page.refresh_runs()
            print("refreshed runs")
            pass

        elif is_file_read:
            # Clear the editor first
            self.file_tree_page.editor.clear()
            # Connect output DIRECTLY to the editor's append function
            self.worker.output_received.connect(self.file_tree_page.display_file_content)
        else:
            self.cmd_page.create_new_output_bubble()

            command = f"$ {command}\n"

            self.cmd_page.update_live_output(command)
            self.simple_ssh_page.console.update_output(command)
            self.worker.output_received.connect(self.cmd_page.update_live_output)
            self.worker.output_received.connect(self.simple_ssh_page.console.update_output)

        self.worker.finished.connect(
            lambda: global_finished(is_tree_update, is_file_read, is_file_save, is_git_clone)
        )

        self.worker.start()

    def global_finished(is_tree_update=False, is_file_read=False, is_file_save=False, is_git_clone=False):
        if is_tree_update or is_file_read or is_file_save or is_git_clone:
            self.simple_ssh_page.update_directory_display(self.current_dir)
            self.cmd_page.update_directory_display(self.current_dir)
            return

        # Normal terminal finish logic
        cmd_start = self.recent_cmd.split(' ')[0]
        add_bubble = cmd_start not in ["cat", "ssh", "git", "find"]
        if self.recent_cmd.startswith("git pull"):
            add_bubble = True
        if is_git_clone:
            add_bubble = False
        print("CMD: ", self.recent_cmd, " ADD: ", add_bubble)
        self.cmd_page.on_command_finished(add_bubble)
        self.simple_ssh_page.console.finish_command(add_bubble, add_sep=not is_git_clone)

        self.simple_ssh_page.update_directory_display(self.current_dir)
        self.cmd_page.update_directory_display(self.current_dir)
        self.cmd_page.send_btn.setEnabled(True)
        self.simple_ssh_page.action_menu.run_curr_btn.setEnabled(True)

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
    self.file_tree_page = FileTreePage(global_run_command, self.home_dir, self.config, self.ssh_manager)
    self.settings_page = SettingsPage(self.config)
    self.graph_page = GraphsPage(self.config)

    # Add pages to the stack
    self.stack.addWidget(self.cmd_page)
    self.stack.addWidget(self.simple_ssh_page)
    self.stack.addWidget(self.file_tree_page)
    self.stack.addWidget(self.graph_page)
    self.stack.addWidget(self.settings_page)

    self.stack.setContentsMargins(10, 0, 25, 20)
    layout.addWidget(self.stack)

    # ---- Navigation Logic ----
    def update_title():
        user = self.config.get("user")
        if user == "":
            self.title_label.setText("Welcome to Easy-SSH!")
        else:
            self.title_label.setText(f"Welcome back, {self.config.get("user")}")

    for index, item in enumerate(nav.nav_items):
        item.clicked.connect(
            lambda _, i=index: self.stack.setCurrentIndex(i)
        )

    self.stack.currentChanged.connect(update_title)
    self.stack.setCurrentIndex(0)
    update_title()
