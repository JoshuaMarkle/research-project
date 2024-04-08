import sys
import numpy as np
from typing import *
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.figure as mpl_fig
import matplotlib.animation as anim

class PlotWindow(QDialog):
    def __init__(self):
        super().__init__()
        # Dialog settings
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Matplotlib live plot in PyQt - example")

        # Set layout and add FigureCanvas
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.myFig = PlotCanvas()
        layout.addWidget(self.myFig)

    def updatePlot(self, newX, newY):
        self.myFig.updatePlot(newX, newY)

class PlotCanvas(FigureCanvas):
    def __init__(self) -> None:
        super().__init__(mpl_fig.Figure())
        self.x = []
        self.y = []
        self.ax = self.figure.subplots()
        self.figure.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
        self.ax.set_xlabel("Generation Number")
        self.ax.set_ylabel("Best Keyboard Value")
        self.ax.set_title("Keyboard Value Over Generation")

    def updatePlot(self, newX:int, newY:float) -> None:
        self.x.append(newX)
        self.y.append(newY)
        self.ax.clear()
        self.ax.plot(self.x, self.y, linestyle=':', marker='o')
        self.ax.set_xlabel("Generation Number")
        self.ax.set_ylabel("Best Keyboard Value")
        self.ax.set_title("Keyboard Value Over Generation")
        self.draw()
