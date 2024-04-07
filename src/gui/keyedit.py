from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config

class KeyEditorSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.keys = []
        self.selectedKeys = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Settings label
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

        # Delete Key Button
        deleteKeyButton = QPushButton("Delete Key", self)  
        deleteKeyButton.pressed.connect(self.onDeleteKey)  
        layout.addWidget(deleteKeyButton)

        # --- Spacer to make everything move to top ---
        label = QLabel()   
        layout.addWidget(label)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(verticalSpacer)

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

    def onDeleteKey(self):
        if self.scene:
            self.scene.onDeleteKey()
