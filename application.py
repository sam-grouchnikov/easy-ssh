import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QWidget
)

class Application(QMainWindow):
    """
    Application that stacks full-page skeletons.
    Each skeleton manages its own sidebar/layout.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("SSH Runner")
        self.setGeometry(100, 100, 1300, 700)

        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        self._pages = {}

    def add_skeleton(self, name: str, skeleton: QMainWindow):
        """
        Add a full-page skeleton to the app.

        We steal its central widget and embed it.
        """
        central = skeleton.centralWidget()
        if central is None:
            raise ValueError("Skeleton has no central widget")

        central.setParent(None)  # detach safely

        self._pages[name] = central
        self._stack.addWidget(central)

    def show_page(self, name: str):
        if name not in self._pages:
            raise ValueError(f"Page '{name}' not found")

        self._stack.setCurrentWidget(self._pages[name])

    def get_page(self, name: str) -> QWidget:
        return self._pages.get(name)

def run():
    app = QApplication(sys.argv)

    window = Application()

    from gui.homepage.skeleton import HomeSkeleton
    from gui.projectSettings.skeleton import ProjectSettingsSkeleton
    from gui.projectDashboard.skeleton import ProjectDashboardSkeleton
    from gui.createProject.skeleton import CreateSkeleton

    home = HomeSkeleton(window.show_page)
    project = ProjectSettingsSkeleton(window.show_page)
    dashboard = ProjectDashboardSkeleton(window.show_page)
    create = CreateSkeleton(window.show_page)

    window.add_skeleton("home", home)
    window.add_skeleton("project", project)
    window.add_skeleton("dashboard", dashboard)
    window.add_skeleton("create", create)

    window.show_page("home")
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()