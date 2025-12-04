from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QWidget, QGridLayout, \
    QHBoxLayout
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtCore import Qt


def setupContent(layout: QVBoxLayout):
    title_label = QLabel("Welcome back, user!")
    title_label.setStyleSheet("color: white; font-size: 40px; font-weight: bold; padding-left: 10px;")
    layout.addWidget(title_label)

    info_label = QLabel("Manage your projects")
    info_label.setStyleSheet("color: gray; font-size: 20px; padding-left: 17px;")
    layout.addWidget(info_label)

    layout.addSpacing(20)

    projects = [
        {"name": "Project 1", "info": "Last run: 1s ago", "status": "Active"},
        {"name": "Project 2", "info": "Last run: 2d ago", "status": "Disconnected"},
        {"name": "Project 3", "info": "Last run: 10d ago", "status": "Disconnected"},
        {"name": "Project 4", "info": "Last run: 1y ago", "status": "Disconnected"},
        {"name": "Project 5", "info": "Last run: 1y ago", "status": "Disconnected"},

    ]

    grid_widget = QWidget()
    grid_layout = QGridLayout()
    grid_layout.setContentsMargins(20, 0, 10, 0)
    grid_layout.setSpacing(15)
    grid_widget.setLayout(grid_layout)

    columns = 3
    for i, project in enumerate(projects):
        card = QWidget()
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(20, 15, 15, 15)

        card.setLayout(card_layout)
        card.setStyleSheet(
            "background-color: #1A1631; border-radius: 10px;"
            "padding-bottom: 20px;"
        )

        card_title = QLabel(project["name"])
        card_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold;")
        card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(card_title)

        status_row = QWidget()
        status_layout = QHBoxLayout()
        status_layout.setContentsMargins(0, 0, 0, 0)
        status_row.setLayout(status_layout)

        status_label = QLabel(f"Status: {project['status']}")
        status_label.setStyleSheet("color: #8F8F8F; font-size: 17px; padding-left: 30px;")
        status_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)


        status_layout.addWidget(status_label)

        status_icon = QLabel()
        if project['status'] == "Active":
            status_icon.setPixmap(
                QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\green_circle.png").scaled(14, 14, Qt.AspectRatioMode.KeepAspectRatio)
            )
        else:
            status_icon.setPixmap(
                QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\red-circle.png").scaled(14,14, Qt.AspectRatioMode.KeepAspectRatio)
            )
        status_layout.addWidget(status_icon)

        status_row.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        card_layout.addWidget(status_row)

        last_run_label = QLabel(f"Last run: {project['info']}")
        last_run_label.setStyleSheet("color: #8F8F8F; font-size: 17px; padding-left: 30px;")
        last_run_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        card_layout.addWidget(last_run_label)

        row = i // columns
        col = i % columns
        grid_layout.addWidget(card, row, col)

    create_card = QWidget()
    create_layout = QVBoxLayout()
    create_layout.setContentsMargins(0, 15, 0, 15)
    create_layout.setSpacing(10)
    create_card.setLayout(create_layout)

    create_card.setStyleSheet(
        "background-color: #2D1631; border-radius: 10px;"
        "padding-bottom: 20px;"
    )

    create_title = QLabel("Create Project")
    create_title.setStyleSheet("color: white; font-size: 23px; font-weight: bold;")
    create_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    create_layout.addWidget(create_title)

    create_icon = QLabel()
    create_icon.setPixmap(
        QPixmap("C:/Users/samgr/PycharmProjects/ssh-runner-app/gui/icons/add-button.png")
        .scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatio)
    )
    create_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    create_icon.setStyleSheet("margin-bottom: 25px")

    create_layout.addWidget(create_icon)

    create_card.setCursor(Qt.CursorShape.PointingHandCursor)

    next_index = len(projects)
    row = next_index // columns
    col = next_index % columns

    grid_layout.addWidget(create_card, row, col)


    layout.addWidget(grid_widget)
    layout.addStretch()