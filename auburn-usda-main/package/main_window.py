"""Main window-style application."""

import csv
import logging
import os
import time
from functools import cached_property

import coloredlogs
from coloredlogs import ColoredFormatter
from PySide6.QtCore import QEvent, QObject, Qt, Signal, Slot
from PySide6.QtGui import QAction, QColor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QStyle,
    QToolBar,
)
from qwt import QwtText

from package.add_annotation_window import AddAnnotationWindow
from package.annotation_list import AnnotationList
from package.chart_view import ChartView
from package.epg_control import EPGControl
from package.log_msg import LogMsg
from package.utils.data_classes import Annotation, DataPoint
from package.utils.enums import Mode
from package.utils.file_reader import anaRead, csvRead
from package.utils.serial_reader import SerialData


class LogSignal(QObject):
    signal = Signal(str)

class LogHandler(logging.Handler):
    # this function will only be called once
    @cached_property
    def log(self):
        return LogSignal()

    def emit(self, record):
        message = self.format(record)
        #print(message)
        self.log.signal.emit(message)

class LogSignal(QObject):
    signal = Signal(str)

class LogHandler(logging.Handler):
    # this function will only be called once
    @cached_property
    def log(self):
        return LogSignal()

    def emit(self, record):
        message = self.format(record)
        #print(message)
        self.log.signal.emit(message)

class MainWindow(QMainWindow):
    """The main window of the application."""
    class CustomFormatter(ColoredFormatter):
            def __init__(self, main_window, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.main_window = main_window

            def format(self, record):
                COLORS = {
                    'DEBUG': '\033[94m',  # Blue
                    'INFO': '\033[92m',   # Green
                    'WARNING': '\033[93m',  # Yellow
                    'ERROR': '\033[91m',   # Red
                }
                RESET_SEQ = '\033[0m'

                asctime = self.formatTime(record, self.datefmt)

                elapsed_time = "N/A"
                if self.main_window.serialData is not None:
                    elapsed_time = "{:.2f}s".format(float(self.main_window.serialData.elapsedTime))
                # levelname = COLORS.get(record.levelname, '\033[37m') + record.levelname + RESET_SEQ
                levelname = record.levelname

                return f"{asctime} {elapsed_time} {levelname}: {record.getMessage()}"

    def __init__(self):
        """
        Initialize the main window, setting up the GUI structure including charts,
        menus, toolbars, and status bar.
        """
        super().__init__(parent=None)
        self.setWindowTitle("EPG Signal Visualizer")
        self.createChartView()
        self._createActions()
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()

        # EPG Recording Variables
        self.serialData = None
        self.annotationWindow = AddAnnotationWindow()
        self.annotationList = AnnotationList()
        self.currentDataPoint = None
        self.epgControl = EPGControl()

        self.logMsg = LogMsg()
        self.annotationWindow.annotationAdded.connect(self.chartView.addMarker)
        self.annotationWindow.annotationAdded.connect(
            self.annotationList.insertAnnotation
        )
        self.chartView.chartMouseReleased.connect(self.showAddAnnotationWindow)
        self.chartView.annotationSelected.connect(self.viewAnnotation)
        self.splitData = None
        self.initializeLogFile()
        self.setupLogging()
    
        custom_formatter = self.CustomFormatter(self, '%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        self.log_handler = LogHandler()
        self.log_handler.setFormatter(custom_formatter)
        logging.basicConfig(filename='epgOutput.log', encoding='utf-8', level=logging.DEBUG, format = custom_formatter._fmt, datefmt='%m/%d/%Y %I:%M:%S %p')
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.DEBUG)
        self.log_handler.log.signal.connect(self.logMsg.update_live_log)

    def setupLogging(self):
            """Setup custom logger for the application."""
            custom_formatter = self.CustomFormatter(self, '%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
            logging.basicConfig(filename='epgOutput.log', encoding='utf-8', level=logging.DEBUG,
                                format = custom_formatter._fmt, datefmt='%m/%d/%Y %I:%M:%S %p')

    def initializeLogFile(self):
        """
        Ensure the log file exists and initialize it if it does not.
        """
        log_file = 'epgOutput.log'
        if not os.path.exists(log_file):
            with open(log_file, 'w') as file:
                file.write("System Time   Recording Time   Log Level   Log Message\n")

        self.mode = None  # Can be in data acquisition mode or post acquisition mode


    """
    Setup of actions, menu, and toolbar 
    """

    def _createActions(self):
        """Creates actions that will be assigned to the menu bar or tool bar later on"""
        # Import file
        self.importAction = QAction("&Import File", self)
        self.importAction.triggered.connect(self.importFile)

        # Import annotations
        self.importAnnotationsAction = QAction("&Import Annotations", self)
        self.importAnnotationsAction.triggered.connect(self.importAnnotations)

        # View annotations
        self.viewAnnotationsAction = QAction("&View annotations", self)
        self.viewAnnotationsAction.triggered.connect(self.viewAnnotations)

        # Set up EPG monitor
        self.setUpEPGAction = QAction("&Set up EPG monitor", self)
        setUpEPGIcon = self.style().standardIcon(getattr(QStyle, "SP_DriveHDIcon"))
        self.setUpEPGAction.setIcon(setUpEPGIcon)
        self.setUpEPGAction.triggered.connect(self.setUpEPG)

        # Start recording serial data
        self.recordSerialDataAction = QAction("&Record serial data", self)
        recordIcon = self.style().standardIcon(getattr(QStyle, "SP_MediaPlay"))
        self.recordSerialDataAction.setIcon(recordIcon)
        self.recordSerialDataAction.triggered.connect(self.recordSerialData)
        self.recordSerialDataAction.setEnabled(False)

        # Pause recording serial data
        self.pauseSerialDataAction = QAction("&Pause recording serial data", self)
        pauseIcon = self.style().standardIcon(getattr(QStyle, "SP_MediaPause"))
        self.pauseSerialDataAction.setIcon(pauseIcon)
        self.pauseSerialDataAction.triggered.connect(self.pauseSerialData)
        self.pauseSerialDataAction.setEnabled(False)

        # Stop recording serial data
        self.stopSerialDataAction = QAction("&Pause recording serial data", self)
        stopIcon = self.style().standardIcon(getattr(QStyle, "SP_MediaStop"))
        self.stopSerialDataAction.setIcon(stopIcon)
        self.stopSerialDataAction.triggered.connect(self.stopSerialData)
        self.stopSerialDataAction.setEnabled(False)

        # Add annotation marker to chart
        self.addAnnotationAction = QAction("&Add Annotation", self)
        self.addAnnotationAction.triggered.connect(self.showAddAnnotationWindow)

        # Open EPG control window
        self.epgControlAction = QAction("&Open EPG Control", self)
        self.epgControlAction.triggered.connect(self.showEpgControl)

        # Show Log
        self.showLogAction = QAction("&Show Log Messages", self)
        self.showLogAction.triggered.connect(self.showLogMsg)


        # Show Log
        self.showLogAction = QAction("&Show Log Messages", self)
        self.showLogAction.triggered.connect(self.showLogMsg)


        # Manually change the value at which to zoom by
        self.changeZoomAction = QAction("&Change zoom scale", self)
        self.changeZoomAction.triggered.connect(self.chartView.changeChartZoom)

    def _createMenu(self):
        """
        Create menu bar with various actions for file operations and settings.
        Connect actions with respective menu items
        """
        menu = self.menuBar().addMenu("&File")
        menu.addAction(self.importAction)
        menu.addAction(self.importAnnotationsAction)

        menu = self.menuBar().addMenu("&View")
        menu.addAction(self.changeZoomAction)

        menu.addAction(self.viewAnnotationsAction)

    def _createToolBar(self):
        """Create the tool bar and connect actions with each tool item"""
        tools = QToolBar()
        self.addToolBar(tools)

        tools.addAction(self.setUpEPGAction)
        tools.addAction(self.recordSerialDataAction)
        tools.addAction(self.pauseSerialDataAction)
        tools.addAction(self.stopSerialDataAction)

        tools.addAction(self.addAnnotationAction)
        tools.addAction(self.epgControlAction)
        tools.addAction(self.showLogAction)

    def _createStatusBar(self):
        """Create status bar that shows important information"""
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)

        # Show how long you've been recording for
        self.timer = QLabel("0s")
        self.statusBar.addWidget(self.timer)

    def createSerialDataConnections(self):
        """After serial port is set up, connect all signals to slots
        Qt.ConnectionType.UniqueConnection ensures that there are not
        multiples of the same connections set up.
        """

        self.serialData.ready.connect(
            self.serialReady, Qt.ConnectionType.UniqueConnection
        )
        self.epgControl.update.connect(
            self.serialData.sendParam, Qt.ConnectionType.UniqueConnection
        )
        self.serialData.startTime.connect(self.assignStartTime)

        self.serialData.progress.connect(
            self.chartView.getCharts()[0].addDataPoints,
            Qt.ConnectionType.UniqueConnection,
        )
        self.serialData.progress.connect(
            self.updateCurrentDataPoint, Qt.ConnectionType.UniqueConnection
        )
        self.serialData.finished.connect(
            self.annotationList.reset()
        )
        self.serialData.finished.connect(
            lambda: self.annotationList.exportAnnotationsGivenFileName(self.serialData.filename[:-4] + "_annotations.csv")
        )
        self.serialData.resumed.connect(
            self.resumeSerialData, Qt.ConnectionType.UniqueConnection
        )
        self.serialData.paused.connect(
            self.chartView.displayPause, Qt.ConnectionType.UniqueConnection
        )
        self.serialData.processed.connect(
            lambda filename: self.importFileGivenName([filename + "_processed.csv"]), Qt.ConnectionType.UniqueConnection
        )
        self.serialData.processed.connect(
            lambda filename: self.importAnnotationsGivenName([filename+ "_annotations.csv"]), Qt.ConnectionType.UniqueConnection
        )
        self.serialData.addAnnotation.connect(
            self.chartView.addMarker, Qt.ConnectionType.UniqueConnection
        )

    @Slot(QEvent)
    def closeEvent(self, event):
        """Close all open windows when main window is closed"""
        QApplication.closeAllWindows()

    """ 
    Functions for controlling EPG monitor from toolbar
    """

    @Slot()
    def setUpEPG(self):
        """Scan open serial ports and select EPG monitor"""
        self.serialData = SerialData()
        self.chartView.reset()
        self.chartView.createChart()  # Must create chart first before hooking up connections

        self.createSerialDataConnections()
        self.serialData.setUpSerial()
        self.changeMode(Mode.DATA_ACQUISITION)
        self.chartView.channels = [0]

    @Slot()
    def serialReady(self):
        """When EPG monitor finishes set up, allow user to start recording.
        In addition, open the EPG control window for user to adjust
        EPG monitor values before starting.
        """
        self.recordSerialDataAction.setEnabled(True)
        self.showEpgControl()

    @Slot()
    def recordSerialData(self):
        """Start recording data coming from the EPG device
        using a multi-threaded approach
        """
        # Initialize chart that will show data
        if not self.serialData.isPaused:
            self.chartView.getCharts()[0].clearChart()

            # Open file dialog to choose where to save EPG data, csv format
            filename = QFileDialog.getSaveFileName(
                self,
                "Save File",
                "resources/session_files/epgOutput.csv",
                "Text files (*.csv)",
            )[0]
            if not filename:
                print("No file selected")
                messageBox = QMessageBox(text="No file selected.")
                messageBox.exec()
                return
            if not self.serialData.file:
                self.serialData.createFile(filename)

        self.serialData.startReadingData()
        self.recordSerialDataAction.setEnabled(False)
        self.pauseSerialDataAction.setEnabled(True)
        self.stopSerialDataAction.setEnabled(True)

    @Slot()
    def pauseSerialData(self):
        """When user clicks the pause button, change chart view to paused state"""

        # Dialog box that informs user recording is paused
        self.serialData.pauseData()
        self.recordSerialDataAction.setEnabled(True)
        self.pauseSerialDataAction.setEnabled(False)
        self.stopSerialDataAction.setEnabled(True)
        dlg = QMessageBox(self)
        dlg.setText("Recording paused")
        dlg.show()

    @Slot(bool, list)
    def resumeSerialData(
        self, savePausedData: bool, buffer: list[DataPoint], timePausedFor: float
    ):
        """When user clicks the play button after pausing, update chart
        depending on whether user chose to keep paused portion or not
        """
        self.chartView.getCharts()[0].savePausedRecording(
            savePausedData, buffer, timePausedFor
        )
        self.recordSerialDataAction.setEnabled(False)
        self.pauseSerialDataAction.setEnabled(True)
        self.stopSerialDataAction.setEnabled(True)

    @Slot()
    def stopSerialData(self):
        """When user clicks stop recording, end recording session"""
        self.serialData.stopData()

        self.recordSerialDataAction.setEnabled(True)
        self.pauseSerialDataAction.setEnabled(False)
        self.stopSerialDataAction.setEnabled(False)

    @Slot(float)
    def assignStartTime(self, startTime: float):
        """ Set start time of recording 
            :param startTime: time in seconds according to Unix epoch
        """
        self.startTime = startTime

    @Slot(DataPoint)
    def updateCurrentDataPoint(self, points: list[DataPoint]):
        """Keep track of most recent point sent over serial data
        :param points: list of most recent packet of serial data
        """
        lastPoint = points[-1]
        self.timer.setText(f"{lastPoint.time:.2f}s")
        self.currentDataPoint = lastPoint

    def showLogMsg(self):
        self.logMsg.show()


    """ 
    Functions associated with different actions in menu
    """

    @Slot()
    def importFile(self):
        """Select an EPG file from file directory in csv or ana format"""
        # Open dialog to select file from your file directory
        print("User selecting file...")
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilters(["Text files (*.CSV *.csv *.ANA *.ana)"])
        dialog.selectNameFilter("Text files")

        if dialog.exec():
            fileName = dialog.selectedFiles()
            if not fileName:
                print("File not given or found...")
                return
            self.splitData = None
            self.importFileGivenName(fileName)

    def importFileGivenName(self, filename: str):
        """Import data given a filename and display it on the chart

        :param filename: filename of file to read from
        """
        self.chartView.reset()

        _, fileType = os.path.splitext(filename[0])
        data = None
        print("Reading in data...")
        if fileType.lower() == ".ana":
            data = anaRead(filename[0])
        if fileType.lower() == ".csv":
            data = csvRead(filename[0])

        print("Separating data channels...")
        self.divideData(data)

        # Display data on chart
        print("Displaying data...")
        for i in range(len(self.chartView.getChannels())):
            self.chartView.createChart()
            title = QwtText(f"Channel {self.chartView.getChannels()[i]}  Data ({len(self.splitData[i])})")
            self.chartView.getCharts()[i].retitle(title)
            self.chartView.getCharts()[i].displayImportedData(self.splitData[i])
        self.chartView.syncXAxis(0)
        # Show first graph as selected by displaying red title
        title = self.chartView.getCharts()[0].title().setColor(QColor("red"))
        self.changeMode(Mode.POST_ACQUISITION)

    def changeMode(self, mode: Mode):
        """ Set software mode to data acquisition mode or post acquisition mode """
        if self.mode != mode:
            self.mode = mode
            self.chartView.mode = mode
            for chart in self.chartView.getCharts():
                chart.canvas().mode = mode

    def divideData(self, data: list[DataPoint]):
        """After data has been obtained, the data is then
        split up based on which channel it belongs to. The sets
        of data representing channels are stored 'splitData'.
        The channel order is stored in 'channels'
        """

        for point in data:
            if data is None:
                break
            if self.splitData is None:
                self.splitData = [[point]]
                self.chartView.channels = [point.channel]
                continue
            try:
                index = self.chartView.channels.index(point.channel)
            except ValueError:
                self.splitData += [[point]]
                self.chartView.channels.append(point.channel)
                continue

            self.splitData[index].append(point)

    def importAnnotations(self):
        """Given csv of annotations, import them into the current imported file"""

        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilters(["Text files (*.CSV *.csv)"])
        dialog.selectNameFilter("Text files")

        if dialog.exec():
            fileName = dialog.selectedFiles()
            if not fileName:
                print("File not given or found...")
                return
            self.importAnnotationsGivenName(fileName)

    def importAnnotationsGivenName(self, filename):
        if self.chartView.getCharts()[0] is not None:
            with open(filename[0], mode="r") as file:
                csvFile = csv.reader(file)
                count = 0
                for row in csvFile:
                    if row == []:
                        continue
                    timeStart, duration, text, channel = row
                    clockTime = "0"
                    annotation = Annotation(
                        timeStart, clockTime, text, duration, channel=channel, id = count
                    )
                    self.annotationList.insertAnnotation(annotation)
                    self.chartView.addMarker(annotation)
                    count += 1

    @Slot(int)
    def viewAnnotation(self, annotationId: int):
        """ If you select a marker, then pull up its corresponding annotation
            :param annotationId: id of annotation
        """
        
        for annotation in self.annotationList.annotations:
            if annotation.id == annotationId:
                self.annotationList.viewAnnotation(annotationId)
                break 

    def viewAnnotations(self):
        """Display annotation list widget that displays all annotations"""
        self.annotationList.show()

    def showAddAnnotationWindow(self, timeStart=None, duration=None):
        """Show window for users to create annotations"""
        # If creating annotation from button and NOT mouse click, then fill in
        # times in add annotation window with the current time
        currentTime = time.time()
        clockTime = None
        if timeStart is None:
            point = self.currentDataPoint
            # clockTime = formatEpochTimeToClockTime(
            #     point.time + self.startTime
            # )  # this doesn't work bc you have to subtract paused for as well
            clockTime = "placeholder"
            timeStart = point.time
            duration = 0
        else:
            clockTime = "placeholder"
            # clockTime = formatEpochTimeToClockTime(timeStart + self.startTime)
        self.annotationWindow.timeStartLabel.setText(f"{timeStart:.4f}")
        self.annotationWindow.durationLabel.setText(f"{duration:.4f}")
        self.annotationWindow.clockTimeLabel.setText(clockTime)
        self.annotationWindow.channel = self.chartView.getChannels()[self.chartView.focusedChartIndex]
        self.annotationWindow.show()

    """
    Chart-related functions
    """

    def createChartView(self):
        """Create a chart view which will be populated with a QChart
        that displays readings from the EPG device
        """
        self.chartView = ChartView()
        self.setCentralWidget(self.chartView)
        self.chartView.show()

    """ 
    Misc functions 
    """

    @Slot()
    def showEpgControl(self):
        self.epgControl.show()
