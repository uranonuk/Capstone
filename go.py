from PyQt5 import QtGui,QtCore
from pydub import generators, utils
import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear



class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.updatesPerSecond = 20
        self.rate = 44100
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        #self.grSaw.plotItem.showGrid(True, True, 0.7)
        self.maxFFT=0
        self.maxPCM=0
        #self.maxSaw=0
        self.ear = SWHear.SWHear(rate=self.rate, updatesPerSecond=self.updatesPerSecond)
        self.ear.stream_start()
        self.generationFreq = 10
        self.sawtooth = generators.Sawtooth(freq=self.generationFreq).to_audio_segment()
        self.sawtooth.export("./generated_signals/demo1.wav", format="wav")

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
            pen=pyqtgraph.mkPen(color='g')
            #self.grSaw.plot(self.sawtooth.get_frame(0))
            
            
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
