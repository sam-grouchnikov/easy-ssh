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


        # ---------------------------
        # RIGHT SIDE — FILE UPLOAD AREA
        # ---------------------------
        # --- RIGHT SIDE — FILE UPLOAD AREA ---
        upload_widget = QWidget()
        upload_layout = QVBoxLayout(upload_widget)
        upload_widget.setMaximumWidth(550)
        upload_widget.setMinimumHeight(550)
        upload_layout.setContentsMargins(20, 20, 20, 20)
        upload_layout.setSpacing(10)
        upload_widget.setStyleSheet("background: #1F1F1F; border-radius: 10px")

        # --- Titles ---
        label = QLabel("File Upload")
        label.setStyleSheet("color: white; font-size: 22px;")
        label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        upload_layout.addWidget(label)

        label2 = QLabel("Add your file(s) here")
        label2.setStyleSheet("color: #A3A3A3; font-size: 15px;")
        label2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        upload_layout.addWidget(label2)

        # --- Upload Area Container ---
        container = QWidget()
        container.setCursor(Qt.CursorShape.PointingHandCursor)
        container.setObjectName("uploadContainer")
        container.setStyleSheet("""
            #uploadContainer {
                background: #1F1F1F;
                border-radius: 10px;
                border: 1px solid #265171;
                transition: all 0.2s;
                margin-top: 15px
            }
            #uploadContainer:hover {
                border: 2px solid #265171;
                background: #252525;
            }
        """)
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(20, 20, 20, 20)
        container_layout.setSpacing(0)

        upload_area = UploadArea()
        upload_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        upload_area.setFixedHeight(140)  # consistent height
        container_layout.addWidget(upload_area)

        upload_layout.addWidget(container)

        # --- Upload Path Inputs ---
        def add_input(label_text, placeholder=""):
            lbl = QLabel(label_text)
            lbl.setStyleSheet("color: #A3A3A3; font-size: 15px; margin-top: 10px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
            upload_layout.addWidget(lbl)

            line_edit = QLineEdit()
            line_edit.setStyleSheet("""
                border: 1px solid #265171;
                border-radius: 5px;
                padding-left: 10px;
                color: white;
            """)
            line_edit.setFixedHeight(38)
            if placeholder:
                line_edit.setPlaceholderText(placeholder)
            line_edit.setMaximumWidth(int(upload_widget.maximumWidth() * 0.6))
            upload_layout.addWidget(line_edit)
            return line_edit

        add_input("Specify the upload path", "ex. parent/first-child/file.py")
        add_input("(Optional) New file name")
        upload_layout.addStretch()

        # --- Confirm Button ---
        confirm_button = QPushButton("Confirm Changes")
        confirm_button.setFixedHeight(40)
        confirm_button.setFixedWidth(200)
        confirm_button.setCursor(Qt.CursorShape.PointingHandCursor)
        confirm_button.setStyleSheet("""
            QPushButton {
                background: #265171;
                border-radius: 10px;
                color: white;
                font-size: 15px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background: #3B6E92;
            }
        """)
        # Center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(confirm_button)
        button_layout.addStretch()
        upload_layout.addLayout(button_layout)

        upload_layout.addStretch()
        main_layout.addWidget(upload_widget, stretch=1)


class UploadArea(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 20, 0, 20)   # keep vertical padding, no horizontal padding

        # --- Icon ---
        icon_label = QLabel()
        icon = QIcon("C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/upload.png")
        icon_label.setPixmap(icon.pixmap(40, 40))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("border: none; background: none;")

        # --- First line text ---
        title = QLabel("Drag your files or browse")
        title.setStyleSheet("color: white; font-size: 20px;; background: none;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --- Second line text ---
        subtitle = QLabel("Drag & drop files here or click to browse")
        subtitle.setStyleSheet("color: #AAAAAA; font-size: 15px;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("border: none; font-size: 15px; color: #8C8C8C; background: none;")

        layout.addWidget(icon_label)
        layout.addWidget(title)
        layout.addWidget(subtitle)




