from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

class DebugBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def write(self, message):
        self.insertPlainText(message + "\n")
        self.moveCursorToBottom()

    def dataWrite(self, data):
        self.insertPlainText(f"Gen {data[0]} - Best {data[1]:.2f} - {data[2]}\n")
        self.moveCursorToBottom()

    def flush(self):
        pass

    def moveCursorToBottom(self):
        cursor = self.textCursor()
        cursor.movePosition(cursor.End)
        self.setTextCursor(cursor)
