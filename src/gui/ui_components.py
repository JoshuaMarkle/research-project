from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config

class DesignScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gridSize = config.GRID_SIZE
        self.setBackgroundBrush(QColor(255, 255, 255))
        self.setSceneRect(0, 0, config.GRID_WIDTH, config.GRID_HEIGHT)

        # Assuming you have set a scene rect somewhere
        centerX = self.width() / 2
        centerY = self.height() / 2

        # Adjust for key size to ensure the center of the key aligns with the center of the scene
        keyPosition = QPointF(centerX - 20, centerY - 20)  # Half of the key size (40/2 = 20)

        # Create and add the key to the scene
        key = Key('A', keyPosition, 1, 'Medium')
        self.addItem(key)

    def drawBackground(self, painter: QPainter, rect):
        self.gridSize = config.GRID_SIZE
        self.setSceneRect(0, 0, config.GRID_WIDTH, config.GRID_HEIGHT)

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

class DesignView(QGraphicsView):
    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setDragMode(QGraphicsView.NoDrag)
        self.lastPanPoint = QPoint()
        self.minZoomLevel = 0.2
        self.maxZoomLevel = 5.0
        self.currentZoomLevel = 1.0

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.lastPanPoint = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.lastPanPoint = QPoint()
            self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if not self.lastPanPoint.isNull():
            # Pan the view
            delta = event.pos() - self.lastPanPoint
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            self.lastPanPoint = event.pos()
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

class Key(QGraphicsItem):
    def __init__(self, letter, position, finger_number, difficulty, parent=None):
        super().__init__(parent)
        self.letter = letter
        self.setPos(position)  # Position should be a QPointF
        self.finger_number = finger_number
        self.difficulty = difficulty
        self.size = config.KEY_SIZE # Key size
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        # Define the bounding box for the key
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget=None):
        # Draw the base
        pen = QPen(QColor('black'), 2)
        painter.setPen(pen)
        painter.setBrush(QColor('lightgrey'))
        painter.drawRect(self.boundingRect())

        # Draw the top
        pen = QPen(QColor('white'), 5)
        topRect = QRectF(self.size * .2, self.size * .13, self.size * .6, self.size * .6)
        painter.setPen(pen)
        painter.setBrush(QColor('white'))
        painter.drawRect(topRect)

        # Draw the letter
        pen = QPen(QColor('black'), 2)
        painter.setPen(pen)
        painter.drawText(topRect, Qt.AlignCenter, self.letter)

    # Snap to grid
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        x = round(event.scenePos().x() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        y = round(event.scenePos().y() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        pos = QPointF(x, y)
        self.setPos(pos)
