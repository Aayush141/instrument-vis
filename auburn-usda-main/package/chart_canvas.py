"""Canvas that Chart uses to plot data"""

from qwt import QwtPlotCanvas

from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QRubberBand
from PySide6.QtCore import QRect, QSize, Signal


class ChartCanvas(QwtPlotCanvas):
    mouseReleased = Signal(float, float)  # beginning x-value, duration
    mouseButtonPressed = Signal(float, float)  # x, y

    def __init__(self, plot=None):
        super().__init__(plot)
        self.rubberBand = None
        self.setStyleSheet("ChartCanvas   {background-color:white}")
        self.installEventFilter(self)
        self.setMouseTracking(True)
        self.mode = None

    def eventFilter(self, object, event):
        """Event filter that catches all user interactions with chart. Handles
        creating annotations through rubber band and getting current position of mouse
        """
        eventType = event.type()
        match eventType:
            case QMouseEvent.Type.MouseMove:
                # Update rubber band position on mouse move
                if self.rubberBand:
                    self.rubberBand.setGeometry(
                        QRect(self.origin, event.pos()).normalized()
                    )
                    return True
            case QMouseEvent.Type.MouseButtonDblClick:
                # Get chart coordinates on double click
                pos = event.pos()
                x = self.plot().invTransform(self.plot().xBottom, pos.x())
                y = self.plot().invTransform(self.plot().yLeft, pos.y())
                self.mouseButtonPressed.emit(x, y)
                return True
            case QMouseEvent.Type.MouseButtonPress:
                # Start rubber band
                self.origin = event.pos()
                if not self.rubberBand:
                    self.rubberBand = QRubberBand(QRubberBand.Shape.Rectangle, self)
                self.rubberBand.setGeometry(QRect(self.origin, QSize()))
                self.rubberBand.show()
                return True
            case QMouseEvent.Type.MouseButtonRelease:
                # End rubber band
                self.rubberBand.hide()
                # Convert pixel coordinates to chart coordinates
                x1 = self.plot().invTransform(self.plot().xBottom, self.origin.x())
                x2 = self.plot().invTransform(self.plot().xBottom, event.pos().x())

                # If user dragged mouse right to left
                duration = x2 - x1
                start = x1
                if x1 > x2:
                    start = x2
                    duration = x1 - x2

                # Send chart coordinates to create annotation window
                self.mouseReleased.emit(start, duration)
                return True
        return False
