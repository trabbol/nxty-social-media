#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio ORIGINALE del reel 19/10 "Il vocale della nonna" ep. 7, generato qui senza brani di terzi.
Stesso tema della serie: pad in Re maggiore, clic di play, due note che salgono sulle righe parlate,
arpeggio sul cartello. Su [la moka che borbotta] il pad si abbassa e si sente la moka che sale: bolle
corte e scure (un tonfo che scende di tono, piu' un filo di rumore) sempre piu' fitte e piu' forti,
come la rampa della forma d'onda, e alla fine il soffio del vapore che si spegne mentre torna il pad.
Mai suoni presi da altri. Tempi = reel_1019.py."""
import numpy as np
from scipy.io import wavfile
SR, DUR = 48000, 11.8
N = int(SR * DUR); t_all = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1019)

def add(sig, start_s, pan=0.0):
    i0 = int(start_s * SR); i1 = min(N, i0 + len(sig))
    gl, gr = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i0:i1] += sig[:i1-i0] * gl * 1.41; R[i0:i1] += sig[:i1-i0] * gr * 1.41

def pluck(f, amp=0.15, tau=0.30, dur=1.3):
    t = np.arange(int(SR * dur)) / SR
    y = (np.sin(2*np.pi*f*t)*np.exp(-t/tau) + 0.28*np.sin(2*np.pi*2*f*t)*np.exp(-t/(tau*.45))
         + 0.08*np.sin(2*np.pi*3*f*t)*np.exp(-t/(tau*.25)))
    return amp * y * np.minimum(1, t/0.004)

def click(amp=0.07):
    n = int(SR*0.025); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(5)/5, mode="same") - np.convolve(z, np.ones(36)/36, mode="same")
    return amp * z * np.exp(-t/0.005)

def clink(amp=0.05):
    t = np.arange(int(SR*0.35)) / SR
    y = sum(a*np.sin(2*np.pi*f*t) for f, a in ((1870, 1.0), (2655, .6), (3310, .45), (4790, .25)))
    return amp * y * np.exp(-t/0.06) * np.minimum(1, t/0.002)

def brusio(dur=1.45, amp=0.045):
    """voce di televisore lontano: banda 300-3000 Hz, inviluppo a 4-6 sillabe al secondo"""
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(8)/8, mode="same") - np.convolve(z, np.ones(80)/80, mode="same")
    sill = np.zeros(n); k = 0
    while k < n:
        lung = int(SR*rng.uniform(0.11, 0.24)); pausa = int(SR*rng.uniform(0.03, 0.09))
        seg = np.sin(np.pi*np.arange(min(lung, n-k))/max(1, lung))**1.5
        sill[k:k+len(seg)] = seg * rng.uniform(0.6, 1.0); k += lung + pausa
    env = np.minimum(1, t/0.08) * np.minimum(1, (dur-t)/0.12)
    return amp * z * sill * env

def forchetta(amp=0.03):
    """un colpo di forchetta sulla ciotola: ceramica acuta che si spegne subito, piu' un filo di rumore"""
    n = int(SR*0.09); t = np.arange(n)/SR
    y = sum(a*np.sin(2*np.pi*f*t) for f, a in ((2310, 1.0), (3170, .55), (4420, .3)))
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(3)/3, mode="same") - np.convolve(z, np.ones(20)/20, mode="same")
    return amp * (y * np.exp(-t/0.012) + 0.35 * z * np.exp(-t/0.006)) * np.minimum(1, t/0.0015)

def fruscio(dur=0.13, amp=0.04):
    """dito che scorre una foto sul vetro: rumore che passa da scuro a chiaro, inviluppo morbido"""
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n + 200)
    scuro = (np.convolve(z, np.ones(10)/10, mode="same") - np.convolve(z, np.ones(90)/90, mode="same"))[100:100+n]
    chiaro = (np.convolve(z, np.ones(3)/3, mode="same") - np.convolve(z, np.ones(24)/24, mode="same"))[100:100+n]
    w = t / dur
    return amp * ((1-w)*scuro + w*chiaro*0.8) * np.sin(np.pi*t/dur)**2

def tocco(amp=0.06):
    n = int(SR*0.02); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(4)/4, mode="same") - np.convolve(z, np.ones(30)/30, mode="same")
    return amp * z * np.exp(-t/0.004)

def respiro(dur=0.85, amp=0.05):
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(12)/12, mode="same") - np.convolve(z, np.ones(120)/120, mode="same")
    env = np.sin(np.pi * t / dur) ** 2
    return amp * z * env

def bolla(amp=0.03):
    """una bolla della moka: tonfo breve che scende di tono (da circa 640 a 300 Hz) e si spegne, piu' un filo di rumore"""
    n = int(SR*0.06); t = np.arange(n)/SR
    f = 300 + 340*np.exp(-t/0.012)
    ph = 2*np.pi*np.cumsum(f)/SR
    y = np.sin(ph)*np.exp(-t/0.016)
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(14)/14, mode="same") - np.convolve(z, np.ones(110)/110, mode="same")
    return amp * (y + 0.5 * z * np.exp(-t/0.01)) * np.minimum(1, t/0.002)

def vapore(dur=0.42, amp=0.022):
    """il soffio del vapore alla fine: rumore chiaro che sale piano e si spegne"""
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(12)/12, mode="same")
    env = np.minimum(1, t/0.08) * np.clip((dur - t)/0.25, 0, 1)
    return amp * z * env

pad = np.zeros(N)
for f, a in ((146.83, .020), (220.00, .015), (369.99, .011)):
    for d in (-0.5, 0.5):
        pad += a*np.sin(2*np.pi*(f+d)*t_all)
env = np.minimum(1, t_all/0.6) * np.clip((DUR - t_all)/0.8, 0, 1)
giu = np.ones(N)                                   # il pad si abbassa mentre sale il caffe' (2.7 - 4.2 s)
a, b = (t_all >= 2.7) & (t_all < 2.9), (t_all >= 4.05) & (t_all < 4.25)
giu[a] = 1 - (t_all[a]-2.7)/0.2*0.6
giu[(t_all >= 2.9) & (t_all < 4.05)] = 0.4
giu[b] = 0.4 + (t_all[b]-4.05)/0.2*0.6
pad *= env * giu * (0.85 + 0.15*np.sin(2*np.pi*0.25*t_all))
L += pad; R += pad

add(click(), 0.02, pan=-0.2)
for k, s in enumerate((0.0, 1.30, 4.20, 5.70, 7.10)):              # righe parlate
    p = 0.18 if k % 2 == 0 else -0.18
    add(pluck(587.33), s + 0.05, pan=p); add(pluck(880.00), s + 0.125, pan=p)
s, j = 2.80, 0                                                       # [la moka che borbotta]
while s < 3.72:                                                     # bolle sempre piu' fitte e piu' forti
    w = (s - 2.80) / 0.92
    add(bolla(amp=0.016 + 0.026 * w), s, pan=(0.12 if j % 2 == 0 else 0.22))
    s += 0.17 - 0.11 * w + (0.012 if j % 3 == 1 else 0.0); j += 1
add(vapore(), 3.70, pan=0.18)                                       # il vapore, poi torna il pad
for j, f in enumerate((146.83, 220.00, 293.66, 369.99, 440.00)):    # cartello
    add(pluck(f, amp=0.11, tau=1.1, dur=2.4), 9.35 + j*0.045, pan=(-0.3 + j*0.15))

st = np.stack([L, R], axis=1); st /= np.max(np.abs(st)) / 0.70
wavfile.write("/home/claude/nxty/demo/audio_1019.wav", SR, (st*32767).astype(np.int16))
print("audio ok", DUR, "s")
