from qwt import QwtPlotItem, QwtScaleMap, QwtInterval
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QRectF


class RangeMarker(QwtPlotItem):
    """ Creates a colored background on a QwtPlot for some x-interval """
    def __init__(self, color: QColor):
        super().__init__()
        self.setZ(10)
        self.color = color 

    def setInterval(self, x1: float, x2: float):
        """ Sets x-interval of marker
        """
        self.interval = QwtInterval(x1, x2)
    
    def setX2(self, x2: float):
        """ Sets the upper-bound of the x-range of the marker
            Typically used for increasing size of range marker

            :param x2: New upper-bound of x-range for marker
        """
        self.interval = QwtInterval(self.interval.minValue(), x2)

    def getInterval(self):
        """ Returns x-interval of marker """
        return self.interval

    def draw(self, painter: QPainter, xMap: QwtScaleMap, yMap: QwtScaleMap, canvasRect: QRectF):
        """ Draws the marker onto the chart
        """
        x1 = round(xMap.transform(self.interval.minValue()))
        x2 = round(xMap.transform(self.interval.maxValue()))
        painter.fillRect(QRectF(x1, canvasRect.top(), x2 - x1, canvasRect.height()), self.color )
