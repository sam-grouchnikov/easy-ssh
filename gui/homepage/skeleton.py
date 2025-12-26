import sys

from PyQt6.QtGui import QCursor
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMainWindow,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QStackedLayout, QFrame, QSizePolicy, QSpacerItem
)
from PyQt6.QtCore import Qt, QPropertyAnimation
from gui.sidebar import setupSidebar
from gui.homepage.content import setupContent

class HomeSkeleton(QMainWindow):
    def __init__(self, navigate):
        super().__init__()
        self.setWindowTitle("Homepage")
        self.setGeometry(100, 100, 1300, 700)
        self.setMinimumSize(600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("background-color: #151515;")

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        self.sidebar_width = 200
        self.sidebar = QWidget()
        self.sidebar.setStyleSheet("background-color: #18181F;")
        self.sidebar.setFixedWidth(self.sidebar_width)
        self.sidebar.setSizePolicy(
            self.sidebar.sizePolicy().horizontalPolicy(),
            QSizePolicy.Policy.Expanding
        )

        self.sidebar_width = 250
        self.sidebar = QWidget()
        self.sidebar.setStyleSheet("background-color: #12121A;")
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(225)
        self.sidebar.setSizePolicy(
            self.sidebar.sizePolicy().horizontalPolicy(),
            QSizePolicy.Policy.Expanding
        )

        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setContentsMargins(10, 10, 10, 10)
        self.sidebar_layout.setSpacing(10)
        self.sidebar.setLayout(self.sidebar_layout)

        self.content = QWidget()
        self.content.setStyleSheet("background-color: #0D0C12;")
        self.content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.content_layout = QVBoxLayout()
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(15)
        self.content.setLayout(self.content_layout)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.content)

        setupSidebar(self.sidebar_layout, navigate)
        setupContent(self.content_layout, navigate)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HomeSkeleton()
    window.show()
    sys.exit(app.exec())