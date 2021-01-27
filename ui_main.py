# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QCheckBox, QInputDialog
import math

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(993, 692)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pbLevel = QtGui.QProgressBar(self.centralwidget)
        self.pbLevel.setMaximum(1000)
        self.pbLevel.setProperty("value", 123)
        self.pbLevel.setTextVisible(False)
        self.pbLevel.setOrientation(QtCore.Qt.Vertical)
        self.pbLevel.setObjectName(_fromUtf8("pbLevel"))
        self.horizontalLayout.addWidget(self.pbLevel)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.grFFT = PlotWidget(self.frame)
        self.grFFT.setObjectName(_fromUtf8("grFFT"))
        self.verticalLayout.addWidget(self.grFFT)

        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.grPCM = PlotWidget(self.frame)
        self.grPCM.setObjectName(_fromUtf8("grPCM"))
        self.verticalLayout.addWidget(self.grPCM)

        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.grSaw = PlotWidget(self.frame)
        self.grSaw.setObjectName(_fromUtf8("grSaw"))
        self.verticalLayout.addWidget(self.grSaw)

        self.label_Amp = QtGui.QLabel(self.frame)
        self.label_Amp.setObjectName(_fromUtf8("label_Amp"))
        self.verticalLayout.addWidget(self.label_Amp)

        self.volumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.volumeSlider.setMaximum(0)
        self.volumeSlider.setMinimum(-30)
        self.volumeSlider.valueChanged.connect(self.volumeChange)
        self.verticalLayout.addWidget(self.volumeSlider)

        self.label_Shift = QtGui.QLabel(self.frame)
        self.label_Shift.setObjectName(_fromUtf8("label_Shift"))
        self.verticalLayout.addWidget(self.label_Shift)

        self.shiftSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.shiftSlider.setMaximum(2*math.pi*100)
        self.shiftSlider.setMinimum(0)
        self.shiftSlider.valueChanged.connect(self.shiftChange)
        self.verticalLayout.addWidget(self.shiftSlider)



        self.checkSine =  QCheckBox('Sine')
        self.checkSine.stateChanged.connect(self.clickedSine)
        self.verticalLayout.addWidget(self.checkSine)

        self.checkPulse =  QCheckBox('Pulse')
        self.checkPulse.stateChanged.connect(self.clickedPulse)
        self.verticalLayout.addWidget(self.checkPulse)

        self.checkSawtooth =  QCheckBox('Sawtooth')
        self.checkSawtooth.stateChanged.connect(self.clickedSawtooth)
        self.verticalLayout.addWidget(self.checkSawtooth)

        self.checkTriangle =  QCheckBox('Triangle')
        self.checkTriangle.stateChanged.connect(self.clickedTriangle)
        self.verticalLayout.addWidget(self.checkTriangle)

        self.checkWhiteNoise =  QCheckBox('White Noise')
        self.checkWhiteNoise.stateChanged.connect(self.clickedWhiteNoise)
        self.verticalLayout.addWidget(self.checkWhiteNoise)

        self.freqButton = QtWidgets.QPushButton("Change Frequency") 
        self.freqButton.clicked.connect(self.getFreqInt)
        self.verticalLayout.addWidget(self.freqButton)

        self.srateButton = QtWidgets.QPushButton("Change Sample Rate") 
        self.srateButton.clicked.connect(self.getSRate)
        self.verticalLayout.addWidget(self.srateButton)



        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def clickedSine(self, state):
        pass

    def volumeChange(self, value):
        pass

    def shiftChange(self, value):
        pass

    def clickedPulse(self, state):
        pass

    def clickedSawtooth(self, state):
        pass

    def clickedTriangle(self, state):
        pass
    def clickedWhiteNoise(self, state):
        pass
    def getSRate(self):
        return QInputDialog.getInt(self, "Change Generator Sample Rate", "enter a sample rate")
    def getFreqInt(self):
        return QInputDialog.getInt(self,"Change Generator Frequency","enter a frequency")

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "frequency data (FFT):", None))
        self.label_2.setText(_translate("MainWindow", "raw data (PCM):", None))
        self.label_3.setText(_translate("MainWindow", "Function Generator", None))
        self.label_Amp.setText(_translate("MainWindow", "Amplitude:", None))
        self.label_Shift.setText(_translate("MainWindow", "Phase Shift:", None))





from pyqtgraph import PlotWidget
