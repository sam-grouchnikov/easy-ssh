from PyQt6.QtWidgets import (
    QVBoxLayout, QLabel, QSizePolicy, QStackedWidget
)
from PyQt6.QtCore import Qt
from gui.navbar import navbar
from gui.projectSettings.pages.FileTree import FileTreePage
from gui.projectSettings.pages.graphs import GraphsPage
from gui.projectSettings.pages.settings import SettingsPage
from gui.projectSettings.pages.SimpleSSH import SimpleSSHPage
from gui.projectSettings.pages.cmd import cmdPage


PAGE_NAMES = [
    "File Tree",
    "Terminal",
    "Simple SSH",
    "Logged Metrics",
    "Project Settings"
]


def setupContent(self, layout: QVBoxLayout, project_name):
    print("Setting up content")
    self.title_label = QLabel()
    self.title_label.setStyleSheet(
        "color: white; font-size: 35px; font-weight: bold; padding-left: 10px;"
    )
    layout.addWidget(self.title_label)

    nav = navbar()
    nav.setContentsMargins(10, 0, 20, 0)
    nav.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    layout.addWidget(nav)

    self.stack = QStackedWidget(self)
    self.stack.addWidget(
        FileTreePage(
            "/gui/projectSettings"
        )
    )
    self.stack.addWidget(cmdPage(project_name))
    self.stack.addWidget(SimpleSSHPage())
    self.stack.addWidget(GraphsPage(project_name))
    self.stack.addWidget(SettingsPage(project_name))

    self.stack.setContentsMargins(10, 0, 25, 20)
    layout.addWidget(self.stack)



    def update_title(index: int):
        self.title_label.setText(f"{project_name} - {PAGE_NAMES[index]}")

    for index, item in enumerate(nav.nav_items):
        item.clicked.connect(
            lambda _, i=index: self.stack.setCurrentIndex(i)
        )

    self.stack.currentChanged.connect(update_title)

    self.stack.setCurrentIndex(0)
    update_title(0)