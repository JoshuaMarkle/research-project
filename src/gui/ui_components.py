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
        centerX = self.width() / 2 - 5 * config.KEY_SIZE
        centerY = self.height() / 2 - 5 * config.KEY_SIZE

        # Generate a standard layout
        abcs = "qwertyuiopasdfghjkl;zxcvbnm,./".upper()
        for i in range(3):
            for j in range(10):
                keyPosition = QPointF(centerX + j * config.GRID_SIZE - config.KEY_SIZE/2, centerY + i * config.GRID_SIZE - config.KEY_SIZE/2)
                key = Key(abcs[j + 10 * i], keyPosition, j, j % 5 + 1)
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
        keyColor = config.KEY_COLOR
        keyColorTop = config.KEY_COLOR_TOP
        keyColorBorder = 'black'
        if config.DIFFICULTY_TOGGLE:
            if self.difficulty == 1:
                keyColor = config.KEY_COLOR_DIFF_1
                keyColorTop = config.KEY_COLOR_TOP_DIFF_1
            if self.difficulty == 2:
                keyColor = config.KEY_COLOR_DIFF_2
                keyColorTop = config.KEY_COLOR_TOP_DIFF_2
            if self.difficulty == 3:
                keyColor = config.KEY_COLOR_DIFF_3
                keyColorTop = config.KEY_COLOR_TOP_DIFF_3
            if self.difficulty == 4:
                keyColor = config.KEY_COLOR_DIFF_4
                keyColorTop = config.KEY_COLOR_TOP_DIFF_4
            if self.difficulty == 5:
                keyColor = config.KEY_COLOR_DIFF_5
                keyColorTop = config.KEY_COLOR_TOP_DIFF_5

        # Draw the base
        path = QPainterPath()
        path.addRoundedRect(self.boundingRect(), 4, 4)
        pen = QPen(QColor(keyColorBorder), 2)
        painter.setPen(pen)
        painter.fillPath(path, QColor(keyColor))
        painter.drawPath(path)
        
        # Draw the top
        path = QPainterPath()
        topRect = QRectF(self.size * .15, self.size * 0.08, self.size * .7, self.size * .7)
        path.addRoundedRect(topRect, 4, 4)
        pen = QPen(QColor(keyColorTop), 0)
        painter.setPen(pen)
        painter.fillPath(path, QColor(keyColorTop))
        painter.drawPath(path)

        # Draw the letter
        pen = QPen(QColor(keyColorBorder), 2)
        painter.setPen(pen)
        painter.drawText(topRect, Qt.AlignCenter, self.letter)

    # Snap to grid
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        x = round(event.scenePos().x() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        y = round(event.scenePos().y() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        pos = QPointF(x, y)
        self.setPos(pos)
