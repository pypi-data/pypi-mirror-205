import os
import numpy as np
from matplotlib import pyplot as plt
import IPython.display as ipd
import librosa

def print_plot_play(path2file, sr=None):
    """ 
        - Prints & Plots information about an audio singal,
        - Creates player
        
    """
    signal, sr = librosa.load(path2file, sr=sr)
    text = 'audiofile: ' + np.char.split(path2file, sep ='/').item(-1)[-1]
    print('%s Fs = %d, x.shape = %s, x.dtype = %s' % (text, sr, signal.shape, signal.dtype))
    
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(12, 7))

    axs[0].plot(signal, color='gray')
    axs[0].set_xlabel('Time (samples)')
    axs[0].set_ylabel('Amplitude')
    axs[1].phase_spectrum(signal, Fs=sr, color='grey')
    axs[2].magnitude_spectrum(signal, Fs=sr, scale='dB', color='grey')
    fig.tight_layout()
    plt.show()
    
    ipd.display(ipd.Audio(data=signal, rate=sr))
    
    return signal, sr
