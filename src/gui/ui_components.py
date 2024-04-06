from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit
from PyQt5.QtGui import QPalette, QPainter, QBrush, QColor, QPen
from PyQt5.QtCore import Qt, QRect, QPointF, QRectF, QPoint

from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsItem, QLabel, QVBoxLayout
from PyQt5.QtGui import QWheelEvent, QMouseEvent

GRID_SIZE = 50
GRID_HEIGHT = GRID_SIZE * 100
GRID_WIDTH = GRID_SIZE * 100

class Sidebar(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set the layout
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Set background color to light gray
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor('#e0e0e0'))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        label = QLabel('Settings', self)
        layout.addWidget(label)

        textbox = QLineEdit(self)
        textbox.setPlaceholderText(str(GRID_SIZE))
        layout.addWidget(textbox)


class DesignScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gridSize = GRID_SIZE
        self.setBackgroundBrush(QColor(255, 255, 255))
        self.setSceneRect(0, 0, GRID_WIDTH, GRID_HEIGHT)

        # Assuming you have set a scene rect somewhere
        centerX = self.width() / 2
        centerY = self.height() / 2

        # Adjust for key size to ensure the center of the key aligns with the center of the scene
        keyPosition = QPointF(centerX - 20, centerY - 20)  # Half of the key size (40/2 = 20)

        # Create and add the key to the scene
        key = Key('A', keyPosition, 1, 'Medium')
        self.addItem(key)

    def drawBackground(self, painter: QPainter, rect):
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
        # self.setRenderHint(QPainter.Antialiasing)
        # self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setDragMode(QGraphicsView.NoDrag)
        self.lastPanPoint = QPoint()

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

    def wheelEvent(self, event: QWheelEvent):
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

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
        self.size = 40  # Key size
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        # Define the bounding box for the key
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget=None):
        # Set the pen for the border of the key
        pen = QPen(QColor('black'), 2)
        painter.setPen(pen)
        
        # Set the brush for the inside of the key
        painter.setBrush(QColor('lightgrey'))
        
        # Draw the key as a rectangle
        painter.drawRect(self.boundingRect())
        
        # Draw the letter in the center of the key
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.letter)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange and self.scene():
            newPos = value.toPointF()

            # Snap the new position to the grid
            newX = round(newPos.x() / GRID_SIZE) * GRID_SIZE
            newY = round(newPos.y() / GRID_SIZE) * GRID_SIZE

            # Ensure the key doesn't leave the grid
            if newX < 0:
                newX = 0
            elif newX + self.size > GRID_WIDTH:
                newX = GRID_WIDTH - self.size

            if newY < 0:
                newY = 0
            elif newY + self.size > GRID_HEIGHT:
                newY = GRID_HEIGHT - self.size

            # Return the adjusted position
            return QPointF(newX, newY)

        return super().itemChange(change, value)
