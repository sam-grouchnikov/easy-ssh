from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem,
    QLabel, QScrollArea, QGridLayout
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
    def __init__(self):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(10)

        self.sidebar = QListWidget()
        self.sidebar.setMaximumWidth(150)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                outline: 0;
            }

            QListWidget::item {
                padding: 5px;
                font-size: 19px;
                color: #FFFFFF;
                background-color: transparent;
            }
            QListWidget::item:hover {
                background-color: #131313;
            }


            QListWidget::item:selected {
                background-color: #202020;
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

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.metrics_display, stretch=1)

        api = wandb.Api()
        project = "sam-grouchnikov-kennesaw-state-university/sudoku-featureless"
        self.runs = list(api.runs(project))

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
