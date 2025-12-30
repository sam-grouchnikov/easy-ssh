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

        current_dir = "sudoku/sudoku-cp-ai/model/"
        l1 = QLabel(f"Current Directory: {current_dir}")
        l1.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        status_container = QWidget()
        status_layout = QHBoxLayout(status_container)
        status_layout.setContentsMargins(0, 0, 0, 0)

        self.status_label = QLabel("Status: Connected")
        self.icon_label = QLabel()
        pixmap = QPixmap("gui/icons/green_circle.png")  # Ensure path is correct
        pixmap = pixmap.scaled(16, 16, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.icon_label.setPixmap(pixmap)

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.icon_label)

        top_tab_layout.addWidget(l1)
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

        row2_layout.addWidget(self.action_menu)
        row2_layout.addWidget(self.console)
        layout.addWidget(row2)

        self.setLayout(layout)

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

