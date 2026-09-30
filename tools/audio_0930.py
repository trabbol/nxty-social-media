#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio ORIGINALE del reel 30/9 "Il vocale della nonna" ep. 1 — generato qui, nessun brano di terzi.
Pad in Re maggiore; un clic di "play" all'inizio; due note che salgono a ogni riga nuova della trascrizione;
durante "[otto secondi di niente]" la musica CALA QUASI A ZERO (la battuta e' il silenzio);
quattro note che scendono sui quattro "ciao"; arpeggio lungo sul cartello. Tempi = reel_0930.py."""
import numpy as np
from scipy.io import wavfile
SR, DUR = 48000, 11.8
N = int(SR * DUR); t_all = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)

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
    z = np.random.default_rng(30).standard_normal(n)
    z = np.convolve(z, np.ones(5)/5, mode="same") - np.convolve(z, np.ones(36)/36, mode="same")
    return amp * z * np.exp(-t/0.005)

# pad Re maggiore, con il "buco" del silenzio fra 4.3 e 5.8 s
pad = np.zeros(N)
for f, a in ((146.83, .020), (220.00, .015), (369.99, .011)):
    for d in (-0.5, 0.5):
        pad += a*np.sin(2*np.pi*(f+d)*t_all)
env = np.minimum(1, t_all/0.6) * np.clip((DUR - t_all)/0.8, 0, 1)
buco = np.ones(N)
giu, su = (t_all >= 4.3) & (t_all < 4.55), (t_all >= 5.6) & (t_all < 5.8)
buco[giu] = 1 - (t_all[giu]-4.3)/0.25*0.94
buco[(t_all >= 4.55) & (t_all < 5.6)] = 0.06
buco[su] = 0.06 + (t_all[su]-5.6)/0.2*0.94
pad *= env * buco * (0.85 + 0.15*np.sin(2*np.pi*0.25*t_all))
L += pad; R += pad

add(click(), 0.02, pan=-0.2)                                   # il "play"
for k, s in enumerate((0.0, 1.30, 2.80, 5.80)):                # righe parlate
    p = 0.18 if k % 2 == 0 else -0.18
    add(pluck(587.33), s + 0.05, pan=p); add(pluck(880.00), s + 0.125, pan=p)   # Re5 -> La5
for j, f in enumerate((880.00, 739.99, 587.33, 440.00)):       # "Ciao. Ciao, ciao, ciao."
    add(pluck(f, amp=0.14, tau=0.20), 7.30 + j*0.16, pan=(0.25 - j*0.16))
for j, f in enumerate((146.83, 220.00, 293.66, 369.99, 440.00)):  # arpeggio sul cartello
    add(pluck(f, amp=0.11, tau=1.1, dur=2.4), 9.35 + j*0.045, pan=(-0.3 + j*0.15))

st = np.stack([L, R], axis=1); st /= np.max(np.abs(st)) / 0.70
wavfile.write("/home/claude/nxty/demo/audio_0930.wav", SR, (st*32767).astype(np.int16))
print("audio ok", DUR, "s")
