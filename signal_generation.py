from pydub import generators, utils, AudioSegment
import numpy as np

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
