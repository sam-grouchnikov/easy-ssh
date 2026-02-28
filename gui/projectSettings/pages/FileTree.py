#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.2.1
Email: sam.grouchnikov@gmail.com
Status: Development
"""


from PyQt6.QtCore import QRegularExpression
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QStandardItemModel, QStandardItem, QCursor, QPixmap
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QPushButton, QPlainTextEdit, QFileDialog, QMessageBox, QLabel, QFrame, QSizePolicy, QGraphicsDropShadowEffect
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


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

        # Keyword Format (e.g., def, class, if, else)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))  # Light Blue
        keywords = ["def", "class", "import", "from", "if", "else", "return", "for", "while", "try", "except", "with",
                    "len", "with", "self"]

        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.rules.append((pattern, keyword_format))

        # String Format (anything between quotes)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))
        self.rules.append((QRegularExpression("\".*\""), string_format))
        self.rules.append((QRegularExpression("'.*'"), string_format))

        # Comment Format (# text)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))
        self.rules.append((QRegularExpression("#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)


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
        self.config = config
        self.ssh_manager = ssh_manager
        self.current_open_path = None

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
        self.top_layout.addWidget(self.suggest_button)
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
        pixmap = QPixmap("gui/icons/editor/files_light.png").scaled(
            19,
            19,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.file_icon.setPixmap(pixmap)
        self.tree_header_layout.addWidget(self.file_icon)

        self.files_label = QLabel("Files")
        self.files_label.setStyleSheet("font-weight: 520; color: #303030; font-size: 16px")
        self.tree_header_layout.addWidget(self.files_label)

        self.tree_header_layout.addStretch()

        self.path_label = QLabel("sam@192.xxx.xx.xx:/~")
        self.path_label.setStyleSheet("color: #888; font-weight: 510; font-size: 14.5px")
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

        self.editor_layout.addWidget(self.editor_header)
        self.editor_layout.addSpacing(7)

        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFixedHeight(2)
        self.line2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.editor_layout.addWidget(self.line2)

    def _setup_editor_area(self):
        self.editor_wrapper = QWidget()
        self.editor_wrapper.setStyleSheet("border: none")
        self.editor_wrapper.setContentsMargins(0, 0, 0, 5)
        self.editor_wrapper_layout = QVBoxLayout(self.editor_wrapper)

        self.editor = QPlainTextEdit()
        self.editor.document().setDocumentMargin(17)
        self.editor.setReadOnly(True)
        self.editor.setPlaceholderText("Select a file to view and edit its contents...")

        font = QFont("Consolas", 12) if "Consolas" in QFont().families() else QFont("Monospace", 12)
        self.editor.setFont(font)

        self.editor_wrapper_layout.addWidget(self.editor)
        self.editor_layout.addWidget(self.editor_wrapper)

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
        self.editor.setPlainText("Select a file to view and edit its contents...")
        self.transfer_button.setEnabled(False)
        self.save_button.setEnabled(False)

    def display_file_content(self, content):
        self.editor.setPlainText(content)
        self.editor.setReadOnly(False)
        self.save_button.setEnabled(True)
        self.transfer_button.setEnabled(True)

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
                item.setIcon(QIcon("gui/icons/document.png"))
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
        self.update_tree_icons("gui/icons/editor/folder_light.png", "gui/icons/document.png")
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
            background-color: #ffffff
        """)
        self.editor_header.setStyleSheet("""
                    background-color: #ffffff
                """)
        self.file_name_label.setStyleSheet(
            "font-size: 16px; font-weight: 520; color: #583068; border: none"
        )

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
                        color: #444;
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
                            color: inherit;
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
                                    background: #E9E9E9;
                                    width: 13px;
                                    margin: 0px 0px 0px 0px;
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
        self.save_button.set_icon("gui/icons/editor/save_light.png")
        self.transfer_button.set_icon("gui/icons/editor/download_light.png")
        self.reload_button.set_icon("gui/icons/editor/refresh_light.png")
        self.scan_button.set_icon("gui/icons/editor/scan_light.png")
        self.suggest_button.set_icon("gui/icons/editor/suggest_light.png")




    def set_dark_mode(self):
        self.update_tree_icons("gui/icons/editor/folder_light", "gui/icons/document_dark.png")
        self.tree_container.setStyleSheet("""
                            QWidget#tree_container {

                                border-radius: 12px;
                            }
                            QWidget { background-color: #1A1921; } 
                        """)
        self.line1.setStyleSheet("background-color: #4E4E4E; border: none")
        self.tree.setStyleSheet("""
                                        QTreeView {
                                            color: #A2A2A2; font-size: 16px; border: none;
                                        }
                                        QTreeView::item {
                                        padding-top: 4px;
                                        padding-bottom: 6px;
                                        padding-left: 5px;
                                        }
                                        QScrollBar:vertical {
                                            border: none;
                                            background: #312D39;
                                            width: 10px;
                                            margin: 0px 0px 0px 0px;
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
                                background-color: #141318;
                                border-radius: 12px;
                            }
                        """)
        self.file_name_label.setStyleSheet(
            "font-size: 32px; font-weight: 520; color: #CC98E1; border: none"
        )
        self.save_button.setStyleSheet("""
                            QPushButton { 
                                background-color: #342E39;
                                border-radius: 15px; 
                                color: #EADCFB;
                            }
                            QPushButton:hover {
                                background-color: #443C4A
                            }
                            QPushButton:pressed { background-color: #342E39; }
                            QPushButton:disabled {
                                color: #AAAAAA;
                            }
                        """)
        self.save_button.text_label.setStyleSheet("""
                            font-size: 16px; 
                            font-weight: 500; 
                            background: transparent; 
                            border: none; 
                            color: #EADCFB;
                        """)
        self.transfer_button.setStyleSheet("""
                            QPushButton { 
                                border-radius: 15px; 
                                background-color: #493E76; 
                                color: #FCFCFC;
                            }
                            QPushButton:hover {
                                background-color: #544983
                            }
                            QPushButton:pressed { background-color: #493E76}
                        """)
        self.transfer_button.text_label.setStyleSheet("""
                            font-size: 16px; 
                            font-weight: 500; 
                            background: transparent; 
                            border: none; 
                            color: #FCFCFC;
                        """)
        self.line2.setStyleSheet("background-color: #434343; border: none")
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
                                            background: #312D39;
                                            width: 13px;
                                            margin: 0px 0px 0px 0px;
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

                            /* Remove the buttons (arrows) at the top and bottom */
                            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                height: 0px;
                            }

                            /* Remove the background area above and below the handle */
                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                        """)
        self.save_button.set_icon("gui/icons/save_dark.png")
        self.transfer_button.set_icon("gui/icons/download_dark.png")
