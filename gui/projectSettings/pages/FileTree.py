#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.1.0
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
from PyQt6.QtWidgets import QStyle


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
        # 1. Clean the individual string
        clean_path = path.strip()

        # 2. Skip useless entries
        if not clean_path or clean_path == ".":
            continue

        # 3. Standardize paths
        if clean_path.startswith("./"):
            clean_path = clean_path[2:]
        elif clean_path.startswith("."):
            clean_path = clean_path[1:]

        parts = clean_path.split('/')
        current_level = tree

        for part in parts:
            if not part:
                continue

            # 4. Use setdefault to merge folders
            if part not in current_level:
                current_level[part] = {}

            current_level = current_level[part]

    return tree


class FileTreePage(QWidget):
    def __init__(self, run_func, home_dir, config, ssh_manager):
        super().__init__()
        self.run_func = run_func
        self.home_dir = home_dir
        self.config = config
        self.ssh_manager = ssh_manager

        # UI Setup
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

        self.tree_container = QWidget()
        # This creates the internal padding for the "Files" title and tree
        self.tree_container.setContentsMargins(3, 10, 3, 10)
        self.tree_container.setFixedWidth(450)
        self.tree_container.setObjectName("tree_container")

        self.tree_container_layout = QVBoxLayout()
        self.tree_container_layout.setContentsMargins(0, 16, 0, 0)
        self.tree_container.setLayout(self.tree_container_layout)

        self.files_title = QLabel("Files")
        self.files_title.setContentsMargins(30,0,0,0)
        self.tree_container_layout.addWidget(self.files_title)
        self.tree_container_layout.addSpacing(5)

        self.line1 = QFrame()
        self.line1.setFrameShape(QFrame.Shape.HLine)
        self.line1.setFixedHeight(2)
        self.line1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.tree_container_layout.addWidget(self.line1)




        # 1. Initialize Model and Tree
        self.model = QStandardItemModel()

        self.tree_layout = QVBoxLayout()
        self.tree_layout.setContentsMargins(23, 0, 0, 0)

        self.tree = QTreeView()
        self.tree.setContentsMargins(0,0,0,0)
        self.tree.setModel(self.model)

        # Styling and Configuration
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(25)
        self.tree.setIconSize(QSize(22, 22))



        # 2. Wire the double-click event
        self.tree.doubleClicked.connect(self.on_item_double_clicked)
        self.tree_layout.addWidget(self.tree)

        self.tree_container_layout.addLayout(self.tree_layout)
        self.main_layout.addWidget(self.tree_container)


        # ---- Editor Container ----
        self.editor_widget = QWidget()
        editor_shadow = QGraphicsDropShadowEffect()
        editor_shadow.setBlurRadius(4)
        editor_shadow.setXOffset(0)
        editor_shadow.setYOffset(0)
        editor_shadow.setColor(QColor(0, 0, 0, 80))
        self.editor_widget.setGraphicsEffect(editor_shadow)
        self.editor_widget.setObjectName("EditorContainer")
        self.editor_widget.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.editor_layout = QVBoxLayout(self.editor_widget)
        self.editor_layout.setContentsMargins(4, 4, 0, 4)
        self.editor_layout.setSpacing(0)

        # ---- Editor Header ----
        self.editor_header = QWidget()
        self.editor_header_layout = QHBoxLayout(self.editor_header)
        self.editor_header_layout.setContentsMargins(25, 23, 20, 0)
        self.editor_header.setStyleSheet("border: none;")
        self.editor_header_layout.setSpacing(15)

        # Title (File Name)
        self.file_name_label = QLabel("No File Selected")

        self.editor_header_layout.addWidget(self.file_name_label)

        self.editor_header_layout.addStretch()

        self.save_button = QPushButton()
        self.save_button.clicked.connect(self.save_remote_file)
        self.save_button.setEnabled(False)
        self.save_button.setFixedSize(180, 35)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(4)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 30))
        self.save_button.setGraphicsEffect(shadow)

        self.save_btn_layout = QHBoxLayout(self.save_button)
        self.save_btn_layout.setContentsMargins(10, 0, 10, 0)
        self.save_btn_layout.setSpacing(12)

        self.save_icon_label = QLabel()

        self.save_icon_label.setStyleSheet("background: transparent; border: none;")

        # 4. Save Text Label
        self.save_text_label = QLabel("Save Changes")


        # 5. Assemble the internal parts
        self.save_btn_layout.addStretch()
        self.save_btn_layout.addWidget(self.save_icon_label)
        self.save_btn_layout.addWidget(self.save_text_label)
        self.save_btn_layout.addStretch()
        self.save_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.transfer_button = QPushButton()
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(4)
        shadow2.setXOffset(0)
        shadow2.setYOffset(0)
        shadow2.setColor(QColor(0, 0, 0, 30))
        self.transfer_button.setGraphicsEffect(shadow2)
        self.transfer_button.setEnabled(False)
        self.transfer_button.clicked.connect(self.transfer_remote_file)
        self.transfer_button.setFixedSize(155, 35)
        self.transfer_button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))



        self.transfer_btn_layout = QHBoxLayout(self.transfer_button)
        self.transfer_btn_layout.setContentsMargins(15, 0, 15, 0)
        self.transfer_btn_layout.setSpacing(12)

        self.transfer_icon_label = QLabel()

        self.transfer_icon_label.setStyleSheet("background: transparent; border: none;")

        self.transfer_text_label = QLabel("Download")


        self.transfer_btn_layout.addStretch()
        self.transfer_btn_layout.addWidget(self.transfer_icon_label)
        self.transfer_btn_layout.addWidget(self.transfer_text_label)
        self.transfer_btn_layout.addStretch()


        # Add buttons to the horizontal header layout
        self.editor_header_layout.addWidget(self.save_button)
        self.editor_header_layout.addWidget(self.transfer_button)

        # --- Add the header and the line to the main editor layout ---
        self.editor_layout.addWidget(self.editor_header)
        self.editor_layout.addSpacing(10)

        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.Shape.HLine)
        self.line2.setFixedHeight(2)
        self.line2.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.editor_layout.addWidget(self.line2)

        self.editor_wrapper= QWidget()
        self.editor_wrapper.setStyleSheet("border: none")
        self.editor_wrapper.setContentsMargins(0,0,0,5)
        self.editor_wrapper_layout = QVBoxLayout(self.editor_wrapper)
        self.editor = QPlainTextEdit()
        self.editor.document().setDocumentMargin(19)
        self.editor.setReadOnly(True)
        self.editor.setPlaceholderText("Select a file to view and edit its contents...")

        font = QFont("Consolas", 12) if "Consolas" in QFont().families() else QFont("Monospace", 12)
        self.editor.setFont(font)

        self.editor_widget.setObjectName("EditorContainer")
        self.editor_wrapper_layout.addWidget(self.editor)
        self.editor_layout.addWidget(self.editor_wrapper)



        self.highlighter = PythonHighlighter(self.editor.document())
        self.main_layout.addWidget(self.editor_widget)
        self.current_open_path = None

        # --- 3. Connections ---
        # Triggered when clicking an item
        self.tree.clicked.connect(self.on_file_selected)


    def update_home(self, new):
        self.home_dir = new

    def on_file_selected(self, index):
        item = self.model.itemFromIndex(index)
        if not item.hasChildren():
            file_path = item.data(Qt.ItemDataRole.UserRole)
            print("checkpihhhh", self.home_dir)
            self.current_open_path = "" + self.home_dir + "/" + file_path
            print(f"Current open_path: {self.current_open_path}")
            self.load_remote_file(self.current_open_path)

    def load_remote_file(self, path):
        print(f"Loading remote file: {path}")
        self.editor.setPlainText(f"Loading {path}...")
        cmd = f"cat '{path}'"
        self.run_func(cmd, is_file_read=True)
        split = path.split("/")
        last = split[len(split) - 1]
        self.file_name_label.setText(last)
        print("Finished load")

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

        print(f"Saving to {self.current_open_path}")
        command = f"cat << 'EOF' > {self.current_open_path}\n{content}\nEOF"

        self.save_button.setEnabled(False)

        self.run_func(command, is_file_save=True)

        # Reset button after a short delay or via the 'finished' signal
        self.save_text_label.setText("Save Changes")
        self.save_button.setEnabled(True)

    def transfer_remote_file(self):
        if not self.current_open_path:
            return

        local_dir = QFileDialog.getExistingDirectory(self, "Select Save Folder")

        if local_dir:
            try:
                transport = self.ssh_manager.client.get_transport()

                with SCPClient(transport) as scp:
                    print(f"Downloading: {self.current_open_path}")
                    scp.get(self.current_open_path, local_dir)

                QMessageBox.information(self, "Success", "File transferred successfully!")

            except Exception as e:
                QMessageBox.critical(self, "Transfer Failed", f"Error: {str(e)}")

    def rebuild_tree(self, raw_find_output):

        print("Rebuild tree started")
        # Completely clear the existing items
        self.model.clear()
        print("Ckpt1")

        # Parse the raw SSH string into a nested dict
        paths = [p for p in raw_find_output.split('\n')]
        print("Ckpt1.5")

        nested_data = build_nested_dict(paths)
        print("Ckpt2")

        # Populate the model starting from the invisible root
        self.populate_tree(self.model.invisibleRootItem(), nested_data)
        print("rebuild tree ended")

    def populate_tree(self, parent_item, data_dict, current_full_path=""):
        # Sort: Folders first, then Alphabetical
        sorted_names = sorted(data_dict.keys(), key=lambda s: (not data_dict[s], s.lower()))

        for name in sorted_names:
            item = QStandardItem(name)
            item.setEditable(False)

            item_path = f"{current_full_path}/{name}" if current_full_path else name
            item.setData(item_path, Qt.ItemDataRole.UserRole)

            if data_dict[name]:
                item.setIcon(QIcon("gui/icons/folder.png"))
                parent_item.appendRow(item)
                self.populate_tree(item, data_dict[name], item_path)
            else:
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

        def traverse(item):
            for i in range(item.rowCount()):
                child = item.child(i)
                if child.hasChildren():
                    child.setIcon(QIcon(folder_icon_path))
                    traverse(child)
                else:
                    child.setIcon(QIcon(file_icon_path))

        traverse(root)

    def set_light_mode(self):
        self.update_tree_icons("gui/icons/folder.png", "gui/icons/document.png")
        self.tree_container.setStyleSheet("""
                    QWidget#tree_container {

                        border-radius: 12px;
                        border: 1px solid #E0D5E0;
                    }
                    QWidget { background-color: #f8f1fa; } 
                """)
        self.files_title.setStyleSheet("font-size: 32px; font-weight: 520; color: #583068")
        self.line1.setStyleSheet("background-color: #CBCBCB")
        self.tree.setStyleSheet("""
                                QTreeView {
                                    color: black; font-size: 16px; border: none;
                                }
                                QTreeView::item {
                                padding-top: 4px;
                                padding-bottom: 4px;
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
        self.editor_widget.setStyleSheet("""
                    QWidget#EditorContainer {
                        background-color: #F9F9FF;
                        border-radius: 12px;
                    }
                """)
        self.file_name_label.setStyleSheet(
            "font-size: 32px; font-weight: 520; color: #583068; border: none"
        )
        self.save_button.setStyleSheet("""
                    QPushButton { 
                        background-color: #f3ecf4;
                        border-radius: 15px; 
                        color: #444;
                    }
                    QPushButton:hover {
                        background-color: #ede6ee
                    }
                    QPushButton:pressed { background-color: #f3ecf4; }
                    QPushButton:disabled {
                        color: #AAAAAA;
                    }
                """)
        self.save_text_label.setStyleSheet("""
                    font-size: 16px; 
                    font-weight: 500; 
                    background: transparent; 
                    border: none; 
                    color: inherit;
                """)
        self.transfer_button.setStyleSheet("""
                    QPushButton { 
                        border-radius: 15px; 
                        background-color: #ECDCFF; 
                        color: #444;
                    }
                    QPushButton:hover {
                        background-color: #E1C7FF
                    }
                    QPushButton:pressed { background-color: #ECDCFF}
                """)
        self.transfer_text_label.setStyleSheet("""
                    font-size: 16px; 
                    font-weight: 500; 
                    background: transparent; 
                    border: none; 
                    color: inherit;
                """)
        self.line2.setStyleSheet("background-color: #D7D7D7")
        self.editor.setStyleSheet("""
                    QPlainTextEdit {
                        color: #444;
                        border: none; 
                        border-bottom: 1px solid #555555;
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
        self.save_pixmap = QPixmap("gui/icons/diskette.png").scaled(
            18, 18,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.save_icon_label.setPixmap(self.save_pixmap)
        self.transfer_pixmap = QPixmap("gui/icons/download.png").scaled(
            17, 17,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.transfer_icon_label.setPixmap(self.transfer_pixmap)




    def set_dark_mode(self):
        self.update_tree_icons("gui/icons/folder_dark.png", "gui/icons/document_dark.png")
        self.tree_container.setStyleSheet("""
                            QWidget#tree_container {

                                border-radius: 12px;
                                border: 1px solid #2A2A2A;
                            }
                            QWidget { background-color: #1A1921; } 
                        """)
        self.files_title.setStyleSheet("font-size: 32px; font-weight: 520; color: #CC98E1")
        self.line1.setStyleSheet("background-color: #4E4E4E; border: none")
        self.tree.setStyleSheet("""
                                        QTreeView {
                                            color: #A2A2A2; font-size: 16px; border: none;
                                        }
                                        QTreeView::item {
                                        padding-top: 4px;
                                        padding-bottom: 4px;
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
                                border: 1px solid #2C2C2C
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
        self.save_text_label.setStyleSheet("""
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
        self.transfer_text_label.setStyleSheet("""
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
                                border-bottom: 1px solid #555555;
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
        self.save_pixmap = QPixmap("gui/icons/save_dark.png").scaled(
            18, 18,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.save_icon_label.setPixmap(self.save_pixmap)
        self.transfer_pixmap = QPixmap("gui/icons/download_dark.png").scaled(
            17, 17,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.transfer_icon_label.setPixmap(self.transfer_pixmap)
