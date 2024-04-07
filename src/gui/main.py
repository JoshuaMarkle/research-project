from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

from scene import DesignScene, DesignView
from showcase import ShowcaseScene, ShowcaseView
from sidebar import Sidebar
from optimizeside import OptimizerSidebar
from keyedit import KeyEditorSidebar
from key import *

# User
# I want to write a python gui that allows the user to create their own physical keyboard. I want to make it so the user can create keys, delete keys, change key characteristics (position, finger number, difficulty, and more), move around the keys on a grid. I want all of this to happen on the right side of the screen. On the left side of the screen, I want a small interactive sidebar that has a bunch of settings adjusters and nice things. For example it would have a toggler for difficulty that would then color all of the keys a shade of red based on the difficulty setting for that key. It would also have input for key size, grid size, import json, and export json. Do you understand this project

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Keyboard Layout Designer')
        self.setGeometry(100, 100, 1200, 800)  # Adjust size as needed

        self.initUI()

    def initUI(self):
        # Initialize QTabWidget
        self.tabs = QTabWidget(self)
        self.setCentralWidget(self.tabs)

        # Editor tab
        self.editorTab = QWidget()
        self.tabs.addTab(self.editorTab, "Editor")
        self.initEditorUI()

        # Optimizer tab
        self.optimizerTab = QWidget()
        self.tabs.addTab(self.optimizerTab, "Optimizer")
        self.initOptimizerUI()

    def initEditorUI(self):
        # Layout for the Editor tab
        editor_layout = QHBoxLayout(self.editorTab)

        # Initialize QSplitter
        splitter = QSplitter(Qt.Horizontal)
        editor_layout.addWidget(splitter)

        self.sidebarTabs = QTabWidget(self)

        # Sidebar
        self.sidebar = Sidebar()
        self.sidebarTabs.addTab(self.sidebar, "Settings")

        # Key Editor
        self.keyedit = KeyEditorSidebar()
        self.sidebarTabs.addTab(self.keyedit, "Key Edit")
        splitter.addWidget(self.sidebarTabs)

        # Design area (scene and view)
        self.designScene = DesignScene()  # Assuming DesignScene() is defined elsewhere
        self.designView = DesignView(self.designScene)  # Assuming DesignView() is defined elsewhere
        self.sidebar.scene = self.designScene
        self.keyedit.scene = self.designScene
        splitter.addWidget(self.designView)

        self.sidebarTabs.setMinimumWidth(200)
        self.designView.setMinimumWidth(500)

        self.designScene.selectionChanged.connect(self.updateSelectedKeys)
        self.designScene.changed.connect(self.updateKeys)
        self.tabs.currentChanged.connect(self.onTabChanged)

    def initOptimizerUI(self):
        # Layout for the Optimizer tab
        optimizer_layout = QVBoxLayout(self.optimizerTab)

        # Initialize QSplitter
        splitter = QSplitter(Qt.Horizontal)
        optimizer_layout.addWidget(splitter)

        # Sidebar
        self.showcaseSidebar = OptimizerSidebar()
        splitter.addWidget(self.showcaseSidebar)

        # Optimizer area (scene and view)
        self.showcaseScene = ShowcaseScene()  # Assuming showcaseScene() is defined elsewhere
        self.showcaseView = ShowcaseView(self.showcaseScene)  # Assuming showcaseView() is defined elsewhere
        self.showcaseSidebar.scene = self.showcaseScene
        splitter.addWidget(self.showcaseView)

        # self.sidebarTabs.setMinimumWidth(200)
        # self.optimizerView.setMinimumWidth(500)
        #
        # self.optimizerScene.selectionChanged.connect(self.updateSelectedKeys)
        # self.optimizerScene.changed.connect(self.updateKeys)

    def updateKeys(self):
        allKeys = [item for item in self.designScene.items() if isinstance(item, Key)]
        self.keyedit.setKeys(allKeys)

    def updateSelectedKeys(self):
        self.keyedit.setSelectedKeys([item for item in self.designScene.selectedItems() if isinstance(item, Key)])
        print("hi")

    def onTabChanged(self, index):
        if self.tabs.widget(index) == self.optimizerTab:
            self.showcaseScene.importFromDesignScene(self.designScene)
            self.showcaseView.fitKeyboardInView()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
