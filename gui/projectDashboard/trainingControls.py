from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QWidget, QGridLayout, \
    QHBoxLayout, QToolButton
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

def controls_widget_constructor():
    controls = QWidget()
    controls_layout = QVBoxLayout()
    controls_layout.setContentsMargins(0, 0, 0, 0)
    controls_title = QLabel("Training Controls")
    controls_title.setStyleSheet("font-size: 30px")
    controls_layout.addWidget(controls_title)
    controls.setLayout(controls_layout)

    grid_widget = QWidget()

    grid_layout = QGridLayout()
    grid_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
    grid_layout.setContentsMargins(0, 0, 10, 0)
    grid_layout.setSpacing(15)
    grid_widget.setLayout(grid_layout)


    grid_layout.addWidget(simple_ssh(), 0, 0)
    grid_layout.addWidget(command_line(), 0, 1)
    grid_layout.addWidget(simple_ssh(), 0, 2)

    controls_layout.addWidget(grid_widget)
    return controls

def simple_ssh():
    card = QWidget()
    card.setStyleSheet(
        "background-color: #1A1631; border-radius: 10px; margin-right: 20px; margin-top: 10px"
    )
    card.setFixedWidth(300)
    card_layout = QVBoxLayout()
    card.setLayout(card_layout)
    card_layout.setContentsMargins(0, 15, 0, 30)
    title_row = QWidget()
    title_layout = QHBoxLayout()
    title_layout.setContentsMargins(0, 0, 0, 0)
    title_row.setLayout(title_layout)
    card_title = ClickableLabel("Simple SSH")
    card_title.setCursor(Qt.CursorShape.PointingHandCursor)
    card_title.setStyleSheet(
        "color: white; font-size: 23px; font-weight: bold;")
    card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_layout.addWidget(card_title)
    card_layout.addWidget(title_row)

    icon = QLabel()
    icon.setStyleSheet("margin-top: 20px")
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\loading.png")
    icon.setPixmap(pixmap.scaled(75, 75, Qt.AspectRatioMode.KeepAspectRatio))
    card_layout.addWidget(icon)

    return card

def command_line():
    card = QWidget()
    card.setStyleSheet(
        "background-color: #1A1631; border-radius: 10px; margin-right: 20px; margin-top: 10px"
    )
    card.setFixedWidth(300)
    card_layout = QVBoxLayout()
    card.setLayout(card_layout)
    card_layout.setContentsMargins(0, 15, 0, 30)
    title_row = QWidget()
    title_layout = QHBoxLayout()
    title_layout.setContentsMargins(0, 0, 0, 0)
    title_row.setLayout(title_layout)
    card_title = ClickableLabel("Command Line")
    card_title.setCursor(Qt.CursorShape.PointingHandCursor)
    card_title.setStyleSheet(
        "color: white; font-size: 23px; font-weight: bold;")
    card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_layout.addWidget(card_title)
    card_layout.addWidget(title_row)

    icon = QLabel()
    icon.setStyleSheet("margin-top: 20px")
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\command.png")
    icon.setPixmap(pixmap.scaled(75, 75, Qt.AspectRatioMode.KeepAspectRatio))
    card_layout.addWidget(icon)

    return card

def file_tree():
    card = QWidget()
    card.setStyleSheet(
        "background-color: #1A1631; border-radius: 10px; margin-right: 20px; margin-top: 10px"
    )
    card.setFixedWidth(300)
    card_layout = QVBoxLayout()
    card.setLayout(card_layout)
    card_layout.setContentsMargins(0, 15, 0, 30)
    title_row = QWidget()
    title_layout = QHBoxLayout()
    title_layout.setContentsMargins(0, 0, 0, 0)
    title_row.setLayout(title_layout)
    card_title = ClickableLabel("File Tree")
    card_title.setCursor(Qt.CursorShape.PointingHandCursor)
    card_title.setStyleSheet(
        "color: white; font-size: 23px; font-weight: bold;")
    card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_layout.addWidget(card_title)
    card_layout.addWidget(title_row)

    icon = QLabel()
    icon.setStyleSheet("margin-top: 20px")
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\code-fork.png")
    icon.setPixmap(pixmap.scaled(75, 75, Qt.AspectRatioMode.KeepAspectRatio))
    card_layout.addWidget(icon)

    return card


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)