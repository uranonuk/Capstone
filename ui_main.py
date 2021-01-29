# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow

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

class AnotherWindow(QMainWindow):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, parent=None):
        super().__init__()
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
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.grFFT = PlotWidget(self.frame)
        self.grFFT.setObjectName(_fromUtf8("grFFT"))
        self.verticalLayout.addWidget(self.grFFT)
        self.horizontalLayout.addWidget(self.frame)
        self.grFFT.plotItem.showGrid(True, True, 0.7)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.display="pcm"
        self.w=AnotherWindow()
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(692, 500)
        
        # Create centralwidget (graph)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))


        # Create paramwidget (params)
        self.paramwidget = QtGui.QWidget()
        self.paramwidget.setObjectName(_fromUtf8("paramwidget"))

        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        #self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        # Frame for graph
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.frame.setMinimumWidth(300)
        self.frame.setMaximumWidth(700)

        self.frame.setMinimumHeight(300)
        self.frame.setMaximumHeight(500)
        #self.frame.setGeometry(0,0,700,500)

        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))


        #self.addParamBox("PCM", "Raw Parameters")
        # Add Raw Data Graph
        self.addGraph("PCM", "Raw Data (PCM)")
        

        # Add FFT graph
        #self.addGraph("FFT", "Frequency Data (FFT)")

        #Add a window for displaying input buffer
        #self.addGraph("inputbuffer", "Input Buffer")
        


        
        self.horizontalLayout.addWidget(self.frame, 4)
        #self.horizontalLayout.addWidget(self.paramwidget, 4)
        
        elems = []
        tmp = []
        
        # Digital Signal Processing options (1st Row of params)
        self.DSP_triggering = QtGui.QPushButton("Triggering")
        self.DSP_triggering.clicked.connect(self.show_new_window)
        self.DSP_triggering.setFixedSize(120,30)

        self.DSP_averaging = QtGui.QPushButton("Averaging")
        self.DSP_averaging.clicked.connect(self.avgbutton)
        self.DSP_averaging.setFixedSize(120,30)

        self.DSP_FFT = QtGui.QPushButton("FFT")
        self.DSP_FFT.clicked.connect(self.fftbutton)
        self.DSP_FFT.setFixedSize(120,30)

        tmp.append(self.DSP_triggering)
        tmp.append(self.DSP_averaging)
        tmp.append(self.DSP_FFT)
        elems.append(tmp)

        '''
        if velems == []:
            velems = None
        if helems == []:
            helems = None
        '''

        # Create the params box
        

        self.horizontalLayout.addWidget(self.createGroupBox( "Parameters", elems))

        MainWindow.setCentralWidget(self.centralwidget)
        
        '''
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
        '''
        

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def show_new_window(self, checked):
        #self.w = AnotherWindow()
        self.w.show()

    def fftbutton(self):
        if (self.display=="fft"):
            self.display="pcm"
        else:
            self.display = "fft"

    def avgbutton(self):
        if (self.display=="buf"):
            self.display="pcm"
        else:
            self.display = "buf"

    def createGroupBox(self, boxTitle, elems=None):
        group_box_settings = QtGui.QGroupBox(self)
        group_box_settings.setTitle(boxTitle)
        
        grid = QtGui.QGridLayout()
        grid.setAlignment(QtCore.Qt.AlignTop)

        row, col = 0, 0
        for row_array in elems:
            for col_elem in row_array:
                grid.addWidget(col_elem, row, col)
                col += 1
            
            row += 1

        group_box_settings.setLayout(grid)

        return group_box_settings
        '''
        setattr(self, field, QtGui.QGroupBox(boxTitle))
        box = getattr(self, field)

        vbox = QtGui.QVBoxLayout(box)
        hbox = QtGui.QHBoxLayout(box)

        if velems != None:
            for velem in velems:
                vbox.addWidget(velem)

        if helems != None:
            for helem in helems:
                hbox.addWidget(helem)

        #self.horizontalLayout(box)
        '''
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
