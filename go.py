from PyQt5 import QtGui,QtCore
from pydub import generators, utils
from signal_generation import generate_wave
import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear

class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        
        super(ExampleApp, self).__init__(parent)
        
        # Setup
        self.setupUi(self)

        self.updatesPerSecond = 20
        self.rate = 44100
        
        #self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        #self.grSaw.plotItem.showGrid(True, True, 0.7)
        #self.inputbuffer.plotItem.showGrid(True, True, 0.7)
        self.maxFFT=0
        self.maxPCM=0
        #self.maxSaw=0
        self.ear = SWHear.SWHear(rate=self.rate, updatesPerSecond=self.updatesPerSecond)
        self.ear.stream_start()
        self.sawtooth = generate_wave('sawtooth')
        print(self.sawtooth)

    

    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax=np.max(np.abs(self.ear.data))
            if pcmMax>self.maxPCM:
                self.maxPCM=pcmMax
                self.grPCM.plotItem.setRange(yRange=[-pcmMax,pcmMax])
                #self.inputbuffer.plotItem.setRange(yRange=[-pcmMax,pcmMax])
            if np.max(self.ear.fft)>self.maxFFT:
                self.maxFFT=np.max(np.abs(self.ear.fft))
                #self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                #self.grFFT.plotItem.setRange(yRange=[0,1])
            #self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
            pen=pyqtgraph.mkPen(color='b')
            self.grPCM.plot(self.ear.datax,self.ear.data,pen=pen,clear=True)
            if self.ear.plotbuff:
                pen=pyqtgraph.mkPen(color='g')
                #self.inputbuffer.plot(self.ear.databuffx,self.ear.databuff,pen=pen,clear=True)
            pen=pyqtgraph.mkPen(color='r')
            #self.grFFT.plot(self.ear.fftx,self.ear.fft/self.maxFFT,pen=pen,clear=True)
            #pen=pyqtgraph.mkPen(color='g')
            #self.grSaw.plot(self.sawtooth.get_frame(0))  
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

def run():
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    form.ear.keepRecording=False
    print("DONE")
    sys.exit()

if __name__=="__main__":
    run()

'''
from PyQt5 import QtGui,QtCore

import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear

class Window(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    
    # Core initial app structure

    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        
        super(Window, self).__init__(parent)
        
        # Setup
        self.setupUi(self)
        
        # bug: Causes quit button to not work
        
        # Plotting initial screen
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        
        self.maxFFT=0
        self.maxPCM=0
        self.ear = SWHear.SWHear(rate=44100,updatesPerSecond=20)
        self.ear.stream_start()
        
        
        # Main menu bar
        extractAction = QtGui.QAction("&Force Quit", self) # Name
        extractAction.setShortcut("Ctrl+Q") # Shortcut
        extractAction.triggered.connect(self.close_application) # Event when pressed

        self.statusBar()

        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction)


        self.home()
        
    # Home page
    def home(self):
        
        
        quit_btn = QtGui.QPushButton("Quit", self)
        quit_btn.clicked.connect(self.close_application)

        quit_btn.resize(quit_btn.minimumSizeHint())
        quit_btn.move(0,100)

        # Toolbar
        extractAction = QtGui.QAction("abc",self)
        extractAction.triggered.connect(self.close_application)

        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction)

        # CheckBox
        checkBox = QtGui.QCheckBox('Enlarge Window', self)
        # checkBox.toggle() # Changes the default toggle setting
        checkBox.stateChanged.connect(self.enlarge_window)
        
        
        # Progress Bar
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(200,80,250,20)

        self.quit_btn = QtGui.QPushButton("Download", self)
        self.quit_btn.move(200,120)
        self.quit_btn.clicked.connect(self.download)
        
        
        # Drop Downs & Styles
        print(self.style().objectName())
        self.styleChoice = QtGui.QLabel("Windows", self)

        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("motif")
        comboBox.addItem("Windows")
        comboBox.addItem("cde")
        comboBox.addItem("Plastique")
        comboBox.addItem("Cleanlooks")
        comboBox.addItem("windowsvista")

        comboBox.move(50, 250)
        self.styleChoice.move(50, 150)
        comboBox.activated[str].connect(self.style_choice)
        

        self.show()

    def style_choice(self, text):
        self.styleChoice.setText(text)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(text)) 
    
    def download(self):
        self.completed = 0

        while self.completed < 100:
            self.completed += 0.001
            self.progress.setValue(self.completed)
    
    def enlarge_window(self, state):
        if state == QtCore.Qt.Checked:
            self.setGeometry(50,50,1000,600)
        else:
            self.setGeometry(50,50,500,300)

    # Closing method
    def close_application(self):
        # Pop up message before quitting
        choice = QtGui.QMessageBox.question(self, 'Extract',
        'Are you sure you want to quit?',
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass

    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax=np.max(np.abs(self.ear.data))
            if pcmMax>self.maxPCM:
                self.maxPCM=pcmMax
                self.grPCM.plotItem.setRange(yRange=[-pcmMax,pcmMax])
            if np.max(self.ear.fft)>self.maxFFT:
                self.maxFFT=np.max(np.abs(self.ear.fft))
                #self.grFFT.plotItem.setRange(yRange=[0,self.maxFFT])
                self.grFFT.plotItem.setRange(yRange=[0,1])
            self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
            pen=pyqtgraph.mkPen(color='b')
            self.grPCM.plot(self.ear.datax,self.ear.data,pen=pen,clear=True)
            pen=pyqtgraph.mkPen(color='r')
            self.grFFT.plot(self.ear.fftx,self.ear.fft/self.maxFFT,pen=pen,clear=True)
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

def run():
    app = QtGui.QApplication(sys.argv)
    window = Window()
    # window.show()
    # window.update() #start with something
    sys.exit(app.exec_())
    print("DONE")

if __name__=="__main__":
    run()
    
    
    
    
'''