from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QGridLayout, QMessageBox
)
from PyQt6.QtCore import Qt
import database.database_crud as db_crud


class SettingsPage(QWidget):
    def __init__(self, project_name):
        super().__init__()
        self.project_name = project_name
        self.inputs = {}

        layout = QVBoxLayout()
        layout.addWidget(self.init_ui())
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

        self.load_project_data()

    def load_project_data(self):
        project = db_crud.get_project(self.project_name)
        if project:
            self.inputs['name'].setText(project['name'])
            self.inputs['ssh_path'].setText(project['ssh_path'])
            self.inputs['ssh_psw'].setText(project['ssh_psw'])
            self.inputs['wandb_api'].setText(project['wandb_api'])
            self.inputs['wandb_user'].setText(project['wandb_user'])
            self.inputs['wandb_proj'].setText(project['wandb_project'])
            self.inputs['github_url'].setText(project['git_url'])
            self.inputs['github_user'].setText(project['git_user'])
            self.inputs['github_token'].setText(project['git_path'])  # Adjust if column name differs

    def save_changes(self):
        updated_data = {
            "ssh_path": self.inputs['ssh_path'].text(),
            "ssh_psw": self.inputs['ssh_psw'].text(),
            "wandb_api": self.inputs['wandb_api'].text(),
            "wandb_user": self.inputs['wandb_user'].text(),
            "wandb_project": self.inputs['wandb_proj'].text(),
            "git_url": self.inputs['github_url'].text(),
            "git_user": self.inputs['github_user'].text(),
            "git_path": self.inputs['github_token'].text(),
        }

        try:
            db_crud.update_project(self.project_name, **updated_data)
            QMessageBox.information(self, "Success", "Project settings updated successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update project: {str(e)}")

    def init_ui(self):
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)
        grid_layout.setContentsMargins(0, 0, 20, 20)
        grid_layout.setHorizontalSpacing(20)
        grid_layout.setVerticalSpacing(10)

        input_style = ("border: 1px solid #3B3B3B; font-size: 16px; border-radius: 5px; "
                       "background: #1B1B20; padding: 0px 5px")
        label_style = "color: #ffffff; font-size: 15px; margin-top: 10px"

        # --- Helper to create labeled inputs ---
        def add_input(layout, label_text, key, password=False):
            lbl = QLabel(label_text)
            lbl.setStyleSheet(label_style)
            layout.addWidget(lbl)

            edit = QLineEdit()
            edit.setStyleSheet(input_style)
            edit.setFixedHeight(33)
            if password:
                edit.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addWidget(edit)
            self.inputs[key] = edit
            return edit

        # --- General Settings Card ---
        gen_card = QWidget()
        gen_card.setStyleSheet("background-color: #16161A; border-radius: 10px;")
        gen_vbox = QVBoxLayout(gen_card)

        gen_title = QLabel("General Settings")
        gen_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold;")
        gen_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gen_vbox.addWidget(gen_title)

        add_input(gen_vbox, "Project Name", "name").setReadOnly(True)  # PK shouldn't be edited easily
        add_input(gen_vbox, "SSH Connection Path", "ssh_path")
        add_input(gen_vbox, "SSH Password", "ssh_psw", True)
        grid_layout.addWidget(gen_card, 0, 0)

        # --- Weights & Biases Card ---
        wandb_card = QWidget()
        wandb_card.setStyleSheet("background-color: #16161A; border-radius: 10px;")
        wandb_vbox = QVBoxLayout(wandb_card)

        wandb_title = QLabel("Weights & Biases")
        wandb_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold;")
        wandb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wandb_vbox.addWidget(wandb_title)

        add_input(wandb_vbox, "API Key", "wandb_api", True)
        add_input(wandb_vbox, "User / Team Name", "wandb_user")
        add_input(wandb_vbox, "Project Name", "wandb_proj")
        grid_layout.addWidget(wandb_card, 0, 1)

        # --- GitHub Card ---
        git_card = QWidget()
        git_card.setStyleSheet("background-color: #16161A; border-radius: 10px;")
        git_vbox = QVBoxLayout(git_card)

        git_title = QLabel("GitHub")
        git_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold;")
        git_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        git_vbox.addWidget(git_title)

        add_input(git_vbox, "Repository URL", "github_url")
        add_input(git_vbox, "GitHub Username", "github_user")
        add_input(git_vbox, "Personal Access Token", "github_token", True)
        grid_layout.addWidget(git_card, 0, 2)

        # --- Button Row ---
        btn_row = QHBoxLayout()
        btn_row.addStretch()

        save_btn = QPushButton("Save Changes")
        save_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        save_btn.setFixedSize(185, 40)
        save_btn.setStyleSheet("background-color: #451C4B; border-radius: 5px; color: white; "
                               "font-weight: bold; font-size: 16px;")
        save_btn.clicked.connect(self.save_changes)
        btn_row.addWidget(save_btn)

        grid_layout.addLayout(btn_row, 1, 0, 1, 3)
        return grid_widget