from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QLabel, QPushButton, QSizePolicy, QLineEdit, QPlainTextEdit
)
from PyQt6.QtGui import QIcon, QCursor, QStandardItemModel, QStandardItem, QFont
from PyQt6.QtCore import Qt, QSize


def build_nested_dict(paths):

    tree = {}

    # 'paths' is the list ['/dir/file1', '/dir/file2']
    for path in paths:
        # 1. Clean the individual string
        # This is where the error was likely happening (calling .strip on the list)
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
    def __init__(self, run_func):
        super().__init__()
        self.run_func = run_func


        # UI Setup
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 10, 15, 10)

        # 1. Initialize Model and Tree
        self.model = QStandardItemModel()

        self.tree = QTreeView()
        self.tree.setModel(self.model)

        # Styling and Configuration
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(25)
        self.tree.setIconSize(QSize(22, 22))
        self.tree.setMinimumWidth(500)
        self.tree.setMaximumWidth(1000)


        self.tree.setStyleSheet("""
                        QTreeView {
                            color: white; font-size: 16px; border: none;
                        }
                        QTreeView::item {
                        padding-top: 4px;
                        padding-bottom: 4px;
                        }
                    """)

        # 2. Wire the double-click event
        self.tree.doubleClicked.connect(self.on_item_double_clicked)

        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)  # Start as read-only until a file is loaded
        self.editor.setPlaceholderText("Select a file to view its content...")

        # Professional Monospace Font for code
        font = QFont("Consolas", 12) if "Consolas" in QFont().families() else QFont("Monospace", 12)
        self.editor.setFont(font)

        self.editor.setStyleSheet("""
                    QPlainTextEdit {
                        color: #d4d4d4;
                        background-color: #1e1e1e;
                        border: 1px solid #333;
                        padding: 10px;
                    }
                """)

        # Add widgets to layout
        self.main_layout.addWidget(self.tree)
        self.main_layout.addWidget(self.editor)

        # --- 3. Connections ---
        # Triggered when clicking an item
        self.tree.clicked.connect(self.on_file_selected)

    def on_file_selected(self, index):
        item = self.model.itemFromIndex(index)
        if not item.hasChildren():
            file_path = item.data(Qt.ItemDataRole.UserRole)
            self.load_remote_file(file_path)

    def load_remote_file(self, path):
        self.editor.setPlainText(f"Loading {path}...")
        cmd = f"cat '{path}'"
        self.run_func(cmd, is_file_read=True)

    def display_file_content(self, content):
        self.editor.setPlainText(content)
        self.editor.setReadOnly(False)

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

            # Metadata: Store the actual remote path
            item_path = f"{current_full_path}/{name}" if current_full_path else name
            item.setData(item_path, Qt.ItemDataRole.UserRole)

            if data_dict[name]:  # This is a folder
                item.setIcon(QIcon("gui/icons/folder.png"))
                parent_item.appendRow(item)
                self.populate_tree(item, data_dict[name], item_path)
            else:  # This is a file
                item.setIcon(QIcon("gui/icons/document.png"))
                parent_item.appendRow(item)

    def on_item_double_clicked(self, index):
        item = self.model.itemFromIndex(index)
        file_path = item.data(Qt.ItemDataRole.UserRole)

        # Don't try to 'cat' folders
        if item.hasChildren():
            return

        # Trigger the load via SSH
        # We wrap in quotes to handle paths with spaces
        self.run_func(f"cat '{file_path}'")