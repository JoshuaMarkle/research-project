from math import ceil

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config
from gui.key import *
from algorithm.entry import OptimizationWorker

class OptimizerSidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.scene = None
        self.debugBox = None
        self.thread = QThread()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Optimizer Settings label
        label = QLabel("Layout Optimizer", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold; font-size: 18px")
        layout.addWidget(label)

        # Layer label
        label = QLabel("Layer Toggle", self)
        label.setAlignment(Qt.AlignLeft)
        label.setStyleSheet("font-weight: bold")
        layout.addWidget(label)

        # Toggle Normal View
        normalToggleLayout = QHBoxLayout()
        normalToggleLabel = QLabel("Toggle Normal View:", self)
        self.normalToggleCheckbox = QCheckBox(self)
        self.normalToggleCheckbox.setChecked(config.NORMAL_TOGGLE)
        normalToggleLayout.addWidget(normalToggleLabel)
        normalToggleLayout.addWidget(self.normalToggleCheckbox)
        self.normalToggleCheckbox.stateChanged.connect(self.onToggleNormal)
        layout.addLayout(normalToggleLayout)

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

        # Start Opt Button
        self.startOptimizationButton = QPushButton("Start Optimization", self)
        layout.addWidget(self.startOptimizationButton)
        self.startOptimizationButton.clicked.connect(self.startOptimization)

        # --- Spacer to make everything move to top ---
        label = QLabel()   
        layout.addWidget(label)
        verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(verticalSpacer)

    def onToggleNormal(self, state):
        if state == 2:
            config.NORMAL_TOGGLE = True
            config.DIFFICULTY_TOGGLE = False
            config.FINGER_TOGGLE = False
            config.FINGER_REST_TOGGLE = False
            self.fingerToggleCheckbox.setChecked(False)
            self.fingerRestToggleCheckbox.setChecked(False)
            self.difficultyToggleCheckbox.setChecked(False)
            if self.scene:
                self.scene.update()
        else:
            config.NORMAL_TOGGLE = False

    def onToggleDifficultyChanged(self, state):
        if state == 2:
            config.DIFFICULTY_TOGGLE = True
            config.NORMAL_TOGGLE = False
            config.FINGER_TOGGLE = False
            config.FINGER_REST_TOGGLE = False
            self.normalToggleCheckbox.setChecked(False)
            self.fingerToggleCheckbox.setChecked(False)
            self.fingerRestToggleCheckbox.setChecked(False)
            if self.scene:
                self.scene.update()
        else:
            config.DIFFICULTY_TOGGLE = False

    def onToggleFingerChanged(self, state):
        if state == 2:
            config.FINGER_TOGGLE = True
            config.NORMAL_TOGGLE = False
            config.DIFFICULTY_TOGGLE = False
            config.FINGER_REST_TOGGLE = False
            self.normalToggleCheckbox.setChecked(False)
            self.difficultyToggleCheckbox.setChecked(False)
            self.fingerRestToggleCheckbox.setChecked(False)
            if self.scene:
                self.scene.update()
        else:
            config.FINGER_TOGGLE = False

    def onToggleFingerRestChanged(self, state):
        if state == 2:
            config.FINGER_REST_TOGGLE = True
            config.NORMAL_TOGGLE = False
            config.DIFFICULTY_TOGGLE = False
            config.FINGER_TOGGLE = False
            self.normalToggleCheckbox.setChecked(False)
            self.difficultyToggleCheckbox.setChecked(False)
            self.fingerToggleCheckbox.setChecked(False)
            if self.scene:
                self.scene.update()
        else:
            config.FINGER_REST_TOGGLE = False

    def startOptimization(self):
        # Check for current thread
        if self.thread.isRunning():
            self.debugBox.write("Cannot Start; Optimization Is Running!")
            return

        # Create a Thread for the optimization algorithm
        self.worker = OptimizationWorker()
        self.worker.moveToThread(self.thread)
        self.debugBox.write("Starting Optimization...")
        self.worker.update.connect(self.scene.optimizationUpdate)
        self.worker.update.connect(self.debugBox.dataWrite)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.completeMessage)
        self.thread.start()

    def completeMessage(self):
        self.debugBox.write("Complete Optimization")
        self.thread.quit()
