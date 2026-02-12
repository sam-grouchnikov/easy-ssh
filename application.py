#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.1.0
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
        self.is_dark = False

        self._pages = {}
        self._skeletons = {}

    def toggle_theme(self):
        self.is_dark = not self.is_dark

        for skeleton in self._skeletons.values():
            if self.is_dark:
                skeleton.set_dark_mode()
            else:
                skeleton.set_light_mode()

    def add_skeleton(self, name: str, skeleton: QMainWindow):
        central = skeleton.centralWidget()
        if central is None:
            raise ValueError("Skeleton has no central widget")


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

        if name == "create" and skeleton and kwargs["signin"] == "true":
            skeleton.setSignIn()

        if name == "project" and skeleton:
            skeleton.update_uid(kwargs["uid"])





    def get_page(self, name: str) -> QWidget:
        return self._pages.get(name)


def run():
    app = QApplication(sys.argv)
    window = Application()

    config = {}
    API_KEY = "AIzaSyCM5k5OWiIMUPeDqA_hhmHN3mnpuguGvcE"
    PROJECT_ID = "easy-ssh"

    from firebase import FirebaseClient

    fb = FirebaseClient(API_KEY, PROJECT_ID)


    from gui.projectSettings.skeleton import ProjectSettingsSkeleton
    from gui.createProject.skeleton import CreateSkeleton
    from gui.welcomePage.skeleton import HomepageSkeleton
    home = HomepageSkeleton(window.show_page, window.toggle_theme)
    create = CreateSkeleton(window.show_page, window.toggle_theme, fb)

    window.add_skeleton("home", home)
    window.add_skeleton("create", create)

    project = ProjectSettingsSkeleton(window.show_page, window.toggle_theme, fb)
    window.add_skeleton("project", project)

    if window.is_dark:
        window.toggle_theme()

    window.show_page("home")
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
