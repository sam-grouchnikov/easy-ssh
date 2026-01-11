from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem,
    QLabel, QScrollArea, QGridLayout, QPushButton
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import wandb

def make_plot(steps, values, title):
    fig, ax = plt.subplots(figsize=(4, 3))

    fig.patch.set_facecolor('#202020')
    ax.set_facecolor("#202020")

    ax.plot(steps, values, color="#6075D4", linewidth=0.8)

    ax.set_xlabel("Step", color="#9E9E9E")
    ax.set_ylabel("Value", color="#9E9E9E")
    ax.tick_params(
        axis='both',
        which='both',
        length=3,
        colors="#9E9E9E"
    )

    ax.spines["bottom"].set_color("#9E9E9E")
    ax.spines["left"].set_color("#9E9E9E")

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.spines["bottom"].set_linewidth(1)
    ax.spines["left"].set_linewidth(1)

    ax.grid(False)
    ax.xaxis.grid(True, color="#434343", linestyle="-", linewidth=0)
    ax.yaxis.grid(True, color="#434343", linestyle="--", linewidth=1)

    fig.subplots_adjust(left=0.20, right=0.98, top=0.95, bottom=0.18)
    return fig




class MetricsPlot(QWidget):
    def __init__(self, fig, title: str):
        super().__init__()

        self.setStyleSheet("background-color: #151515;")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        label = QLabel(title)
        label.setStyleSheet("""
            color: white;
            font-weight: bold;
            font-size: 16px;
            background-color: transparent;
        """)

        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color: #151515;")
        canvas.setMinimumHeight(300)

        layout.addWidget(label)
        layout.addWidget(canvas)


class MetricsDisplay(QScrollArea):
    def __init__(self):
        super().__init__()
        self.setWidgetResizable(True)

        self.container = QWidget()

        self.grid = QGridLayout(self.container)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.grid.setSpacing(20)

        self.setWidget(self.container)

        self.columns = 2

    def clear(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def load_run(self, run):
        self.clear()

        history = run.history()

        if "trainer/global_step" not in history:
            self.grid.addWidget(QLabel("No step data available."), 0, 0)
            return

        step_col = "trainer/global_step"

        row = 0
        col_idx = 0

        for col in history.columns:
            if col == step_col:
                continue

            series = history[[step_col, col]].dropna()
            if series.empty:
                continue

            fig = make_plot(
                series[step_col].to_list(),
                series[col].to_list(),
                col
            )

            plot_widget = MetricsPlot(fig, col)

            self.grid.addWidget(plot_widget, row, col_idx)

            col_idx += 1
            if col_idx >= self.columns:
                col_idx = 0
                row += 1


class GraphsPage(QWidget):
    def __init__(self, config):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)
        self.config = config

        self.side_widget = QWidget()
        self.side_layout = QVBoxLayout(self.side_widget)
        self.side_layout.setContentsMargins(0,2,0,0)

        self.refresh_btn = QPushButton("Refresh List")
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background: none;
                border: 1px solid SeaGreen; 
                color: white;
                border-radius: 5px; 
                padding: 5px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #14131C; }
        """)
        self.refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_btn.clicked.connect(self.refresh_runs)
        self.side_layout.addWidget(self.refresh_btn, alignment=Qt.AlignmentFlag.AlignTop)

        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(150)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                outline: 0;
            }

            QListWidget::item {
                padding: 5px;
                margin-left:3px;
                font-size: 19px;
                color: #FFFFFF;
                background-color: transparent;
            }
            QListWidget::item:hover {
                background-color: #14131C;
            }


            QListWidget::item:selected {
                background-color: #1F1D2C;
                color: #FFFFFF;
                border: none;
            }

            QListWidget::item:selected:!active {
                background-color: #202020;
                color: #FFFFFF;
                border: none;
            }

            QListWidget::item:focus {
                outline: 0;
            }
        """)

        self.sidebar.setMouseTracking(True)
        self.sidebar.viewport().setMouseTracking(True)

        self.metrics_display = MetricsDisplay()
        self.side_layout.addWidget(self.sidebar)

        main_layout.addWidget(self.side_widget)
        main_layout.addWidget(self.metrics_display, stretch=1)

        self.runs = []
        print("Project is not none")
        user = self.config.get("wandbuser")
        proj = self.config.get("wandbproj")
        api_key = self.config.get("wandbapi")
        api = wandb.Api()
        wandb_project = f"{user}/{proj}"
        if user:
            print(f"Details: user: {user}, project: {wandb_project}")
            self.runs = list(api.runs(wandb_project))
        else:
            self.runs = []
        print("Finished wandb")


        runs_title = QListWidgetItem("Runs")
        runs_title.setFlags(Qt.ItemFlag.NoItemFlags)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        runs_title.setFont(font)
        self.sidebar.addItem(runs_title)


        self.sidebar.itemEntered.connect(self.on_item_hovered)

        for run in self.runs:
            item = QListWidgetItem(run.name)
            item.setData(Qt.ItemDataRole.UserRole, run)
            item.setFont(QFont("Arial", 13))
            item.setForeground(QColor("#FFFFFF"))


            self.sidebar.addItem(item)

        self.sidebar.itemClicked.connect(self.on_run_selected)

    def refresh_runs(self):
        """Refreshes the run list from WandB and updates the sidebar."""
        user = self.config.get("wandbuser")
        proj = self.config.get("wandbproj")

        if not user or not proj:
            print("WandB config incomplete.")
            return
        self.refresh_btn.setText("Refreshing...")
        self.refresh_btn.setEnabled(False)
        from PyQt6.QtWidgets import QApplication
        QApplication.processEvents()
        try:
            # 1. Re-fetch data from API
            api = wandb.Api()
            wandb_project = f"{user}/{proj}"
            self.runs = list(api.runs(wandb_project))

            # 2. Clear current sidebar items (except the "Runs" header)
            while self.sidebar.count() > 1:
                self.sidebar.takeItem(1)

            # 3. Re-populate the list
            for run in self.runs:
                item = QListWidgetItem(run.name)
                item.setData(Qt.ItemDataRole.UserRole, run)
                item.setFont(QFont("Arial", 13))
                item.setForeground(QColor("#FFFFFF"))
                self.sidebar.addItem(item)

            print(f"Refreshed {len(self.runs)} runs.")

        except Exception as e:
            print(f"Error refreshing WandB runs: {e}")
        finally:
            # 5. Restore Button State
            self.refresh_btn.setText("Refresh List")
            self.refresh_btn.setEnabled(True)

    def on_run_selected(self, item: QListWidgetItem):
        run = item.data(Qt.ItemDataRole.UserRole)
        if run is None:
            return

        self.metrics_display.load_run(run)

    def on_item_hovered(self, item: QListWidgetItem):
        if item.flags() & Qt.ItemFlag.ItemIsSelectable:
            self.sidebar.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.sidebar.viewport().setCursor(Qt.CursorShape.ArrowCursor)
