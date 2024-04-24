from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import config

class SettingsTab(QWidget):
    fontSizeChanged = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)

        # Title label for settings section
        settingsLabel = QLabel("Settings", self)
        settingsLabel.setAlignment(Qt.AlignLeft)
        settingsLabel.setStyleSheet("font-weight: bold; font-size: 18px")
        layout.addWidget(settingsLabel)

        # Font size setting
        fontSizeLayout = QHBoxLayout()
        fontSizeLabel = QLabel("Font Size:", self)
        self.fontSizeCombo = QComboBox()
        self.fontSizeCombo.addItems(['10', '12', '14', '16', '18'])  # Possible font sizes
        self.fontSizeCombo.setCurrentText(str(config.DEFAULT_FONT_SIZE))
        fontSizeLayout.addWidget(fontSizeLabel)
        fontSizeLayout.addWidget(self.fontSizeCombo)
        self.fontSizeCombo.currentIndexChanged.connect(self.changeFontSize)
        layout.addLayout(fontSizeLayout)

        # Autosave toggle setting
        autosaveLayout = QHBoxLayout()
        autosaveLabel = QLabel("Enable Autosave:", self)
        self.autosaveCheckbox = QCheckBox()
        self.autosaveCheckbox.setChecked(config.ENABLE_AUTOSAVE)
        autosaveLayout.addWidget(autosaveLabel)
        autosaveLayout.addWidget(self.autosaveCheckbox)
        self.autosaveCheckbox.stateChanged.connect(self.toggleAutosave)
        layout.addLayout(autosaveLayout)

        # Spacer to push everything up
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

    def changeFontSize(self, index):
        new_size = self.fontSizeCombo.currentText()
        config.DEFAULT_FONT_SIZE = int(new_size)  # Update the font size in config
        QApplication.instance().setStyleSheet(f"* {{ font-size: {fontSize}px; }}")

    def toggleAutosave(self, state):
        config.ENABLE_AUTOSAVE = bool(state)

# This QWidget can be directly added into your main application window as a new tab.
