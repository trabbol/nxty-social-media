#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio ORIGINALE del reel 29/9 "Dal mammese all'italiano" ep. 1 — MODELLO della serie.
Pad in La maggiore; tocco di tasto quando compare la frase della madre; due note che salgono (Mi-La)
a ogni "Ti voglio bene"; tre che scendono sulla battuta; arpeggio sul cartello. Tempi = reel_0929.py.
Ricostruito il 30/9 dopo l'azzeramento del container, identico all'originale."""
import numpy as np
from scipy.io import wavfile
SR, DUR = 48000, 11.58
N = int(SR * DUR); L = np.zeros(N); R = np.zeros(N); t_all = np.arange(N) / SR
def add(sig, start_s, pan=0.0):
    i0 = int(start_s * SR); i1 = min(N, i0 + len(sig))
    g_l, g_r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i0:i1] += sig[: i1 - i0] * g_l * 1.41; R[i0:i1] += sig[: i1 - i0] * g_r * 1.41
def pluck(f, amp=0.16, tau=0.32, dur=1.4):
    t = np.arange(int(SR * dur)) / SR
    y = (np.sin(2*np.pi*f*t) * np.exp(-t/tau) + 0.28*np.sin(2*np.pi*2*f*t) * np.exp(-t/(tau*0.45))
         + 0.08*np.sin(2*np.pi*3*f*t) * np.exp(-t/(tau*0.25)))
    return amp * y * np.minimum(1, t / 0.004)
def tap(amp=0.05):
    n = int(SR * 0.03); t = np.arange(n) / SR
    z = np.random.default_rng(7).standard_normal(n)
    z = np.convolve(z, np.ones(6)/6, mode="same") - np.convolve(z, np.ones(40)/40, mode="same")
    return amp * z * np.exp(-t/0.006)
pad = np.zeros(N)
for f, a in ((110.0, .020), (164.81, .016), (277.18, .012)):
    for d in (-0.6, 0.6):
        pad += a * np.sin(2*np.pi*(f+d)*t_all)
env = np.minimum(1, t_all/0.6) * np.clip((DUR - t_all)/0.8, 0, 1)
pad *= env * (0.85 + 0.15*np.sin(2*np.pi*0.25*t_all)); L += pad; R += pad
SRC = [0.0, 1.70, 3.40, 5.10, 7.40]; TVB = [0.55, 2.25, 3.95, 7.95]; BATTUTA = 5.65; FINE = 9.28
for s in SRC: add(tap(), s + 0.01, pan=-0.15)
for k, s in enumerate(TVB):
    p = 0.18 if k % 2 == 0 else -0.18
    add(pluck(659.25), s, pan=p); add(pluck(880.00), s + 0.075, pan=p)
for j, f in enumerate((880.00, 739.99, 587.33)): add(pluck(f, amp=0.15, tau=0.22), BATTUTA + j*0.11, pan=0.0)
for j, f in enumerate((220.00, 329.63, 440.00, 554.37, 659.25)):
    add(pluck(f, amp=0.11, tau=1.1, dur=2.4), FINE + j*0.045, pan=(-0.3 + j*0.15))
st = np.stack([L, R], axis=1); st /= np.max(np.abs(st)) / 0.70
wavfile.write("/home/claude/nxty/demo/audio_0929.wav", SR, (st * 32767).astype(np.int16))
print("audio ok:", DUR, "s")
