# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QMainWindow, QCheckBox, QInputDialog
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

class TogglePushButtonWidget(QtWidgets.QPushButton):
    """Toggles between on and off text
    Changes color depending on state"""
    def __init__(self, parent, on, off):
        super().__init__(parent)
        self.on = on
        self.off = off
        self.state = True
        self.setText(self.on)
        self.setStyleSheet("background-color: red")
        self.pressed.connect(self.toggle_state)    
    
    def toggle_state(self):
        self.state = not self.state
        if self.state:
            self.setText(self.on)
            self.setStyleSheet("background-color: red")
        else:
            self.setText(self.off)
            self.setStyleSheet("background-color: green")

class AnotherWindow(QMainWindow):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, app):
        super().__init__()
        self.setObjectName(_fromUtf8("FG"))
        self.resize(692, 500)
        self.centralwidget = QtGui.QWidget()
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.grSaw = PlotWidget(self.frame)
        self.grSaw.setObjectName(_fromUtf8("grSaw"))
        self.verticalLayout.addWidget(self.grSaw)
        self.grSaw.plotItem.showGrid(True, True, 0.7)


        self.label_Amp = QtGui.QLabel(self.frame)
        self.label_Amp.setObjectName(_fromUtf8("label_Amp"))
        self.verticalLayout.addWidget(self.label_Amp)

        self.volumeSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.volumeSlider.setMaximum(0)
        self.volumeSlider.setMinimum(-30)
        self.volumeSlider.valueChanged.connect(app.volumeChange)
        self.verticalLayout.addWidget(self.volumeSlider)

        self.label_Shift = QtGui.QLabel(self.frame)
        self.label_Shift.setObjectName(_fromUtf8("label_Shift"))
        self.verticalLayout.addWidget(self.label_Shift)

        self.shiftSlider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.shiftSlider.setMaximum(2*math.pi*100)
        self.shiftSlider.setMinimum(0)
        self.shiftSlider.valueChanged.connect(app.shiftChange)
        self.verticalLayout.addWidget(self.shiftSlider)
        
        self.checkSine =  QCheckBox('Sine')
        self.checkSine.stateChanged.connect(app.clickedSine)
        self.verticalLayout.addWidget(self.checkSine)

        self.checkPulse =  QCheckBox('Pulse')
        self.checkPulse.stateChanged.connect(app.clickedPulse)
        self.verticalLayout.addWidget(self.checkPulse)

        self.checkSawtooth =  QCheckBox('Sawtooth')
        self.checkSawtooth.stateChanged.connect(app.clickedSawtooth)
        self.verticalLayout.addWidget(self.checkSawtooth)

        self.checkTriangle =  QCheckBox('Triangle')
        self.checkTriangle.stateChanged.connect(app.clickedTriangle)
        self.verticalLayout.addWidget(self.checkTriangle)

        self.checkWhiteNoise =  QCheckBox('White Noise')
        self.checkWhiteNoise.stateChanged.connect(app.clickedWhiteNoise)
        self.verticalLayout.addWidget(self.checkWhiteNoise)

        self.bandwidth = QtWidgets.QPushButton("Change Bandwidth") 
        self.bandwidth.clicked.connect(app.setBandwidth)
        self.verticalLayout.addWidget(self.bandwidth)

        self.freqButton = QtWidgets.QPushButton("Change Ramp Time/Frequency") 
        self.freqButton.clicked.connect(app.getFreqInt)
        self.verticalLayout.addWidget(self.freqButton)

        self.srateButton = QtWidgets.QPushButton("Change Sample Rate") 
        self.srateButton.clicked.connect(app.getSRate)
        self.verticalLayout.addWidget(self.srateButton)

        self.another = TogglePushButtonWidget(self, "Generate", "Turn off")
        self.another.clicked.connect(app.play_signal)
        self.verticalLayout.addWidget(self.another)

        self.horizontalLayout.addWidget(self.frame)

    def getBandwidth(self, bw):
        return QInputDialog.getDouble(self, "Change Bandwidth", "enter bandwidth in MHz", bw, 0, 1000, 4)

    def getSRate(self, rate):
        return QInputDialog.getInt(self, "Change Generator Sample Rate", "enter a sample rate", rate)

    def getFreqInt(self, ramp):
        return QInputDialog.getDouble(self, "Change Generator Ramp Time/Frequency","enter a ramp time/frequency", ramp, 0, 1, 4)
   

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.w=AnotherWindow(app=self)
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(993, 692)
        
        # Create centralwidget (graph)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # Create paramwidget (params)
        self.paramwidget = QtGui.QWidget()
        self.paramwidget.setObjectName(_fromUtf8("paramwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        # level bar on the left
        self.pbLevel = QtGui.QProgressBar(self.centralwidget)
        self.pbLevel.setMaximum(1000)
        self.pbLevel.setProperty("value", 123)
        self.pbLevel.setTextVisible(False)
        self.pbLevel.setOrientation(QtCore.Qt.Vertical)
        self.pbLevel.setObjectName(_fromUtf8("pbLevel"))
        self.horizontalLayout.addWidget(self.pbLevel)

        # Frame for graph
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        
        # graph dimensions restricting
        '''
        self.frame.setMinimumWidth(500)
        self.frame.setMaximumWidth(700)
        self.frame.setMinimumHeight(300)
        self.frame.setMaximumHeight(500)
        '''
        #self.frame.setGeometry(0,0,700,500)

        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))


        #self.addParamBox("PCM", "Raw Parameters")
        # Add Raw Data Graph
        self.addGraph("PCM", "Raw Data (PCM)")
        #setattr(self, label, QtGui.QLabel(self.frame))


        # Add FFT graph
        self.addGraph("FFT", "Frequency Data (FFT)")

        #Add a window for displaying input buffer
        #self.addGraph("inputbuffer", "Input Buffer")
        
        self.horizontalLayout.addWidget(self.frame, 4)
        #self.horizontalLayout.addWidget(self.paramwidget, 4)
        
        elems = []
        tmp = []
        
        # Digital Signal Processing options (1st Row of params)
        self.function_generator = QtGui.QPushButton("Function Generator")
        self.function_generator.clicked.connect(self.show_new_window)
        self.function_generator.setFixedHeight(30)

        self.input_inputbuffer = QtGui.QPushButton("Plot 1: Input/Input Buffer")
        self.input_inputbuffer.clicked.connect(self.inputbutton)
        self.input_inputbuffer.setFixedHeight(30)

        self.spectrogram = QtGui.QPushButton("Plot 2: FFT/Spectrogram")
        self.spectrogram.clicked.connect(self.spectrogrambutton)
        self.spectrogram.setFixedHeight(30)

        self.averaging = QtGui.QPushButton("Signal Averaging")
        self.averaging.clicked.connect(self.avgbutton)
        self.averaging.setFixedHeight(30)

        self.rangedet = QtGui.QPushButton("Range Detection")
        self.rangedet.clicked.connect(self.rangebutton)
        self.rangedet.setFixedHeight(30)

        self.buffertofile = QtGui.QPushButton("Output buffer to file")
        self.buffertofile.clicked.connect(self.bufferfilebutton)
        self.buffertofile.setFixedHeight(30)

        tmp.append(self.function_generator)
        tmp.append(self.input_inputbuffer)
        tmp.append(self.spectrogram)
        tmp.append(self.averaging)
        tmp.append(self.rangedet)
        tmp.append(self.buffertofile)
        elems.append(tmp)


        # Create the params box
        self.horizontalLayout.addWidget(self.createGroupBox( "Parameters", elems))

        MainWindow.setCentralWidget(self.centralwidget)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def show_new_window(self, checked):
        #self.w = AnotherWindow()
        self.w.show()

    def avgbutton(self):
        pass

    def rangebutton(self):
        pass

    def bufferfilebutton(self):
        pass

    def spectrogrambutton(self):
        if (self.display2=="fft"):
            self.display2="spectro"
            self.FFT_label.setText("Spectrogram")
        else:
            self.display2 = "fft"
            self.FFT_label.setText("FFT")


    def inputbutton(self):
        if (self.display=="buf"):
            self.display="pcm"
            self.PCM_label.setText("Raw Data (PCM)")
        else:
            self.display = "buf"
            self.PCM_label.setText("Raw Data Buffered (3s)")

    def createGroupBox(self, boxTitle, elems=None):
        group_box_settings = QtGui.QGroupBox(self)
        group_box_settings.setTitle(boxTitle)
        
        grid = QtGui.QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)

        row, col = 0, 0
        for row_array in elems:
            for col_elem in row_array:
                grid.addWidget(col_elem, row, col)
                #col += 1
                row += 1
            
            #row += 1

        group_box_settings.setLayout(grid)

        return group_box_settings

    # Creates a data graph
    def addGraph(self, name, title, state=1):
        label = name + "_label"
        print("label: ", label)
        print("name: ", name)
        grName = "gr" + name

        #self.label = QtGui.QLabel(self.frame)
        setattr(self, label, QtGui.QLabel(self.frame))

        #self.label.setObjectName(_fromUtf8("label"))  -> self.label becomes tmp
        tmp = getattr(self, label)
        tmp.setObjectName(_fromUtf8("label"))

        self.verticalLayout.addWidget(tmp)

        #self.grName = PlotWidget(self.frame)
        setattr(self, grName, PlotWidget(self.frame))

        #self.grName.setObjectName(_fromUtf8(grName))  -> self.grName becomes tmp2
        tmp2 = getattr(self, grName)
        tmp2.setObjectName(_fromUtf8(grName))
        
        if state:
            self.verticalLayout.addWidget(tmp2)
        else:
            pass
        
        # RetranslateUi:
        #self.label.setText(_translate("MainWindow", "frequency data (FFT):", None))
        tmp.setText(_translate("MainWindow", title, None))

    # Creates a parameter box
    def addParamBox(self, attr, type, state=1):
        pass

    # Creates a modes tab
    def addModesTab(self, state=1):
        pass

    # Unused now
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "frequency data (FFT):", None))
        self.label_2.setText(_translate("MainWindow", "Raw Data (PCM):", None))
        self.label_3.setText(_translate("MainWindow", "Input Buffer:", None))

from pyqtgraph import PlotWidget
