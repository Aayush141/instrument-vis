# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_annotation_window.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QFormLayout, QLabel, QPlainTextEdit, QSizePolicy,
    QWidget)

class Ui_AddAnnotationWindow(object):
    def setupUi(self, AddAnnotationWindow):
        if not AddAnnotationWindow.objectName():
            AddAnnotationWindow.setObjectName(u"AddAnnotationWindow")
        AddAnnotationWindow.resize(400, 300)
        self.buttonBox = QDialogButtonBox(AddAnnotationWindow)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.textInput = QPlainTextEdit(AddAnnotationWindow)
        self.textInput.setObjectName(u"textInput")
        self.textInput.setGeometry(QRect(20, 110, 351, 111))
        self.formLayoutWidget = QWidget(AddAnnotationWindow)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(20, 30, 351, 71))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.timeStartLabel = QLabel(self.formLayoutWidget)
        self.timeStartLabel.setObjectName(u"timeStartLabel")
        self.timeStartLabel.setAutoFillBackground(False)
        self.timeStartLabel.setStyleSheet(u"background-color: rgba(0, 0, 0, 73)")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.timeStartLabel)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.durationLabel = QLabel(self.formLayoutWidget)
        self.durationLabel.setObjectName(u"durationLabel")
        self.durationLabel.setAutoFillBackground(False)
        self.durationLabel.setStyleSheet(u"background-color: rgba(0, 0, 0, 73)")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.durationLabel)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.clockTimeLabel = QLabel(self.formLayoutWidget)
        self.clockTimeLabel.setObjectName(u"clockTimeLabel")
        self.clockTimeLabel.setAutoFillBackground(False)
        self.clockTimeLabel.setStyleSheet(u"background-color: rgba(0, 0, 0, 73)")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.clockTimeLabel)


        self.retranslateUi(AddAnnotationWindow)

        QMetaObject.connectSlotsByName(AddAnnotationWindow)
    # setupUi

    def retranslateUi(self, AddAnnotationWindow):
        AddAnnotationWindow.setWindowTitle(QCoreApplication.translate("AddAnnotationWindow", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("AddAnnotationWindow", u"Time start (s)", None))
        self.timeStartLabel.setText("")
        self.label_2.setText(QCoreApplication.translate("AddAnnotationWindow", u"Duration (s)", None))
        self.durationLabel.setText("")
        self.label_3.setText(QCoreApplication.translate("AddAnnotationWindow", u"Clock time (hh:mm:ss)", None))
        self.clockTimeLabel.setText("")
    # retranslateUi

