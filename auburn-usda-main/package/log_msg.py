from package.ui_python.log_msg_ui import Ui_LogMsg
from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import Qt, qDebug, QIODevice, Signal
from PySide6.QtGui import QTextCharFormat, QColor, QFont, QTextCursor, QSyntaxHighlighter
import re

class LogMsgHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.rules = [
            (r'\[\d+m(DEBUG)\s', Qt.blue),
            (r'\[\d+m(INFO)\s', Qt.green),
            (r'\[\d+m(WARNING)\s', Qt.yellow),
            (r'\[\d+m(ERROR)\s', Qt.red)
        ]

    def highlightBlock(self, text):
        for pattern, color in self.rules:
            for match in re.finditer(pattern, text):
                start_index = match.start(1)
                end_index = match.end(1)
                self.setFormat(start_index, end_index - start_index, QTextCharFormat().setForeground(color))
        return None

class LogMsg(QMainWindow):
    """ Pop-up window that prints out the log messages.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_LogMsg()
        self.ui.setupUi(self)
        self.highlighter = LogMsgHighlighter(self.ui.plainTextEdit)

    def update_live_log(self, log_msg):
          self.ui.plainTextEdit.appendPlainText(log_msg)
