import json
from math import ceil

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config
from gui.key import *

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.keys = []
        self.selectedKeys = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Settings label
        label = QLabel("Settings", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        layout.addWidget(label)

        # Grid label
        label = QLabel("Grid Settings", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold")
        layout.addWidget(label)

        # Toggle Grid
        # Reset grid button

        # Grid Size Setting
        gridSizeLayout = QHBoxLayout()
        gridSizeLabel = QLabel("Grid Size:", self)
        gridSizeInput = QLineEdit(self)
        gridSizeInput.setPlaceholderText(str(config.GRID_SIZE))
        gridSizeInput.setText(str(config.GRID_SIZE))
        gridSizeInput.setValidator(QIntValidator(0, 9999, self))
        gridSizeLayout.addWidget(gridSizeLabel)
        gridSizeLayout.addWidget(gridSizeInput)
        gridSizeInput.textChanged.connect(self.onGridSizeChanged)
        layout.addLayout(gridSizeLayout)

        # Grid Height Setting
        gridHeightLayout = QHBoxLayout()
        gridHeightLabel = QLabel("Grid Height:", self)
        gridHeightInput = QLineEdit(self)
        gridHeightInput.setPlaceholderText(str(config.GRID_HEIGHT))
        gridHeightInput.setText(str(config.GRID_HEIGHT))
        gridHeightInput.setValidator(QIntValidator(0, 9999, self))
        gridHeightLayout.addWidget(gridHeightLabel)
        gridHeightLayout.addWidget(gridHeightInput)
        gridHeightInput.textChanged.connect(self.onGridHeightChanged)
        layout.addLayout(gridHeightLayout)

        # Grid Width Setting
        gridWidthLayout = QHBoxLayout()
        gridWidthLabel = QLabel("Grid Width:", self)
        gridWidthInput = QLineEdit(self)
        gridWidthInput.setPlaceholderText(str(config.GRID_WIDTH))
        gridWidthInput.setText(str(config.GRID_WIDTH))
        gridWidthInput.setValidator(QIntValidator(1, 999, self))
        gridWidthLayout.addWidget(gridWidthLabel)
        gridWidthLayout.addWidget(gridWidthInput)
        gridWidthInput.textChanged.connect(self.onGridWidthChanged)
        layout.addLayout(gridWidthLayout)

        # Layer label
        label = QLabel("Layer Toggle", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold")
        layout.addWidget(label)

        # Toggle Difficulty View
        difficultyToggleLayout = QHBoxLayout()
        difficultyToggleLabel = QLabel("Toggle Difficulty View:", self)
        self.difficultyToggleCheckbox = QCheckBox(self)
        self.difficultyToggleCheckbox.setChecked(config.DIFFICULTY_TOGGLE)
        difficultyToggleLayout.addWidget(difficultyToggleLabel)
        difficultyToggleLayout.addWidget(self.difficultyToggleCheckbox)
        self.difficultyToggleCheckbox.stateChanged.connect(self.onToggleDifficultyChanged)
        layout.addLayout(difficultyToggleLayout)

        # Toggle Finger View
        fingerToggleLayout = QHBoxLayout()
        fingerToggleLabel = QLabel("Toggle Finger View:", self)
        self.fingerToggleCheckbox = QCheckBox(self)
        self.fingerToggleCheckbox.setChecked(config.FINGER_TOGGLE)
        fingerToggleLayout.addWidget(fingerToggleLabel)
        fingerToggleLayout.addWidget(self.fingerToggleCheckbox)
        self.fingerToggleCheckbox.stateChanged.connect(self.onToggleFingerChanged)
        layout.addLayout(fingerToggleLayout)

        # Toggle Finger Rest View
        fingerRestToggleLayout = QHBoxLayout()
        fingerRestToggleLabel = QLabel("Finger Resting Pos View:", self)
        self.fingerRestToggleCheckbox = QCheckBox(self)
        self.fingerRestToggleCheckbox.setChecked(config.FINGER_REST_TOGGLE)
        fingerRestToggleLayout.addWidget(fingerRestToggleLabel)
        fingerRestToggleLayout.addWidget(self.fingerRestToggleCheckbox)
        self.fingerRestToggleCheckbox.stateChanged.connect(self.onToggleFingerRestChanged)
        layout.addLayout(fingerRestToggleLayout)

        # Add Key Button
        addKeyButton = QPushButton("Add Key", self)  
        addKeyButton.pressed.connect(self.onAddKey)  
        layout.addWidget(addKeyButton)

        # Delete Key Button
        deleteKeyButton = QPushButton("Delete Key", self)  
        deleteKeyButton.pressed.connect(self.onDeleteKey)  
        layout.addWidget(deleteKeyButton)

        # Preset label
        label = QLabel("Template Layouts", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold")
        layout.addWidget(label)

        # Preset dropdown
        keyboardLayoutDropdown = QComboBox(self)
        keyboardLayoutDropdown.addItem("Standard")
        keyboardLayoutDropdown.addItem("Corne")
        keyboardLayoutDropdown.addItem("100%")
        layout.addWidget(keyboardLayoutDropdown)

        # Json label
        label = QLabel("Json Toggle", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold")
        layout.addWidget(label)

        # Export Json Button
        exportJsonButton = QPushButton("Export JSON", self)  
        exportJsonButton.pressed.connect(self.onExportJson)  
        layout.addWidget(exportJsonButton)

        # Import Json Button
        importJsonButton = QPushButton("Import JSON", self)  
        importJsonButton.pressed.connect(self.onImportJson)  
        layout.addWidget(importJsonButton)

        # Keyedit label
        label = QLabel("Key Editor", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        layout.addWidget(label)

        # Label label : CHANGE THIS TO AN INPUT
        keyLabelLayout = QHBoxLayout()
        label = QLabel("Label:", self)
        self.keyLabel = QLabel("", self)
        keyLabelLayout.addWidget(label)
        keyLabelLayout.addWidget(self.keyLabel)
        layout.addLayout(keyLabelLayout)

        # Key Index label
        keyIndexLabelLayout = QHBoxLayout()
        label = QLabel("Index:", self)
        self.keyIndexLabel = QLabel("", self)
        keyIndexLabelLayout.addWidget(label)
        keyIndexLabelLayout.addWidget(self.keyIndexLabel)
        layout.addLayout(keyIndexLabelLayout)

        # Grid Size Setting
        positionLayout = QHBoxLayout()
        positionLabel = QLabel("Position: (", self)
        self.positionInputX = QLabel("", self)
        self.positionInputY = QLabel("", self)
        positionLayout.addWidget(positionLabel)
        positionLayout.addWidget(self.positionInputX)
        positionLayout.addWidget(self.positionInputY)
        positionLabel = QLabel(")", self)
        positionLayout.addWidget(positionLabel)
        layout.addLayout(positionLayout)

        # Finger Number Setting
        fingerNumberLayout = QHBoxLayout()
        fingerNumberLabel = QLabel("Finger Number:", self)
        self.fingerNumberInput = QLineEdit(self)
        # fingerNumberInput.setPlaceholderText(str(config.GRID_HEIGHT))
        self.fingerNumberInput.setValidator(QIntValidator(1, 10, self))
        fingerNumberLayout.addWidget(fingerNumberLabel)
        fingerNumberLayout.addWidget(self.fingerNumberInput)
        self.fingerNumberInput.textChanged.connect(self.onFingerNumberChanged)
        layout.addLayout(fingerNumberLayout)

        # Difficulty Setting
        difficultyLayout = QHBoxLayout()
        difficultyLabel = QLabel("Difficulty:", self)
        self.difficultyInput = QLineEdit(self)
        self.difficultyInput.setValidator(QIntValidator(0, 999, self))
        difficultyLayout.addWidget(difficultyLabel)
        difficultyLayout.addWidget(self.difficultyInput)
        self.difficultyInput.textChanged.connect(self.onDifficultyChanged)
        layout.addLayout(difficultyLayout)

        # Toggle Main Finger Checkbox
        mainFingerToggleLayout = QHBoxLayout()
        mainFingerToggleLabel = QLabel("Finger Rest Location:", self)
        self.mainFingerToggleCheckbox = QCheckBox(self)
        self.mainFingerToggleCheckbox.setChecked(False)
        mainFingerToggleLayout.addWidget(mainFingerToggleLabel)
        mainFingerToggleLayout.addWidget(self.mainFingerToggleCheckbox)
        self.mainFingerToggleCheckbox.stateChanged.connect(self.onToggleFingerRestChanged)
        layout.addLayout(mainFingerToggleLayout)

        # --- Spacer to make everything move to top ---
        label = QLabel()   
        layout.addWidget(label)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(verticalSpacer)

    def onGridSizeChanged(self, value):
        if value:
            try:
                value = min(int(value), 2000)
                config.GRID_SIZE = int(value)
            except: pass

    def onGridHeightChanged(self, value):
        if value:
            try:
                value = min(int(value), 2000)
                config.GRID_HEIGHT = int(value)
            except: pass

    def onGridWidthChanged(self, value):
        if value:
            config.GRID_WIDTH = int(value)


    def onToggleDifficultyChanged(self, state):
        if state == 2:
            config.DIFFICULTY_TOGGLE = True
            config.FINGER_TOGGLE = False
            config.FINGER_REST_TOGGLE = False
            self.fingerToggleCheckbox.setChecked(False)
            self.fingerRestToggleCheckbox.setChecked(False)
        else:
            config.DIFFICULTY_TOGGLE = False

    def onToggleFingerChanged(self, state):
        if state == 2:
            config.FINGER_TOGGLE = True
            config.DIFFICULTY_TOGGLE = False
            config.FINGER_REST_TOGGLE = False
            self.difficultyToggleCheckbox.setChecked(False)
            self.fingerRestToggleCheckbox.setChecked(False)
        else:
            config.FINGER_TOGGLE = False

    def onToggleFingerRestChanged(self, state):
        if state == 2:
            config.FINGER_REST_TOGGLE = True
            config.DIFFICULTY_TOGGLE = False
            config.FINGER_TOGGLE = False
            self.difficultyToggleCheckbox.setChecked(False)
            self.fingerToggleCheckbox.setChecked(False)
        else:
            config.FINGER_REST_TOGGLE = False

    def onImportJson(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open JSON", "", "JSON Files (*.json)")
        if filename:
            with open(filename, 'r') as infile:
                keys_data = json.load(infile)

            # Clear existing keys
            existing_keys = [item for item in self.scene.items() if isinstance(item, Key)]
            for key in existing_keys:
                self.scene.removeItem(key)

            # Add new keys from the imported data
            for key_data in keys_data:
                label = key_data.get('label', 'A')  # Default to 'A' if label is not specified
                index = key_data.get('index', 1)  # Default to 1 if index is not specified
                x = key_data['position']['x']
                y = key_data['position']['y']
                finger_number = key_data.get('finger_number', 1)  # Default to 1 if finger_number is not specified
                difficulty = key_data.get('difficulty', 0) # Default to 1 if difficulty is not specified
                resting_position = key_data.get('resting_position', False)
                newKey = Key(label, QPointF(x, y), finger_number, difficulty, resting_position, index)
                self.scene.addItem(newKey)

            self.scene.fillKeyIndices()

            print(f"Keyboard layout imported from {filename}.")

    def onExportJson(self):
        if not self.scene:
            print("Something went wrong! No scene available for export.")
            return

        keys_data = []
        for item in self.scene.items():
            if isinstance(item, Key):
                key_data = {
                    'label': item.label,
                    'index': item.index,
                    'position': {'x': item.pos().x(), 'y': item.pos().y()},
                    'finger_number': item.finger_number,
                    'difficulty': item.difficulty,
                    'resting_position': item.main_finger
                }
                keys_data.append(key_data)

        filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'JSON (*.json)')[0]
        if filename[-5:] != ".json":
            filename += ".json"
        if filename:
            with open(filename, 'w') as outfile:
                json.dump(keys_data, outfile, indent=4)
            print(f"Keyboard layout exported to {filename}.")

    def onAddKey(self):
        if self.scene:
            self.scene.onAddKey()

    def onDeleteKey(self):
        if self.scene:
            self.scene.onDeleteKey()

    def setKeys(self, keys):
        self.keys = keys

    def setSelectedKeys(self, keys):
        self.selectedKeys = keys
        if not keys:  # No keys selected
            self.keyLabel.setText("")
            self.keyIndexLabel.setText("")
            self.fingerNumberInput.setText("")
            self.difficultyInput.setText("")
            self.positionInputX.setText("")
            self.positionInputY.setText("")
            self.positionInputY.setText("")
        else:
            keyLabels = {key.label for key in keys}
            keyIndexs = {key.index for key in keys}
            fingerNumbers = {key.finger_number for key in keys}
            difficulties = {key.difficulty for key in keys}
            mainFingerKeys = {key.main_finger for key in keys}
            positionsX = {key.pos().x() for key in keys}
            positionsY = {key.pos().x() for key in keys}

            if len(set(fingerNumbers)) == 1: self.fingerNumberInput.setText(str(fingerNumbers.pop()))
            else: self.fingerNumberInput.setPlaceholderText("Mult. Vals")
            if len(set(difficulties)) == 1: self.difficultyInput.setText(str(difficulties.pop()))
            else: self.difficultyInput.setPlaceholderText("Mult. Vals")
            if len(set(mainFingerKeys)) == 1: self.mainFingerToggleCheckbox.setChecked(mainFingerKeys.pop())
            if len(set(keyIndexs)) == 1: self.keyIndexLabel.setText(str(keyIndexs.pop()))
            if len(set(keyLabels)) == 1: self.keyLabel.setText(keyLabels.pop())
            else: self.keyLabel.setText("-")
            if len(positionsX) == 1:
                self.positionInputX.setText(str(positionsX.pop()))
                self.positionInputY.setText(str(positionsY.pop()))
            else: 
                self.positionInputX.setText("-")
                self.positionInputY.setText("-")

    def onFingerNumberChanged(self, value):
        if value:
            try: 
                value = max(1, min(int(value), 10))
                for key in self.selectedKeys:
                    if key.finger_number != int(value):
                        key.finger_number = int(value)
                        key.main_finger = False
            except: pass

    def onDifficultyChanged(self, value):
        if value:
            try: 
                value = max(1, min(int(value), 100))
                for key in self.selectedKeys:
                    key.difficulty = int(value)
            except: pass

    def onToggleFingerRestChanged(self, state):
        if state == 2:
            for key in self.selectedKeys:
                for k in self.keys:
                    if k.finger_number == key.finger_number and k.main_finger:
                        # Only one finger can have a main key status (raise notification)
                        break
                else:
                    key.main_finger = True
        else:
            for key in self.selectedKeys:
                key.main_finger = False
