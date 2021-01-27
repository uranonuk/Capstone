from pydub import generators, utils, AudioSegment
import numpy as np
import math

#wave types include sine, pulse, square, sawtooth, triagle
def generate_wave(wave_type, sample_rate=44100, freq=10, bit_depth=16, duration=1000, volume=-20, phase_shift=0):
    if wave_type == 'sine':
        wave = generators.Sine(freq=freq, sample_rate=sample_rate, bit_depth=bit_depth).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'pulse':
        wave = generators.Pulse(freq=freq, sample_rate=sample_rate, bit_depth=bit_depth).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'square':
        wave = generators.Sawtooth(freq=freq, sample_rate=sample_rate, bit_depth=bit_depth).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'sawtooth':
        wave = generators.Sawtooth(freq=freq, sample_rate=sample_rate, bit_depth=bit_depth).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'triangle':
        wave = generators.Triangle(freq=freq, sample_rate=sample_rate, bit_depth=bit_depth).to_audio_segment(duration=duration, volume=volume)
    if wave_type == 'whitenoise':
        wave = generators.WhiteNoise(sample_rate=sample_rate, bit_depth=bit_depth).to_audio_segment(duration=duration, volume=volume)
    #wave is an AudioSegment
    wave = wave.get_array_of_samples()
    wave = np.array(wave)
    shift = int((phase_shift/(2*math.pi))*sample_rate/freq)
    wave = np.roll(wave, shift)
    return wave
