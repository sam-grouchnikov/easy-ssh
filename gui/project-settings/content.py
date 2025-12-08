from PyQt6.QtWidgets import QVBoxLayout, QLabel, QSizePolicy, QStackedWidget
from PyQt6.QtCore import Qt, pyqtSignal
from gui.navbar import navbar
from pages.FileTree import FileTreePage
from pages.graphs import GraphsPage
from pages.settings import SettingsPage
from pages.SimpleSSH import SimpleSSHPage
from pages.cmd import cmdPage

def setupContent(self, layout: QVBoxLayout):
    project = "Project 1"

    title_label = QLabel(f"{project}")
    title_label.setStyleSheet("color: white; font-size: 40px; font-weight: bold; padding-left: 10px;")
    layout.addWidget(title_label)

    nav = navbar()
    nav.setContentsMargins(20, 0, 20, 0)
    nav.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    for index, item in enumerate(nav.nav_items):
        item.clicked.connect(lambda _, i=index: self.stack.setCurrentIndex(i))

    layout.addWidget(nav)


    self.stack = QStackedWidget()
    self.stack.addWidget(FileTreePage("C:\\Users\\samgr\\PycharmProjects\\ssh-runner-app\\gui\\project-settings"))
    self.stack.addWidget(cmdPage())
    self.stack.addWidget(SimpleSSHPage())
    self.stack.addWidget(GraphsPage())
    self.stack.addWidget(SettingsPage())
    self.stack.setContentsMargins(20, 0, 20, 20)
    layout.addWidget(self.stack)


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)