from PySide6.QtWidgets import QWidget 
from package.ui_python.annotation_details_ui import Ui_Annotation_Details
class AnnotationDetails(QWidget, Ui_Annotation_Details):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
