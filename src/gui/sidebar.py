from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Set background color to light gray
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#e0e0e0'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Settings label
        label = QLabel('Settings', self)
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)

        # Grid label
        label = QLabel('Grid Settings', self)
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(label)

        # Grid Size Setting
        gridSizeLayout = QHBoxLayout()
        gridSizeLabel = QLabel('Grid Size:', self)
        gridSizeInput = QLineEdit(self)
        gridSizeInput.setPlaceholderText(str(config.GRID_SIZE))
        gridSizeInput.setValidator(QIntValidator(20, 200, self))
        gridSizeLayout.addWidget(gridSizeLabel)
        gridSizeLayout.addWidget(gridSizeInput)
        gridSizeInput.textChanged.connect(self.onGridSizeChanged)
        layout.addLayout(gridSizeLayout)

        # Grid Height Setting
        gridHeightLayout = QHBoxLayout()
        gridHeightLabel = QLabel('Grid Height:', self)
        gridHeightInput = QLineEdit(self)
        gridHeightInput.setPlaceholderText(str(config.GRID_HEIGHT))
        gridHeightInput.setValidator(QIntValidator(1, 999, self))
        gridHeightLayout.addWidget(gridHeightLabel)
        gridHeightLayout.addWidget(gridHeightInput)
        gridHeightInput.textChanged.connect(self.onGridHeightChanged)
        layout.addLayout(gridHeightLayout)

        # Grid Width Setting
        gridWidthLayout = QHBoxLayout()
        gridWidthLabel = QLabel('Grid Width:', self)
        gridWidthInput = QLineEdit(self)
        gridWidthInput.setPlaceholderText(str(config.GRID_WIDTH))
        gridWidthInput.setValidator(QIntValidator(1, 999, self))
        gridWidthLayout.addWidget(gridWidthLabel)
        gridWidthLayout.addWidget(gridWidthInput)
        gridWidthInput.textChanged.connect(self.onGridWidthChanged)
        layout.addLayout(gridWidthLayout)

        # Layer label
        settings_label = QLabel('Layer Toggle', self)
        label.setAlignment(Qt.AlignLeft)
        layout.addWidget(settings_label)

        # Toggle Difficulty View
        difficultyToggleLayout = QHBoxLayout()
        difficultyToggleLabel = QLabel('Toggle Difficulty View:', self)
        difficultyToggleCheckbox = QCheckBox(self)
        difficultyToggleCheckbox.setChecked(False)
        difficultyToggleLayout.addWidget(difficultyToggleLabel)
        difficultyToggleLayout.addWidget(difficultyToggleCheckbox)
        difficultyToggleCheckbox.stateChanged.connect(self.onToggleDifficultyChanged)
        layout.addLayout(difficultyToggleLayout)

        # Spacer to make everything move to top
        label = QLabel()   
        layout.addWidget(label)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(verticalSpacer)


    def onGridSizeChanged(self, value):
        if value:
            config.GRID_SIZE = int(value)
            print(f"Grid size changed to: {value}")
        print(config.GRID_SIZE)

    def onGridHeightChanged(self, value):
        if value:
            config.GRID_HEIGHT = int(value)
            print(f"Grid size changed to: {value}")
        print(config.GRID_HEIGHT)

    def onGridWidthChanged(self, value):
        if value:
            config.GRID_WIDTH = int(value)
            print(f"Grid size changed to: {value}")
        print(config.GRID_WIDTH)


    def onToggleDifficultyChanged(self, state):
        # Handle the difficulty toggle change here
        # state will be 0 if unchecked, 2 if checked
        if state == 2:
            print("Difficulty view enabled")
        else:
            print("Difficulty view disabled")
