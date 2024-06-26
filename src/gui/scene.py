from math import ceil

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config
from gui.key import *

class DesignScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gridSize = config.GRID_SIZE
        self.setBackgroundBrush(QColor(255, 255, 255))
        self.setSceneRect(0, 0, config.GRID_WIDTH * config.GRID_SIZE, config.GRID_HEIGHT * config.GRID_SIZE)

        # Assuming you have set a scene rect somewhere
        centerX = self.width() / 2 - 5 * config.KEY_SIZE
        centerY = self.height() / 2 - 5 * config.KEY_SIZE

    def drawBackground(self, painter: QPainter, rect):
        self.gridSize = config.GRID_SIZE
        self.setSceneRect(0, 0, config.GRID_WIDTH * config.GRID_SIZE, config.GRID_HEIGHT * config.GRID_SIZE)

        # Redraw the whole background (only here for dynamic GRID_SIZE)
        self.setBackgroundBrush(QColor(255, 255, 255))

        # Call the base class method to ensure the scene's background is drawn
        super().drawBackground(painter, rect)

        # Set the color and style for the grid lines
        gridPen = QPen(QColor(220, 220, 220))  # Light gray color for the grid lines
        gridPen.setWidth(0)  # Thin lines
        painter.setPen(gridPen)

        # Draw horizontal grid lines
        topLeft = self.sceneRect().topLeft()
        bottomRight = self.sceneRect().bottomRight()
        for y in range(int(topLeft.y()), int(bottomRight.y()), self.gridSize):
            painter.drawLine(int(topLeft.x()), y, int(bottomRight.x()), y)

        # Draw vertical grid lines
        for x in range(int(topLeft.x()), int(bottomRight.x()), self.gridSize):
            painter.drawLine(x, int(topLeft.y()), x, int(bottomRight.y()))

        # Draw the axis on the grid
        axisPen = QPen(QColor(config.COLOR_ALT))
        axisPen.setWidth(2)
        painter.setPen(axisPen)
        centerX = self.sceneRect().width() / 2
        centerY = self.sceneRect().height() / 2
        painter.drawLine(int(self.sceneRect().left()), int(centerY), int(self.sceneRect().right()), int(centerY))
        painter.drawLine(int(centerX), int(self.sceneRect().top()), int(centerX), int(self.sceneRect().bottom()))

    def onAddKey(self):
        x = round(self.sceneRect().width() / 2 / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        y = round(self.sceneRect().height() / 2 / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        newPos = QPointF(x, y)
        keys = [item for item in self.items() if isinstance(item, Key)]
        if len(keys) != 0:
            lastKey = keys[0]
            for key in keys:
                if lastKey.index < key.index:
                    lastKey = key
            x = lastKey.pos().x() + ceil(config.KEY_SIZE / config.GRID_SIZE) * config.GRID_SIZE
            newPos = QPointF(x, lastKey.pos().y())

        newKey = Key("A", newPos, 1, 1, False, len(keys) + 1)
        self.addItem(newKey)

    def onDeleteKey(self):
        for key in self.selectedItems():
            self.removeItem(key)
        self.fillKeyIndices()

    # Called when there are gaps within the key indexs
    def fillKeyIndices(self):
        keys = [item for item in self.items() if isinstance(item, Key)]
        keys.sort(key=lambda x: x.index)
        for i in range(len(keys)):
            keys[i].index = i + 1

class DesignView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setDragMode(QGraphicsView.NoDrag)
        self.lastPanPoint = QPoint()
        self.minZoomLevel = 0.5
        self.maxZoomLevel = 2.0
        self.currentZoomLevel = 1.0
        self.selectionRect = None  # Initialize selection rectangle

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mousePressEvent(event) # Drag items around
        if event.button() == Qt.MidButton:
            self.lastPanPoint = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        if event.button() == Qt.RightButton:
            self.origin = event.pos()  # Starting point for the selection rectangle
            self.selectionRect = QRect(self.origin, QSize())  # Initialize the selection rectangle
            self.update()  # Trigger a repaint

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MidButton:
            self.lastPanPoint = QPoint()
            self.setCursor(Qt.ArrowCursor)
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
        if not self.lastPanPoint.isNull():
            # Pan the view
            delta = event.pos() - self.lastPanPoint
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.lastPanPoint = event.pos()
        if event.buttons() & Qt.RightButton and self.selectionRect is not None:
            self.selectionRect.setBottomRight(event.pos())  # Update the selection rectangle
            self.update()  # Trigger a repaint

        super().mouseMoveEvent(event)

    def wheelEvent(self, event):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Calculate the new zoom level
        if event.angleDelta().y() > 0:  # Zoom in
            newZoomLevel = self.currentZoomLevel * zoomInFactor
        else:  # Zoom out
            newZoomLevel = self.currentZoomLevel * zoomOutFactor

        # Apply zoom if it's above the minimum zoom level
        if newZoomLevel >= self.minZoomLevel and newZoomLevel <= self.maxZoomLevel:
            self.scale(zoomInFactor if event.angleDelta().y() > 0 else zoomOutFactor, zoomInFactor if event.angleDelta().y() > 0 else zoomOutFactor)
            self.currentZoomLevel = newZoomLevel

            # Get the new position
            newPos = self.mapToScene(event.pos())

            # Move scene to old position
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())

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

