from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QWidget, QGridLayout, \
    QHBoxLayout, QToolButton
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal

def second_widget_constructor():
    outer_grid = QWidget()
    outer_layout = QHBoxLayout()
    outer_grid.setLayout(outer_layout)

    metrics = QWidget()
    metrics_layout = QVBoxLayout()
    metrics_layout.setContentsMargins(0, 0, 0, 0)
    metrics_title = QLabel("Metric Logging")
    metrics_title.setStyleSheet("font-size: 30px")
    metrics_layout.addWidget(metrics_title)
    metrics.setLayout(metrics_layout)
    metrics_layout.addWidget(view_graphs())

    outer_layout.addWidget(metrics)

    settings_card = QWidget()
    settings_layout = QVBoxLayout()
    settings_layout.setContentsMargins(0, 0, 0, 0)
    settings_title = QLabel("Metric Logging")
    settings_title.setStyleSheet("font-size: 30px")
    settings_layout.addWidget(settings_title)
    settings_card.setLayout(settings_layout)
    settings_layout.addWidget(settings())
    settings_card.setStyleSheet("margin-left: 15px;")


    outer_layout.addWidget(settings_card)
    outer_layout.addStretch()
    return outer_grid

def view_graphs():
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
    card_title = ClickableLabel("View Graphs")
    card_title.setCursor(Qt.CursorShape.PointingHandCursor)
    card_title.setStyleSheet(
        "color: white; font-size: 23px; font-weight: bold;")
    card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_layout.addWidget(card_title)
    card_layout.addWidget(title_row)

    icon = QLabel()
    icon.setStyleSheet("margin-top: 20px")
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\line-graph.png")
    icon.setPixmap(pixmap.scaled(75, 75, Qt.AspectRatioMode.KeepAspectRatio))
    card_layout.addWidget(icon)

    return card

def settings():
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
    card_title = ClickableLabel("Miscellaneous")
    card_title.setCursor(Qt.CursorShape.PointingHandCursor)
    card_title.setStyleSheet(
        "color: white; font-size: 23px; font-weight: bold;")
    card_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title_layout.addWidget(card_title)
    card_layout.addWidget(title_row)

    icon = QLabel()
    icon.setStyleSheet("margin-top: 20px")
    icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
    pixmap = QPixmap("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\icons\\setting.png")
    icon.setPixmap(pixmap.scaled(75, 75, Qt.AspectRatioMode.KeepAspectRatio))
    card_layout.addWidget(icon)

    return card




class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)