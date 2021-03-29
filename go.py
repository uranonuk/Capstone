from PyQt5 import QtGui,QtCore
from pydub import generators, utils
from pydub.playback import play
from signal_generation import generate_wave
import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear
import threading

class ExampleApp(QtGui.QMainWindow, ui_main.Ui_MainWindow):
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(ExampleApp, self).__init__(parent)
        # Setup
        self.updatesPerSecond = 20
        self.rate = 44100
        self.maxFFT=0
        self.maxPCM=0
        self.sample_rate = 44100
        self.maxSaw=0
        self.freq = 1000
        self.volume = 0
        self.phase_shift = 0
        self.generateSignal = False;
        self.display="pcm"
        self.display2 = "fft"
        
        self.setupUi(self)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        
        self.ear = SWHear.SWHear(rate=self.rate, updatesPerSecond=self.updatesPerSecond)
        self.ear.stream_start()
        self.w.grSaw.setYRange(-np.iinfo('int16').max, np.iinfo('int16').max)
        self.currentGeneratorType = 'sawtooth'
        self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)    


    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax=np.max(np.abs(self.ear.data))
            if pcmMax>self.maxPCM:
                self.maxPCM=pcmMax
            if np.max(self.ear.fft)>self.maxFFT:
                self.maxFFT=np.max(np.abs(self.ear.fft))

            if self.w.isVisible():
                pen=pyqtgraph.mkPen(color='g')
                self.w.grSaw.plotItem.showGrid(True, True, 0.7)
                self.w.grSaw.plotItem.setRange(xRange=[0, 5*self.sample_rate*(1/self.freq)])
                self.sawtooth = self.sawtooth.astype('float64')
                self.w.grSaw.plot(self.sawtooth, pen=pen, clear=True)
                self.sawtooth = self.sawtooth.astype('int16')
            else:
                pass
            
            self.pbLevel.setValue(1000*pcmMax/self.maxPCM)
            
            if self.display=="pcm":
                pen=pyqtgraph.mkPen(color='b')
                self.grPCM.setYRange(-np.iinfo('int16').max, np.iinfo('int16').max)
                self.ear.data = self.ear.data.astype('float64')
                self.grPCM.plot(self.ear.datax,self.ear.data,pen=pen,clear=True)
                self.ear.data = self.ear.data.astype('int16')
            elif self.display=="buf":
                self.grPCM.setYRange(-np.iinfo('int16').max, np.iinfo('int16').max)
                pen=pyqtgraph.mkPen(color='g')
                self.ear.databuff = self.ear.databuff.astype('float64')
                self.grPCM.plot(self.ear.databuffx,self.ear.databuff,pen=pen,clear=True)
                self.ear.databuff = self.ear.databuff.astype('int16')

            if (self.display2=="fft"):
                pen=pyqtgraph.mkPen(color='r')
                self.grFFT.plotItem.setRange(yRange=[0,1])
                self.grFFT.plot(self.ear.fftx,self.ear.fft/self.maxFFT,pen=pen,clear=True)
            #elif self.display2=="spectro":
            # ADD spectrogram here

            #pen=pyqtgraph.mkPen(color='g')
            #self.grSaw.plot(self.sawtooth.get_frame(0))  
        QtCore.QTimer.singleShot(1, self.update) # QUICKLY repeat

    def clickedSine(self, state):
        if state:
            self.currentGeneratorType = 'sine'
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def clickedPulse(self, state):
        if state:
            self.currentGeneratorType = 'pulse'
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def clickedSawtooth(self, state):
        if state:
            self.currentGeneratorType = 'sawtooth'
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
    def clickedTriangle(self, state):
        if state:
            self.currentGeneratorType = 'triangle'
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
            
    def clickedWhiteNoise(self, state):
        if state:
            self.currentGeneratorType = 'whitenoise'
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
    def volumeChange(self, value):
        self.volume = value
        self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def shiftChange(self, value):
        value = value/100 #for slider only returns ints
        self.phase_shift = value
        self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def getFreqInt(self):
        num, ok = self.w.getFreqInt(self.freq)
        if ok:
            self.freq = num
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
            
    def getSRate(self):
        num, ok = self.w.getSRate(self.sample_rate)
        if ok:
            self.sample_rate = num
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)

    def play_signal(self):
        if self.generateSignal == False:
            self.generateSignal = not self.generateSignal
            self.t2 = threading.Thread(target=self.play_wave)
            self.t2.start()
        else:
            self.generateSignal = not self.generateSignal

    def play_wave(self):
        while (self.generateSignal == True):
            play(self.playable)
        sys.exit()

    def closeEvent(self, event):
        print("Closing all windows")
        self.w.close()
        self.generateSignal = False
        event.accept()

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
