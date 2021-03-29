from scipy import signal
from scipy.fft import fftshift
import matplotlib.pyplot as plt
import numpy as np

def plot_spectogram(data, sampleRate):
    print(data)
    data = np.array(data)
    f, t, Sxx = signal.spectrogram(data, sampleRate)
    plt.pcolormesh(t, f, Sxx, shading='gouraud')
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()