from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt
from ui_components import DesignScene, DesignView
from sidebar import Sidebar

# User
# I want to write a python gui that allows the user to create their own physical keyboard. I want to make it so the user can create keys, delete keys, change key characteristics (position, finger number, difficulty, and more), move around the keys on a grid. I want all of this to happen on the right side of the screen. On the left side of the screen, I want a small interactive sidebar that has a bunch of settings adjusters and nice things. For example it would have a toggler for difficulty that would then color all of the keys a shade of red based on the difficulty setting for that key. It would also have input for key size, grid size, import json, and export json. Do you understand this project

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Keyboard Layout Designer')
        self.setGeometry(100, 100, 1200, 800)  # Adjust size as needed

        self.initUI()

    def initUI(self):
        # Main widget and horizontal layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar, alignment=Qt.AlignLeft)

        # Design area (scene and view)
        self.designScene = DesignScene()
        self.designView = DesignView(self.designScene)
        main_layout.addWidget(self.designView)

        # Set the stretch factors to give the design area more space
        main_layout.setStretch(0, 1)  # Design area gets more space
        main_layout.setStretch(1, 6)  # Sidebar gets less space

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
