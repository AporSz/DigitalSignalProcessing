import numpy as np
import matplotlib.pyplot as plt

N = 4096
fs = 2048
dt = 1/fs
fsamp = 128

fgood = 32
dgood = 1/fgood
Ngood = N * fgood//fs
fbad = 8
dbad = 1/fbad
Nbad = N * fbad//fs

rect_lim = 10

freq = np.fft.fftshift(np.fft.fftfreq(N, dt))
F = np.zeros_like(freq)
F[np.abs(freq) < rect_lim] = 1

t = np.arange(-N//2, N//2) * dt
f = np.real(np.fft.fftshift(np.fft.ifft(np.fft.ifftshift(F)))) * fs

plt.plot(freq, F)
plt.show()

plt.plot(t, f)
plt.show()

t_bad = np.arange(-Nbad//2, Nbad//2) * dbad
step = fs // fbad
f_bad_samp = f[::step]

t_good = np.arange(-Ngood//2, Ngood//2) * dgood
step = fs // fgood
f_good_samp = f[::step]

plt.stem(t_good, f_good_samp, linefmt='b:')
plt.stem(t_bad, f_bad_samp, linefmt='r--')
plt.plot(t, f, 'k')
# plt.xlim([-0.4, 0.4])
plt.show()

freq_good = np.fft.fftshift(np.fft.fftfreq(Ngood, dgood))
freq_bad = np.fft.fftshift(np.fft.fftfreq(Nbad, dbad))
Fgood = np.fft.fftshift(np.fft.fft(np.fft.fftshift(f_good_samp))) * dgood
Fbad = np.fft.fftshift(np.fft.fft(np.fft.fftshift(f_bad_samp))) * dbad

plt.plot(freq, F, 'k')
plt.stem(freq_good, Fgood, 'b:')
plt.stem(freq_bad, Fbad, 'r--')
plt.xlim([-15, 15])
plt.show()
