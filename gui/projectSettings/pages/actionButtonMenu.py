import re

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QFrame, QPushButton, QScrollArea, \
    QPlainTextEdit, QInputDialog
from PyQt6.QtGui import QPixmap, QCursor, QTextCursor

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QPushButton
from PyQt6.QtGui import QCursor


class ActionButtonMenu(QWidget):
    def __init__(self, console, run_func=None, connect_func=None):
        super().__init__()
        self.run_func = run_func
        self.connect_func = connect_func
        self.console = console
        self.init_ui()

    def init_ui(self):
        self.outer_layout = QVBoxLayout(self)
        self.outer_layout.setContentsMargins(0, 0, 0, 0)
        self.outer_layout.setSpacing(0)

        self.wrapper = QFrame()
        self.wrapper.setObjectName("MainWrapper")  # Use an ID for specific styling
        self.wrapper.setStyleSheet("""
            #MainWrapper {
                border: 2px solid #3B3B3B; 
                border-radius: 10px;
            }
        """)

        self.main_layout = QVBoxLayout(self.wrapper)
        self.main_layout.setContentsMargins(15, 15, 15, 15)  # Internal padding
        self.main_layout.setSpacing(6)

        # --- TITLE ---
        title = QLabel("Actions")
        title.setStyleSheet("color: #AAAAAA; font-size: 21px; border: none; padding: 0px")
        self.main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop)

        self.add_divider("#FFFFFF", 1)

        # --- SECTIONS ---
        self.main_layout.addLayout(self.create_connection_section())
        self.main_layout.addSpacing(3)
        self.main_layout.addLayout(self.create_navigation_section())
        self.main_layout.addSpacing(3)
        self.main_layout.addLayout(self.create_commands_section())

        self.main_layout.addStretch()

        # 4. Finalize: Add the wrapper to the actual widget layout
        self.outer_layout.addWidget(self.wrapper)

    def add_divider(self, color, height, top_spacing=0, bottom_spacing=0):
        if top_spacing: self.main_layout.addSpacing(top_spacing)
        line = QFrame()
        line.setFixedHeight(height)
        line.setStyleSheet(f"background-color: #3B3B3B; border: none;")
        self.main_layout.addWidget(line)
        if bottom_spacing: self.main_layout.addSpacing(bottom_spacing)

    def create_connection_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel("Connection/Environment")
        title.setStyleSheet("color: #A0A0A0; font-size: 17px; border: none")
        layout.addWidget(title)

        # Buttons
        row1 = QHBoxLayout()
        self.ssh_con_btn = self.make_btn("Connect to SSH", "#1D5F1F")
        self.ssh_con_btn.clicked.connect(self.connect_func)
        self.run_curr_btn = self.make_btn("Run Select File", "#1D5F1F")
        self.run_curr_btn.clicked.connect(self.open_run_dialog)
        row1.addWidget(self.ssh_con_btn)
        row1.addWidget(self.run_curr_btn)
        row1.addStretch()

        row2 = QHBoxLayout()
        self.term_con_btn = self.make_btn("Terminate Connection", "#5F1D1D")
        self.term_con_btn.clicked.connect(lambda: self.run_func("exit"))
        self.term_run_btn = self.make_btn("Terminate Run", "#5F1D1D")
        self.term_con_btn.clicked.connect(lambda: self.run_func("Ctrl+C"))
        row2.addWidget(self.term_con_btn)
        row2.addWidget(self.term_run_btn)
        row2.addStretch()

        row3 = QHBoxLayout()
        self.create_venv_btn = self.make_btn("Create Virtual Environment", "#1D405F")
        def create_venv():
            self.run_func("python3 -m venv venv")
            self.run_func(". venv/bin/activate")
        self.create_venv_btn.clicked.connect(create_venv)

        row3.addWidget(self.create_venv_btn)
        row3.addStretch()



        layout.addLayout(row1)
        layout.addLayout(row2)
        layout.addLayout(row3)
        return layout

    def open_run_dialog(self):
        file, ok = QInputDialog.getText(
            self,
            "Run File",
            "Enter file name:",
        )

        if ok and file:
            command = f"python3 {file}"
            print(f"Running command (1): {command}")
            if not file.endswith(".py") and not '.' in file:
                command += f".py"
            print("Running command:", command)
            self.run_func(command)

    def create_navigation_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        title = QLabel("Quick Navigation")
        title.setStyleSheet("color: #A0A0A0; font-size: 17px; border: none")
        layout.addWidget(title)

        row = QHBoxLayout()
        self.cd_btn = self.make_btn("Change Directory", "#1D405F")
        self.cd_btn.clicked.connect(self.open_cd_dialog)
        self.rd_btn = self.make_btn("Reset Directory", "#1D405F")
        self.rd_btn.clicked.connect(lambda: self.run_func("cd ~"))
        row.addWidget(self.cd_btn)
        row.addWidget(self.rd_btn)
        row.addStretch()
        layout.addLayout(row)
        return layout

    def open_cd_dialog(self):

        path, ok = QInputDialog.getText(
            self,
            "Change Directory",
            "Enter remote path:",
        )

        if ok and path:
            command = f"cd {path}"
            self.run_func(command)

    def open_packages_dialog(self):

        packages, ok = QInputDialog.getText(
            self,
            "Install Packages",
            "Enter package names (seperated by a single space):",
        )

        if ok and packages:
            command = f"pip install {packages}"
            self.run_func(command)

    def open_git_dialogue(self):

        branch, ok = QInputDialog.getText(
            self,
            "Pull Latest Changes",
            "Enter active branch name (ex. main, master):",
        )

        if ok and branch:
            command = f"git pull origin {branch}"
            self.run_func(command)

    def create_commands_section(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)
        title = QLabel("Quick Commands")
        title.setStyleSheet("color: #A0A0A0; font-size: 17px; border: none")
        layout.addWidget(title)

        r1 = QHBoxLayout()
        self.inst_pack_btn = self.make_btn("Install Packages", "#1D405F")
        self.inst_pack_btn.clicked.connect(self.open_packages_dialog)
        r1.addWidget(self.inst_pack_btn)

        r1.addStretch()

        r2 = QHBoxLayout()
        self.dir_btn = self.make_btn("Directory Files List", "#1D405F")
        self.dir_btn.clicked.connect(lambda: self.run_func("ls"))
        r2.addWidget(self.dir_btn)
        self.status_btn=self.make_btn("GPU Status", "#1D405F")
        self.status_btn.clicked.connect(lambda: self.run_func("nvidia-smi"))
        r2.addWidget(self.status_btn)
        r2.addStretch()

        r3 = QHBoxLayout()
        self.pull_btn = self.make_btn("Pull Latest Changes", "#1D405F")
        self.pull_btn.clicked.connect(self.open_git_dialogue)
        r3.addWidget(self.pull_btn)
        self.clear_btn = self.make_btn("Clear Console", "#5F1D1D")
        self.clear_btn.clicked.connect(self.console.clear)
        r3.addWidget(self.clear_btn)
        r3.addStretch()

        layout.addLayout(r2)
        layout.addLayout(r3)
        layout.addLayout(r1)

        return layout

    def make_btn(self, text, border_color):
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                color: #808080; 
                background: none; 
                border: 1px solid {border_color}; 
                padding: 4px 20px; 
                border-radius: 10px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #1E1E1E;
            }}
        """)
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setFixedHeight(35)

        return btn



class ConsoleOutput(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        self.main_container = QWidget()
        self.main_container.setObjectName("ConsoleBackground")
        self.main_container.setStyleSheet("""
            QWidget#ConsoleBackground {
                background-color: #18181F;
                border: 1px solid #555555;
                border-radius: 10px;
                font-size: 16px;
            }
        """)

        content_layout = QVBoxLayout(self.main_container)
        content_layout.setContentsMargins(20, 15, 20, 15)
        content_layout.setSpacing(6)

        title = QLabel("Console Output")
        title.setStyleSheet("color: #AAAAAA; font-size: 21px; border: none; background: transparent;")
        content_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop)

        border = QFrame()
        border.setFixedHeight(2)
        border.setStyleSheet("background-color: #3B3B3B; border: none;")
        content_layout.addWidget(border)

        self.text_display = QPlainTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setStyleSheet("background: transparent; border: none; color: #AAAAAA;"
                                        "font-family: 'Consolas', 'Monospace', 'Courier New';")
        content_layout.addWidget(self.text_display)

        outer_layout.addWidget(self.main_container)

    def apply_line_spacing(self):
        """Helper to ensure all text in the widget uses 150% line height."""
        cursor = self.text_display.textCursor()
        cursor.select(QTextCursor.SelectionType.Document)
        block_format = cursor.blockFormat()
        block_format.setLineHeight(150, 1)
        cursor.setBlockFormat(block_format)

    def add_command_line(self, command):
        """Adds the command with a $ prefix without excessive spacing."""
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        if self.text_display.toPlainText() == "Waiting for command...":
            self.text_display.setPlainText("")

        cursor.insertText(f"$ {command}\n")

        self.apply_line_spacing()

    def update_output(self, raw_text):
        """Appends output and handles \r only for progress bars."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_text = ansi_escape.sub('', raw_text)

        if not clean_text:
            return

        cursor = self.text_display.textCursor()
        v_scroll = self.text_display.verticalScrollBar().value()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        # 1. Check if this chunk is a progress bar (Epoch/Step)
        # We only want to use the '\r' overwrite logic for these.
        is_progress = any(x in clean_text.lower() for x in ["epoch", "step", "it/s", "%"])

        if '\r' in clean_text and is_progress:
            parts = clean_text.split('\r')
            final_text = parts[-1]

            # Move to start of line and delete only for progress updates
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor)
            line_content = cursor.selectedText().strip()

            if line_content:
                cursor.removeSelectedText()
            cursor.insertText(final_text)
        else:
            # 2. For everything else (nvidia-smi, ls, etc.), use standard append.
            # We treat \r as a standard newline if it's not a progress bar.
            standard_text = clean_text.replace('\r\n', '\n').replace('\r', '\n')
            cursor.insertText(standard_text)

        # OPTIMIZATION: Don't call apply_line_spacing() here.
        # It selects the whole document and will freeze your app during fast output.
        # Set the line height once in initUI instead.
        self.text_display.verticalScrollBar().setValue(v_scroll)

    def finish_command(self):
        """Appends the finish marker quietly."""
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(f"\n[Command Finished]\n{'-' * 40}\n")
        self.apply_line_spacing()

    def clear(self):
        self.text_display.setPlainText("")