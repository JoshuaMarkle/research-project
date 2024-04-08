from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config
from gui.key import *

class ShowcaseScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.keys = None
        self.plotWindow = None
        self.setBackgroundBrush(QColor(255, 255, 255))  # Set background color
        self.setSceneRect(0, 0, config.GRID_WIDTH * config.GRID_SIZE, config.GRID_HEIGHT * config.GRID_SIZE)

    def drawBackground(self, painter: QPainter, rect):
        # Call the base class method to ensure the scene's background is drawn
        super().drawBackground(painter, rect)
        if self.keys:
            for key in self.keys:
                key.paint(painter)
        # No grid or additional elements are drawn here

    def importFromDesignScene(self, designScene):
        # First, remove any existing items in the showcase scene
        for item in self.items():
            self.removeItem(item)

        # Import items from the DesignScene
        for item in designScene.items():
            if isinstance(item, Key):
                # Create a copy of the Key item to add to the ShowcaseScene
                keyCopy = Key(item.label, QPointF(item.pos()), item.finger_number, item.difficulty, item.main_finger, item.index)
                self.addItem(keyCopy)

        padding = 20
        rect = self.itemsBoundingRect()
        self.setSceneRect(rect.adjusted(-padding, -padding, padding, padding))

    def optimizationUpdate(self, data):
        self.plotWindow.updatePlot(data[0], data[1])
        layout = data[2]
        for key in self.items():
            key.label = layout[key.index - 1]

class ShowcaseView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setDragMode(QGraphicsView.NoDrag)
        self.lastPanPoint = QPoint()
        self.minZoomLevel = 0.5
        self.maxZoomLevel = 2.0
        self.currentZoomLevel = 1.0
        self.selectionRect = None  # Initialize selection rectangle
        self.setAlignment(Qt.AlignCenter)  # Align the scene's content to the center of the view
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Always hide horizontal scrollbar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Always hide vertical scrollbar
        self.setDragMode(QGraphicsView.NoDrag)  # Disable dragging
        self.setInteractive(False)  # Disable interaction with the scene's items
        self.fitKeyboardInView()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitKeyboardInView()

    def fitKeyboardInView(self):
        rect = self.scene().itemsBoundingRect()
        self.fitInView(rect, Qt.KeepAspectRatio)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.origin = event.pos()  # Starting point for the selection rectangle
            self.selectionRect = QRect(self.origin, QSize())  # Initialize the selection rectangle
            self.update()  # Trigger a repaint

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton and self.selectionRect is not None:
            # Convert QRectF to QPainterPath
            selectionPath = QPainterPath()
            rect = QRectF(self.mapToScene(self.selectionRect.topLeft()), self.mapToScene(self.selectionRect.bottomRight()))
            selectionPath.addRect(rect)  # Add the QRectF as a rectangle path to the QPainterPath

            # Use the QPainterPath for selection
            self.scene().setSelectionArea(selectionPath)  # Now using a QPainterPath

            self.selectionRect = None  # Reset the selection rectangle
            self.update()  # Trigger a repaint

        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.RightButton and self.selectionRect is not None:
            self.selectionRect.setBottomRight(event.pos())  # Update the selection rectangle
            self.update()  # Trigger a repaint

        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        return

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.selectionRect: # Draw selection area
            painter = QPainter(self.viewport())
            painter.setPen(Qt.DashLine)
            painter.drawRect(self.selectionRect)

            fillColor = QColor(config.COLOR_8)
            fillColor.setAlpha(50)
            pen = QPen(fillColor, 1)
            painter.setPen(pen)
            painter.drawRect(self.selectionRect)
            painter.fillRect(self.selectionRect, fillColor)
