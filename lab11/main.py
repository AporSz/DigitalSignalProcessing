from pylab import *
from scipy import signal

ds = signal.dlti([1], [1, -0.5])

n, h = ds.impulse()

# plot(n, h[0], '.')
# show()

ht = zeros(len(h[0]))
ht[1:] = 0.5 ** arange(len(h[0])-1)

# plot(n, ht, '.-')
# yscale('log')
# show()

ds = signal.dlti([1], [1, -1, 0.5])
n, h = ds.impulse()

# stem(n, h[0], '.')
# show()

ht = zeros(len(h[0]))
ht[1:] = (lambda n: 2 * sin((n-1)*pi/4)/sqrt(2)**(n-1))(arange(1, len(h[0]))-1)
#
# plot(n, ht)
# stem(n, h[0])
# show()

# print(ds.to_zpk())

w, H = ds.freqresp()
w, gain, phase = ds.bode(w = w)

# semilogy(w, gain, '-k', w, abs(H), 'r-', linewidth=3, alpha=0.5) # not decibel scale


# semilogy(w, gain, '-k', linewidth=2, alpha=1) # decibel scale
# semilogy(w, 20 * log10(abs(H)), 'r-', linewidth=15, alpha=0.3)
#
# show()

d = 1 - pi / 40
k = (1 + d ** 2 - 2 * d / sqrt(2)) / (2 - sqrt(2))
print(k)

ds = signal.dlti(k * array([1, -sqrt(2), 1]), array([1, -sqrt(2) * d, d**2]), dt = 1/160)
w, gain, phase = ds.bode()

plot(w/(2 * pi), gain, '.-')
hlines([-3], [0], [80])
vlines([18, 22], [0, 0], [-200, -200])
grid()
show()