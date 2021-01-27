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
        self.setupUi(self)
        self.updatesPerSecond = 20
        self.rate = 44100
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.grSaw.plotItem.showGrid(True, True, 0.7)
        self.maxFFT=0
        self.maxPCM=0
        self.sample_rate = 44100
        self.maxSaw=0
        self.freq = 10
        self.volume = 0
        self.phase_shift = 0
        self.ear = SWHear.SWHear(rate=self.rate, updatesPerSecond=self.updatesPerSecond)
        self.ear.stream_start()
        self.grSaw.setYRange(-np.iinfo('int16').max, np.iinfo('int16').max)
        self.currentGeneratorType = 'sawtooth'
        self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)


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
            self.grSaw.plot(self.sawtooth, pen=pen,clear=True)
            
            
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat
    def clickedSine(self, state):
        if state:
            self.currentGeneratorType = 'sine'
            self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def clickedPulse(self, state):
        if state:
            self.currentGeneratorType = 'pulse'
            self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def clickedSawtooth(self, state):
        if state:
            self.currentGeneratorType = 'sawtooth'
            self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
    def clickedTriangle(self, state):
        if state:
            self.currentGeneratorType = 'triangle'
            self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
            
    def clickedWhiteNoise(self, state):
        if state:
            self.currentGeneratorType = 'whitenoise'
            self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
    def volumeChange(self, value):
        self.volume = value
        self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def shiftChange(self, value):
        value = value/100 #for slider only returns ints
        self.phase_shift = value
        self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def getFreqInt(self):
        num, ok = super().getFreqInt()
        if ok:
            self.freq = num
            self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
            
    def getSRate(self):
        num, ok = super().getFreqInt()
        if ok:
            self.sample_rate = num
            self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
            
        
if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
