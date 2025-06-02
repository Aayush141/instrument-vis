from qwt import QwtPlotCanvas

from PySide6.QtGui import QMouseEvent
from PySide6.QtCore import Signal

class AnnotationBarCanvas(QwtPlotCanvas):
    mouseReleased = Signal(float) # x-value where clicked

    def __init__(self, plot = None):
        super().__init__(plot)

    def mousePressEvent(self, event: QMouseEvent):
        """On mouse press, save what position mouse clicked

        :param event: QMouseEvent object with coordinates of mouse location
        """
        self.origin = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        """On mouse release, emit what x-position mouse was clicked at
        
        :param event: QMouseEvent object with coordinates of mouse location
        """
        x = self.plot().invTransform(self.plot().xBottom, self.origin.x())
        self.mouseReleased.emit(x)


