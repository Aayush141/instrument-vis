# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'epg_control.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSlider, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_EPGControl(object):
    def setupUi(self, EPGControl):
        if not EPGControl.objectName():
            EPGControl.setObjectName(u"EPGControl")
        EPGControl.resize(716, 350)
        self.centralWidget = QWidget(EPGControl)
        self.centralWidget.setObjectName(u"centralWidget")
        self.verticalLayoutWidget = QWidget(self.centralWidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(80, 20, 581, 271))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.inputResistance = QHBoxLayout()
        self.inputResistance.setObjectName(u"inputResistance")
        self.inputResistance.setContentsMargins(-1, -1, 0, -1)
        self.inputResistanceTitle = QLabel(self.verticalLayoutWidget)
        self.inputResistanceTitle.setObjectName(u"inputResistanceTitle")

        self.inputResistance.addWidget(self.inputResistanceTitle)

        self.inputResistanceInput = QComboBox(self.verticalLayoutWidget)
        self.inputResistanceInput.addItem("")
        self.inputResistanceInput.addItem("")
        self.inputResistanceInput.addItem("")
        self.inputResistanceInput.addItem("")
        self.inputResistanceInput.addItem("")
        self.inputResistanceInput.addItem("")
        self.inputResistanceInput.addItem("")
        self.inputResistanceInput.setObjectName(u"inputResistanceInput")

        self.inputResistance.addWidget(self.inputResistanceInput)

        self.inputResistanceUnit = QLabel(self.verticalLayoutWidget)
        self.inputResistanceUnit.setObjectName(u"inputResistanceUnit")

        self.inputResistance.addWidget(self.inputResistanceUnit)


        self.verticalLayout.addLayout(self.inputResistance)

        self.ampliferGain = QHBoxLayout()
        self.ampliferGain.setObjectName(u"ampliferGain")
        self.ampliferGain.setContentsMargins(-1, -1, 0, -1)
        self.amplifierGainTitle = QLabel(self.verticalLayoutWidget)
        self.amplifierGainTitle.setObjectName(u"amplifierGainTitle")

        self.ampliferGain.addWidget(self.amplifierGainTitle)

        self.amplifierGainSlider = QSlider(self.verticalLayoutWidget)
        self.amplifierGainSlider.setObjectName(u"amplifierGainSlider")
        self.amplifierGainSlider.setMinimum(84)
        self.amplifierGainSlider.setMaximum(10000)
        self.amplifierGainSlider.setOrientation(Qt.Horizontal)

        self.ampliferGain.addWidget(self.amplifierGainSlider)

        self.amplifierGainInput = QLineEdit(self.verticalLayoutWidget)
        self.amplifierGainInput.setObjectName(u"amplifierGainInput")
        self.amplifierGainInput.setEnabled(True)
        self.amplifierGainInput.setMaximumSize(QSize(50, 16777215))
        self.amplifierGainInput.setMouseTracking(False)
        self.amplifierGainInput.setMaxLength(32767)

        self.ampliferGain.addWidget(self.amplifierGainInput)

        self.amplifierGainUnit = QLabel(self.verticalLayoutWidget)
        self.amplifierGainUnit.setObjectName(u"amplifierGainUnit")

        self.ampliferGain.addWidget(self.amplifierGainUnit)


        self.verticalLayout.addLayout(self.ampliferGain)

        self.amplifierOffset = QHBoxLayout()
        self.amplifierOffset.setObjectName(u"amplifierOffset")
        self.amplifierOffsetTitle = QLabel(self.verticalLayoutWidget)
        self.amplifierOffsetTitle.setObjectName(u"amplifierOffsetTitle")

        self.amplifierOffset.addWidget(self.amplifierOffsetTitle)

        self.amplifierOffetSlider = QSlider(self.verticalLayoutWidget)
        self.amplifierOffetSlider.setObjectName(u"amplifierOffetSlider")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.amplifierOffetSlider.sizePolicy().hasHeightForWidth())
        self.amplifierOffetSlider.setSizePolicy(sizePolicy)
        self.amplifierOffetSlider.setMaximum(33)
        self.amplifierOffetSlider.setSingleStep(0)
        self.amplifierOffetSlider.setOrientation(Qt.Horizontal)

        self.amplifierOffset.addWidget(self.amplifierOffetSlider)

        self.amplifierOffsetInput = QLineEdit(self.verticalLayoutWidget)
        self.amplifierOffsetInput.setObjectName(u"amplifierOffsetInput")
        self.amplifierOffsetInput.setEnabled(True)
        self.amplifierOffsetInput.setMaximumSize(QSize(50, 16777215))
        self.amplifierOffsetInput.setMouseTracking(False)
        self.amplifierOffsetInput.setMaxLength(32767)

        self.amplifierOffset.addWidget(self.amplifierOffsetInput)

        self.amplifierOffsetUnit = QLabel(self.verticalLayoutWidget)
        self.amplifierOffsetUnit.setObjectName(u"amplifierOffsetUnit")

        self.amplifierOffset.addWidget(self.amplifierOffsetUnit)


        self.verticalLayout.addLayout(self.amplifierOffset)

        self.excitationAmplitude = QHBoxLayout()
        self.excitationAmplitude.setObjectName(u"excitationAmplitude")
        self.excitationAmplitudeTitle = QLabel(self.verticalLayoutWidget)
        self.excitationAmplitudeTitle.setObjectName(u"excitationAmplitudeTitle")

        self.excitationAmplitude.addWidget(self.excitationAmplitudeTitle)

        self.excitationAmplitudeSlider = QSlider(self.verticalLayoutWidget)
        self.excitationAmplitudeSlider.setObjectName(u"excitationAmplitudeSlider")
        self.excitationAmplitudeSlider.setMaximum(33)
        self.excitationAmplitudeSlider.setOrientation(Qt.Horizontal)

        self.excitationAmplitude.addWidget(self.excitationAmplitudeSlider)

        self.excitationAmplitudeInput = QLineEdit(self.verticalLayoutWidget)
        self.excitationAmplitudeInput.setObjectName(u"excitationAmplitudeInput")
        self.excitationAmplitudeInput.setEnabled(True)
        self.excitationAmplitudeInput.setMaximumSize(QSize(50, 16777215))
        self.excitationAmplitudeInput.setMouseTracking(False)
        self.excitationAmplitudeInput.setMaxLength(32767)

        self.excitationAmplitude.addWidget(self.excitationAmplitudeInput)

        self.excitationAmplitudeUnit = QLabel(self.verticalLayoutWidget)
        self.excitationAmplitudeUnit.setObjectName(u"excitationAmplitudeUnit")

        self.excitationAmplitude.addWidget(self.excitationAmplitudeUnit)


        self.verticalLayout.addLayout(self.excitationAmplitude)

        self.excitationFrequency = QHBoxLayout()
        self.excitationFrequency.setObjectName(u"excitationFrequency")
        self.excitationFrequencyTitle = QLabel(self.verticalLayoutWidget)
        self.excitationFrequencyTitle.setObjectName(u"excitationFrequencyTitle")

        self.excitationFrequency.addWidget(self.excitationFrequencyTitle)

        self.excitationFrequencyInput = QComboBox(self.verticalLayoutWidget)
        self.excitationFrequencyInput.addItem("")
        self.excitationFrequencyInput.addItem("")
        self.excitationFrequencyInput.addItem("")
        self.excitationFrequencyInput.setObjectName(u"excitationFrequencyInput")

        self.excitationFrequency.addWidget(self.excitationFrequencyInput)

        self.excitationFrequencyUnit = QLabel(self.verticalLayoutWidget)
        self.excitationFrequencyUnit.setObjectName(u"excitationFrequencyUnit")

        self.excitationFrequency.addWidget(self.excitationFrequencyUnit)


        self.verticalLayout.addLayout(self.excitationFrequency)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.cancelBtn = QPushButton(self.verticalLayoutWidget)
        self.cancelBtn.setObjectName(u"cancelBtn")

        self.horizontalLayout_4.addWidget(self.cancelBtn)

        self.revertToDefaultsBtn = QPushButton(self.verticalLayoutWidget)
        self.revertToDefaultsBtn.setObjectName(u"revertToDefaultsBtn")

        self.horizontalLayout_4.addWidget(self.revertToDefaultsBtn)

        self.applyBtn = QPushButton(self.verticalLayoutWidget)
        self.applyBtn.setObjectName(u"applyBtn")

        self.horizontalLayout_4.addWidget(self.applyBtn)

        self.applyAndCloseBtn = QPushButton(self.verticalLayoutWidget)
        self.applyAndCloseBtn.setObjectName(u"applyAndCloseBtn")

        self.horizontalLayout_4.addWidget(self.applyAndCloseBtn)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        EPGControl.setCentralWidget(self.centralWidget)
        self.statusbar = QStatusBar(EPGControl)
        self.statusbar.setObjectName(u"statusbar")
        EPGControl.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(EPGControl)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 716, 21))
        self.menuChannel_1 = QMenu(self.menubar)
        self.menuChannel_1.setObjectName(u"menuChannel_1")
        EPGControl.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuChannel_1.menuAction())

        self.retranslateUi(EPGControl)

        QMetaObject.connectSlotsByName(EPGControl)
    # setupUi

    def retranslateUi(self, EPGControl):
        EPGControl.setWindowTitle(QCoreApplication.translate("EPGControl", u"MainWindow", None))
        self.inputResistanceTitle.setText(QCoreApplication.translate("EPGControl", u"Input Resistance      ", None))
        self.inputResistanceInput.setItemText(0, QCoreApplication.translate("EPGControl", u"100K", None))
        self.inputResistanceInput.setItemText(1, QCoreApplication.translate("EPGControl", u"1M", None))
        self.inputResistanceInput.setItemText(2, QCoreApplication.translate("EPGControl", u"10M", None))
        self.inputResistanceInput.setItemText(3, QCoreApplication.translate("EPGControl", u"100M", None))
        self.inputResistanceInput.setItemText(4, QCoreApplication.translate("EPGControl", u"1G", None))
        self.inputResistanceInput.setItemText(5, QCoreApplication.translate("EPGControl", u"10G", None))
        self.inputResistanceInput.setItemText(6, QCoreApplication.translate("EPGControl", u"100G", None))

        self.inputResistanceUnit.setText(QCoreApplication.translate("EPGControl", u"\u03a9", None))
        self.amplifierGainTitle.setText(QCoreApplication.translate("EPGControl", u"Amplifier Gain          ", None))
        self.amplifierGainInput.setText(QCoreApplication.translate("EPGControl", u"0", None))
        self.amplifierGainUnit.setText(QCoreApplication.translate("EPGControl", u"dB", None))
        self.amplifierOffsetTitle.setText(QCoreApplication.translate("EPGControl", u"DC Bias                     ", None))
        self.amplifierOffsetInput.setText(QCoreApplication.translate("EPGControl", u"0", None))
        self.amplifierOffsetUnit.setText(QCoreApplication.translate("EPGControl", u"dV", None))
        self.excitationAmplitudeTitle.setText(QCoreApplication.translate("EPGControl", u"Excitation Amplitude", None))
        self.excitationAmplitudeInput.setText(QCoreApplication.translate("EPGControl", u"0", None))
        self.excitationAmplitudeUnit.setText(QCoreApplication.translate("EPGControl", u"dV", None))
        self.excitationFrequencyTitle.setText(QCoreApplication.translate("EPGControl", u"Excitation Frequency", None))
        self.excitationFrequencyInput.setItemText(0, QCoreApplication.translate("EPGControl", u"100", None))
        self.excitationFrequencyInput.setItemText(1, QCoreApplication.translate("EPGControl", u"1000", None))
        self.excitationFrequencyInput.setItemText(2, QCoreApplication.translate("EPGControl", u"2000", None))

        self.excitationFrequencyUnit.setText(QCoreApplication.translate("EPGControl", u"Hz", None))
        self.cancelBtn.setText(QCoreApplication.translate("EPGControl", u"Cancel", None))
        self.revertToDefaultsBtn.setText(QCoreApplication.translate("EPGControl", u"Revert to Defaults", None))
        self.applyBtn.setText(QCoreApplication.translate("EPGControl", u"Apply", None))
        self.applyAndCloseBtn.setText(QCoreApplication.translate("EPGControl", u"Apply and Close", None))
        self.menuChannel_1.setTitle(QCoreApplication.translate("EPGControl", u"Channel 1", None))
    # retranslateUi

