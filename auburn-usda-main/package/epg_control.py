from PySide6.QtCore import Signal
from PySide6.QtWidgets import QMainWindow

from package.ui_python.epg_control_ui import Ui_EPGControl
from PySide6.QtWidgets import QMainWindow
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo
from PySide6.QtCore import Qt, qDebug, QIODevice, Signal

class EPGControl(QMainWindow, Ui_EPGControl):
    update = Signal(str)

    def __init__(self, parent=None):
        """GUI for controlling values of the EPG. Changing values and applying
        them should cause the EPG to register these changes
        """
        super().__init__(parent)
        self.setupUi(self)
        self.defaultValues = [1000.0, 0.0, 0.0, 0.0, 0.0]
        self.channel = 1

        # Group sliders and text inputs into lists for easier management
        self.sliders = [
            self.amplifierGainSlider,
            self.amplifierOffetSlider,
            self.excitationAmplitudeSlider,
        ]
        self.textInputs = [
            self.amplifierGainInput,
            self.amplifierOffsetInput,
            self.excitationAmplitudeInput,
        ]
        self.menuInputs = [self.inputResistanceInput, self.excitationFrequencyInput]

        self.updateCurrentValues()
        # Connect values of the sliders and the text inputs together so that
        # if one changes, the other does too
        for i in range(len(self.sliders)):
            self.sliders[i].valueChanged.connect(
                self.connectHelper(i, self.sliderValueChanged)
            )
            self.textInputs[i].textEdited.connect(
                self.connectHelper(i, self.inputValueChanged)
            )

        self.inputResistanceInput.currentIndexChanged.connect(self.updateCurrentValues)
        self.excitationFrequencyInput.currentIndexChanged.connect(
            self.updateCurrentValues
        )

        # Setup connections for button actions
        self.cancelBtn.clicked.connect(self.cancelEPG)
        self.revertToDefaultsBtn.clicked.connect(self.revertToDefaults)
        self.applyBtn.clicked.connect(self.apply)
        self.applyAndCloseBtn.clicked.connect(self.applyAndClose)

    def updateCurrentValues(self):
        """Update the current values based on user interaction or initialization."""
        self.ri = self.riReader(self.menuInputs[0].currentText())
        self.freq = int(self.menuInputs[1].currentText())
        self.gain = self.sliders[0].value()
        self.bias = self.sliders[1].value() * 0.1
        self.amp = self.sliders[2].value() * 0.1

    def connectHelper(self, i: int, func):
        """Helper function needed due to Python's lazy eval which prevents
        functions from being passed into QT's connect functions properly
        :param i: the index that represents which sliders/input changed
        :param func: the function to apply given some signal
        :return: the function that should be connected to the signal
        """
        return lambda event: func(event, i)

    def sliderValueChanged(self, event: int, i: int):
        """If slider is changed, then update the value of the input box
        :param event: the value the slider has been set to
        :param i: the index representing which slider has been changed
        """
        self.textInputs[i].setText(str(event))
        self.updateCurrentValues()

    def inputValueChanged(self, event: str, i: int):
        """If input is changed, then update the value of the slider
        :param event: the value the input has been set to
        :param i: the index representing which input has been changed
        """
        if event == "":
            event = 0
        self.sliders[i].setValue(int(event))
        self.updateCurrentValues()

    def revertToDefaults(self):
        """Set all sliders and inputs to the default"""
        for i in range(len(self.sliders)):
            self.sliders[i].setValue(self.defaultValues[i])
            self.textInputs[i].setText(str(self.defaultValues[i]))
        # TODO: deal with the drop-down menu case
        self.updateCurrentValues()

    def apply(self):
        """Apply changes to values without closing the window"""
        message = ["PARAM", str(self.channel)]
        values = [self.ri, self.gain, f"{self.bias:.3f}", self.freq, f"{self.amp:.3f}"]
        values_string = [str(value) for value in values]
        message += values_string
        message_string = ",".join(map(str, message))
        message_string += "\n"
        self.update.emit(message_string)

    def applyAndClose(self):
        """Apply changes to values and close the window"""
        self.apply()
        self.close()

    def cancelEPG(self):
        """Close the window"""
        self.close()

    def riReader(self, text: str):
        """Conversion for input resistance"""
        if text == "":
            return 
        suffix = text[-1]
        match suffix:
            case "K":
                return int(text[:-1]) * 10**3
            case "M":
                return int(text[:-1]) * 10**6
            case "G":
                return int(text[:-1]) * 10**9
