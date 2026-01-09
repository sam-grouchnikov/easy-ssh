from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView,
    QLabel, QPushButton, QSizePolicy, QLineEdit, QPlainTextEdit
)
from PyQt6.QtGui import QIcon, QCursor, QStandardItemModel, QStandardItem, QFont
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PyQt6.QtCore import QRegularExpression


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, parent):
        super().__init__(parent)
        self.rules = []

        # Keyword Format (e.g., def, class, if, else)
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))  # Light Blue
        keywords = ["def", "class", "import", "from", "if", "else", "return", "for", "while", "try", "except", "with", "len", "with"]

        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.rules.append((pattern, keyword_format))

        # String Format (anything between quotes)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))  # Salmon/Orange
        self.rules.append((QRegularExpression("\".*\""), string_format))
        self.rules.append((QRegularExpression("'.*'"), string_format))

        # Comment Format (# text)
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))  # Green
        self.rules.append((QRegularExpression("#.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, format in self.rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

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
    def __init__(self, run_func, home_dir):
        super().__init__()
        self.run_func = run_func
        self.home_dir = home_dir


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
        self.tree.setMaximumWidth(600)


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

        self.editor_widget = QWidget()
        self.editor_layout = QVBoxLayout(self.editor_widget)

        self.save_button = QPushButton("Save Changes")
        self.save_button.setFixedWidth(120)
        self.save_button.clicked.connect(self.save_remote_file)
        self.save_button.setEnabled(False)
        self.editor_layout.addWidget(self.save_button)

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
        self.editor_layout.addWidget(self.editor)
        self.highlighter = PythonHighlighter(self.editor.document())
        # Add widgets to layout
        self.main_layout.addWidget(self.tree)
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
        print("Finished load")

    def display_file_content(self, content):
        self.editor.setPlainText(content)
        self.editor.setReadOnly(False)
        self.save_button.setEnabled(True)

    def save_remote_file(self):
        print("Saving remote file")
        if not self.current_open_path:
            return

        content = self.editor.toPlainText()

        # We use a 'heredoc' to write the file.
        # 'EOF' is quoted to prevent the shell from evaluating variables like $HOME
        print(f"Saving to {self.current_open_path}")
        command = f"cat << 'EOF' > {self.current_open_path}\n{content}\nEOF"

        self.save_button.setText("Saving...")
        self.save_button.setEnabled(False)

        # Run the command. We don't need a special flag here unless
        # you want to capture the 'Success' message specifically.
        self.run_func(command, is_file_save=True)

        # Reset button after a short delay or via the 'finished' signal
        self.save_button.setText("Save Changes")
        self.save_button.setEnabled(True)
        print("Saved")


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
        self.run_func(f"cat '{file_path}'", is_file_read=True)