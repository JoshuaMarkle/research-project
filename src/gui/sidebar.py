import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config
from key import *

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Settings label
        label = QLabel('Settings', self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet('font-weight: bold; font-size: 18px')
        layout.addWidget(label)

        # Grid label
        label = QLabel('Grid Settings', self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet('font-weight: bold')
        layout.addWidget(label)

        # Grid Size Setting
        gridSizeLayout = QHBoxLayout()
        gridSizeLabel = QLabel('Grid Size:', self)
        gridSizeInput = QLineEdit(self)
        gridSizeInput.setPlaceholderText(str(config.GRID_SIZE))
        gridSizeInput.setText(str(config.GRID_SIZE))
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
        gridHeightInput.setText(str(config.GRID_HEIGHT))
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
        gridWidthInput.setText(str(config.GRID_WIDTH))
        gridWidthInput.setValidator(QIntValidator(1, 999, self))
        gridWidthLayout.addWidget(gridWidthLabel)
        gridWidthLayout.addWidget(gridWidthInput)
        gridWidthInput.textChanged.connect(self.onGridWidthChanged)
        layout.addLayout(gridWidthLayout)

        # Layer label
        label = QLabel('Layer Toggle', self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet('font-weight: bold')
        layout.addWidget(label)

        # Toggle Difficulty View
        difficultyToggleLayout = QHBoxLayout()
        difficultyToggleLabel = QLabel('Toggle Difficulty View:', self)
        self.difficultyToggleCheckbox = QCheckBox(self)
        self.difficultyToggleCheckbox.setChecked(config.DIFFICULTY_TOGGLE)
        difficultyToggleLayout.addWidget(difficultyToggleLabel)
        difficultyToggleLayout.addWidget(self.difficultyToggleCheckbox)
        self.difficultyToggleCheckbox.stateChanged.connect(self.onToggleDifficultyChanged)
        layout.addLayout(difficultyToggleLayout)

        # Toggle Finger View
        fingerToggleLayout = QHBoxLayout()
        fingerToggleLabel = QLabel('Toggle Finger View:', self)
        self.fingerToggleCheckbox = QCheckBox(self)
        self.fingerToggleCheckbox.setChecked(config.FINGER_TOGGLE)
        fingerToggleLayout.addWidget(fingerToggleLabel)
        fingerToggleLayout.addWidget(self.fingerToggleCheckbox)
        self.fingerToggleCheckbox.stateChanged.connect(self.onToggleFingerChanged)
        layout.addLayout(fingerToggleLayout)

        # Preset label
        label = QLabel('Template Layouts', self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet('font-weight: bold')
        layout.addWidget(label)

        # Preset dropdown
        keyboardLayoutDropdown = QComboBox(self)
        keyboardLayoutDropdown.addItem("Standard")
        keyboardLayoutDropdown.addItem("Corne")
        keyboardLayoutDropdown.addItem("100%")
        layout.addWidget(keyboardLayoutDropdown)

        # Export Json Button
        exportJsonButton = QPushButton("Load Preset", self)  
        exportJsonButton.pressed.connect(self.onExportJson)  
        layout.addWidget(exportJsonButton)

        # Json label
        label = QLabel('Json Toggle', self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet('font-weight: bold')
        layout.addWidget(label)

        # Export Json Button
        exportJsonButton = QPushButton("Export JSON", self)  
        exportJsonButton.pressed.connect(self.onExportJson)  
        layout.addWidget(exportJsonButton)

        # Import Json Button
        importJsonButton = QPushButton("Import JSON", self)  
        importJsonButton.pressed.connect(self.onImportJson)  
        layout.addWidget(importJsonButton)


        # --- Spacer to make everything move to top ---
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
        if state == 2:
            print("Difficulty view enabled")
            config.DIFFICULTY_TOGGLE = True
            config.FINGER_TOGGLE = False
            self.fingerToggleCheckbox.setChecked(False)
        else:
            print("Difficulty view disabled")
            config.DIFFICULTY_TOGGLE = False

    def onToggleFingerChanged(self, state):
        if state == 2:
            print("Finger view enabled")
            config.FINGER_TOGGLE = True
            config.DIFFICULTY_TOGGLE = False
            self.difficultyToggleCheckbox.setChecked(False)
        else:
            print("Finger view disabled")
            config.FINGER_TOGGLE = False

    def onImportJson(self):
        print('importing')

    def onExportJson(self):
        if not self.scene:
            print("No scene available for export.")
            return

        keys_data = []
        for item in self.scene.items():
            if isinstance(item, Key):
                key_data = {
                    'letter': item.letter,
                    'position': {'x': item.pos().x(), 'y': item.pos().y()},
                    'finger_number': item.finger_number,
                    'difficulty': item.difficulty
                }
                keys_data.append(key_data)

        filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'JSON (*.json)')[0]
        if filename:
            with open(filename, 'w') as outfile:
                json.dump(keys_data, outfile, indent=4)
            print(f"Keyboard layout exported to {filename}.")





