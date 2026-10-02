#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio ORIGINALE del reel 2/10 "Il vocale della nonna" ep. 2 — generato qui, nessun brano di terzi.
Stesso tema della serie (pad in Re maggiore, clic di play, due note che salgono sulle righe parlate,
arpeggio sul cartello). In piu': tintinnii metallici brevi sulle [pentole] e, sul [nonno che respira],
il pad cala quasi a zero e restano due respiri di rumore filtrato. Tempi = reel_1002.py."""
import numpy as np
from scipy.io import wavfile
SR, DUR = 48000, 11.8
N = int(SR * DUR); t_all = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1002)

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

def respiro(dur=0.85, amp=0.05):
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(12)/12, mode="same") - np.convolve(z, np.ones(120)/120, mode="same")
    env = np.sin(np.pi * t / dur) ** 2
    return amp * z * env

pad = np.zeros(N)
for f, a in ((146.83, .020), (220.00, .015), (369.99, .011)):
    for d in (-0.5, 0.5):
        pad += a*np.sin(2*np.pi*(f+d)*t_all)
env = np.minimum(1, t_all/0.6) * np.clip((DUR - t_all)/0.8, 0, 1)
giu = np.ones(N)                                   # il pad cala sul nonno che respira (7.1 - 9.0 s)
a, b = (t_all >= 7.1) & (t_all < 7.35), (t_all >= 8.8) & (t_all < 9.0)
giu[a] = 1 - (t_all[a]-7.1)/0.25*0.9
giu[(t_all >= 7.35) & (t_all < 8.8)] = 0.10
giu[b] = 0.10 + (t_all[b]-8.8)/0.2*0.9
pad *= env * giu * (0.85 + 0.15*np.sin(2*np.pi*0.25*t_all))
L += pad; R += pad

add(click(), 0.02, pan=-0.2)
for k, s in enumerate((0.0, 1.30, 4.20, 5.70)):                    # righe parlate
    p = 0.18 if k % 2 == 0 else -0.18
    add(pluck(587.33), s + 0.05, pan=p); add(pluck(880.00), s + 0.125, pan=p)
for j, s in enumerate((2.72, 2.88, 3.10, 3.34)):                    # [rumore di pentole]
    add(clink(), s, pan=(-0.3 + j*0.2))
add(respiro(), 7.30, pan=0.0); add(respiro(dur=0.95), 8.15, pan=0.0)   # [il nonno respira]
for j, f in enumerate((146.83, 220.00, 293.66, 369.99, 440.00)):    # cartello
    add(pluck(f, amp=0.11, tau=1.1, dur=2.4), 9.35 + j*0.045, pan=(-0.3 + j*0.15))

st = np.stack([L, R], axis=1); st /= np.max(np.abs(st)) / 0.70
wavfile.write("/home/claude/nxty/demo/audio_1002.wav", SR, (st*32767).astype(np.int16))
print("audio ok", DUR, "s")
