#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Sam Grouchnikov
License: GPL-3.0
Version: 1.2.0
Email: sam.grouchnikov@gmail.com
Status: Development
"""

import matplotlib.pyplot as plt
import wandb
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor, QCursor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem,
    QLabel, QScrollArea, QGridLayout, QPushButton, QApplication
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QStyledItemDelegate

THEMES = {
    "dark": {
        "bg_main": "#151515",
        "bg_side": "#000000",
        "bg_plot": "#202020",
        "text": "#FFFFFF",
        "text_dim": "#9E9E9E",
        "grid": "#434343",
        "accent": "#6075D4"
    },
    "light": {
        "bg_main": "#F5F5F5",
        "bg_side": "#E0E0E0",
        "bg_plot": "#FFFFFF",
        "text": "#000000",
        "text_dim": "#333333",
        "grid": "#D1D1D1",
        "accent": "#3E4EB8"
    }
}

import pyqtgraph as pg


def create_plot_widget(steps, values, title, theme_mode):
    colors = THEMES[theme_mode]

    plot_node = pg.PlotWidget()

    plot_node.setBackground(colors["bg_plot"])

    label_style = {'color': colors["text_dim"], 'font-size': '12px'}
    plot_node.setLabel('bottom', "Step", **label_style)
    plot_node.setLabel('left', title, **label_style)

    # Styling the Axes (Spines)
    pen = pg.mkPen(color=colors["text_dim"], width=1)
    plot_node.getAxis('left').setPen(pen)
    plot_node.getAxis('bottom').setPen(pen)
    plot_node.getAxis('left').setTextPen(pen)
    plot_node.getAxis('bottom').setTextPen(pen)

    # Grid
    plot_node.showGrid(x=False, y=True, alpha=0.3)

    data_pen = pg.mkPen(color=colors["accent"], width=0.9)
    plot_node.plot(steps, values, pen=data_pen, antialias=True)

    plot_node.setMouseEnabled(x=True, y=True)

    return plot_node


class MetricsPlot(QWidget):
    def __init__(self, plot_widget, title: str, theme_mode):
        super().__init__()
        self.plot_widget = plot_widget
        self.title_str = title

        self.layout = QVBoxLayout(self)
        self.label = QLabel(title)
        self.layout.addWidget(self.label)
        self.layout.addSpacing(3)
        self.layout.addWidget(self.plot_widget)
        self.setContentsMargins(0,0,0,0)

        self.apply_theme(theme_mode)

    def apply_theme(self, theme_mode):
        colors = THEMES[theme_mode]
        self.label.setStyleSheet(f"color: {colors['text']}; font-weight: bold; font-size: 16px;")

        # Update the pyqtgraph colors
        self.plot_widget.setBackground(colors["bg_plot"])

        # Update Axis colors
        pen = pg.mkPen(color=colors["text_dim"], width=1)
        for axis in ['left', 'bottom']:
            ax = self.plot_widget.getAxis(axis)
            ax.setPen(pen)
            ax.setTextPen(pen)


class MetricsDisplay(QScrollArea):
    def __init__(self, theme):
        super().__init__()
        self.setWidgetResizable(True)

        self.container = QWidget()

        self.grid = QGridLayout(self.container)
        self.grid.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.grid.setSpacing(15)

        self.setWidget(self.container)
        self.setContentsMargins(0,0,0,0)
        self.update_theme(theme)

        self.columns = 2

    def clear(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            widget = item.widget()
            if widget:
                if hasattr(widget, 'canvas'):
                    plt.close(widget.canvas.figure)
                widget.deleteLater()
    def load_run(self, run, theme_mode):

        self.clear()
        history = run.history()

        if "trainer/global_step" not in history.columns:
            self.grid.addWidget(QLabel("No step data available."), 0, 0)
            return

        step_col = "trainer/global_step"

        row = 0
        col_idx = 0

        for col in history.columns:
            if col in ["_step", "_trainer", "_runtime", "_timestamp"]:
                continue
            if col == step_col:
                continue

            series = history[[step_col, col]].dropna()
            if series.empty:
                continue

            plot_widget = create_plot_widget(
                series[step_col].to_list(),
                series[col].to_list(),
                col,
                theme_mode=theme_mode
            )

            display_item = MetricsPlot(plot_widget, col, theme_mode=theme_mode)
            display_item.setMinimumHeight(350)

            self.grid.addWidget(display_item, row, col_idx)

            col_idx += 1
            if col_idx >= self.columns:
                col_idx = 0
                row += 1

    def update_theme(self, mode):
        for i in range(self.grid.count()):
            item = self.grid.itemAt(i)
            widget = item.widget()

            if isinstance(widget, MetricsPlot):
                widget.apply_theme(mode)

    def set_light_mode(self):
        self.update_theme("light")

    def set_dark_mode(self):
        self.update_theme("dark")


class GraphsPage(QWidget):
    def __init__(self, config):
        super().__init__()

        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(12, 30, 0, 30)
        self.config = config
        self.doc_path = None

        self.side_widget = QWidget()
        self.side_layout = QVBoxLayout(self.side_widget)
        self.side_layout.setContentsMargins(0, 0, 0, 0)
        self.side_layout.setSpacing(5)

        self.refresh_btn = QPushButton("Refresh List")

        self.refresh_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.refresh_btn.clicked.connect(self.refresh_runs)
        self.side_layout.addWidget(self.refresh_btn, alignment=Qt.AlignmentFlag.AlignTop)
        self.refresh_btn.setFixedHeight(35)
        self.side_layout.addSpacing(5)

        self.sidebar_container = QWidget()
        self.sidebar_container.setStyleSheet("border-radius: 10px;")
        self.container_layout = QVBoxLayout(self.sidebar_container)
        self.container_layout.setContentsMargins(5, 5, 5, 5)

        self.sidebar = QListWidget()
        self.sidebar.setContentsMargins(0,0,0,0)
        self.sidebar.setMaximumWidth(150)
        self.container_layout.addWidget(self.sidebar)



        self.sidebar.setMouseTracking(True)
        self.sidebar.viewport().setMouseTracking(True)

        self.current_theme = "light"
        self.metrics_display = MetricsDisplay(self.current_theme)
        self.metrics_display.setContentsMargins(15,15,15,0)

        self.side_layout.addWidget(self.sidebar_container)

        main_layout.addSpacing(5)
        main_layout.addWidget(self.side_widget)
        main_layout.addWidget(self.metrics_display, stretch=1)

        self.runs = []
        print("Project is not none")
        try:
            user = self.config.get("wandbuser")
            proj = self.config.get("wandbproj")
            api = wandb.Api()
            wandb_project = f"{user}/{proj}"
        except:
            user = None
            proj = None
            api = None
            wandb_project = None
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

    def update_config(self, new, path):
        self.config = new
        self.doc_path = path

    def refresh_runs(self):
        """Refreshes the run list from WandB and updates the sidebar."""
        user = self.config.get("wandb_user")
        proj = self.config.get("wandb_proj")

        if not user or not proj:
            print("WandB config incomplete.")
            return
        self.refresh_btn.setText("Refreshing...")
        self.refresh_btn.setEnabled(False)
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
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        try:
            print("Trying to load")
            self.metrics_display.load_run(run, self.current_theme)
            print("Finished loading")
        finally:
            # Restore normal cursor even if there's an error
            QApplication.restoreOverrideCursor()

    def on_item_hovered(self, item: QListWidgetItem):
        if item.flags() & Qt.ItemFlag.ItemIsSelectable:
            self.sidebar.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        else:
            self.sidebar.viewport().setCursor(Qt.CursorShape.ArrowCursor)


    def set_light_mode(self):
        self.current_theme = "light"
        self.metrics_display.set_light_mode()
        self.refresh_btn.setStyleSheet("""
                    QPushButton {
                        background: #e6dff9;
                        color: #484458;
                        border-radius: 12px; 
                        padding: 5px;
                        font-size: 17px;
                        font-weight: 520
                    }
                    QPushButton:hover { background-color: #cec2f0; }
                """)

        self.sidebar_container.setStyleSheet("""
                background-color: #F9F1F9;
                border-radius: 10px;
        """)

        self.sidebar.setStyleSheet("""
                    QListWidget {outline: none; border-radius: 10px;
                        border: none;}
                     

                    QListWidget::item {
                        padding: 0px 10px;
                        margin-left:3px;
                        font-size: 16px;
                        color: #333;
                        background-color: transparent;
                        border-radius: 10px;
                        margin-left: 5px;
                        margin-right: 5px;
                        margin-bottom: 5px;
                    }
                    QListWidget::item:hover {
                        background-color: #ECE6F1;
                    }


                    QListWidget::item:selected {
                        background-color: #e6dff9;
                        border: none;
                    }


                    QListWidget::item:focus {
                        outline: 0;
                    }
                    QScrollBar:vertical {
                        border: none;
                        background: #ECE6F1;
                        width: 13px;
                        margin: 0px 0px 0px 0px;
                    }

                    QScrollBar::handle:vertical {
                        background: #DDD5E2;
                        min-height: 20px;
                        border-radius: 5px;
                        margin: 2px;
                    }

                    QScrollBar::handle:vertical:hover {
                        background: #DCD1E2;
                    }

                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        height: 0px;
                    }

                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }
                """)
        self.metrics_display.setStyleSheet("""
                    QScrollBar:vertical {
                        border: none;
                        background: #ECE6F1;
                        width: 13px;
                        margin: 0px 0px 0px 0px;
                    }
                    QScrollArea {
                        border: none;
                    }
                   

                    QScrollBar::handle:vertical {
                        background: #DDD5E2;
                        min-height: 20px;
                        border-radius: 5px;
                        margin: 2px;
                    }

                    QScrollBar::handle:vertical:hover {
                        background: #DAD2DE;
                    }

                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        height: 0px;
                    }

                    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                        background: none;
                    }
                """)

    def set_dark_mode(self):
        self.current_theme = "dark"
        self.metrics_display.set_dark_mode()
        self.refresh_btn.setStyleSheet("""
                            QPushButton {
                                background: #1A1921;
                                color: #C38BFF;
                                border-radius: 12px; 
                                padding: 5px;
                                font-size: 17px;
                                font-weight: 520
                            }
                            QPushButton:hover { background-color: #24232D; }
                        """)
        self.sidebar_container.setStyleSheet("""
                        background-color: #1A1921;
                        border-radius: 10px;
                """)
        self.sidebar.setStyleSheet("""
                            QListWidget {background-color: #1A1921;outline: none; border-radius: 10px;
                                border: none;}
                            
                            
                            QListWidget::item {
                                padding: 0px 10px;
                                margin-left:3px;
                                font-size: 16px;
                                color: #9D9D9D;
                                background-color: transparent;
                                border-radius: 10px;
                                margin-left: 5px;
                                margin-right: 5px;
                                margin-bottom: 5px;
                            }
                            QListWidget::item:hover {
                                background-color: #24222A;
                            }
    

                            QListWidget::item:selected {
                                background-color: #362A48;
                                border: none;
                            }


                            QListWidget::item:focus {
                                outline: 0;
                            }
                            QScrollBar:vertical {
                                border: none;
                                background: #312D39;
                                width: 13px;
                                margin: 0px 0px 0px 0px;
                            }

                            QScrollBar::handle:vertical {
                                background: #211E29;
                                min-height: 20px;
                                border-radius: 5px;
                                margin: 2px;
                            }

                            QScrollBar::handle:vertical:hover {
                                background: #1A1723;
                            }

                            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                height: 0px;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                        """)
        self.metrics_display.setStyleSheet("""
                            QScrollArea {
                                    border: none;
                            }
                            QScrollBar:vertical {
                                border: none;
                                background: #312D39;
                                width: 13px;
                                margin: 0px 0px 0px 0px;
                            }

                            QScrollBar::handle:vertical {
                                background: #211E29;
                                min-height: 20px;
                                border-radius: 5px;
                                margin: 2px;
                            }

                            QScrollBar::handle:vertical:hover {
                                background: #1A1723;
                            }

                            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                height: 0px;
                            }

                            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                                background: none;
                            }
                        """)


