#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.2.1
Email: sam.grouchnikov@gmail.com
Status: Development
"""


import ast
import re

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtCore import Qt, QSize, QRect
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem, QCursor, QPixmap, QPainter, QPalette
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont, QTextFormat
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QPushButton, QPlainTextEdit, QFileDialog, QMessageBox, QLabel, QFrame, QSizePolicy, QGraphicsDropShadowEffect,
    QListWidget, QListWidgetItem, QTextEdit
)
from scp import SCPClient


class CustomButton(QPushButton):
    def __init__(self, text, icon_size, spacing, cursor, parent=None):
        super().__init__(parent)
        self._icon_size = icon_size
        if cursor:
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.button_layout = QHBoxLayout(self)

        self.button_layout.setContentsMargins(12, 2, 12, 2)
        self.button_layout.setSpacing(spacing)

        self.button_layout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetFixedSize)

        self.icon_label = QLabel()
        self.icon_label.setStyleSheet("background: transparent; border: none;")
        self.text_label = QLabel(text)

        self.button_layout.addWidget(self.icon_label)
        self.button_layout.addWidget(self.text_label)

    def set_icon(self, icon_path):
        pixmap = QPixmap(icon_path).scaled(
            self._icon_size.width(),
            self._icon_size.height(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.icon_label.setPixmap(pixmap)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_number_area = LineNumberArea(self)
        self._line_number_text_color = self.palette().mid().color()
        self._line_number_bg_color = self.palette().color(self.palette().ColorRole.Base)

        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)
        self.cursorPositionChanged.connect(self.highlight_current_line)

        self.update_line_number_area_width(0)
        self.highlight_current_line()

    def line_number_area_width(self):
        if self.isReadOnly() or self.blockCount() <= 1 and not self.toPlainText().strip():
            return 0

        digits = len(str(max(1, self.blockCount())))
        return 12 + self.fontMetrics().horizontalAdvance('9') * digits

    def update_line_number_area_width(self, _):
        width = self.line_number_area_width()
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)
        if width == 0:
            self.line_number_area.hide()
        else:
            self.line_number_area.show()

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        contents_rect = self.contentsRect()
        self.line_number_area.setGeometry(QRect(
            contents_rect.left(),
            contents_rect.top(),
            self.line_number_area_width(),
            contents_rect.height(),
        ))

    def line_number_area_paint_event(self, event):
        if self.isReadOnly() and not self.toPlainText().strip():
            return

        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), self._line_number_bg_color)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = round(self.blockBoundingGeometry(block).translated(self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(self._line_number_text_color)
                painter.drawText(
                    0,
                    top,
                    self.line_number_area.width() - 6,
                    self.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1

    def set_line_number_colors(self, text_color, background_color):
        self._line_number_text_color = QColor(text_color)
        self._line_number_bg_color = QColor(background_color)
        self.line_number_area.update()

    def setReadOnly(self, value):
        super().setReadOnly(value)
        self.highlight_current_line()
        self.update_line_number_area_width(0)

    def highlight_current_line(self):
        if self.isReadOnly():
            self.setExtraSelections([])
            return

        line_selection = QTextEdit.ExtraSelection()
        line_selection.format.setBackground(self.palette().base().color().lighter(104))
        line_selection.format.setProperty(QTextFormat.Property.FullWidthSelection, True)
        line_selection.cursor = self.textCursor()
        line_selection.cursor.clearSelection()
        self.setExtraSelections([line_selection])


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []
        self.tri_string_format = QTextCharFormat()
        self.tri_single_re = QRegularExpression("'''")
        self.tri_double_re = QRegularExpression('"""')

        # Default to a balanced theme on initialization
        self.set_theme({
            'keyword': '#C586C0',
            'builtin': '#569CD6',
            'function': '#B9B96F',
            'class': '#4EC9B0',
            'string': '#CE9178',
            'comment': '#6A9955',
            'number': '#B5CEA8',
            'decorator': '#DCDCAA'
        })

    def set_theme(self, colors):
        self.rules = []

        # 1. Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor(colors['keyword']))
        keywords = [
            "def", "class", "import", "from", "if", "else", "elif", "return",
            "for", "while", "try", "except", "finally", "with", "as", "lambda",
            "yield", "break", "continue", "pass", "assert", "raise"
        ]
        for word in keywords:
            self.rules.append((QRegularExpression(f"\\b{word}\\b"), keyword_format))

        # 2. Built-ins and Constants
        builtin_format = QTextCharFormat()
        builtin_format.setForeground(QColor(colors['builtin']))
        builtins = ["self", "None", "True", "False", "print", "len", "range", "enumerate"]
        for word in builtins:
            self.rules.append((QRegularExpression(f"\\b{word}\\b"), builtin_format))

        # 3. Function Definitions (Capture group 1)
        func_format = QTextCharFormat()
        func_format.setForeground(QColor(colors['function']))
        self.rules.append((QRegularExpression(r"\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)"), func_format))

        # 4. Class Definitions (Capture group 1)
        class_format = QTextCharFormat()
        class_format.setForeground(QColor(colors['class']))
        self.rules.append((QRegularExpression(r"\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)"), class_format))

        # 5. Strings
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(colors['string']))
        self.rules.append((QRegularExpression(r"\"[^\"\\]*(\\.[^\"\\]*)*\""), string_format))
        self.rules.append((QRegularExpression(r"'[^'\\]*(\\.[^'\\]*)*'"), string_format))

        # 6. Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor(colors['comment']))
        self.rules.append((QRegularExpression(r"#[^\n]*"), comment_format))

        # 7. Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor(colors['number']))
        self.rules.append((QRegularExpression(r"\b[0-9]+\b"), number_format))

        # 8. Decorators
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(QColor(colors['decorator']))
        self.rules.append((QRegularExpression(r"@[a-zA-Z_][a-zA-Z0-9_]*"), decorator_format))

        # Update multi-line string color
        self.tri_string_format.setForeground(QColor(colors['string']))

        self.rehighlight()

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                if match.lastCapturedIndex() > 0:
                    self.setFormat(match.capturedStart(1), match.capturedLength(1), fmt)
                else:
                    self.setFormat(match.capturedStart(), match.capturedLength(), fmt)

        # Multi-line strings state management
        self.setCurrentBlockState(0)
        start_index = 0
        if self.previousBlockState() != 1:
            start_index = text.find('"""')
            if start_index == -1:
                start_index = text.find("'''")

        while start_index >= 0:
            end_match = self.tri_double_re.match(text, start_index + 3)
            if not end_match.hasMatch():
                end_match = self.tri_single_re.match(text, start_index + 3)

            if not end_match.hasMatch():
                self.setCurrentBlockState(1)
                self.setFormat(start_index, len(text) - start_index, self.tri_string_format)
                break
            else:
                length = end_match.capturedEnd() - start_index
                self.setFormat(start_index, length, self.tri_string_format)
                start_index = text.find('"""', start_index + length)
                if start_index == -1:
                    start_index = text.find("'''", start_index + length)


def build_nested_dict(paths):
    tree = {}

    for path in paths:
        clean_path = path.strip()
        if not clean_path or clean_path == ".":
            continue

        if clean_path.startswith("./"):
            clean_path = clean_path[2:]
        elif clean_path.startswith("."):
            clean_path = clean_path[1:]

        parts = clean_path.split('/')
        current_level = tree

        # Iterate through all parts except the very last one
        for i in range(len(parts)):
            part = parts[i]
            if not part:
                continue

            is_last = (i == len(parts) - 1)

            if is_last:
                # If it's the last part, and it's not already a folder, mark as file
                if part not in current_level:
                    current_level[part] = None  # None indicates a file
            else:
                # If it's not the last part, it MUST be a folder
                if part not in current_level or not isinstance(current_level[part], dict):
                    current_level[part] = {}
                current_level = current_level[part]

    return tree


class FileTreePage(QWidget):
    def __init__(self, run_func, home_dir, config, ssh_manager, update_func):
        super().__init__()
        self.update_func = update_func
        self.run_func = run_func
        self.home_dir = home_dir
        self.config = ""
        self.ssh_manager = ssh_manager
        self.current_open_path = None
        self.current_file_is_python = False
        self.syntax_warnings = []

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(0)

        self.top_row = QWidget()
        self.top_layout = QHBoxLayout(self.top_row)
        self.top_row.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.top_row.setFixedHeight(28)
        self.top_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.top_layout.setContentsMargins(0,0,5,0)

        self.content_row = QWidget()
        self.content_layout = QHBoxLayout(self.content_row)
        self.content_layout.setContentsMargins(3, 3, 3, 3)
        self.content_layout.setSpacing(5)


        self.main_layout.addWidget(self.top_row)
        self.main_layout.addWidget(self.content_row)

        self.setup_top_row()
        self._setup_tree_container()
        self._setup_editor_container()
        self._wire_signals()
        self.highlighter = PythonHighlighter(self.editor.document())

    def setup_top_row(self):

        self.reload_button = CustomButton("Reload", QSize(14, 14), 2, False)
        self.reload_button.adjustSize()
        self.reload_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.reload_button.clicked.connect(self.update_func)

        self.scan_button = CustomButton("Scan for Errors", QSize(14, 14), 2, False)
        self.scan_button.adjustSize()
        self.scan_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.scan_button.clicked.connect(self.run_syntax_check)

        self.suggest_button = CustomButton("Suggest Improvements", QSize(14, 14), 2, False)
        self.suggest_button.adjustSize()
        self.suggest_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.save_button = CustomButton("Save Changes", QSize(14, 14), 2, True)
        self.save_button.clicked.connect(self.save_remote_file)
        self.save_button.setEnabled(False)

        self.transfer_button = CustomButton("Download", QSize(14, 14), 2, True)
        self.transfer_button.clicked.connect(self.transfer_remote_file)
        self.transfer_button.setEnabled(False)

        self.top_layout.addWidget(self.reload_button)
        self.top_layout.addSpacing(362)
        self.top_layout.addWidget(self.scan_button)
        # self.top_layout.addWidget(self.suggest_button)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.save_button)
        self.top_layout.addWidget(self.transfer_button)


    def _setup_tree_container(self):
        self.tree_container = QWidget()
        self.tree_container.setContentsMargins(1, 10, 1, 10)
        self.tree_container.setFixedWidth(450)
        self.tree_container.setObjectName("tree_container")

        self.tree_container_layout = QVBoxLayout()
        self.tree_container_layout.setContentsMargins(0, 0, 0, 0)
        self.tree_container.setLayout(self.tree_container_layout)
        self.tree_container.setGraphicsEffect(self._build_shadow(blur_radius=15, alpha=30))

        self.tree_header = QWidget()
        self.tree_header_layout = QHBoxLayout(self.tree_header)
        self.tree_header_layout.setContentsMargins(15, 0, 15, 0)
        self.tree_header_layout.setSpacing(7)
        self.tree_header_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.file_icon = QLabel()
        self.file_icon.setContentsMargins(0,2,0,0)

        self.tree_header_layout.addWidget(self.file_icon)

        self.files_label = QLabel("Files")

        self.tree_header_layout.addWidget(self.files_label)

        self.tree_header_layout.addStretch()

        if self.config:
            self.path_label = QLabel(f"{self.config.get('ssh_user')}@{self.config.get('ssh_ip')}")
        else:
            self.path_label = QLabel("none@none")
        self.tree_header_layout.addWidget(self.path_label)

        # IMPORTANT: Add the widget, not just the layout
        self.tree_container_layout.addWidget(self.tree_header)

        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.Shape.HLine)
        self.line1.setFixedHeight(2)
        self.line1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tree_container_layout.addWidget(self.line1)

        self.model = QStandardItemModel()
        self.tree_layout = QVBoxLayout()
        self.tree_layout.setContentsMargins(15, 0, 15, 0)

        self.tree = QTreeView()
        self.tree.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tree.setAllColumnsShowFocus(True)
        self.tree.setContentsMargins(0, 0, 0, 0)
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(25)
        self.tree.setIconSize(QSize(17, 17))
        self.tree_layout.addWidget(self.tree)

        self.tree_container_layout.addLayout(self.tree_layout)
        self.content_layout.addWidget(self.tree_container)

    def _setup_editor_container(self):
        self.editor_widget = QWidget()
        self.editor_widget.setObjectName("EditorContainer")
        self.editor_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.editor_layout = QVBoxLayout(self.editor_widget)
        self.editor_layout.setContentsMargins(1, 4, 1, 4)
        self.editor_layout.setSpacing(0)
        self.editor_widget.setGraphicsEffect(self._build_shadow(blur_radius=15, alpha=30))

        self._setup_editor_header()
        self._setup_editor_area()
        self.content_layout.addWidget(self.editor_widget)

    def _setup_editor_header(self):
        self.editor_header = QWidget()
        self.editor_header_layout = QHBoxLayout(self.editor_header)
        self.editor_header_layout.setContentsMargins(25, 5, 20, 0)
        self.editor_header.setStyleSheet("border: none;")
        self.editor_header_layout.setSpacing(15)

        self.file_name_label = QLabel("No File Selected")
        self.editor_header_layout.addWidget(self.file_name_label)
        self.editor_header_layout.addStretch()

        self.syntax_warning_breadcrumb = QPushButton("Warnings: 0")
        self.syntax_warning_breadcrumb.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.syntax_warning_breadcrumb.setFlat(True)
        self.syntax_warning_breadcrumb.clicked.connect(self.toggle_syntax_panel)
        self.editor_header_layout.addWidget(self.syntax_warning_breadcrumb)

        self.editor_layout.addWidget(self.editor_header)
        self.editor_layout.addSpacing(7)

        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFixedHeight(2)
        self.line2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.editor_layout.addWidget(self.line2)

    def update_config(self, user, ip):
        self.path_label.setText(f"{user}@{ip}")

    def _setup_editor_area(self):
        self.editor_wrapper = QWidget()
        self.editor_wrapper.setStyleSheet("border: none")
        self.editor_wrapper.setContentsMargins(0, 0, 0, 0)
        self.editor_wrapper_layout = QVBoxLayout(self.editor_wrapper)
        self.editor_wrapper_layout.setContentsMargins(8, 0, 8, 8)
        self.editor_wrapper_layout.setSpacing(10)

        self.editor = CodeEditor()
        self.editor.document().setDocumentMargin(17)
        self.editor.setReadOnly(True)
        self.editor.setPlaceholderText("Select a file to view and edit its contents...")

        font = QFont("Consolas", 12) if "Consolas" in QFont().families() else QFont("Monospace", 12)
        self.editor.setFont(font)

        self.editor_shell = QWidget()
        self.editor_shell.setObjectName("EditorShell")
        self.editor_shell_layout = QVBoxLayout(self.editor_shell)
        self.editor_shell_layout.setContentsMargins(5, 0, 5, 5)
        self.editor_shell_layout.setSpacing(0)
        self.editor_shell_layout.addWidget(self.editor)
        self.editor_wrapper_layout.addWidget(self.editor_shell)

        self.syntax_panel = QWidget()
        self.syntax_panel.setObjectName("SyntaxPanel")
        self.syntax_panel.setContentsMargins(5, 0, 5, 0)
        self.syntax_panel.setMaximumHeight(180)
        self.syntax_panel_layout = QVBoxLayout(self.syntax_panel)
        self.syntax_panel_layout.setContentsMargins(20, 12, 20, 12)
        self.syntax_panel_layout.setSpacing(8)

        self.syntax_panel_title = QLabel("Syntax warnings")
        self.syntax_panel_layout.addWidget(self.syntax_panel_title)

        self.syntax_list = QListWidget()
        self.syntax_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.syntax_panel_layout.addWidget(self.syntax_list)
        self.syntax_panel.setGraphicsEffect(self._build_shadow(blur_radius=15, alpha=25))
        self.syntax_panel.setVisible(False)
        self.editor_wrapper_layout.addWidget(self.syntax_panel)

        self.editor_layout.addWidget(self.editor_wrapper)

        self.editor.textChanged.connect(self.on_editor_text_changed)

    def _build_shadow(self, blur_radius, alpha):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(blur_radius)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, alpha))
        return shadow

    def _wire_signals(self):
        self.tree.doubleClicked.connect(self.on_item_double_clicked)
        self.tree.clicked.connect(self.on_file_selected)


    def update_home(self, new):
        self.home_dir = new

    def on_file_selected(self, index):
        item = self.model.itemFromIndex(index)
        if not item.hasChildren():
            file_path = item.data(Qt.ItemDataRole.UserRole)
            self.current_open_path = "" + self.home_dir + "/" + file_path
            self.load_remote_file(self.current_open_path)

    def load_remote_file(self, path):
        self.editor.setPlainText(f"Loading {path}...")
        cmd = f"cat '{path}'"
        self.run_func(cmd, is_file_read=True)
        split = path.split("/")
        last = split[len(split) - 1]
        self.file_name_label.setText(last)

    def reset_editor_text(self):
        self.editor.clear()  # Better than setPlainText("") for resetting
        self.editor.setPlaceholderText("Select a file to view and edit its contents...")
        self.editor.setReadOnly(True)

        # This will now trigger the .hide() logic added in Step 1
        self.editor.update_line_number_area_width(0)

        self.file_name_label.setText("No File Selected")
        self.transfer_button.setEnabled(False)
        self.save_button.setEnabled(False)
        self.current_file_is_python = False
        self.syntax_warnings = []
        self.update_syntax_warning_breadcrumb()
        self.refresh_syntax_panel()
        self.set_syntax_panel_open(False)

    def display_file_content(self, content):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        clean_content = ansi_escape.sub('', content)
        clean_content = clean_content.strip()

        self.editor.setPlainText(clean_content)

        self.editor.setReadOnly(False)
        self.editor.update_line_number_area_width(0)
        self.save_button.setEnabled(True)
        self.transfer_button.setEnabled(True)
        self.current_file_is_python = bool(self.current_open_path and self.current_open_path.lower().endswith(".py"))
        self.run_syntax_check()

    def on_editor_text_changed(self):
        if self.current_file_is_python and not self.editor.isReadOnly():
            self.run_syntax_check()

    def run_syntax_check(self):
        if not self.current_file_is_python:
            self.syntax_warnings = []
            self.update_syntax_warning_breadcrumb()
            self.refresh_syntax_panel()
            return

        content = self.editor.toPlainText()
        warnings = []

        try:
            ast.parse(content)
        except SyntaxError as error:
            line_number = error.lineno or 0
            message = error.msg or "Invalid syntax"
            warnings.append({"line": line_number, "message": message})

        self.syntax_warnings = warnings
        self.update_syntax_warning_breadcrumb()
        self.refresh_syntax_panel()

    def update_syntax_warning_breadcrumb(self):
        if not self.current_file_is_python:
            self.syntax_warning_breadcrumb.setText("Warnings: --")
            self.syntax_warning_breadcrumb.setEnabled(False)
            return

        self.syntax_warning_breadcrumb.setEnabled(True)
        warning_count = len(self.syntax_warnings)
        label = "warning" if warning_count == 1 else "warnings"
        self.syntax_warning_breadcrumb.setText(f"{warning_count} {label}")

    def refresh_syntax_panel(self):
        self.syntax_list.clear()
        if not self.current_file_is_python:
            self.syntax_list.addItem(QListWidgetItem("Syntax checker is available for Python files."))
            return

        if not self.syntax_warnings:
            self.syntax_list.addItem(QListWidgetItem("No syntax warnings found."))
            return

        for warning in self.syntax_warnings:
            line_number = warning.get("line", 0)
            message = warning.get("message", "Invalid syntax")
            self.syntax_list.addItem(QListWidgetItem(f"Line {line_number}: {message}"))

    def toggle_syntax_panel(self):
        if not self.current_file_is_python:
            return
        self.set_syntax_panel_open(not self.syntax_panel.isVisible())

    def set_syntax_panel_open(self, is_open):
        self.syntax_panel.setVisible(is_open)

    def save_remote_file(self):
        if not self.current_open_path:
            return


        content = self.editor.toPlainText()

        command = f"cat << 'EOF' > {self.current_open_path}\n{content}\nEOF"

        self.save_button.setEnabled(False)

        self.run_func(command, is_file_save=True)

        # Reset button after a short delay or via the 'finished' signal
        self.save_button.text_label.setText("Save Changes")
        self.save_button.setEnabled(True)

    def transfer_remote_file(self):
        if not self.current_open_path:
            return

        local_dir = QFileDialog.getExistingDirectory(self, "Select Save Folder")

        if local_dir:
            try:
                transport = self.ssh_manager.client.get_transport()

                with SCPClient(transport) as scp:
                    scp.get(self.current_open_path, local_dir)

                QMessageBox.information(self, "Success", "File transferred successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Transfer Failed", f"Error: {str(e)}")

    def rebuild_tree(self, raw_find_output):

        # Completely clear the existing items
        self.model.clear()

        # Parse the raw SSH string into a nested dict
        paths = [p for p in raw_find_output.split('\n')]

        nested_data = build_nested_dict(paths)

        # Populate the model starting from the invisible root
        self.populate_tree(self.model.invisibleRootItem(), nested_data)

    def populate_tree(self, parent_item, data_dict, current_full_path=""):
        # Sort: Folders first, then Alphabetical
        sorted_names = sorted(data_dict.keys(), key=lambda s: (not data_dict[s], s.lower()))

        for name in sorted_names:
            item = QStandardItem(name)
            item.setEditable(False)

            item_path = f"{current_full_path}/{name}" if current_full_path else name
            item.setData(item_path, Qt.ItemDataRole.UserRole)

            # 1. Folder Check: Must be a dictionary
            if isinstance(data_dict[name], dict):
                item.setData("folder", Qt.ItemDataRole.UserRole + 1)
                item.setIcon(QIcon("gui/icons/editor/folder_light.png"))
                parent_item.appendRow(item)

                # Only recurse if the folder actually has contents
                if data_dict[name]:
                    self.populate_tree(item, data_dict[name], item_path)

            # 2. Python File Check: Must NOT be a dict, and end in .py
            elif name.lower().endswith(".py"):
                item.setData("python", Qt.ItemDataRole.UserRole + 1)
                item.setIcon(QIcon("gui/icons/editor/python.png"))
                parent_item.appendRow(item)

            # 3. Generic File Check
            else:
                item.setData("file", Qt.ItemDataRole.UserRole + 1)
                item.setIcon(QIcon("gui/icons/file.png"))
                parent_item.appendRow(item)

    def on_item_double_clicked(self, index):
        item = self.model.itemFromIndex(index)
        file_path = item.data(Qt.ItemDataRole.UserRole)

        # Don't try to 'cat' folders
        if item.hasChildren():
            return

        # Trigger the load via SSH
        self.run_func(f"cat '{file_path}'", is_file_read=True)

    def update_tree_icons(self, folder_icon_path, file_icon_path):
        root = self.model.invisibleRootItem()
        python_icon_path = "gui/icons/editor/python.png"

        def traverse(item):
            for i in range(item.rowCount()):
                child = item.child(i)
                item_type = child.data(Qt.ItemDataRole.UserRole + 1)

                if item_type == "folder":
                    child.setIcon(QIcon(folder_icon_path))
                elif item_type == "python":
                    child.setIcon(QIcon(python_icon_path))
                else:
                    child.setIcon(QIcon(file_icon_path))

                traverse(child)

        traverse(root)

    def set_light_mode(self):
        self.highlighter.set_theme({
            'keyword': '#6666BE',  # Pure Blue
            'builtin': '#267F99',  # Dark Cyan
            'function': '#795E26',  # Dark Gold
            'class': '#267F99',  # Dark Cyan
            'string': '#A31515',  # Deep Red
            'comment': '#008000',  # Pure Green
            'number': '#098658',  # Emerald Green
            'decorator': '#795E26'  # Dark Gold
        })
        self.update_tree_icons("gui/icons/editor/folder_light.png", "gui/icons/file.png")
        self.tree_container.setStyleSheet("""
                    QWidget#tree_container {

                        border-radius: 12px;
                    }
                    QWidget { background-color: #ffffff; } 
                """)
        self.line1.setStyleSheet("background-color: #CBCBCB")
        self.tree.setStyleSheet("""
                                QTreeView {
                                    color: black; font-size: 15px; border: none;
                                    show-decoration-selected: 1;
                                    outline: 0;
                                }
                                QTreeView::item {
                                padding-top: 4px;
                                padding-bottom: 4px;
                                padding-left: 3px;
                                }
                                QScrollBar:vertical {
                                    border: none;
                                    background: #E9E9E9;
                                    width: 13px;
                                    margin: 0px 0px 0px 0px;
                                }
                                QTreeView::item:selected {
                                    background-color: #E7EFFD; /* Subtle blue */
                                    color: #121212;
                                    border-radius: 4px;
                                    border: none;
                                }
                                QTreeView::item:selected:!active {
                                    background-color: #F2F2F2;
                                }
                                QTreeView::item:hover {
                                    background-color: #F5F5F5;
                                    border-radius: 4px;
                                }
                                QTreeView::item:focus {
    outline: none;
    border: none;
}

                    QScrollBar::handle:vertical {
                                    background: #D7D7D7;
                                    min-height: 20px;
                                    border-radius: 5px;
                                    margin: 2px;
                                }

                    QScrollBar::handle:vertical:hover {
                                    background: #CBCBCB;
                                }

                                /* Remove the buttons (arrows) at the top and bottom */
                                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                    height: 0px;
                                }

                                /* Remove the background area above and below the handle */
                                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                    background: none;
                                }
                            """)

        self.editor_widget.setStyleSheet("""
                    QWidget#EditorContainer {
                        background-color: #ffffff;
                        border-radius: 12px;
                    }
                """)

        self.editor_wrapper.setStyleSheet("""
            background-color: #ffffff;
            border: none;
        """)
        self.editor_header.setStyleSheet("""
                    background-color: #ffffff
                """)
        self.file_name_label.setStyleSheet(
            "font-size: 16px; font-weight: 520; color: #583068; border: none"
        )
        self.syntax_warning_breadcrumb.setStyleSheet(
            "font-size: 13px; color: #6A4A7A; border: none; font-weight: 520;"
        )
        self.files_label.setStyleSheet("font-weight: 520; color: #303030; font-size: 16px")
        self.path_label.setStyleSheet("color: #9B9393; font-weight: 510; font-size: 14.5px")


        self.save_button.text_label.setStyleSheet("""
                    font-size: 16px; 
                    font-weight: 500; 
                    background: transparent; 
                    border: none; 
                    color: inherit;
                """)
        self.transfer_button.setStyleSheet("""
                    QPushButton { 
                        border-radius: 10px; 
                        background-color: #ECDCFF; 
                        color: #303030;
                    }
                    QPushButton:hover {
                        background-color: #E1C7FF
                    }
                    QPushButton:pressed { background-color: #ECDCFF}
                """)
        self.transfer_button.text_label.setStyleSheet("""
                    font-size: 13px; 
                            font-weight: 520; 
                            background: transparent; 
                            border: none; 
                            color: #303030;
                            padding-bottom: 2px;
                """)
        for button in [self.reload_button, self.suggest_button, self.scan_button, self.save_button]:
            button.setStyleSheet("""
                    QPushButton { 
                                background-color: rgba(0, 0, 0, 0);
                                border-radius: 7px; 
                                color: #444;
                                padding: 5px 0px;
                            }
                            QPushButton:hover {
                                background-color: #f3ecf4
                            }
                            QPushButton:pressed {
                                background-color: rgba(0,0,0,0);
                            }
            """)
            button.text_label.setStyleSheet("""
                            font-size: 13px; 
                            font-weight: 515; 
                            background: transparent; 
                            border: none; 
                            color: inherit;
                            padding-bottom: 2px;
            """)
        self.line2.setStyleSheet("background-color: #D7D7D7")
        self.editor.setStyleSheet("""
                    QPlainTextEdit {
                        color: #444;
                        border: none; 
                        border-top-left-radius: 10px;
                        border-top-right-radius: 10px;
                        font-family: 'Consolas', 'Monospace', 'Courier New';
                        font-size: 14px;
                    }
                    QScrollBar:vertical {
                                    border: none;
                                    border-radius: 8px;
                                    background: #E9E9E9;
                                    width: 13px;
                                    margin: 8px 0px 8px 0px;
                                }

                    QScrollBar::handle:vertical {
                                    background: #D7D7D7;
                                    min-height: 20px;
                                    border-radius: 8px;
                                    margin: 2px;
                                }

                    QScrollBar::handle:vertical:hover {
                                    background: #CBCBCB;
                                }

                    /* Remove the buttons (arrows) at the top and bottom */
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        height: 0px;
                    }

                    /* Remove the background area above and below the handle */
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }
                """)
        self.editor_shell.setStyleSheet("background-color: #ffffff; border-radius: 10px;")
        self.editor.set_line_number_colors("#6E5E77", "#F3EEF8")
        self.syntax_panel.setStyleSheet("background-color: #F8F5FB; border-radius: 15px;")
        self.syntax_panel_title.setStyleSheet("font-size: 13px; color: #6A4A7A; font-weight: 600;")
        self.syntax_list.setStyleSheet("""
                    QListWidget {
                        border: none;
                        background-color: transparent;
                        color: #4A3B52;
                        font-size: 12px;
                    }
                    QListWidget::item {
                        padding: 3px 2px;
                    }
                """)
        self.save_button.set_icon("gui/icons/editor/save_light.png")
        self.transfer_button.set_icon("gui/icons/editor/download_light.png")
        self.reload_button.set_icon("gui/icons/editor/refresh_light.png")
        self.scan_button.set_icon("gui/icons/editor/scan_light.png")
        self.suggest_button.set_icon("gui/icons/editor/suggest_light.png")
        pixmap = QPixmap("gui/icons/editor/files_light.png").scaled(
            19,
            19,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.file_icon.setPixmap(pixmap)

    def set_dark_mode(self):
        self.highlighter.set_theme({
            'keyword': '#C586C0',  # Purple
            'builtin': '#569CD6',  # Blue
            'function': '#DCDCAA',  # Yellow
            'class': '#4EC9B0',  # Teal
            'string': '#CE9178',  # Salmon
            'comment': '#6A9955',  # Green
            'number': '#B5CEA8',  # Light Green
            'decorator': '#DCDCAA'  # Yellow
        })
        # 1. Updated Icons (Added missing reload, scan, suggest icons)
        self.update_tree_icons("gui/icons/editor/folder_light.png", "gui/icons/file_dark.png")
        self.save_button.set_icon("gui/icons/editor/save_dark.png")
        self.transfer_button.set_icon("gui/icons/editor/download_dark.png")
        self.reload_button.set_icon("gui/icons/editor/refresh_dark.png")
        self.scan_button.set_icon("gui/icons/editor/scan_dark.png")
        self.suggest_button.set_icon("gui/icons/editor/suggest_dark.png")
        pixmap = QPixmap("gui/icons/editor/files_dark.png").scaled(
            19,
            19,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.file_icon.setPixmap(pixmap)

        # 2. Containers
        self.tree_container.setStyleSheet("""
                    QWidget#tree_container {
                        border-radius: 12px;
                    }
                    QWidget { background-color: #231E23; } 
                """)

        self.editor_widget.setStyleSheet("""
                    QWidget#EditorContainer {
                        background-color: #231E23;
                        border-radius: 12px;
                    }
                """)
        self.files_label.setStyleSheet("font-weight: 520; color: #979797; font-size: 16px")
        self.path_label.setStyleSheet("color: #696262; font-weight: 510; font-size: 14.5px")

        # Missing in previous dark mode: Editor wrapper and header
        self.editor_wrapper.setStyleSheet("background-color: #231E23;")
        self.editor_shell.setStyleSheet("background-color: #1F1D23; border-radius: 10px;")
        self.editor_header.setStyleSheet("background-color: #231E23;")

        self.line1.setStyleSheet("background-color: #373737; border: none")
        self.line2.setStyleSheet("background-color: #373737; border: none")

        # 3. Tree Styling (Synced padding and added missing selection/hover states)
        self.tree.setStyleSheet("""
                    QTreeView {
                        color: #BDBDBD; 
                        font-size: 15px; 
                        border: none;
                        show-decoration-selected: 1;
                        outline: 0;
                    }
                    QTreeView::item {
                        padding-top: 4px;
                        padding-bottom: 4px;
                        padding-left: 3px;
                    }
                    QTreeView::item:selected {
                        background-color: #352B48;
                        border-radius: 4px;
                    }
                    QTreeView::item:selected:!active {
                        background-color: #302C35;
                    }
                    QTreeView::item:hover {
                        background-color: #302C35;
                        border-radius: 4px;
                    }
                    QTreeView::item:focus {
                        outline: none;
                        border: none;
                    }
                    QScrollBar:vertical {
                        border: none;
                        background: #312D39;
                        width: 13px;
                        margin: 0px;
                    }
                    QScrollBar::handle:vertical {
                        background: #211E29;
                        min-height: 20px;
                        border-radius: 5px;
                        margin: 2px;
                    }
                    QScrollBar::handle:vertical:hover {
                        background: #1A1723;
                    }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        height: 0px;
                    }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }
                """)

        # 4. Labels
        self.file_name_label.setStyleSheet(
            "font-size: 16px; font-weight: 520; color: #BDBDBD; border: none"
        )
        self.syntax_warning_breadcrumb.setStyleSheet(
            "font-size: 13px; color: #AD8FD0; border: none; font-weight: 520;"
        )

        # 5. Buttons (Synced the loop and specific transfer button style)
        self.transfer_button.setStyleSheet("""
                    QPushButton { 
                        border-radius: 10px; 
                        background-color: #2D274A; 
                        color: #B3B3B3;
                    }
                    QPushButton:hover {
                        background-color: #393158
                    }
                    QPushButton:disabled {
                        color: #B3B3B3;
                    }
                    QPushButton:pressed { background-color: #2D274A}
                """)
        self.transfer_button.text_label.setStyleSheet("""
                    font-size: 13px; 
                    font-weight: 520; 
                    background: transparent; 
                    border: none; 
                    color: #B3B3B3;
                    padding-bottom: 2px;
                """)

        for button in [self.reload_button, self.suggest_button, self.scan_button, self.save_button]:
            button.setStyleSheet("""
                    QPushButton { 
                        background-color: rgba(0, 0, 0, 0);
                        border-radius: 7px; 
                        color: #979797;
                        padding: 5px 0px;
                    }
                    QPushButton:hover {
                        background-color: #323039;
                    }
                    QPushButton:pressed {
                        background-color: rgba(0,0,0,0);
                    }
            """)
            button.text_label.setStyleSheet("""
                    font-size: 13px; 
                    font-weight: 515; 
                    background: transparent; 
                    border: none; 
                    color: inherit;
                    padding-bottom: 2px;
                    color: #979797;
            """)

        # 6. Editor Style
        self.editor.setStyleSheet("""
                    QPlainTextEdit {
                        color: #ddd;
                        border: none; 
                        border-top-left-radius: 10px;
                        border-top-right-radius: 10px;
                        font-family: 'Consolas', 'Monospace', 'Courier New';
                        font-size: 14px;
                    }
                    QScrollBar:vertical {
                        border: none;
                        border-radius: 8px;
                        background: #312D39;
                        width: 13px;
                        margin: 8px 0px 8px 0px;
                    }
                    QScrollBar::handle:vertical {
                        background: #211E29;
                        min-height: 20px;
                        border-radius: 8px;
                        margin: 2px;
                    }
                    QScrollBar::handle:vertical:hover {
                        background: #1A1723;
                    }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        height: 0px;
                    }
                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }
                """)
        self.editor.set_line_number_colors("#8F8699", "#1F1D23")
        self.syntax_panel.setStyleSheet("background-color: #2B2630; border-radius: 10px;")
        self.syntax_panel_title.setStyleSheet("font-size: 13px; color: #C4A3E8; font-weight: 600;")
        self.syntax_list.setStyleSheet("""
                    QListWidget {
                        border: none;
                        background-color: transparent;
                        color: #CFC8D8;
                        font-size: 12px;
                    }
                    QListWidget::item {
                        padding: 3px 2px;
                    }
                """)
