from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QLabel, QPushButton, QSizePolicy, QLineEdit
)
from PyQt6.QtGui import QIcon, QCursor, QStandardItemModel, QStandardItem
from PyQt6.QtCore import Qt, QSize


def build_nested_dict(self, paths):
    tree = {}
    for path in paths:
        # 1. Clean the string
        clean_path = path.strip()

        # 2. Skip useless entries
        if not clean_path or clean_path == ".":
            continue

        # 3. Remove leading './' properly
        if clean_path.startswith("./"):
            clean_path = clean_path[2:]
        elif clean_path.startswith("."):  # Case for just '.'
            clean_path = clean_path[1:]

        parts = clean_path.split('/')
        current_level = tree

        for part in parts:
            if not part: continue  # Skip double slashes //

            # 4. The "Merge" Logic
            # If the folder doesn't exist, create it.
            # If it DOES exist, we just move 'current_level' into it.
            if part not in current_level:
                current_level[part] = {}

            current_level = current_level[part]

    return tree


class FileTreePage(QWidget):
    def __init__(self, run_func):
        super().__init__()
        self.run_func = run_func


        # UI Setup
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 10, 15, 10)

        # 1. Initialize Model and Tree
        self.model = QStandardItemModel()
        self.tree = QTreeView()
        self.tree.setModel(self.model)

        # Styling and Configuration
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(25)
        self.tree.setIconSize(QSize(22, 22))
        self.tree.setStyleSheet("QTreeView { color: white; font-size: 16px; border: none; }")

        # 2. Wire the double-click event
        self.tree.doubleClicked.connect(self.on_item_double_clicked)

        main_layout.addWidget(self.tree)

    def rebuild_tree(self, raw_find_output):
        print(raw_find_output)
        """
        Call this every time you want to refresh the tree.
        It clears everything and rebuilds from the new 'find' string.
        """
        # Completely clear the existing items
        self.model.clear()

        # Parse the raw SSH string into a nested dict
        paths = [p for p in raw_find_output.strip().split('\n') if p.strip()]
        nested_data = self.build_nested_dict(paths)

        # Populate the model starting from the invisible root
        self.populate_tree(self.model.invisibleRootItem(), nested_data)

        # Optional: Auto-expand the first level for better UX
        self.tree.expandToDepth(0)

    def build_nested_dict(self, paths):
        """
        Transforms flat path strings into a nested dictionary structure.
        Expected input: ['./models/cnn.py', './data/train.csv', 'utils.py']
        """
        tree = {}
        for path in paths:
            # Clean the path: remove leading './', strip whitespace
            clean_path = path.strip()
            if clean_path.startswith("./"):
                clean_path = clean_path[2:]

            # Skip if it's just the root dot or empty
            if not clean_path or clean_path == ".":
                continue

            parts = clean_path.split('/')
            current_level = tree

            for i, part in enumerate(parts):
                # If we are at the last part, it's a file (unless it was already a folder)
                if i == len(parts) - 1:
                    if part not in current_level:
                        current_level[part] = {}  # Mark as leaf (empty dict)
                else:
                    # It's a directory
                    if part not in current_level:
                        current_level[part] = {}
                    elif not isinstance(current_level[part], dict):
                        # Safety check: if a file and folder share a name (rare in Linux)
                        current_level[part] = {}

                    current_level = current_level[part]
        return tree

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