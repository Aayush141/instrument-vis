from qwt import QwtScaleMap
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import QRectF, QPointF

from package.utils.enums import AnnotationType
from package.range_marker import RangeMarker
class AnnotationMarker(RangeMarker):
    """ Creates a colored background on a QwtPlot for some x-interval """
    def __init__(self, color):
        super().__init__(color)
        self.setZ(10)
        self.type = None 

    def setType(self, annotationType:AnnotationType):
        self.type = annotationType 

    def setText(self, text):
        self.text = text 

    def draw(self, painter: QPainter, xMap: QwtScaleMap, yMap: QwtScaleMap, canvasRect: QRectF):
        borderSize = 10
        padding = 5
        x1 = round(xMap.transform(self.interval.minValue()))
        x2 = round(xMap.transform(self.interval.maxValue()))
        painter.fillRect(QRectF(x1, canvasRect.top(), x2 - x1, canvasRect.height()), self.color)

        # Draw the borders of the annotation
        if self.type == AnnotationType.DURATION:
            painter.fillRect(QRectF(x2 - borderSize, canvasRect.top(), borderSize, canvasRect.height()), self.color)
            painter.fillRect(QRectF(x1, canvasRect.top(), borderSize, canvasRect.height()), self.color)
        else:
            painter.fillRect(QRectF(x1, canvasRect.top(), borderSize, canvasRect.height()), self.color)

        # Draw annotation text in black
        pos = QPointF(x1 + borderSize + padding, canvasRect.height() // 2)
        painter.setPen(QPen(QColor("black"), 3))
        painter.drawText(pos, self.text)
    

