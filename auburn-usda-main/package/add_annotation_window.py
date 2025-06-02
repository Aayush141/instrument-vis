from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDialog
from package.ui_python.add_annotation_window_ui import Ui_AddAnnotationWindow
from package.utils.data_classes import DataPoint, Annotation
from package.utils.enums import AnnotationType
import logging


class AddAnnotationWindow(QDialog, Ui_AddAnnotationWindow):
    annotationAdded = Signal(Annotation)

    def __init__(self, parent=None, point=DataPoint(0, 0, 0)):
        """Dialog box to create an annotation"""
        super().__init__(parent)
        self.setupUi(self)
        self.buttonBox.accepted.connect(self.acceptAnnotation)
        self.buttonBox.rejected.connect(self.rejectAnnotation)
        self.count = 0 
        self.channel = 0

    def setCurrentPoint(self, point: DataPoint):
        self.point = point

    def acceptAnnotation(self):
        """ If confirmed, create annotation 
        """
        print("Adding annotation...")
        text = self.textInput.toPlainText()
        clockTime = self.clockTimeLabel.text()
        timeStart = self.timeStartLabel.text()
        duration = self.durationLabel.text()
        id = self.count 
        channel = self.channel 
        self.count += 1
        annotationType = None
        if duration == "0":
            annotationType = AnnotationType.POINT
        else:
            annotationType = AnnotationType.DURATION
        newAnnotation = Annotation(timeStart, clockTime, text, duration, annotationType, channel=channel, id=id)
        self.annotationAdded.emit(newAnnotation)
        dur = str(float(duration)-float(timeStart))
        logging.info("A new annotation, \""+text+"\", is added at elapsed time "+timeStart+"s with duration "+
                     dur+"s.")
        self.resetAnnotation()
        self.close()

    def rejectAnnotation(self):
        """ If closed out of window, then do nothing and reset form """
        self.resetAnnotation()
        self.close()

    def resetAnnotation(self):
        """ Reset fields in form to be empty """
        self.textInput.setPlainText("")
        self.timeStartLabel.setText("")
        self.clockTimeLabel.setText("")
        self.durationLabel.setText("")
