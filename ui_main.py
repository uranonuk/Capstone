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
        MainWindow.resize(500, 692)
        
        # Create centralwidget (graph)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        
        # Create paramwidget (params)
        self.paramwidget = QtGui.QWidget(MainWindow)
        self.paramwidget.setObjectName(_fromUtf8("paramwidget"))

        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Plain)
        self.frame.setObjectName(_fromUtf8("frame"))

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

        # Add Raw Data Graph
        self.addGraph("PCM", "Raw Data (PCM)")

        # Add FFT graph
        #self.addGraph("FFT", "Frequency Data (FFT)")

        #Add a window for displaying input buffer
        #self.addGraph("inputbuffer", "Input Buffer")
        
        self.addParamBox()

        self.horizontalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
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
    def addParamBox(self, state=1):
        container = QtGui.QWidget()
        container.setLayout(QtGui.QVBoxLayout())

        # Buttons
        ex = QtGui.QPushButton("example")
        container.layout().addWidget(ex)
        self.layout().addWidget(container)

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
