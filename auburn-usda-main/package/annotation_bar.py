from PySide6.QtCore import Signal
from qwt import QwtPlot
from qwt.scale_draw import QwtScaleDraw

from package.utils.data_classes import Annotation 
from package.annotation_bar_canvas import AnnotationBarCanvas

class AnnotationBar(QwtPlot):
    annotationCreated = Signal(Annotation)
    def __init__(self, parent = None):
        QwtPlot.__init__(self, parent)
        self.canvas().lower()
        self.canvas().deleteLater()

        self.setStyleSheet("AnnotationBarCanvas   {background-color:white}")

        self.annotations = []
        self.markers = []
        self.setCanvas(AnnotationBarCanvas(plot=self))

        # Set up axes
        self.enableAxis(QwtPlot.yLeft, "y")
        self.enableAxis(QwtPlot.xBottom, "x")
        self.setAxisAutoScale(QwtPlot.yLeft, False)
        self.setAxisAutoScale(QwtPlot.xBottom, False)
        self.setAxisScale(QwtPlot.yLeft, 0, 10)
        self.axisScaleDraw(QwtPlot.yLeft).enableComponent(QwtScaleDraw.Labels, False)
        self.axisScaleDraw(QwtPlot.yLeft).enableComponent(QwtScaleDraw.Ticks, False)
        self.axisScaleDraw(QwtPlot.xBottom).enableComponent(QwtScaleDraw.Labels, False)
        self.axisScaleDraw(QwtPlot.xBottom).enableComponent(QwtScaleDraw.Ticks, False)

        self.setAutoFillBackground(True)
        self.replot()
        self.show()

    def syncXAxis(self, xMin: float, xMax: float):
        """ Given a lower bound and a upper bound, adjust x-axis of annotation
            bar so that it matches with the corresponding chart 

            :param xMin: lower bound of x-axis 
            :param xMax: upper bound of x-axis
            
        """
        self.setAxisScale(QwtPlot.xBottom, xMin, xMax)
        self.replot()
    
    

