from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTreeView, QFileIconProvider,
    QLabel, QPushButton, QSizePolicy, QLineEdit
)
from PyQt6.QtGui import QFileSystemModel, QIcon, QCursor
from PyQt6.QtCore import Qt, QDir, QSize


class CustomIconProvider(QFileIconProvider):
    def icon(self, file_info):
        if file_info.isDir():
            return QIcon("C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/folder.png")
        else:
            ext = file_info.suffix().lower()
            if ext in ["py", "txt", "md"]:
                return QIcon("C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/document.png")
            return QIcon("C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/document.png")


class FileTreePage(QWidget):
    def __init__(self, project_path: str):
        super().__init__()
        self.project_path = project_path

        # ----- MAIN HBOX LAYOUT -----
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 10, 15, 10)
        main_layout.setSpacing(20)

        # ---------------------------
        # LEFT SIDE — FILE TREE
        # ---------------------------
        self.model = QFileSystemModel()
        self.model.setRootPath(self.project_path)
        self.model.setFilter(QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot)
        self.model.setIconProvider(CustomIconProvider())

        self.tree = QTreeView()
        self.tree.setMaximumWidth(700)
        self.tree.setMinimumWidth(500)
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(self.project_path))
        self.tree.setHeaderHidden(True)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setAnimated(True)
        self.tree.setIndentation(30)
        self.tree.setIconSize(QSize(20, 20))
        self.tree.setUniformRowHeights(True)

        self.tree.setStyleSheet("""
            QTreeView {
                color: white;
                font-size: 18px;
                border: none;
                outline: 0;
            }
            QTreeView::item:selected {
                background-color: #18181F;
                color: white;
                border: none;
            }
            QTreeView::branch:has-siblings:!adjoins-item {
                border-image: none;
            }
            QTreeView::item {
                height: 36px;
            }
        """)

        main_layout.addWidget(self.tree, alignment=Qt.AlignmentFlag.AlignLeft)

