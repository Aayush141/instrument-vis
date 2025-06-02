from PySide6.QtCore import Slot, Qt, Signal
from PySide6.QtGui import QColor, QPen
from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QInputDialog
)
from qwt import QwtPlot, QwtPlotMarker, QwtPlotItem

from package.annotation_bar import AnnotationBar
from package.qwt_chart import Chart
from package.annotation_marker import AnnotationMarker
from package.utils.data_classes import Annotation, MarkerGroup 
from package.utils.enums import AnnotationType

class ChartView(QWidget):
    chartMouseReleased = Signal(float, float) # xVal, duration
    annotationSelected = Signal(int) # annotation id
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.nestedLayout = QVBoxLayout()
        self.annotationBar = AnnotationBar()

        self.layout.addWidget(self.annotationBar)
        self.annotationBar.setFixedHeight(75)

        self.layout.addLayout(self.nestedLayout)
        self.setLayout(self.layout)
        self.charts = []
        self.channels = []
        self.markers = {}
        
        self.focusedChartIndex = 0

        # Initialize Chart object
        Chart(id=0)
        self.createChart() # Start with an empty chart
        self.syncXAxis(0)
       
        # Align y-axis of annotation bar and charts
        chartWidget = self.charts[0].axisWidget(QwtPlot.yLeft)
        extent = chartWidget.scaleDraw().extent(chartWidget.font())
        self.annotationBar.axisWidget(QwtPlot.yLeft).scaleDraw().setMinimumExtent(
            extent
        )

        self._createConnections()
    
    def _createConnections(self):   
        self.annotationBar.canvas().mouseReleased.connect(self.selectMarker)

    def getCharts(self):
        return self.charts
    
    def getChannels(self):
        return self.channels 

    def getAnnotationBar(self):
        return self.annotationBar
    
    """
    Visualization
    """

    def createChart(self):
        """ Create a new chart and insert it into the layout """
        chart = Chart(id=len(self.charts))        
        chart.canvas().mouseReleased.connect(
            lambda xVal, duration: self.chartMouseReleased.emit(xVal, duration)
        )
        # Sync x-axis of annotation bar according to x-axis of chart
        # Default syncs to first chart
        chart.axisWidget(QwtPlot.xBottom).scaleDivChanged.connect(
            lambda: self.syncXAxis(chart.id)
        )     
        chart.focusChanged.connect(self.focusChanged)
        self.charts.append(chart)
        self.nestedLayout.addWidget(chart)

    def syncXAxis(self, chartId):
        """Sync the x-axis of the annotation bar with the currently focused chart."""
        if chartId == self.focusedChartIndex:
            xAxis = self.charts[chartId].axisScaleDiv(QwtPlot.xBottom)
            self.annotationBar.syncXAxis(xAxis.lowerBound(), xAxis.upperBound())

    def focusChanged(self, chartId: int):
        """ If chart focus has changed, update annotation bar to only show
            annotations from currently selected chart """
        # Display annotations corresponding to chart that is currently selected
        if self.channels == [] or self.focusedChartIndex == chartId:
            return 
        self.focusedChartIndex = chartId 
        selectedChannel = self.getChannels()[chartId]
        self.syncXAxis(chartId)
        for channel in self.markers:
            if channel == selectedChannel:
                for markerGroup in self.markers[channel]:
                    markerGroup.marker.show()
                    markerGroup.leftBorder.show()
                    if markerGroup.rightBorder:
                        markerGroup.rightBorder.show()
            else:
                for markerGroup in self.markers[channel]:
                    markerGroup.marker.hide()
                    markerGroup.leftBorder.hide()
                    if markerGroup.rightBorder:
                        markerGroup.rightBorder.hide()
        for chart in self.charts:
            print(chart.id, chartId)
            if chart.id == chartId:
                chart.title().setColor(QColor("red"))
            else:
                chart.title().setColor(QColor("black"))
            chart.replot()
        self.annotationBar.replot()


    def changeChartZoom(self):
        """Creates a dialog box that looks for a double input and
        returns that, setting the new zoom scaling value to user
        input for all charts being displayed.
        """
        value, ok = QInputDialog.getDouble(
            self, "Zoom Scale", "Scalar", 1, 0, 10, 2, Qt.WindowFlags(), 0.1
        )

        if ok:
            for chart in self.charts:
                chart.changeZoomScalar(value)

    def reset(self):
        """Reset the view by clearing data and UI components
        in chart layout and the annotation bar"""
        self.channels = []
        self.splitData = None
        self.charts = []
        self.centerWidget = QWidget()
        
        # Delete all widgets in chart layout
        while True:
            item = self.nestedLayout.layout().takeAt(0)
            if item is None:
                break
            item.widget().deleteLater()
            item = None 
        self.nestedLayout.layout().deleteLater()
        self.nestedLayout.deleteLater()
        self.nestedLayout = QVBoxLayout()
        self.layout.addLayout(self.nestedLayout)

        # Remove markers from annotation bar
        self.markers = {}
        self.annotationBar.detachItems(QwtPlotItem.Rtti_PlotMarker)
        self.annotationBar.replot()


    """
    Annotations
    """
    @Slot(float)
    def selectMarker(self, xValue: float):
        """ Select marker in annotation bar and bring up full view in annotation list """
        selectedChannel = self.getChannels()[self.focusedChartIndex]
        for markerGroup in self.markers[selectedChannel]:
            if markerGroup.marker.getInterval().contains(xValue):
                print("Marker found")
                self.annotationSelected.emit(markerGroup.id)
                return 
        print("No marker found") 
    

    @Slot(Annotation)
    def addMarker(self, annotation: Annotation):
        """ Add annotation marker to annotation bar"""
        marker = AnnotationMarker(QColor(170, 255, 0,50))
        marker.setText(annotation.text)
        markerGroup = MarkerGroup(id = annotation.id, marker = marker, leftBorder=self.addVerticalLineMarker(annotation.timeStart, QColor(170, 255, 0,100), annotation.channel))

        if annotation.duration == 0:  # Point marker 
            marker.setType(AnnotationType.POINT)
            marker.setInterval(annotation.timeStart, annotation.timeStart + 10)
        else: # Duration marker
            marker.setType(AnnotationType.DURATION)
            marker.setInterval(
                annotation.timeStart, annotation.timeStart + annotation.duration)   
            markerGroup.rightBorder = self.addVerticalLineMarker(annotation.timeStart + annotation.duration, QColor(170, 255, 0,100), annotation.channel)

        # Set text label to be aligned to the top-right of the marker
        marker.attach(self.annotationBar)

        # Divide annotations based on channel
        if annotation.channel not in self.markers:
            self.markers[annotation.channel] = [markerGroup]
        else:
            self.markers[annotation.channel].append(markerGroup)

    @Slot(Annotation)
    def addVerticalLineMarker(self, xValue, color, annotationChannel = 1):
        """Create a vertical line on the chart to show user where the
        recording was paused.
        """
        line = QwtPlotMarker()
        line.setLineStyle(QwtPlotMarker.VLine)
        line.setXValue(xValue)
        line.setLinePen(QPen(color, 5))
        line.attach(self.charts[self.getChannels().index(annotationChannel)])
        return line 

    @Slot()
    def displayPause(self):
        """Pause in recording"""
        self.charts[0].isPaused = True 
        self.charts[0].resetCurve(lastTime=self.charts[0].times[-1], lastVoltage=self.charts[0].voltages[-1])

