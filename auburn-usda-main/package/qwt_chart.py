import time

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QColor, QPen
from qwt import QwtPlot, QwtPlotCurve, QwtPlotItem, QwtPlotGrid

from package.chart_canvas import ChartCanvas
from package.range_marker import RangeMarker
from package.utils.data_classes import DataPoint


class Chart(QwtPlot):
    """Chart that contains data from EPG device"""

    createAnnotationFromChart = Signal(int, int)
    focusChanged = Signal(int)

    def __init__(self, id, parent=None):
        QwtPlot.__init__(self, parent)
        self.id = id
        self.canvas().deleteLater()
        self.setCanvas(ChartCanvas(plot=self))
        self.setMinimumHeight(100)
        self.setAutoFillBackground(True)
        self.setStyleSheet("ChartCanvas   {background-color:white}")

        # Set up axes
        self.enableAxis(QwtPlot.yLeft, "Voltage (V)")
        self.enableAxis(QwtPlot.xBottom, "Time (s)")
        self.setAxisAutoScale(QwtPlot.xBottom, True)
        self.setAxisAutoScale(QwtPlot.yLeft, True)
        self.setAxisMaxMajor(self.yLeft, 10)
        self.setAxisMaxMajor(self.xBottom, 10)
        QwtPlotGrid.make(self, color=QColor(211, 211, 211, 255), width=0, style=Qt.PenStyle.DotLine)

        self.curve = QwtPlotCurve()
        self.curve.attach(self)

        self.canvas().mouseButtonPressed.connect(self.pointSelected)

        # Accepts keyboard focus by tabbing and clicking
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        # Data Storage
        self.times = []
        self.voltages = []
        self.timeSets = []
        self.voltageSets = []

        # Viewing Axes
        self.viewMin = 0
        self.viewMax = 30
        self.absMin = 0
        self.absMax = 0
        self.total_zoom = 1
        self.zoomFactor = 1
        self.xRange = 30
        self.yMin = -2
        self.yMax = 8
        self.setAxisScale(QwtPlot.xBottom, 0, self.xRange)

        self.isPaused = False
        self.pauseMarker = None
        # Default Sampling Rate
        self.samplesPerSecond = 100
        self.replot()

    def focusInEvent(self, event):
        """ When a chart is focused on, emit its id """
        super().focusInEvent(event)
        self.focusChanged.emit(self.id)

    @Slot(float, float)
    def pointSelected(self, x, y):
        """ When point on chart is selected, print out coordinates 
            TODO: placeholder function for checking what point on waveform
            was clicked on by mouse
        """
        print(x, y)

    def keyPressEvent(self, event) -> None:
        """Takes in a key event, retaining the functionality of
        the Qt function of the same name. Based on the key, it enacts a
        certain action affecting the charts being displayed.
        :param event: a event that is a QKeyEvent which represents if
                a key was pressed
        """
        super().keyPressEvent(event)
        match event.key():
            case Qt.Key.Key_Minus:
                print("Zooming in")
                self.zoomX(2)
            case Qt.Key.Key_Equal:
                print("Zooming out")
                self.zoomX(0.5)
            case Qt.Key.Key_A:
                print("Scrolling to left by 1 unit")
                self.scroll(-1, 0)
            case Qt.Key.Key_Left:
                print("Scrolling to left by 2 units")
                self.scroll(-2, 0)
            case Qt.Key.Key_S:
                print("Scrolling to right by 1 unit")
                self.scroll(1,0)
            case Qt.Key.Key_Right:
                print("Scrolling to right by 2 units")
                self.scroll(2, 0)
            case Qt.Key.Key_R:
                print("Resetting the view")
                self.resetView()
            case Qt.Key.Key_W:
                print("Showing whole view")
                self.maxView()
            case Qt.Key.Key_Up:
                self.scroll(1, 1)
                print("Scrolling up by 1 unit")
            case Qt.Key.Key_Down:
                self.scroll(-1, 1)
                print("Scrolling down by 1 unit")
            case _:
                pass

    def displayImportedData(self, data: list[DataPoint]):
        """Displays data from an imported EPG file on chart
        :param data: List of DataPoints
        """

        for point in data:
            self.times.append(point.time)
            self.voltages.append(point.voltage)
            if point.voltage >= self.yMax:
                self.yMax = point.voltage
            elif point.voltage <= self.yMin:
                self.yMin = point.voltage

        self.curve.setData(self.times, self.voltages)
        self.curve.attach(self)

        self.absMin = self.times[0]  # Finds the range of the data
        self.absMax = self.times[-1]

        if len(data) > 4000:  # Ensures that only =<2000 points are plotted
            self.viewMin = self.absMin
            self.viewMax = self.times[3999]
            self.setAxisScale(self.xBottom, self.viewMin, self.viewMax)
        else:  # Plots all points if data is 2000 pts or less
            self.viewMin = self.absMin
            self.viewMax = self.absMax
            self.setAxisAutoScale(self.xBottom, True)

        self.setAxisAutoScale(self.yLeft, True)

        # print(f'Current Range: {self.viewMin} to {self.viewMax}')
        # print(f'Total Range: {self.absMin} to {self.absMax}')

    def addDataPoint(self, point: DataPoint):
        """Adds a new data point to a pre-existing chart and updates accordingly
        :param point: DataPoint retrieved from live serial data
        """
        self.times.append(point.time)
        self.voltages.append(point.voltage)
        print("Plotting...")
        self.curve.setData(self.times, self.voltages)
        self.curve.attach(self)
        self.setAxisAutoScale(QwtPlot.xBottom, True)
        # self.setAxisAutoScale(QwtPlot.yLeft, False)
        self.replot()

    @Slot(DataPoint)
    def addDataPoints(self, points: list[DataPoint]):
        """Adds a new data point to a pre-existing chart and updates accordingly
        :param points: list of DataPoints retrieved from live serial data
        """

        # yChanged = False
        # xChanged = False
        for point in points:
            self.times.append(point.time)
            self.voltages.append(point.voltage)
            if self.yMax <= point.voltage:
                self.yMax = point.voltage
            elif self.yMin >= point.voltage:
                self.yMin = point.voltage
        xAxis = self.axisScaleDiv(QwtPlot.xBottom)
        self.absMax = points[-1].time + self.xRange
        if points[-1].time > xAxis.upperBound():
            self.scroll(9, 0)

        self.curve.setData(self.times, self.voltages)


        if self.isPaused:
            if self.pauseMarker is None:
                self.pauseMarker = RangeMarker(QColor(255, 140, 0, 50))
                self.pauseMarker.setInterval(points[-1].time, points[-1].time)
                self.pauseMarker.attach(self)
            self.pauseMarker.setX2(points[-1].time)

        self.replot()

    def savePausedRecording(
        self, savePaused: bool, buffer: list[DataPoint], timePausedFor
    ):
        currentTime = time.time()

        # Remove orange background in chart that indicates pause
        self.isPaused = False
        self.pauseMarker.detach()
        self.pauseMarker = None

        firstPoint = buffer[0]
        if savePaused:
            self.curve.setPen(QPen(Qt.GlobalColor.black))
        else:
            # Clear paused portion of graph
            self.curve.detach()  # is this needed
            self.replot()
            self.resetCurve(firstPoint.time, firstPoint.voltage)

        self.addDataPoints(buffer)

    def resetCurve(self, lastTime: float, lastVoltage: float):
        """Clears current curve from graph and creates a new one"""
        # Take last point of previous curve to make old curve and
        # new curve "connected"
        self.times = [lastTime]
        self.voltages = [lastVoltage]
        self.curve = QwtPlotCurve()
        self.curve.setData(self.times, self.voltages)
        self.curve.setPen(QPen(Qt.GlobalColor.black))
        self.curve.attach(self)

    def zoomX(self, x):
        """Zooms the chart view by value x in the X axis.
            Values between [0,1] zooms out and values >1.0
            zoom in by said amount. Values 0 and 1 do nothing
            and the view remains the same.
        :param x : a float scalar to zoom by
        """
        time_diff = self.viewMax - self.viewMin
        new_scale_diff = round(time_diff / x * 0.5, 3)
        self.total_zoom *= x

        if x > 1:
            self.viewMin += new_scale_diff
            self.viewMax -= new_scale_diff
        elif x < 1 and x > 0:
            self.viewMin -= new_scale_diff
            self.viewMax += new_scale_diff
        else:
            pass

        self.setAxisScale(self.xBottom, self.viewMin, self.viewMax)
        self.replot()

    def zoom(self):
        """Zooms the chart by the native variable zoom
        which outside classes have access to.
        """
        self.zoomX(self.zoomFactor)

    def resetView(self):
        """Resets the viewing scale to the inital range prior
        to any zoom changes
        """
        print("Resetting the view...")
        if len(self.times) > 4000:
            self.zoomFactor = 1
            self.viewMin = self.absMin
            self.viewMax = self.times[3999]
        else:
            self.viewMin = self.absMin
            self.viewMax = self.absMax

        self.setAxisScale(self.xBottom, self.viewMin, self.viewMax)
        self.replot()

    def changeZoomScalar(self, x: float):
        """Changes the value by which zoomX() zooms in by
        :param x : the new zoom scale value to call zoomX by
        """
        self.zoomFactor = x

    def scroll(self, dir: int, axis: int):
        """Shifts the axis range by a 1/10th of the total viewing range.
            Absolute values greater than 1 shift however many 1/10ths of
            the range over. Negative values shift left while positive
            values shift right. A dir of 0 doesn't shift.
        :param dir : an int value determining how many sections to shift
                    and what direction
        """
        if axis == 0:
            viewMax = self.viewMax
            viewMin = self.viewMin
        elif axis == 1:
            viewMax = self.yMax
            viewMin = self.yMin
        else:
            print('Error 1: Given integer other than 0 or 1')


        time_diff = viewMax - viewMin
        step = time_diff / 10
        viewMin += step * dir
        viewMax += step * dir

        if axis == 0:
            if viewMin < self.absMin:
                range_diff = self.absMin - viewMin
                viewMin = self.absMin
                viewMax += range_diff
            elif viewMax > self.absMax:
                range_diff = viewMax - self.absMax
                viewMax = self.absMax
                viewMin -= range_diff
            
            self.viewMin = viewMin
            self.viewMax = viewMax
            self.setAxisScale(self.xBottom, self.viewMin, self.viewMax)
        elif axis == 1:
            self.yMin = viewMin
            self.yMax = viewMax
            self.setAxisScale(self.yLeft, self.yMin, self.yMax)
        else: 
            print("Bruh")
        self.replot()

    def retitle(self, name: str):
        """Changes the title of the chart
        :param name : the new title to be given to the chart
        """
        self.setTitle(name)

    def maxView(self):
        self.viewMin = self.absMin
        self.viewMax = self.absMax
        self.setAxisScale(self.xBottom, self.viewMin, self.viewMax)
        self.replot()

    def splithelper(self, voltages, times, decimation_list):
        filtered_values = [[]] * len(decimation_list)
        filtered_times = [[]] * len(decimation_list)

        for i in range(len(voltages)):
            for n in range(len(decimation_list)):
                if i % decimation_list[n] == 0:
                    filtered_values[n].append(voltages[i])
                    filtered_times[n].append(times[i])

        return filtered_values, filtered_times

    def point_relative_change_test_func(self):
        diffs = [0]
        variances = [0]

        for i in range(1, len(self.voltages)):
            diff_before = self.voltages[i] - self.voltages[i - 1]
            variances.append(diff_before**2)
            diffs.append(diff_before)

        var_avg = sum(variances) / len(variances)
        assert len(diffs) == len(self.voltages) == len(self.times) == len(variances)

        filtered_data = [self.voltages[0]]
        filtered_times = [self.times[0]]

        for i in range(1, len(diffs)):
            if variances[i] > var_avg / 6:
                filtered_data.append(self.voltages[i])
                filtered_times.append(self.times[i])

        filtered_data = [x + 30 for x in filtered_data]

        return filtered_data, filtered_times

    def initialize_subgraphs(self):
        if self.voltages == [] or self.times == []:
            print("Insufficient data for initialization")

        filter_values = [2, 3, 4]
        residuals_data, residuals_times = self.point_relative_change_test_func()
        decimated_vals_lsts, decimated_times_lsts = self.splithelper(
            self.voltages, self.times, filter_values
        )

        self.voltageSets = decimated_vals_lsts.append(residuals_data)
        self.timeSets = decimated_times_lsts.append(residuals_times)

        pass

    def clearChart(self):
        """Erase all curves and markers from the chart"""
        self.detachItems(QwtPlotItem.Rtti_PlotCurve)
        self.detachItems(QwtPlotItem.Rtti_PlotMarker)

        self.curve = QwtPlotCurve()
        self.curve.attach(self)

        self.times = []
        self.voltages = []
        self.timeSets = []
        self.voltageSets = []
        self.curve.setData(self.times, self.voltages)
        self.xRange = 30
        self.xMin = 0
        self.xMax = self.xRange
        self.setAxisScale(QwtPlot.xBottom, self.xMin, self.xMax)

        self.yMin = -10
        self.yMax = 10


    def increaseYAxis(self, range_increase : float):
        
        self.yMax += range_increase
        self.yMin -= range_increase

        self.setAxisScale(QwtPlot.yLeft, self.yMin, self.yMax)
        self.replot()
    
