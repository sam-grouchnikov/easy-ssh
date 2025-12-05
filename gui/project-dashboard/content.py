from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QWidget, QGridLayout, \
    QHBoxLayout, QToolButton
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from trainingControls import controls_widget_constructor
from metricsAndSettings import second_widget_constructor


def setupContent(layout: QVBoxLayout):
    project = "Project 1"

    title_label = QLabel(f"{project} - Dashboard")
    title_label.setStyleSheet("color: white; font-size: 40px; font-weight: bold; padding-left: 10px;")
    layout.addWidget(title_label)

    info_label = QLabel("Manage your project settings, files, and runs")
    info_label.setStyleSheet("color: gray; font-size: 20px; padding-left: 17px;")
    layout.addWidget(info_label)

    sections = QWidget()
    sections_layout = QVBoxLayout()
    sections_layout.setContentsMargins(20, 20, 0, 0)
    sections.setLayout(sections_layout)

    sections_layout.addWidget(controls_widget_constructor())
    sections_layout.addWidget(second_widget_constructor())

    layout.addWidget(sections)
    layout.addStretch()



class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)