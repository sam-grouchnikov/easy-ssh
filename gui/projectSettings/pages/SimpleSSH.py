from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QSizePolicy, QPushButton
from PyQt6.QtGui import QPixmap
from .actionButtonMenu import action_button_menu, ConsoleOutput


class SimpleSSHPage(QWidget):
    def __init__(self, run_func):  # Receives the 'chauffeur' function from content.py
        super().__init__()
        self.run_func = run_func

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # ---- TOP BAR (Status & Directory) ----
        top_bar = QWidget()
        top_bar.setStyleSheet(
            "background-color: #1F1F1F; font-size: 18px; color: #7D7D7D; border-radius: 5px"
        )
        top_tab_layout = QHBoxLayout(top_bar)

        self.dir_label = QLabel("Current Directory: None")
        top_tab_layout.addWidget(self.dir_label)

        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)

        self.status_label = QLabel("Status: Disconnected")
        self.icon_label = QLabel()
        self.green_icon = QPixmap("gui/icons/green_circle.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio,
                                                                       Qt.TransformationMode.SmoothTransformation)
        self.red_icon = QPixmap("gui/icons/red-circle.png").scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio,
                                                                   Qt.TransformationMode.SmoothTransformation)
        self.icon_label.setPixmap(self.red_icon)

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.icon_label)

        top_tab_layout.addStretch()
        top_tab_layout.addWidget(status_container)
        layout.addWidget(top_bar)

        # ---- MAIN CONTENT ROW (Buttons + Mini Console) ----
        row2 = QWidget()
        row2_layout = QHBoxLayout(row2)
        row2_layout.setContentsMargins(0, 15, 0, 0)
        row2_layout.setSpacing(20)

        # Pass the run_func into the menu so buttons can trigger commands
        self.action_menu = action_button_menu()
        self.action_menu.setMaximumWidth(425)
        self.action_menu.setMaximumHeight(650)


        self.console = ConsoleOutput()

        row2_layout.addWidget(self.action_menu, alignment=Qt.AlignmentFlag.AlignTop)
        row2_layout.addWidget(self.console)
        layout.addWidget(row2)

        self.setLayout(layout)

    def update_directory_display(self, path):
        clean_path = path.strip()
        self.dir_label.setText(f"Current Directory: {clean_path}")

    def update_connection_status(self, connected: bool):
        if connected:
            self.status_label.setText("Status: Connected")
            self.icon_label.setPixmap(self.green_icon)
        else:
            self.status_label.setText("Status: Disconnected")
            self.icon_label.setPixmap(self.red_icon)

    def set_busy(self, busy: bool):
        """
        Locks/Unlocks the shortcut buttons.
        Called by global_run_command in content.py
        """
        self.action_menu.setEnabled(not busy)
        if busy:
            self.action_menu.setGraphicsEffect(None)

    def on_command_finished(self):
        """
        Re-enables the UI once the SSH worker is done.
        """
        self.set_busy(False)

