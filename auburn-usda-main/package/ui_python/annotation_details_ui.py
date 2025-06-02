# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'annotation_details.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QLabel, QSizePolicy,
    QTextBrowser, QWidget)

class Ui_Annotation_Details(object):
    def setupUi(self, Annotation_Details):
        if not Annotation_Details.objectName():
            Annotation_Details.setObjectName(u"Annotation_Details")
        Annotation_Details.resize(456, 358)
        self.formLayoutWidget = QWidget(Annotation_Details)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 1179, 341))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.formLayoutWidget)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.timeStart = QLabel(self.formLayoutWidget)
        self.timeStart.setObjectName(u"timeStart")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.timeStart)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.duration = QLabel(self.formLayoutWidget)
        self.duration.setObjectName(u"duration")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.duration)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_5)

        self.text = QTextBrowser(self.formLayoutWidget)
        self.text.setObjectName(u"text")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.text)


        self.retranslateUi(Annotation_Details)

        QMetaObject.connectSlotsByName(Annotation_Details)
    # setupUi

    def retranslateUi(self, Annotation_Details):
        Annotation_Details.setWindowTitle(QCoreApplication.translate("Annotation_Details", u"Form", None))
        self.label.setText(QCoreApplication.translate("Annotation_Details", u"Time start:", None))
        self.timeStart.setText("")
        self.label_3.setText(QCoreApplication.translate("Annotation_Details", u"Duration:", None))
        self.duration.setText(QCoreApplication.translate("Annotation_Details", u"TextLabel", None))
        self.label_5.setText(QCoreApplication.translate("Annotation_Details", u"Text:", None))
    # retranslateUi

