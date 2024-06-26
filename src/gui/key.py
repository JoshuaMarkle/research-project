from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

import config
import time

class Key(QGraphicsItem):
    def __init__(self, letter, position, finger_number, difficulty, resting_pos, ind, parent=None):
        super().__init__(parent)
        self.label = letter
        self.setPos(position)  # Position should be a QPointF
        self.finger_number = finger_number
        self.main_finger = resting_pos
        self.difficulty = difficulty
        self.size = config.KEY_SIZE # Key size
        self.index = ind
        self.setFlags(QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        # Define the bounding box for the key
        return QRectF(0, 0, self.size, self.size)

    def paint(self, painter, option, widget=None):
        keyColor = config.COLOR_DARK_0
        keyColorTop = config.COLOR_0
        keyColorBorder = config.COLOR_SELECTED_BORDER if self.isSelected() else 'black'
        text = str(self.index)

        if config.NORMAL_TOGGLE:
            text = self.label.upper()
        if config.DIFFICULTY_TOGGLE:
            min_difficulty, max_difficulty = self.findDifficultyRange()
            keyColorTop, keyColor = self.mapDifficultyToColor(min_difficulty, max_difficulty, self.difficulty)
            text = str(self.difficulty)
        if config.FINGER_TOGGLE:
            colorsTop = [config.COLOR_1, config.COLOR_2, config.COLOR_3, config.COLOR_4, config.COLOR_5, config.COLOR_6, config.COLOR_7, config.COLOR_8, config.COLOR_9, config.COLOR_10]
            colors = [config.COLOR_DARK_1, config.COLOR_DARK_2, config.COLOR_DARK_3, config.COLOR_DARK_4, config.COLOR_DARK_5, config.COLOR_DARK_6, config.COLOR_DARK_7, config.COLOR_DARK_8, config.COLOR_DARK_9, config.COLOR_DARK_10]
            keyColorTop = colorsTop[self.finger_number - 1]
            keyColor = colors[self.finger_number - 1]
            text = str(self.finger_number)
        if config.FINGER_REST_TOGGLE:
            keyColorTop = config.COLOR_DARK_0
            keyColor = config.COLOR_ALT
            text = str(self.finger_number)
            if self.main_finger:
                keyColorTop = config.COLOR_3
                keyColor = config.COLOR_DARK_3

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
        painter.drawText(topRect, Qt.AlignCenter, text)

    # Snap to grid
    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        x = round(event.scenePos().x() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        y = round(event.scenePos().y() / config.GRID_SIZE) * config.GRID_SIZE - config.KEY_SIZE / 2
        pos = QPointF(x, y)
        self.setPos(pos)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.startPos = self.pos() # Start of the selection
        super().mousePressEvent(event)

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

    def mapDifficultyToColor(self, min_difficulty, max_difficulty, difficulty):
        
        colors = [QColor(config.COLOR_1), QColor(config.COLOR_2), QColor(config.COLOR_3), QColor(config.COLOR_4), QColor(config.COLOR_5)]
        dark_colors = [QColor(config.COLOR_DARK_1), QColor(config.COLOR_DARK_2), QColor(config.COLOR_DARK_3), QColor(config.COLOR_DARK_4), QColor(config.COLOR_DARK_5)]
        colors.reverse()
        dark_colors.reverse()

        normalized_difficulty = (difficulty - min_difficulty) / (max_difficulty - min_difficulty) if max_difficulty > min_difficulty else 0
        position = normalized_difficulty * (len(colors) - 1)
        index = int(position)
        index = max(0, min(index, len(colors) - 2))
        segment_pos = position - index

        start_color = colors[index]
        end_color = colors[index + 1]
        r = start_color.red() + (end_color.red() - start_color.red()) * segment_pos
        g = start_color.green() + (end_color.green() - start_color.green()) * segment_pos
        b = start_color.blue() + (end_color.blue() - start_color.blue()) * segment_pos
        light_color = QColor(int(r), int(g), int(b))
        
        start_dark_color = dark_colors[index]
        end_dark_color = dark_colors[index + 1]
        r_dark = start_dark_color.red() + (end_dark_color.red() - start_dark_color.red()) * segment_pos
        g_dark = start_dark_color.green() + (end_dark_color.green() - start_dark_color.green()) * segment_pos
        b_dark = start_dark_color.blue() + (end_dark_color.blue() - start_dark_color.blue()) * segment_pos
        dark_color = QColor(int(r_dark), int(g_dark), int(b_dark))

        return light_color, dark_color

    def findDifficultyRange(self):
        min_difficulty = float('inf')
        max_difficulty = float('-inf')
        for item in self.scene().items():
            if isinstance(item, Key):
                min_difficulty = min(min_difficulty, item.difficulty)
                max_difficulty = max(max_difficulty, item.difficulty)
        return min_difficulty, max_difficulty
