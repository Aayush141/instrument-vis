
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QMainWindow, QToolBar, QFileDialog, QWidgetAction, QLineEdit
from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QAction

import csv 

from package.utils.data_classes import Annotation 
from package.annotation_details import AnnotationDetails

class AnnotationList(QMainWindow):
    """The main window of the application.
    """
    def __init__(self, parent = None):
        super().__init__(parent)
        self.annotations = []
        self._createActions()
        self._createToolBar()
        self._createTable()
        self.annotationViewer = AnnotationDetails()
    
    def _createActions(self):
        """ Creates actions that will be assigned to the tool bar
        """

        # Export annotations
        self.exportAnnotationsAction = QAction("&Export annotations", self)
        self.exportAnnotationsAction.triggered.connect(self.exportAnnotations)

    def _createToolBar(self):
        """ Create the tool bar and connect actions with each tool item
        """
        tools = QToolBar()
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, tools)
        tools.setMovable(False)
        
        # Search bar        
        searchWidgetAction = QWidgetAction(tools)
        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textEdited.connect(self.search)

        searchWidgetAction.setDefaultWidget(self.searchBar)
        tools.addAction(searchWidgetAction)

        tools.addAction(self.exportAnnotationsAction)

    def _createTable(self):
        """ Create table that will list all created annotations
        """
        self.table = QTableWidget()
        self.table.setRowCount(0)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Clock time", "Start (s)", "Duration (s)", "Text"])
        self.table.horizontalHeader().setStretchLastSection(True)

        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSortingEnabled(True)
        self.setCentralWidget(self.table)

        self.table.doubleClicked.connect(lambda index: self.viewAnnotation(index.row()))
    
    def viewAnnotation(self, row:int):
        annotation = self.annotations[row]
        print(annotation)
        self.annotationViewer.timeStart.setText(str(annotation.timeStart))
        self.annotationViewer.duration.setText(str(annotation.duration ))
        self.annotationViewer.text.setText(annotation.text)
        self.annotationViewer.show()

    def insertAnnotation(self, annotation: Annotation):
        """ Insert annotation into table widget
            param annotation: annotation to insert
        """
        self.annotations.append(annotation)
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(annotation.clockTime)))
        self.table.setItem(row, 1, QTableWidgetItem(str(annotation.timeStart)))
        self.table.setItem(row, 2, QTableWidgetItem(str(annotation.duration)))
        self.table.setItem(row, 3, QTableWidgetItem(str(annotation.text)))
    
    @Slot()
    def exportAnnotations(self):
        """ Export all annotations in table to csv format
        """
        filename = QFileDialog.getSaveFileName(self, "Save File", "resources/session_files/epgOutput.csv", "Text files (*.csv)")[0]
        self.exportAnnotationsGivenFilename(filename)

    def exportAnnotationsGivenFileName(self, filename):
        with open(filename, "w", newline='') as file:
            csvwriter = csv.writer(file)
            # Header row
            for annotation in self.annotations:
                row = [annotation.timeStart, annotation.duration, annotation.text, annotation.channel]
                csvwriter.writerow(row)

    @Slot(str)
    def search(self, text):
        print(text)
    
    def reset(self):
        self.annotations = []
        self.table.clearContents()
        self.table.setRowCount(0)
        print("reset")