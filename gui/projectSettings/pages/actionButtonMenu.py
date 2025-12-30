import re

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QFrame, QPushButton, QScrollArea, \
    QPlainTextEdit
from PyQt6.QtGui import QPixmap, QCursor, QTextCursor


def action_button_menu():
    main_widget = QWidget()
    main_layout = QVBoxLayout(main_widget)
    main_layout.setContentsMargins(20, 15, 20, 0)
    main_layout.setSpacing(6)

    main_widget.setStyleSheet("border: 3px solid #3B3B3B;"
                              "border-radius: 5px;")

    # --- TITLE + BORDER ---
    title = QLabel("Actions")
    title.setContentsMargins(0, 0, 0, 0)
    title.setStyleSheet("color: #AAAAAA;"
                        "font-size: 21px;"
                        "border: none;"
                        "padding: 0px")
    main_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignTop)

    border = QFrame()
    border.setFixedHeight(2)
    border.setStyleSheet(
        "background-color: #FFFFFF;"
    )
    main_layout.addWidget(border)

    main_layout.addLayout(button_row_1())
    main_layout.addLayout(button_row_2())
    main_layout.addLayout(button_row_3())

    border2 = QFrame()
    border2.setFixedHeight(2)
    border2.setStyleSheet(
        "background-color: #FFFFFF;"
    )
    main_layout.addSpacing(10)
    main_layout.addWidget(border2)
    main_layout.addSpacing(2)
    selected = "model_cnn.py"
    selected_label = QLabel(f"Selected file to run: {selected}")
    selected_label.setStyleSheet("color: #A0A0A0; font-size: 17px; border: none; margin-bottom: 15px;")
    main_layout.addWidget(selected_label)

    main_layout.addStretch(0)
    return main_widget

def button_row_1():
    # --- ROW 1: Connection + Environment
    row1 = QVBoxLayout()
    row1_title = QLabel("Connection/Environment")
    row1_title.setStyleSheet("color: #A0A0A0;"
                             "font-size: 17px;"
                             "border: none")
    row1.setSpacing(10)
    row1_title.setAlignment(Qt.AlignmentFlag.AlignTop)
    row1.addWidget(row1_title)

    # button row 1
    row1_br1 = QHBoxLayout()
    ssh_con = QPushButton("Connect to SSH")
    ssh_con.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D5F1F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    ssh_con.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    ssh_con.setFixedHeight(35)
    row1_br1.addWidget(ssh_con)
    row1_br1.addSpacing(5)
    con_settings = QPushButton("Update Connection Settings")
    con_settings.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    con_settings.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    con_settings.setFixedHeight(35)
    row1_br1.addWidget(con_settings)
    row1_br1.addStretch()
    row1.addLayout(row1_br1)
    # button row 2
    row1_br2 = QHBoxLayout()
    term_con = QPushButton("Terminate Connection")
    term_con.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #5F1D1D; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    term_con.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    term_con.setFixedHeight(35)
    row1_br2.addWidget(term_con)
    row1_br2.addSpacing(5)
    term_run = QPushButton("Terminate Run")
    term_run.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #5F1D1D; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    term_run.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    term_run.setFixedHeight(35)
    row1_br2.addWidget(term_run)
    row1_br2.addStretch()
    row1.addLayout(row1_br2)
    # button row 3
    row1_br3 = QHBoxLayout()
    create_venv = QPushButton("Create Virtual Environment")
    create_venv.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    create_venv.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    create_venv.setFixedHeight(35)
    row1_br3.addWidget(create_venv)
    row1_br3.addSpacing(5)
    run_curr = QPushButton("Run Current File")
    run_curr.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D5F1F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    run_curr.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    run_curr.setFixedHeight(35)
    row1_br3.addWidget(run_curr)
    row1_br3.addStretch()
    row1.addLayout(row1_br3)
    return row1

def button_row_2():
    row1 = QVBoxLayout()

    row1_title = QLabel("Quick Navigation")
    row1_title.setStyleSheet("color: #A0A0A0;"
                             "font-size: 17px;"
                             "border: none")
    row1.setSpacing(10)
    row1_title.setAlignment(Qt.AlignmentFlag.AlignTop)
    row1.addWidget(row1_title)

    # button row 1
    row1_br1 = QHBoxLayout()
    change_dir = QPushButton("Change Directory")
    change_dir.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    change_dir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    change_dir.setFixedHeight(35)
    row1_br1.addWidget(change_dir)
    row1_br1.addSpacing(5)
    reset_dir = QPushButton("Reset Directory")
    reset_dir.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    reset_dir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    reset_dir.setFixedHeight(35)
    row1_br1.addWidget(reset_dir)
    row1_br1.addStretch()
    row1.addLayout(row1_br1)

    return row1

def button_row_3():
    row1 = QVBoxLayout()
    row1_title = QLabel("Quick Commands")
    row1_title.setStyleSheet("color: #A0A0A0;"
                             "font-size: 17px;"
                             "border: none")
    row1.setSpacing(10)
    row1_title.setAlignment(Qt.AlignmentFlag.AlignTop)
    row1.addWidget(row1_title)

    # button row 1
    row1_br1 = QHBoxLayout()
    install_reqs = QPushButton("Install requirements-txt")
    install_reqs.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    install_reqs.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    install_reqs.setFixedHeight(35)
    row1_br1.addWidget(install_reqs)
    row1_br1.addSpacing(5)
    install_packages = QPushButton("Install Packages")
    install_packages.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    install_packages.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    install_packages.setFixedHeight(35)
    row1_br1.addWidget(install_packages)
    row1_br1.addStretch()
    row1.addLayout(row1_br1)
    # button row 2
    row1_br2 = QHBoxLayout()
    dir_files = QPushButton("Directory Files List")
    dir_files.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    dir_files.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    dir_files.setFixedHeight(35)
    row1_br2.addWidget(dir_files)
    row1_br2.addSpacing(5)
    gpu_status = QPushButton("GPU Status")
    gpu_status.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    gpu_status.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    gpu_status.setFixedHeight(35)
    row1_br2.addWidget(gpu_status)
    row1_br2.addStretch()
    row1.addLayout(row1_br2)
    # button row 3
    row1_br3 = QHBoxLayout()
    pull_latest = QPushButton("Pull Latest Changes")
    pull_latest.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #1D405F; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    pull_latest.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    pull_latest.setFixedHeight(35)
    row1_br3.addWidget(pull_latest)
    row1_br3.addSpacing(5)
    clear_console = QPushButton("Clear Console")
    clear_console.setStyleSheet(
        "color: #808080; background: none; border: 1px solid #5F1D1D; padding: 4px 20px; border-radius: 10px;"
        "font-size: 14px;"
    )
    clear_console.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    clear_console.setFixedHeight(35)
    row1_br3.addWidget(clear_console)
    row1_br3.addStretch()
    row1.addLayout(row1_br3)
    return row1


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
        self.text_display.setStyleSheet("background: transparent; border: none; color: #AAAAAA;")
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
        """Appends output and handles \r without creating empty space."""
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_text = ansi_escape.sub('', raw_text)

        if not clean_text:
            return

        cursor = self.text_display.textCursor()
        v_scroll = self.text_display.verticalScrollBar().value()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        if '\r' in clean_text:
            parts = clean_text.split('\r')
            final_text = parts[-1]

            # Check if current line is empty before deleting
            # (Prevents deleting the command line if data comes in too fast)
            cursor.movePosition(QTextCursor.MoveOperation.StartOfLine, QTextCursor.MoveMode.KeepAnchor)
            line_content = cursor.selectedText().strip()

            # If the line has content (like an old progress bar), replace it.
            # If it's empty, just insert.
            if line_content:
                cursor.removeSelectedText()

            cursor.insertText(final_text)
        else:
            # Standard append
            cursor.insertText(clean_text)

        self.apply_line_spacing()
        self.text_display.verticalScrollBar().setValue(v_scroll)

    def finish_command(self):
        """Appends the finish marker quietly."""
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(f"\n[Command Finished]\n{'-' * 40}")
        self.apply_line_spacing()
        # Removed: self.text_display.ensureCursorVisible()

    def clear(self):
        self.text_display.setPlainText("")