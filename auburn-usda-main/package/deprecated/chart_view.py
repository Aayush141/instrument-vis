from PySide6.QtCore import Qt, QEvent
from PySide6.QtCharts import QChartView, QChart

class ChartView(QChartView):
    """ Displays a QChart
    """
    def __init__(self, chart, parent = None):
        super().__init__(chart, parent)
        self.mouseTouching = False 
        self.zFactor = 2
        self.totalZoom = 1

    def viewportEvent(self, event):
        if event.type() == QEvent.Type.TouchBegin:
            self.mouseTouching = True 
            self.chart().setAnimationOptions(QChart.AnimationOption.NoAnimation)
        return super().viewportEvent(event)
    
    def mousePressEvent(self,event):
        if self.mouseTouching:
            return 
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.mouseTouching:
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.mouseTouching = False 
        self.chart().setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        super().mouseReleaseEvent(event)
    
    def keyPressEvent(self, event):
        match event.key():
            case Qt.Key.Key_W:
                self.chart().zoom(self.zFactor)
                self.totalZoom *= self.zFactor 
            case Qt.Key.Key_E:
                self.chart().zoom(1/self.zFactor)
                self.totalZoom /= self.zFactor 



        

