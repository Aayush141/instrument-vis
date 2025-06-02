# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'log_msg.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QMainWindow,
    QPlainTextEdit, QSizePolicy, QVBoxLayout, QWidget)

class Ui_LogMsg(object):
    def setupUi(self, LogMsg):
        if not LogMsg.objectName():
            LogMsg.setObjectName(u"LogMsg")
        LogMsg.resize(600, 354)
        self.centralWidget = QWidget(LogMsg)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayoutWidget = QWidget(self.centralWidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 581, 331))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout.addWidget(self.label_4)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.plainTextEdit = QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout.addWidget(self.plainTextEdit)

        LogMsg.setCentralWidget(self.centralWidget)

        self.retranslateUi(LogMsg)

        QMetaObject.connectSlotsByName(LogMsg)
    # setupUi

    def retranslateUi(self, LogMsg):
        LogMsg.setWindowTitle(QCoreApplication.translate("LogMsg", u"Log", None))
        self.label_2.setText(QCoreApplication.translate("LogMsg", u" System Time", None))
        self.label.setText(QCoreApplication.translate("LogMsg", u"  Recording Time", None))
        self.label_3.setText(QCoreApplication.translate("LogMsg", u"Log Level", None))
        self.label_4.setText(QCoreApplication.translate("LogMsg", u"Log Message", None))
    # retranslateUi

