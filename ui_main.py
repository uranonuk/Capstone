# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_main.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

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

        
        # Frame for params
        self.frame2 = QtGui.QFrame(self.paramwidget)
        self.frame2.setFrameShape(QtGui.QFrame.Box)
        self.frame2.setFrameShadow(QtGui.QFrame.Plain)
        self.frame2.setObjectName(_fromUtf8("frame2"))
        self.frame2.setMaximumWidth(700)
        self.frame2.setMaximumHeight(500)
        self.frame2.setGeometry(0,0,0,0)

        
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))

        '''
        # Progress Bar
        self.pbLevel = QtGui.QProgressBar(self.centralwidget)
        self.pbLevel.setMaximum(1000)
        self.pbLevel.setProperty("value", 123)
        self.pbLevel.setTextVisible(False)
        self.pbLevel.setOrientation(QtCore.Qt.Vertical)
        self.pbLevel.setObjectName(_fromUtf8("pbLevel"))
        #self.horizontalLayout.addWidget(self.pbLevel)
        '''

        #self.addParamBox("PCM", "Raw Parameters")
        # Add Raw Data Graph
        self.addGraph("PCM", "Raw Data (PCM)")
        

        # Add FFT graph
        #self.addGraph("FFT", "Frequency Data (FFT)")

        #Add a window for displaying input buffer
        #self.addGraph("inputbuffer", "Input Buffer")
        


        
        self.horizontalLayout.addWidget(self.frame, 4)
        #self.horizontalLayout.addWidget(self.paramwidget, 4)
        
        velems, helems = [], []
        '''
        # Create what will be inside Parameters
        self.textBox =  QtGui.QLabel('Parameters')
        self.textBox.setAlignment(QtCore.Qt.AlignLeft)
        velems.append(self.textBox)
        '''
        # Digital Signal Processing options
        self.DSP_triggering = QtGui.QPushButton("Triggering")
        self.DSP_averaging = QtGui.QPushButton("Averaging")
        velems.append(self.DSP_triggering)
        velems.append(self.DSP_averaging)

        if velems == []:
            velems = None
        if helems == []:
            helems = None
        
        # Create the params box
        self.createGroupBox("groupBox", "Parameters", velems, helems)

        self.horizontalLayout.addWidget(self.groupBox)

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
        
    def createGroupBox(self, field, boxTitle, velems=None, helems=None):
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
