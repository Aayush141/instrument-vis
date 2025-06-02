import logging
import os
import time

import pandas as pd
from PySide6.QtCore import QObject, Qt, Signal, Slot
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtWidgets import QMessageBox, QProgressDialog

from package.utils.data_classes import Annotation, DataPoint
from package.utils.enums import AnnotationType
from package.utils.utils import formatEpochTimeToClockTime, formatEpochTimeToDuration


class SerialData(QObject):
    """Reads live serial data from EPG device"""

    ready = Signal()
    progress = Signal(DataPoint)
    finished = Signal()
    processed = Signal(str)  # filenames
    resumed = Signal(
        bool, list, float
    )  # Save recording?, buffer, pause duration
    paused = Signal()
    startTime = Signal(float)
    addAnnotation = Signal(Annotation)
    addVerticalLine = Signal(float)  # x value, color

    def __init__(self):
        super().__init__()
        self.serialData = None
        self.isPlaying = False
        self.isPaused = False
        self.file = None
        self.filename = ""

        self.buffer = []
        self.waitingForUserInput = False

        # Time management
        self.started = 0
        self.ended = 0
        self.sampleRate = 100 # samples per second, Hz
        self.elapsedTime = 0  # in seconds
        self.timeWhenPaused = 0  # in seconds
        self.totalTimePaused = 0

    """ 
    Serial port-related functions
    """

    def setUpSerial(self, deviceManufacturers: list[str] = ["teensy", "arduino"]):
        """Scans all available serial ports and selects the EPG monitor
        :param deviceManufacturers: list of names that fit the EPG monitor
        """
        logging.info("Setting up serial...")
        ports = QSerialPortInfo.availablePorts()
        candidateDevices = []
        for port in ports:
            portName = port.portName().lower()
            # TODO: identify better identification methods
            # if deviceName in port.manufacturer().lower() and ("usb" in portName or "ttyacm0" in portName):
            candidateDevices.append(port)
        logging.info("Available ports: " + str([(port.portName(), port.manufacturer()) for port in candidateDevices]))
        portName = ""
        for port in candidateDevices:
            if port.manufacturer() == "Teensyduino" or port.manufacturer() == "Microsoft":
                logging.info("Port successfully located, Port: "+ port.portName()+", Manufacturer: "
                            + port.manufacturer()+", Description: "+port.description()+".")
                portName = port.portName()
                break

        if portName == "":
            logging.error("Port could not be found")
            self.finished.emit()
            return -1

        # Set up serial port for reading
        self.serial = QSerialPort()
        self.serial.setPortName(portName)
        self.serial.setBaudRate(
            QSerialPort.BaudRate.Baud9600, QSerialPort.Direction.Input
        )

        # Wait for EPG to be ready before streaming data
        if (not self.serial.open(QSerialPort.OpenModeFlag.ReadWrite)):
                print("Unable to open serial port")
                logging.error("Unable to open serial port.")
                return 
        
        # Wait for response from EPG
        self.serial.readyRead.connect(lambda message = "INIT":self.waitForMessageFromEPG(message), Qt.ConnectionType.UniqueConnection)

        # To test without dealing with EPG setup, comment out everything after
        # the line that says wait for EPG to be ready before streaming data.
        # Also upload code in resources/teensy_code/noInitialization to Teensy

        self.ready.emit()
        self.serial.readyRead.connect(self.readData)

    @Slot(str)
    def waitForMessageFromEPG(self, message: str):
        """Waits until serial data matching specific message can be read.
        param message: message that should be waited for before proceeding
        to next step of initialization

        :param message: message that should be waited for
        """
        while self.serial.canReadLine():
            data = str(self.serial.readLine().data(), "utf-8").strip()
            label = data.split(",")[0]
            if label != message:
                return

            match label:
                case "INIT":
                    logging.info("INIT message received  - teensy initialization is complete.")
                    logging.info("Sending BEGIN message...")
                    self.serial.readyRead.disconnect()
                    self.serial.readyRead.connect(
                        lambda message="BEGIN": self.waitForMessageFromEPG(message)
                    )
                    self.serial.flush()
                    self.serial.readAll()
                    self.serial.write(bytes(f"BEGIN,{self.sampleRate}\n".encode()))
                    break
                case "BEGIN":
                    logging.info("BEGIN message received - teensy is ready to read parameters.")
                    logging.info("Sending default parameters, Ri = 100000, Gain = 0, Bias = 0, Freq = 100, Amp = 0.")
                    self.serial.readyRead.disconnect()
                    self.serial.readyRead.connect(
                        lambda message="PARAM": self.waitForMessageFromEPG(message)
                    )
                    # PARAM, channel #, input resistance, amplifier gain, DC bias, excitation frequency, excitation amplitude
                    self.serial.write(bytes("PARAM,1,100000,0,1,1000,0\n".encode()))
                    break
                case "PARAM":
                    logging.info("Default parameter values are set, ready to record.")
                    self.serial.readyRead.disconnect()
                    self.serial.readyRead.connect(
                        self.readData, Qt.ConnectionType.UniqueConnection
                    )
                    self.serial.close()
                    self.ready.emit()
                    break

    def startReadingData(self):
        """Opens serial port and reads data when available"""

        if self.isPlaying:
            return
        
        if self.started == 0:
            self.started = time.time()
            self.startTime.emit(self.started)
            if not self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
                logging.error("Unable to open serial port.")

        # If resuming from a paused recording
        if self.isPaused:
            # Add amount of time that the recording was paused
            timePausedFor = time.time() - self.timeWhenPaused
            self.file.write(f"{self.elapsedTime},RESUME,{timePausedFor:.4f}\n")
            self.promptSavePaused(timePausedFor)

        self.isPlaying = True
        self.isPaused = False

    @Slot()
    def readData(self):
        """Given output in the form of 'O, pre-rect voltage, post-rect voltage',
        displays on visualizer and saves to file
        :param data: bytes representing voltage data
        """

        while self.serial.canReadLine():
            data = str(self.serial.readLine(), "utf-8").strip().split(",")
            label = data[0]
            if label == "O":
                self.elapsedTime = round(
                    time.time() - self.totalTimePaused - self.started, 4
                )
                voltage = data[1]
                channel = 0 # Placeholder value
                point = DataPoint(self.elapsedTime, voltage, channel)
                row = f"{point.time:.4f},DATA,{point.voltage:.4f},{channel}\n"
                # If user is deciding where to save paused data or not
                # store incoming data points into buffer
                if self.waitingForUserInput:
                    self.buffer.append(point)
                else:
                    self.progress.emit([point])
                self.file.write(row)
            elif label == "PARAM": # The Teensy writes back if it reads a parameter change request
                logging.info("Change in parameters registered by Teensy, " + data)
            else:
                print("Error in parsing")
                logging.error("Unable to parse the received data, " + data)

    def pauseData(self):
        """Pauses serial data acquisition"""
        if self.isPaused:
            return
        self.paused.emit()

        elapsedTime = self.elapsedTime
        self.timeWhenPaused = time.time()

        logging.info("Recording is paused.")

        self.file.write(f"{elapsedTime:.4f},PAUSE\n")
        self.saveFile()

        self.isPaused = True
        self.isPlaying = False

    def stopData(self):
        """Stops serial data acquisition. The next time recording is started,
        it will start as a new file.
        """
        self.ended = time.time()
        if self.isPaused:
            # If recording is paused when user ends the session,
            # ask user whether they want to keep the paused portion or not
            timePausedFor = self.ended - self.timeWhenPaused
            self.file.write(f"{self.elapsedTime},RESUME,{timePausedFor:.4f}\n")
            self.promptSavePaused(timePausedFor)

        totalTime = self.elapsedTime + self.totalTimePaused
        #print("Stopping serial communication and closing file...")
        logging.info("Recording has stopped. Saving recording...")
        self.finished.emit()
        text = f"{self.elapsedTime:.4f},END,Total elapsed time in hh:mm:ss: {formatEpochTimeToDuration(self.elapsedTime)}. Total recording time including time paused: {formatEpochTimeToDuration(totalTime)}. Computer clock says it has been {formatEpochTimeToDuration(self.ended - self.started)}\n"

        self.file.write(text)

        self.saveFile()
        self.closeFile()
        self.serial.close()

        # Reset time
        self.elapsedTime = 0
        self.timeWhenPaused = 0
        self.totalTimePaused = 0
        self.started = 0
        self.ended = 0
        self.processData()

    def processData(self):
        """Once user ends recording, process data in output csv such that
        timing is adjusted in accordance to what paused sections were preserved or not"""
        # Popup progress dialog box
        print("Processing file...")
        progressDialog = QProgressDialog(
            "Processing file...", "Delete recording", 0, 10
        )
        progressDialog.setWindowModality(Qt.WindowModality.WindowModal)
        df = pd.read_csv(
            self.filename, names=["timestamp", "label", "value1", "value2", "value3"]
        )
        pauses = df[df["label"] == "PAUSE"].index.tolist()
        resumes = df[df["label"] == "RESUME"].index.tolist()
        saves = df[df["label"] == "SAVE"].index.tolist()
        progressDialog.setMaximum(len(pauses) + 1)
        for i in range(len(pauses)):
            save = df.loc[saves[i]]["value1"]
            if save == "F":
                timePausedFor = float(df.at[resumes[i], "value1"])
                df.loc[resumes[i] + 1 : saves[i], "timestamp"] -= timePausedFor
                df.drop(df.loc[pauses[i] : (resumes[i])].index, inplace=True)
                df.drop(saves[i], inplace=True)
            else:
                df.drop([pauses[i], resumes[i], saves[i]], inplace=True)
            progressDialog.setValue(i)

        # change data to fit specifications

        df["value2"] = df["value2"].astype("Int64")
        df = df.drop("label", axis=1)
        df = df.iloc[:-1]  # Drop last row, TEMP
        df.timestamp.round(4)
        outputFile = os.path.splitext(self.filename)[0]
        pd.DataFrame(df).to_csv(outputFile + "_processed.csv", index=False)
        progressDialog.setValue(len(pauses))

        # Prompt user whether they want to view recording in
        # post-acquisition mode
        answer = QMessageBox.question(
            None,
            "Save",
            "Open recording in post-acquisition mode?",
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.processed.emit(outputFile)


    def sendParam(self, param: str):
        """Gets parameters from the EPG GUI and writes them to the serial
        port to update configurations on the hardware side.
        :param param: string representing parameters to change
        """
        isOpen = self.serial.isOpen()
        if not isOpen:
            if not self.serial.open(QSerialPort.OpenModeFlag.ReadWrite):
                print("Couldn't open port")
                logging.error("Serial port is not open, unable to send to parameters.")
                #TODO: report attempted values, and the original value
                return 
        self.serial.write(bytes(param.encode()))
        parts = param.strip().split(',')
        output_vector = [int(float(parts[2])), float(parts[3]), float(parts[4]), int(float(parts[5])), float(parts[6])]
        # PARAM, channel #, input resistance, amplifier gain, DC bias, excitation frequency, excitation amplitude
        logging.info("Updating parameters, Ri: "+str(output_vector[0])+", Gain: "+str(output_vector[1])+", Bias: "+str(output_vector[2])+", Freq: "+str(output_vector[3])
                     +", Amp: "+str(output_vector[4])+".")
        #TODO: ADD UNITS; check for error/confirmation - what are some possible feedback from engineers
        if not isOpen:
            self.serial.close()

    def promptSavePaused(self, timePausedFor):
        """Show message box that asks user whether or not to keep the
        paused portion of the recording or not

        :param timePausedFor: Duration of the paused portion
        """
        self.waitingForUserInput = True
        answer = QMessageBox.question(
            None,
            "Save",
            "Save paused portion of recording?",
            QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )

        clockTime = formatEpochTimeToClockTime(self.timeWhenPaused)
        timeStart = self.timeWhenPaused - self.totalTimePaused - self.started
        text = f"Paused for {timePausedFor} seconds"
        annotationType = AnnotationType.VERTICAL
        duration = timePausedFor

        if answer == QMessageBox.StandardButton.Yes:
            # No annotation to save, save paused portion
            self.file.write(f"{self.elapsedTime},SAVE,T\n")
            self.resumed.emit(True, self.buffer, timePausedFor)
            self.buffer = []
            self.waitingForUserInput = False
            logging.info("Paused portion is saved, and recording is resumed.")
        else:
            # Get elapsed time when recording was paused
            timeStart = self.timeWhenPaused - self.totalTimePaused - self.started
            self.totalTimePaused += timePausedFor

            duration = 0
            self.file.write(f"{self.elapsedTime},SAVE,F\n")
            logging.info("Paused portion is not saved, and recording is resumed.")
            # Edit times of points in buffer to account for paused portion
            # being removed
            buffer = list(
                map(
                    lambda point: DataPoint(
                        point.time - timePausedFor, point.voltage, point.channel
                    ),
                    self.buffer,
                )
            )
            self.resumed.emit(False, buffer, timePausedFor)
            self.buffer = []
            self.waitingForUserInput = False

        # Create autogenerated annotation about pause
        annotation = Annotation(
            timeStart=round(timeStart, 4),
            clockTime=clockTime,
            text=text,
            duration=round(duration, 4),
            annotationType=annotationType,
            autogenerated=True,
        )
        self.addAnnotation.emit(annotation)

    """ 
    File operations
    """

    def createFile(self, name="epgOutput.csv"):
        """Creates a new csv file where data is stored"""
        #print("Saving data in " + name)
        logging.info("Recording starts and will be saved to"+name)
        self.file = open(name, "w")
        self.filename = name

    def saveFile(self):
        """Saves data by flushing out data in memory"""
        self.file.flush()

    def closeFile(self):
        """Closes current file that EPG data is saved to"""
        self.file.close()      
        self.file = None
        logging.info("Recording is saved.")