from PyQt5 import QtGui,QtCore
from PyQt5.QtWidgets import QFileDialog
from pydub import generators, utils, AudioSegment
from pydub.playback import play
from signal_generation import generate_wave
import sys
import ui_main
import numpy as np
import pyqtgraph
import SWHear
import threading
import wave
import struct

def getFFT(data,rate):
    """Given some data and rate, returns FFTfreq and FFT (half)."""
    data=data*np.hamming(len(data))
    fft=np.fft.fft(data)
    fft=np.abs(fft)
    #fft=10*np.log10(fft)
    freq=np.fft.fftfreq(len(fft),1.0/rate)
    return freq[:int(len(freq)/2)],fft[:int(len(fft)/2)]

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
        self.c = 299792458
        self.bandwidth = 120e6
        self.ramp_time = 10e-3
        self.volume = 0
        self.phase_shift = 0
        self.generateSignal = False
        self.display="pcm"
        self.display2 = "fft"
        self.loadFileName = ""
        self.fileLoaded = False
        self.loadedBuff = None
        self.loadedBuffX = None
        self.loadShift = 0
        self.ramp_time = 10e-3
        self.averageFrames = 0
        self.distanceSet = False
        self.steer_angle = -2
        self.averageFrames = 0
        self.averagingFrames = False
        self.distanceSet = False
        self.setupUi(self)
        self.grPCM.plotItem.showGrid(True, True, 0.7)
        self.grFFT.plotItem.showGrid(True, True, 0.7)
        self.distancex = None
        
        self.ear = SWHear.SWHear(rate=self.rate, updatesPerSecond=self.updatesPerSecond)
        self.ear.stream_start()
        self.w.grSaw.setYRange(-np.iinfo('int16').max, np.iinfo('int16').max)
        self.currentGeneratorType = 'sawtooth'
        self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)    


    def update(self):
        if not self.ear.data is None and not self.ear.fft is None:
            pcmMax=np.max(np.abs(self.ear.data))
            if self.fileLoaded:
                pass
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
            elif self.display=="Loaded buff":
                pen=pyqtgraph.mkPen(color='b')
                self.grPCM.setYRange(self.loadedYmin, self.loadedYmax)
                self.grPCM.plot(self.loadedBuffX[:192000], self.loadedBuff[:192000].astype('float64'), pen=pen, clear=True)
                #print(len(self.loadedBuffX))
                #print(len(self.loadedBuff))
            elif self.display=="buf":
                #self.grPCM.setYRange(-np.iinfo('int16').max, np.iinfo('int16').max)
                pen=pyqtgraph.mkPen(color='g')
                self.ear.databuff = self.ear.databuff.astype('float64')
                self.grPCM.plot(self.ear.databuffx,self.ear.databuff,pen=pen,clear=True)
                self.ear.databuff = self.ear.databuff.astype('int16')

            if (self.display2=="fft"):
                if self.display=="Loaded buff":
                    pen=pyqtgraph.mkPen(color='r')
                    self.grFFT.plotItem.setRange(yRange=[0,1])
                    self.grFFT.plot(self.loadedFTTx[:300],self.loadedFTT[:300]/self.maxLoadFTT,pen=pen,clear=True)
                else:
                    pen=pyqtgraph.mkPen(color='r')
                    if self.averagingFrames:
                        self.ear.fft = signal_averaging(self.ear.fft, self.averageFrames)
                    if self.distanceSet:
                        self.grFFT.plotItem.setRange(yRange=[0,1])
                        self.grFFT.plot(self.distancex[:500],self.ear.fft[:500]/self.maxFFT,pen=pen,clear=True)
                    else:
                        self.grFFT.plotItem.setRange(yRange=[0,1])
                        self.grFFT.plot(self.ear.fftx[:500],self.ear.fft[:500]/self.maxFFT,pen=pen,clear=True)
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
    
    def setBandwidth(self):
        num, ok = self.w.getBandwidth(self.volume)
        if ok:
            self.bandwidth = num * 10e6
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
        num, ok = self.w.getFreqInt(1/float(self.freq))
        if ok:
            self.ramp_time = num
            self.freq = 1/ramp
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
    def setAverageFrames(self):
        num, ok = self.w.averageFrames(self.averageFrames)
        if ok:
            if num > 0:
                self.averageFrames = num
                self.averagingFrames = True
                if self.display == "Loaded buff":
                    if self.averagingFrames:
                        self.loadedFTT = signal_averaging(self.loadedFTT, self.averageFrames)

            if num <= 0:
                self.averageFrames = 0
                self.averagingFrames = False

    
    def getSRate(self):
        num, ok = self.w.getSRate(self.sample_rate)
        if ok:
            self.sample_rate = num
            self.playable, self.sawtooth = generate_wave(self.currentGeneratorType, freq=self.freq,
                volume=self.volume, sample_rate=self.sample_rate, phase_shift=self.phase_shift)
    def setDistance(self):
        if self.distanceSet == False:
            if self.display == "Loaded buff":
                self.loadedFTTx = distance_scale(self.loadedFTTx, self.c, self.bandwidth, self.ramp_time)
            self.distanceSet = True
            self.distancex = distance_scale(self.ear.fftx, self.c, self.bandwidth, self.ramp_time)
        else:
            self.distanceSet = False
            self.loadedFTTx, self.loadedFTT = getFFT(self.loadedBuff[0:int(wav.getframerate()*ramptime)], wav.getframerate())
            if self.averagingFrames:
                self.loadedFTT = signal_averaging(self.loadedFTT, self.averageFrames)


        

    def setSteerAngle(self):
        num, ok = self.w.steerAngle(self.steer_angle)
        if ok:
            self.steer_angle = num
            print(self.steer_angle)

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

    def loadfilebutton(self):
        #options = QFileDialog.Options()
        #option |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", "All Files (*)")
        if fileName:
            self.loadFileName = fileName
            wav = wave.open(self.loadFileName, mode='rb')
            chunksize = wav.getnframes()
            sizes = {1:'B', 2:'h', 4: 'i'}
            format_size = sizes[wav.getsampwidth()]
            fmt = "<" + format_size * wav.getnchannels() * chunksize
            ramptime = 10e-3
            
            decoded = struct.unpack(fmt, wav.readframes(int(chunksize)))
            out= np.asarray(decoded)
            out = np.reshape(out, (wav.getnchannels(), chunksize), order='F')
            self.loadedBuff = out[0]
            self.loadFrameRate = wav.getframerate()
            self.loadedBuffX = np.arange(len(self.loadedBuff))
            print(self.loadedBuff.shape)
            print(self.loadedBuff)
            print(self.loadedBuffX)
            self.grPCM.setYRange(self.loadedBuff.min()-10, self.loadedBuff.max()+10)
            self.loadedYmin = self.loadedBuff.min()-10
            self.loadedYmax = self.loadedBuff.max()+10
            self.loadedFTTx, self.loadedFTT = getFFT(self.loadedBuff[0:int(wav.getframerate()*ramptime)], wav.getframerate())
            print("LoadedFTTlen=", len(self.loadedFTT))
            if self.distanceSet:
                self.loadedFTTx = distance_scale(self.loadedFTTx, self.c, self.bandwidth, self.ramp_time)
            if self.averagingFrames:
                self.loadedFTT = signal_averaging(self.loadedFTT, self.averageFrames)
            self.maxLoadFTT = self.loadedFTT.max()
            self.fileLoaded = True
            self.display = "Loaded buff"
            self.textbox1.setText("Sample range = 0:{}".format(int(wav.getframerate()*ramptime)))


            #self.display2 = "Loaded buff FTT"
    def clickedLeft(self):
        if self.loadShift - self.ramp_time >= 0:
            self.loadShift -= self.ramp_time
        self.loadedFTTx, self.loadedFTT = getFFT(self.loadedBuff[0+int(self.loadShift*self.loadFrameRate):int(self.loadFrameRate*self.ramp_time)+int(self.loadShift*self.loadFrameRate)],self.loadFrameRate)
        if self.averagingFrames:
            self.loadedFTT = signal_averaging(self.loadedFTT, self.averageFrames)       
        self.maxLoadFTT = self.loadedFTT.max()
        self.textbox1.setText("Sample range = {}:{}".format(0+int(self.loadShift*self.loadFrameRate), int(self.loadFrameRate*self.ramp_time)+int(self.loadShift*self.loadFrameRate)))
        print(self.loadShift)
    def clickedRight(self):
        self.loadShift += self.ramp_time
        self.loadedFTTx, self.loadedFTT = getFFT(self.loadedBuff[0+int(self.loadShift*self.loadFrameRate):int(self.loadFrameRate*self.ramp_time)+int(self.loadShift*self.loadFrameRate)], self.loadFrameRate)
        if self.averagingFrames:
            self.loadedFTT = signal_averaging(self.loadedFTT, self.averageFrames)
        self.maxLoadFTT = self.loadedFTT.max()
        self.textbox1.setText("Sample range = {}:{}".format(0+int(self.loadShift*self.loadFrameRate), int(self.loadFrameRate*self.ramp_time)+int(self.loadShift*self.loadFrameRate)))

        print(self.loadShift)
       

    def loadSoundCard(self):
        self.display = "pcm"
        self.fileLoaded = False
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

def signal_averaging(signal, frames):
    N=len(signal)
    signal2 = np.zeros(N)
    signal2 = signal2+signal
    for i in range(N):
        summed = 1
        for j in range(frames):
            if i-j>=0 :
                signal[i] += signal2[i-j]
                summed += 1#The averaging is done out of place to avoid average buildup
            if i+j<N:
                signal[i] += signal2[i+j]
                summed += 1
        signal[i] = signal[i]/summed #all frames in for loop plus itself
    return signal

def distance_scale(signal, c, band, ramp):
    for i in range(len(signal)):
        signal[i] = signal[i] * c * ramp / (2*band)
    return signal

if __name__=="__main__":
    run()


