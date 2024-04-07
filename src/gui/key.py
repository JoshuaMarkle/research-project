from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config

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
        keyColor = config.COLOR_DARK_0
        keyColorTop = config.COLOR_0
        keyColorBorder = 'black'
        if self.isSelected():
            keyColorBorder = config.COLOR_DARK_8
        if config.DIFFICULTY_TOGGLE:
            if self.difficulty == 1:
                keyColorTop = config.COLOR_1
                keyColor = config.COLOR_DARK_1
            if self.difficulty == 2:
                keyColorTop = config.COLOR_2
                keyColor = config.COLOR_DARK_2
            if self.difficulty == 3:
                keyColorTop = config.COLOR_3
                keyColor = config.COLOR_DARK_3
            if self.difficulty == 4:
                keyColorTop = config.COLOR_4
                keyColor = config.COLOR_DARK_4
            if self.difficulty == 5:
                keyColorTop = config.COLOR_5
                keyColor = config.COLOR_DARK_5
        if config.FINGER_TOGGLE:
            if self.finger_number == 1:
                keyColorTop = config.COLOR_1
                keyColor = config.COLOR_DARK_1
            if self.finger_number == 2:
                keyColorTop = config.COLOR_2
                keyColor = config.COLOR_DARK_2
            if self.finger_number == 3:
                keyColorTop = config.COLOR_3
                keyColor = config.COLOR_DARK_3
            if self.finger_number == 4:
                keyColorTop = config.COLOR_4
                keyColor = config.COLOR_DARK_4
            if self.finger_number == 5:
                keyColorTop = config.COLOR_5
                keyColor = config.COLOR_DARK_5
            if self.finger_number == 6:
                keyColorTop = config.COLOR_6
                keyColor = config.COLOR_DARK_6
            if self.finger_number == 7:
                keyColorTop = config.COLOR_7
                keyColor = config.COLOR_DARK_7
            if self.finger_number == 8:
                keyColorTop = config.COLOR_8
                keyColor = config.COLOR_DARK_8
            if self.finger_number == 9:
                keyColorTop = config.COLOR_9
                keyColor = config.COLOR_DARK_9
            if self.finger_number == 10:
                keyColorTop = config.COLOR_10
                keyColor = config.COLOR_DARK_10

        # Draw the base
        path = QPainterPath()
        path.addRoundedRect(self.boundingRect(), 5, 5)
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

        if config.FINGER_TOGGLE:
            painter.drawText(topRect, Qt.AlignCenter, str(self.finger_number))
        else:
            painter.drawText(topRect, Qt.AlignCenter, self.letter)

    # Snap to grid
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        x = round(event.scenePos().x() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        y = round(event.scenePos().y() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        pos = QPointF(x, y)
        self.setPos(pos)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.startPos = self.pos()  # Record the starting position
        super().mousePressEvent(event)  # Call the superclass method to ensure default behavior

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        # Original position of the key being dragged before moving
        originalPos = self.pos()

        # Snap the position of the key being dragged to the grid
        x = round(event.scenePos().x() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        y = round(event.scenePos().y() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        snappedPos = QPointF(x, y)
        self.setPos(snappedPos)

        # Calculate the movement delta based on the snapped position
        delta = snappedPos - originalPos

        for item in self.scene().selectedItems(): # Move all other keys by same delta
            if isinstance(item, Key) and item != self:
                item.setPos(item.pos() + delta)
