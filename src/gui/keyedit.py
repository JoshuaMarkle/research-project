from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config

class KeyEditorSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.selectedKeys = []
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Settings label
        label = QLabel('Key Editor', self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet('font-weight: bold; font-size: 18px')
        layout.addWidget(label)

        # Grid Size Setting
        positionLayout = QHBoxLayout()
        positionLabel = QLabel('Position: (', self)
        self.positionInputX = QLabel('', self)
        self.positionInputY = QLabel('', self)
        positionLayout.addWidget(positionLabel)
        positionLayout.addWidget(self.positionInputX)
        positionLayout.addWidget(self.positionInputY)
        positionLabel = QLabel(')', self)
        positionLayout.addWidget(positionLabel)
        layout.addLayout(positionLayout)

        # Finger Number Setting
        fingerNumberLayout = QHBoxLayout()
        fingerNumberLabel = QLabel('Finger Number:', self)
        self.fingerNumberInput = QLineEdit(self)
        # fingerNumberInput.setPlaceholderText(str(config.GRID_HEIGHT))
        self.fingerNumberInput.setValidator(QIntValidator(1, 10, self))
        fingerNumberLayout.addWidget(fingerNumberLabel)
        fingerNumberLayout.addWidget(self.fingerNumberInput)
        self.fingerNumberInput.textChanged.connect(self.onFingerNumberChanged)
        layout.addLayout(fingerNumberLayout)

        # Difficulty Setting
        difficultyLayout = QHBoxLayout()
        difficultyLabel = QLabel('Difficulty:', self)
        self.difficultyInput = QLineEdit(self)
        self.difficultyInput.setValidator(QIntValidator(0, 999, self))
        difficultyLayout.addWidget(difficultyLabel)
        difficultyLayout.addWidget(self.difficultyInput)
        self.difficultyInput.textChanged.connect(self.onDifficultyChanged)
        layout.addLayout(difficultyLayout)

        # --- Spacer to make everything move to top ---
        label = QLabel()   
        layout.addWidget(label)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(verticalSpacer)

    def setSelectedKeys(self, keys):
        self.selectedKeys = keys
        if not keys:  # No keys selected
            self.fingerNumberInput.setText('')
            self.difficultyInput.setText('')
            self.positionInputX.setText('')
            self.positionInputY.setText('')
        else:
            fingerNumbers = {key.finger_number for key in keys}
            difficulties = {key.difficulty for key in keys}
            positionsX = {key.pos().x() for key in keys}
            positionsY = {key.pos().x() for key in keys}

            if len(set(fingerNumbers)) == 1: self.fingerNumberInput.setText(str(fingerNumbers.pop()))
            else: self.fingerNumberInput.setPlaceholderText("Mult. Vals")
            if len(set(difficulties)) == 1: self.difficultyInput.setText(str(difficulties.pop()))
            else: self.difficultyInput.setPlaceholderText("Mult. Vals")
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
                    key.finger_number = int(value)
            except: pass

    def onDifficultyChanged(self, value):
        if value:
            try: 
                value = max(1, min(int(value), 100))
                for key in self.selectedKeys:
                    key.difficulty = int(value)
            except: pass

