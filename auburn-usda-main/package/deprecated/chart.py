from PySide6.QtCore import Qt, QEvent
from PySide6.QtCharts import QChart
from PySide6.QtCharts import QLineSeries, QChart, QValueAxis
from PySide6.QtCore import *

class Chart(QChart):
    """" Chart that contains data from EPG deviec
    """
    def __init__(self, parent = None, wFlags =  Qt.WindowType.Window):
        super().__init__(QChart.ChartTypeCartesian, parent, wFlags)

        # Member variables
        self.series = QLineSeries()
        self.xRange = 30 # seconds
        self.xMin = 0
        self.xMax = self.xMin + self.xRange 
        self.yMin = float("inf")
        self.yMax = 0
        self.timeBegin = None 

        self.grabGesture(Qt.GestureType.PanGesture)
        self.grabGesture(Qt.GestureType.PinchGesture)

        # Settings for chart
        self.setTitle("Data Display")
        self.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        self.legend().hide()

        self.addSeries(self.series)

        # Set up x and y axes for chart 
        xAxis = QValueAxis()
        self.addAxis(xAxis, Qt.AlignmentFlag.AlignBottom)
        self.series.attachAxis(xAxis)
        xAxis.setTitleText("Time (sec)")

        yAxis = QValueAxis()
        self.addAxis(yAxis, Qt.AlignmentFlag.AlignLeft)
        self.series.attachAxis(yAxis)
        yAxis.setTitleText("Voltage (V)")

    def displayImportedData(self, data):
        """ Displays data from an imported EPG file on chart
        :param data: List of DataPoints
        """
        for point in data:
            self.series.append(QPointF(point.time, point.voltage))

            # Keep track of min and max values to update axes
            self.yMin = min(point.voltage, self.yMin)
            self.yMax = max(point.voltage, self.yMax)

        # Update axes on chart
        self.updateAxes(xMin = data[0].time,  xMax = point.time, yMin = self.yMin, yMax = self.yMax)
    
    def addDataPoint(self, point):
        """ Adds a new data point to a pre-existing chart and updates accordingly
        :param point: DataPoint retrieved from live serial data
        """
        print(point)
        self.series.append(QPointF(point.time, point.voltage))

        # Set beginning of x-axis as the first DataPoint's time
        if not self.timeBegin:
            self.timeBegin = point.time 
            self.xMax = self.timeB

        # Update axes if a point goes out of bounds
        if point.time > self.xMax:
            print("Going out of bounds!")
            self.updateXAxis()
        if point.voltage >= self.yMax or point.voltage <= self.yMin:
            self.yMin = min(point.voltage, self.yMin)
            self.yMax = max(point.voltage, self.yMax)
            self.updateYAxis()

    def updateYAxis(self):
        """ Update the x and y axis upon adding data such that 
            all of data is in display
        """
        self.axisY().setRange(self.yMin, self.yMax)
    
    def updateXAxis(self):
        """ Update the x-axis if DataPoint currently being processed
        is out of range on the axis
        """
        self.xMin = self.xMin + self.xRange 
        self.xMax = self.xMax + self.xRange
        self.axisX().setRange(self.xMin, self.xMax)

    def resetChart(self):
        """ Reset Chart's member variables
        """
        self.series = QLineSeries()
        self.yMin, self.yMax = float('inf'), 0
            
    def viewportEvent(self, event):
        if event.type() == QEvent.Type.TouchBegin:
            self.mouseTouching = True 
            self.setAnimationOptions(QChart.AnimationOption.NoAnimation)
        return super().viewportEvent(event)


