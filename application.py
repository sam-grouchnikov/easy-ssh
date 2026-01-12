#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.0.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QWidget
)

from backend.config.ConfigWiring import AppConfig


class Application(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SSH Runner")
        self.setGeometry(100, 100, 1300, 700)

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._pages = {}
        self._skeletons = {}

    def add_skeleton(self, name: str, skeleton: QMainWindow):
        central = skeleton.centralWidget()
        if central is None:
            raise ValueError("Skeleton has no central widget")

        central.setParent(None)

        self._pages[name] = central

        if not hasattr(self, "_skeletons"):
            self._skeletons = {}
        self._skeletons[name] = skeleton

        self._stack.addWidget(central)

    def show_page(self, name: str, **kwargs):
        if name not in self._pages:
            raise ValueError(f"Page '{name}' not found")

        skeleton = self._skeletons.get(name)

        if skeleton and hasattr(skeleton, "refresh"):
            skeleton.refresh()

        self._stack.setCurrentWidget(self._pages[name])

    def get_page(self, name: str) -> QWidget:
        return self._pages.get(name)


def run():
    app = QApplication(sys.argv)
    window = Application()
    config = AppConfig("user_data.json")
    from gui.projectSettings.skeleton import ProjectSettingsSkeleton

    from gui.createProject.skeleton import CreateSkeleton
    from gui.welcomePage.skeleton import HomepageSkeleton
    home = HomepageSkeleton(window.show_page)
    create = CreateSkeleton(window.show_page, config)
    project = ProjectSettingsSkeleton(window.show_page, config)

    window.add_skeleton("project", project)
    window.add_skeleton("create", create)
    window.add_skeleton("home", home)

    if config.is_complete():

        window.show_page("project")
    else:
        window.show_page("home")
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
