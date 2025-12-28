import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QWidget
)

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

        if name == "project" and skeleton and "project_name" in kwargs:
            skeleton.set_project(kwargs["project_name"])

        if skeleton and hasattr(skeleton, "refresh"):
            skeleton.refresh()

        self._stack.setCurrentWidget(self._pages[name])

    def get_page(self, name: str) -> QWidget:
        return self._pages.get(name)

def run():
    app = QApplication(sys.argv)
    import database.database as db
    db.init_db()
    window = Application()
    from gui.homepage.skeleton import HomeSkeleton
    from gui.projectSettings.skeleton import ProjectSettingsSkeleton
    from gui.createProject.skeleton import CreateSkeleton

    home = HomeSkeleton(window.show_page)
    project = ProjectSettingsSkeleton(window.show_page)
    create = CreateSkeleton(window.show_page)

    window.add_skeleton("home", home)
    window.add_skeleton("project", project)
    window.add_skeleton("create", create)

    window.show_page("home")
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()