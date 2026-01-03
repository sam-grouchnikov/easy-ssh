from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QWidget,
    QGridLayout, QHBoxLayout, QToolButton, QFrame, QLineEdit
)
from PyQt6.QtCore import Qt
import database.database_crud
from database.database import get_connection
import time


def setupContent(layout: QVBoxLayout, navigate, config):
    title_label = QLabel("Welcome to Easy-SSH!")
    title_label.setStyleSheet("color: white; font-size: 40px; font-weight: bold; margin-left: 13px; padding-left: 0px")
    layout.addWidget(title_label)

    secondary_label = QLabel("Enter your details below")
    secondary_label.setStyleSheet("color: gray; font-size: 19px; margin-left: 20px")
    layout.addWidget(secondary_label)


    border = QFrame()
    border.setFrameShape(QFrame.Shape.HLine)
    border.setFixedHeight(3)
    border.setStyleSheet("color: #969696; margin-left: 20px")
    layout.addWidget(border)

    layout.addWidget(projectOptions(navigate, config))

    layout.addStretch()


def projectOptions(navigate, config):
    grid_widget = QWidget()
    grid_layout = QGridLayout()
    grid_widget.setLayout(grid_layout)

    grid_layout.setContentsMargins(20, 5, 20, 20)
    grid_layout.setHorizontalSpacing(20)
    grid_layout.setVerticalSpacing(20)

    # Shared Styles
    input_style = (
        "border: 1px solid #3B3B3B;"
        "font-size: 16px;"
        "border-radius: 5px;"
        "background: #1B1B20;"
        "padding: 0px 5px"
    )
    label_style = "color: #ffffff; font-size: 18px;"

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
    gen_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold; margin-bottom: 10px;")
    gen_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    gen_settings_layout.addWidget(gen_title)

    # Name
    lbl = QLabel("Username")
    lbl.setStyleSheet(label_style)
    gen_settings_layout.addWidget(lbl)

    name_input = QLineEdit()
    name_input.setStyleSheet(input_style)
    name_input.setFixedHeight(30)
    gen_settings_layout.addWidget(name_input)

    # SSH Path
    # 1. Create a horizontal container and layout
    ssh_conn_container = QWidget()
    ssh_conn_layout = QHBoxLayout(ssh_conn_container)
    ssh_conn_layout.setContentsMargins(0, 0, 0, 0)
    ssh_conn_layout.setSpacing(10)

    # 2. Connection Path Section (VBox to keep label over input)
    path_vbox = QVBoxLayout()
    path_lbl = QLabel("SSH Connection Path")
    path_lbl.setStyleSheet(label_style)
    path_input = QLineEdit()
    path_input.setStyleSheet(input_style)
    path_input.setFixedHeight(30)
    path_vbox.addWidget(path_lbl)
    path_vbox.addWidget(path_input)

    # 3. Port Section (VBox to keep label over input)
    port_vbox = QVBoxLayout()
    port_lbl = QLabel("Port")
    port_lbl.setStyleSheet(label_style)
    port_input = QLineEdit()
    port_input.setFixedWidth(80)  # Ports are small
    port_input.setStyleSheet(input_style)
    port_input.setFixedHeight(30)
    port_vbox.addWidget(port_lbl)
    port_vbox.addWidget(port_input)

    # 4. Add VBoxes to the HBox
    ssh_conn_layout.addLayout(path_vbox, stretch=4)  # Path gets more space
    ssh_conn_layout.addLayout(port_vbox, stretch=1)  # Port stays small

    # 5. Add the container to your main settings layout
    gen_settings_layout.addWidget(ssh_conn_container)

    # SSH Password
    lbl = QLabel("SSH Password")
    lbl.setStyleSheet(label_style)
    gen_settings_layout.addWidget(lbl)

    ssh_psw_input = QLineEdit()
    ssh_psw_input.setStyleSheet(input_style)
    ssh_psw_input.setFixedHeight(30)
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
    wandb_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold; margin-bottom: 10px;")
    wandb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    wandb_layout.addWidget(wandb_title)

    # API Key
    lbl = QLabel("API Key")
    lbl.setStyleSheet(label_style)
    wandb_layout.addWidget(lbl)

    wandb_api = QLineEdit()
    wandb_api.setStyleSheet(input_style)
    wandb_api.setFixedHeight(30)
    wandb_api.setEchoMode(QLineEdit.EchoMode.Password)
    wandb_layout.addWidget(wandb_api)

    # User/Team Name
    lbl = QLabel("User / Team Name")
    lbl.setStyleSheet(label_style)
    wandb_layout.addWidget(lbl)

    wandb_user = QLineEdit()
    wandb_user.setStyleSheet(input_style)
    wandb_user.setFixedHeight(30)
    wandb_layout.addWidget(wandb_user)

    # Project Name
    lbl = QLabel("Project Name")
    lbl.setStyleSheet(label_style)
    wandb_layout.addWidget(lbl)

    wandb_proj = QLineEdit()
    wandb_proj.setStyleSheet(input_style)
    wandb_proj.setFixedHeight(30)
    wandb_layout.addWidget(wandb_proj)

    grid_layout.addWidget(wandb_widget, 0, 1)

    github_widget = QWidget()
    github_layout = QVBoxLayout()
    github_layout.setContentsMargins(20, 20, 20, 20)
    github_widget.setLayout(github_layout)
    github_widget.setStyleSheet("background-color: #16161A; border-radius: 10px;")

    github_title = QLabel("GitHub")
    github_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold; margin-bottom: 10px;")
    github_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    github_layout.addWidget(github_title)

    # Repo URL
    lbl = QLabel("Repository URL")
    lbl.setStyleSheet(label_style)
    github_layout.addWidget(lbl)

    github_url = QLineEdit()
    github_url.setStyleSheet(input_style)
    github_url.setFixedHeight(30)
    github_layout.addWidget(github_url)

    # Username
    lbl = QLabel("GitHub Username")
    lbl.setStyleSheet(label_style)
    github_layout.addWidget(lbl)

    github_user = QLineEdit()
    github_user.setStyleSheet(input_style)
    github_user.setFixedHeight(30)
    github_layout.addWidget(github_user)

    # Personal Access Token
    lbl = QLabel("Personal Access Token")
    lbl.setStyleSheet(label_style)
    github_layout.addWidget(lbl)

    github_token = QLineEdit()
    github_token.setStyleSheet(input_style)
    github_token.setFixedHeight(30)
    github_token.setEchoMode(QLineEdit.EchoMode.Password)
    github_layout.addWidget(github_token)

    # Add to grid
    grid_layout.addWidget(github_widget, 0, 2)


    # ---- BUTTON ROW ----
    button_row = QHBoxLayout()
    button_row.setContentsMargins(0, 5, 0, 0)

    # Cancel button (left)
    # cancel_btn = QPushButton("Cancel")
    # cancel_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    #
    # cancel_btn.setStyleSheet(
    #     "background-color: #1A1631; color: white; "
    #     "padding: 8px 20px; border-radius: 10px; font-size: 17px; padding: 10px"
    # )
    # button_row.addWidget(cancel_btn, alignment=Qt.AlignmentFlag.AlignLeft)
    # cancel_btn.setMinimumWidth(185)
    # cancel_btn.setMinimumHeight(40)
    # cancel_btn.clicked.connect(lambda _, p="home": navigate(p))

    # Spacer to push the next button to the right
    button_row.addStretch()

    # Create Project button (right)
    create_btn = QPushButton("Get Started")
    create_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    create_btn.setMinimumWidth(185)
    create_btn.setMinimumHeight(40)
    create_btn.setStyleSheet(
        "background-color: #183C86; color: white; "
        "padding: 8px 20px; border-radius: 10px; font-size: 17px; padding: 10px"
    )

    name_input.setText(config.get("user"))
    path_input.setText(config.get("sshcon"))
    port_input.setText(config.get("sshport"))
    ssh_psw_input.setText(config.get("sshpsw"))
    wandb_api.setText(config.get("wandbapi"))
    wandb_user.setText(config.get("wandbuser"))
    wandb_proj.setText(config.get("wandbproj"))
    github_url.setText(config.get("giturl"))
    github_user.setText(config.get("gituser"))
    github_token.setText(config.get("gitpat"))

    def create_project_and_save():
        name = name_input.text()
        ssh_path = path_input.text()
        ssh_port = port_input.text()
        ssh_psw = ssh_psw_input.text()  # optionally encrypt
        wandb_api_text = wandb_api.text()  # optionally encrypt
        wandb_user_val = wandb_user.text()
        wandb_project_val = wandb_proj.text()
        github_url_val = github_url.text()
        github_user_val = github_user.text()
        git_pat = github_token.text()  # or add an input for local git path

        config.set("user", name)
        config.set("sshcon", ssh_path)
        config.set("sshport", ssh_port)
        config.set("sshpsw", ssh_psw)
        config.set("wandbapi", wandb_api_text)
        config.set("wandbuser", wandb_user_val)
        config.set("wandbproj", wandb_project_val)
        config.set("giturl", github_url_val)
        config.set("gituser", github_user_val)
        config.set("gitpat", git_pat)
        config.set("lastrun", "N/A")

        print("Config set, moving to project")
        navigate("project")

    create_btn.clicked.connect(create_project_and_save)
    button_row.addWidget(create_btn, alignment=Qt.AlignmentFlag.AlignRight)

    # Add row to the grid widget (below cards)
    grid_layout.addLayout(button_row, grid_layout.rowCount(), 0, 1, -1)


    return grid_widget
