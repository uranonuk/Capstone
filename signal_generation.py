from pydub import generators, utils, AudioSegment
import numpy as np
import math
from random import rand

#wave types include sine, pulse, square, sawtooth, triagle
def generate_wave(wave_type, freq=10, bit_depth=16, duration=1000, volume=0):
    if wave_type == 'sine':
        wave = generators.Sine(freq=freq).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'pulse':
        wave = generators.Pulse(freq=freq).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'square':
        wave = generators.Sawtooth(freq=freq).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'sawtooth':
        wave = generators.Sawtooth(freq=freq).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'triangle':
        wave = generators.Triangle(freq=freq).to_audio_segment(duration=duration, volume=volume)
    #wave is an AudioSegment
    wave = wave.get_array_of_samples()
    wave = np.array(wave)
    return wave

def signal_averaging(signal, replicates):
    N=len(signal)
    even = np.zeros(N)
    odd = np.zeros(N)
    actual_noise = np.zeroes(N)
    x = np.linspace(0, math.pi*4, N)
    for i in range(1, replicates + 1):
        noise = np.random.randn(N)
        actual_noise = actual_noise+noise
        if i%2:
            even = even + noise + x
        else:
            odd = odd + noise + x
    even_avg = even/(replicates/2)
    odd_avg = odd/(replicates/2)
    actual_avg = actual_noise/replicates
    return np.sqrt(np.mean(actual_avg**2))

        
