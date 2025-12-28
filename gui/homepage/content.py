from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QWidget, QGridLayout, QHBoxLayout, QSizePolicy
)
from PyQt6.QtGui import QCursor, QPixmap, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QSize

import database.database_crud


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

def setupContent(layout: QVBoxLayout, navigate):
    # Clear layout first
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.setParent(None)

    # Title
    title_label = QLabel("Welcome back, user!")
    title_label.setStyleSheet(
        "color: white; font-size: 40px; font-weight: bold; padding-left: 10px; margin-bottom: 0px;"
    )
    layout.addWidget(title_label)

    # Subtitle
    info_label = QLabel("Manage your projects")
    info_label.setStyleSheet("color: gray; font-size: 20px; padding-left: 17px;")
    layout.addWidget(info_label)

    # Projects grid
    setup_project_grid(layout, navigate)
    layout.addStretch()


def setup_project_grid(layout, navigate):
    projects = database.database_crud.get_all_projects()

    grid_widget = QWidget()
    grid_layout = QGridLayout()
    grid_layout.setContentsMargins(20, 5, 10, 0)
    grid_layout.setSpacing(20)
    grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
    grid_widget.setLayout(grid_layout)

    columns = 3

    # Add project cards
    for i, project in enumerate(projects):
        card = create_project_card(project, navigate)
        row = i // columns
        col = i % columns
        grid_layout.addWidget(card, row, col)

    # Add "Create Project" card
    create_card = create_project_button(navigate)
    next_index = len(projects)
    row = next_index // columns
    col = next_index % columns
    grid_layout.addWidget(create_card, row, col)

    # Make columns stretch evenly
    for c in range(columns):
        grid_layout.setColumnStretch(c, 1)

    layout.addWidget(grid_widget)


def create_project_card(project, navigate):
    card = QPushButton()
    card.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    card.setMinimumHeight(200)
    card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    card_layout = QVBoxLayout()
    card_layout.setContentsMargins(30, 20, 15, 15)
    card.setLayout(card_layout)
    card.setStyleSheet(
        "background-color: #1A1631; border-radius: 10px; padding-bottom: 20px;"
    )

    # Title row
    title_row = QWidget()
    title_layout = QHBoxLayout(title_row)
    title_layout.setContentsMargins(25, 0, 75, 0)

    card_title = QLabel(project["name"])
    card_title.setStyleSheet(
        "color: white; font-size: 25px; font-weight: bold"
    )
    card_title.setAlignment(Qt.AlignmentFlag.AlignLeft)

    icon_path = "C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\delete.png"

    delete_btn = QPushButton()
    delete_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
    delete_btn.setIcon(QIcon(icon_path))
    delete_btn.setIconSize(QSize(25, 25))

    def delete_project(id):
        from database.database_crud import delete_project
        delete_project(id)
        navigate("home")

    delete_btn.clicked.connect(lambda _, p=project["id"]: (
        delete_project(p),
        None
    ))
    title_layout.addWidget(delete_btn)
    title_layout.addSpacing(10)
    title_layout.addWidget(card_title)
    title_layout.addStretch()

    card_layout.addWidget(title_row)


    # Status row
    status_row = QWidget()
    status_layout = QHBoxLayout(status_row)
    status_layout.setContentsMargins(30, 0, 0, 0)
    status_layout.setSpacing(5)

    status_icon = QLabel()
    icon_path = "C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\green_circle.png" \
        if project['status'] == 1 else \
        "C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\red-circle.png"
    status_icon.setPixmap(QPixmap(icon_path).scaled(14, 14, Qt.AspectRatioMode.KeepAspectRatio))
    status_layout.addWidget(status_icon)

    status_label = QLabel(f"Status: {'Active' if project['status'] == 1 else 'Inactive'}")
    status_label.setStyleSheet("color: #8F8F8F; font-size: 17px;")
    status_layout.addWidget(status_label)
    status_layout.addStretch(0)
    card_layout.addWidget(status_row)

    # Last run
    last_run_label = QLabel(f"Last run: {project['last_update']}")
    last_run_label.setStyleSheet("color: #8F8F8F; font-size: 17px; padding-left: 30px;")
    last_run_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    card_layout.addWidget(last_run_label)
    card_layout.addStretch(8)
    card.clicked.connect(
        lambda _, pid=project['name']: navigate("project", project_id=pid)
    )

    return card


def create_project_button(navigate):
    create_card = QPushButton()
    create_card.setFixedHeight(200)
    create_layout = QVBoxLayout()
    create_layout.setContentsMargins(0, 10, 0, 40)
    create_card.setLayout(create_layout)
    create_card.setStyleSheet("background-color: #2D1631; border-radius: 10px; padding-bottom: 20px;")
    create_card.setCursor(Qt.CursorShape.PointingHandCursor)

    create_title = QLabel("Create Project")
    create_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold;")
    create_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    create_layout.addWidget(create_title)

    create_icon = QLabel()
    create_icon.setPixmap(QPixmap("C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/add-button.png")
                           .scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio))
    create_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    create_layout.addWidget(create_icon)

    create_card.clicked.connect(lambda: navigate("create"))
    return create_card


def navigate_project(project_id, navigate):
    navigate("project", project_id)