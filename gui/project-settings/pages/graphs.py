from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import wandb


def make_plot(steps, values, title):
    fig, ax = plt.subplots()
    ax.plot(steps, values)
    ax.set_title(title)
    ax.set_xlabel("Step")
    ax.set_ylabel("Value")
    return fig

class GraphsPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        api = wandb.Api()
        run = api.run("sam-grouchnikov-kennesaw-state-university/sudoku-featureless/8ynfsu1e")
        history = run.history()

        filtered = history[["trainer/global_step", "train_loss"]].dropna()

        steps = filtered["trainer/global_step"].to_list()
        loss = filtered["train_loss"].to_list()

        fig = make_plot(steps, loss, "Loss")

        layout.addWidget(MetricsPlot(fig))

        self.setLayout(layout)

class MetricsPlot(QWidget):
    def __init__(self, fig):
        super().__init__()
        layout = QVBoxLayout(self)

        canvas = FigureCanvas(fig)
        canvas.setFixedHeight(400)

        layout.addWidget(canvas)
