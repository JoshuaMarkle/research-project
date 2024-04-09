from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

from gui.scene import DesignScene, DesignView
from gui.showcase import ShowcaseScene, ShowcaseView
from gui.sidebar import Sidebar
from gui.optimizeside import OptimizerSidebar
from gui.plot import PlotWindow
from gui.key import Key
from gui.debug import DebugBox

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

        # Sidebar
        self.sidebar = Sidebar()
        splitter.addWidget(self.sidebar)

        # Design area (scene and view)
        self.designScene = DesignScene()  # Assuming DesignScene() is defined elsewhere
        self.designView = DesignView(self.designScene)  # Assuming DesignView() is defined elsewhere
        self.sidebar.scene = self.designScene
        self.sidebar.scene = self.designScene
        splitter.addWidget(self.designView)

        self.sidebar.setMinimumWidth(200)
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

        # Add plot & debug box
        plotDebugWidget = QWidget()
        plotDebugLayout = QVBoxLayout(plotDebugWidget)
        self.plotWindow = PlotWindow()
        self.showcaseScene.plotWindow = self.plotWindow  
        self.debugBox = DebugBox()
        plotDebugLayout.addWidget(self.plotWindow)
        plotDebugLayout.addWidget(self.debugBox)
        splitter.addWidget(plotDebugWidget)  
        self.showcaseSidebar.debugBox = self.debugBox

        self.showcaseSidebar.setMinimumWidth(200)
        self.showcaseView.setMinimumWidth(200)
        plotDebugWidget.setMinimumWidth(500)

    def updateKeys(self):
        allKeys = [item for item in self.designScene.items() if isinstance(item, Key)]
        self.sidebar.setKeys(allKeys)

    def updateSelectedKeys(self):
        self.sidebar.setSelectedKeys([item for item in self.designScene.selectedItems() if isinstance(item, Key)])
        print("hi")

    def onTabChanged(self, index):
        if self.tabs.widget(index) == self.optimizerTab:
            self.showcaseScene.importFromDesignScene(self.designScene)
            self.showcaseView.fitKeyboardInView()
