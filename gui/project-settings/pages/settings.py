from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(projectOptions())
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)


def projectOptions():
    grid_widget = QWidget()
    grid_layout = QGridLayout()
    grid_widget.setLayout(grid_layout)

    grid_layout.setContentsMargins(0, 0, 20, 20)
    grid_layout.setHorizontalSpacing(20)
    grid_layout.setVerticalSpacing(10)

    # Shared Styles
    input_style = (
        "border: 1px solid #474747;"
        "font-size: 16px;"
        "border-radius: 5px;"
        "background: #18181F;"
        "padding: 0px 5px"


    )
    label_style = "color: #ffffff; font-size: 15px; margin-top: 10px"

    # -------------------------------------------------------------
    # ------------------- GENERAL SETTINGS CARD -------------------
    # -------------------------------------------------------------
    gen_settings = QWidget()
    gen_settings.setMinimumWidth(300)
    gen_settings.setMinimumHeight(300)

    gen_settings_layout = QVBoxLayout()
    gen_settings_layout.setContentsMargins(20, 20, 20, 20)
    gen_settings.setLayout(gen_settings_layout)
    gen_settings.setStyleSheet("background-color: #16161A; border-radius: 10px;")

    gen_title = QLabel("General Settings")
    gen_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold; margin-bottom: 0px;")
    gen_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    gen_settings_layout.addWidget(gen_title)

    # Name
    lbl = QLabel("Project Name")
    lbl.setStyleSheet(label_style)
    gen_settings_layout.addWidget(lbl)

    name_input = QLineEdit()
    name_input.setStyleSheet(input_style)
    name_input.setFixedHeight(33)
    gen_settings_layout.addWidget(name_input)

    # SSH Path
    lbl = QLabel("SSH Connection Path")
    lbl.setStyleSheet(label_style)
    gen_settings_layout.addWidget(lbl)

    ssh_path_input = QLineEdit()
    ssh_path_input.setStyleSheet(input_style)
    ssh_path_input.setFixedHeight(33)
    gen_settings_layout.addWidget(ssh_path_input)

    # SSH Password
    lbl = QLabel("SSH Password")
    lbl.setStyleSheet(label_style)
    gen_settings_layout.addWidget(lbl)

    ssh_psw_input = QLineEdit()
    ssh_psw_input.setStyleSheet(input_style)
    ssh_psw_input.setFixedHeight(33)
    ssh_psw_input.setEchoMode(QLineEdit.EchoMode.Password)
    gen_settings_layout.addWidget(ssh_psw_input)

    # Add card to grid
    grid_layout.addWidget(gen_settings, 0, 0)


    # -------------------------------------------------------------
    # ------------------ WEIGHTS & BIASES CARD --------------------
    # -------------------------------------------------------------
    wandb_widget = QWidget()
    wandb_layout = QVBoxLayout()
    wandb_layout.setContentsMargins(20, 20, 20, 20)
    wandb_widget.setLayout(wandb_layout)
    wandb_widget.setStyleSheet("background-color: #16161A; border-radius: 10px;")

    wandb_title = QLabel("Weights & Biases")
    wandb_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold; margin-bottom: 0px;")
    wandb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    wandb_layout.addWidget(wandb_title)

    # API Key
    lbl = QLabel("API Key")
    lbl.setStyleSheet(label_style)
    wandb_layout.addWidget(lbl)

    wandb_api = QLineEdit()
    wandb_api.setStyleSheet(input_style)
    wandb_api.setFixedHeight(33)
    wandb_api.setEchoMode(QLineEdit.EchoMode.Password)
    wandb_layout.addWidget(wandb_api)

    # User/Team Name
    lbl = QLabel("User / Team Name")
    lbl.setStyleSheet(label_style)
    wandb_layout.addWidget(lbl)

    wandb_user = QLineEdit()
    wandb_user.setStyleSheet(input_style)
    wandb_user.setFixedHeight(33)
    wandb_layout.addWidget(wandb_user)

    # Project Name
    lbl = QLabel("Project Name")
    lbl.setStyleSheet(label_style)
    wandb_layout.addWidget(lbl)

    wandb_proj = QLineEdit()
    wandb_proj.setStyleSheet(input_style)
    wandb_proj.setFixedHeight(33)
    wandb_layout.addWidget(wandb_proj)

    grid_layout.addWidget(wandb_widget, 0, 1)


    # -------------------------------------------------------------
    # ------------------------- GITHUB CARD ------------------------
    # -------------------------------------------------------------
    github_widget = QWidget()
    github_layout = QVBoxLayout()
    github_layout.setContentsMargins(20, 20, 20, 20)
    github_widget.setLayout(github_layout)
    github_widget.setStyleSheet("background-color: #16161A; border-radius: 10px;")

    github_title = QLabel("GitHub")
    github_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold; margin-bottom: 0px;")
    github_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    github_layout.addWidget(github_title)

    # Repo URL
    lbl = QLabel("Repository URL")
    lbl.setStyleSheet(label_style)
    github_layout.addWidget(lbl)

    github_url = QLineEdit()
    github_url.setStyleSheet(input_style)
    github_url.setFixedHeight(33)
    github_layout.addWidget(github_url)

    # Username
    lbl = QLabel("GitHub Username")
    lbl.setStyleSheet(label_style)
    github_layout.addWidget(lbl)

    github_user = QLineEdit()
    github_user.setStyleSheet(input_style)
    github_user.setFixedHeight(33)
    github_layout.addWidget(github_user)

    # Personal Access Token
    lbl = QLabel("Personal Access Token")
    lbl.setStyleSheet(label_style)
    github_layout.addWidget(lbl)

    github_token = QLineEdit()
    github_token.setStyleSheet(input_style)
    github_token.setFixedHeight(33)
    github_token.setEchoMode(QLineEdit.EchoMode.Password)
    github_layout.addWidget(github_token)

    # Add to grid
    grid_layout.addWidget(github_widget, 0, 2)


    # ---- BUTTON ROW ----
    button_row = QHBoxLayout()
    button_row.setContentsMargins(10, 5, 0, 0)

    button_row.addStretch()

    # Create Project button (right)
    create_btn = QPushButton("Save Changes")
    create_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    create_btn.setMinimumWidth(185)
    create_btn.setMinimumHeight(40)
    create_btn.setStyleSheet(
        "background-color: #451C4B;"
                "border-radius: 5px;"
                "border: 0px solid #555555;"
                "padding: 8px 20px;"
                "color: white;"
                "font-weight: bold;"
                "font-size: 16px;"
    )
    button_row.addWidget(create_btn, alignment=Qt.AlignmentFlag.AlignRight)

    # Add row to the grid widget (below cards)
    grid_layout.addLayout(button_row, grid_layout.rowCount(), 0, 1, -1)


    return grid_widget