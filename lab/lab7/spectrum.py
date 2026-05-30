#--------------------------------------------------------------------------------------------
from pylab import *
import numpy as np
import types

#----------------------------------------------------------------    
def apply_window(x, window):
    """
    'window' is either a function that is applied elementwise on 'x'
    or
    it is an array of the same shape as 'x' that is multiplied with the later
    """
    if type(window) == types.FunctionType:
        return window(x)
    else:
        return window*x

#----------------------------------------------------------------    
def _spectral_helper(x, NFFT=256, Fs=2, detrend=detrend_none,
                 window=window_hanning, noverlap=0, pad_to=None):

    """

    """
    n = len(x)

    # zero pad if X is too short
    if len(x) < NFFT:
        x = np.resize(x, (NFFT,))
        x[n:] = 0

    if pad_to is None:
        pad_to = NFFT

    pad_to = 2**int(np.ceil(np.log2(pad_to))) # only powers of two
                
    numFreqs = pad_to//2+1

    ind = list(range(0, n-NFFT+1, NFFT-noverlap))
    numSlices  = len(ind)
    FFTSlices = np.zeros((numSlices, numFreqs), dtype=np.complex128)
    slices     = list(range(numSlices))
    normVal    = np.linalg.norm(apply_window(np.ones(NFFT), window))
    for iSlice in slices:
        FFTSlices[iSlice, :] = np.fft.fft(apply_window(detrend(x[ind[iSlice]:ind[iSlice]+NFFT]), window), n=pad_to)[:numFreqs]
    freqs = float(Fs)/NFFT*np.arange(numFreqs)
    FFTSlices[:, 1:-1] *= np.sqrt(2)
    return FFTSlices/normVal/np.sqrt(Fs), freqs
 #       Pxx[iCol] = np.divide(np.mean(abs(Slices)**2, axis=0), normVal)

#--------------------------------------------------------------------------------------------
def psd(x, NFFT=256, Fs=2, detrend=detrend_none, window=window_hanning, noverlap=0, pad_to=None):
    X, f =     _spectral_helper(x, NFFT, Fs, detrend, window, noverlap, pad_to)
    Pxx = np.abs(X)**2
    return Pxx.mean(axis=0), f


#---------------------------
from scipy.io import wavfile
import scipy.io
samplerate, data = wavfile.read("02. School Boy-9.wav")
print(data)
s, f = psd(data[:, 0], Fs=samplerate, NFFT=2**15, noverlap=2**14, detrend=detrend_mean)
figure(1)
semilogy(f, s)
grid()

# spectrogram
#---------------------------
time_resolution = 0.1 # sec (time window of the short time Fourier transforms)
s, f = _spectral_helper(data[:, 0], Fs=samplerate, NFFT=2**14, noverlap=2**14-int(time_resolution*samplerate), detrend=detrend_mean)
index_fmax = 2000 # 
s = s[:, :index_fmax]
figure(2)
imshow(log(abs(s).T)**2, aspect='auto', origin='lower', extent=[0, len(data)/samplerate, 0, f[index_fmax]], cmap=cm.jet)
ylim([0, f[index_fmax]]) # limit the shown frequency range 
xlabel('time (s)')
ylabel('freq (Hz)')
grid()

show()