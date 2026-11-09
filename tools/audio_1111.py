#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio ORIGINALE del reel 11/11 "Il vocale della nonna" ep. 14, generato qui senza brani di terzi.
Stesso tema della serie: pad in Re maggiore, clic di play, due note che salgono sulle righe parlate,
arpeggio sul cartello. Su [chiude la scatola con due giri di scotch] il pad si abbassa e si sentono due giri di nastro
da pacchi: il nastro che si srotola (rumore chiaro battuto dallo scatto della colla che si stacca, sempre piu' veloce,
con un fischio acuto sopra) e lo strappo sul bordo dentellato, con la mano che preme il nastro sul cartone; due volte,
come i due nastri e i due strappi della forma d'onda. Suono mai usato nella serie. Mai suoni presi da altri.
Tempi = reel_1111.py."""
import numpy as np
from scipy.io import wavfile
SR, DUR = 48000, 11.8
N = int(SR * DUR); t_all = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1111)

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

def scotch(dur=0.40, amp=0.085, f0=170.0, f1=310.0):
    """lo scotch da pacchi che si srotola: rumore chiaro (banda alta) battuto dallo scatto della colla che si stacca
    (impulsi stretti da f0 a f1 Hz, un po' irregolari: il nastro accelera), con un fischio acuto che vibra sopra"""
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n + 80)
    chiaro = (np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(22)/22, mode="same"))[40:40+n]
    f = f0 + (f1 - f0) * (t/dur)
    fase = 2*np.pi*np.cumsum(f * (1 + 0.04*rng.standard_normal(n)))/SR
    scatti = (0.5 + 0.5*np.cos(fase)) ** 6
    fischio = (np.sin(2*np.pi*2350*t + 0.8*np.sin(2*np.pi*23*t)) + 0.5*np.sin(2*np.pi*3610*t + 1.3)) * 0.18
    env = np.minimum(1, t/0.02) * np.clip((dur - t)/0.03, 0, 1) * (0.75 + 0.25*t/dur)
    return amp * (chiaro * (0.30 + 0.70*scatti) + fischio * scatti) * env

def strappo(amp=0.12):
    """lo strappo del nastro sul bordo dentellato: uno schiocco chiaro di pochi millisecondi, poi la mano che preme il
    nastro sul cartone (tonfo sordo e corto, 150-215 Hz, con un soffio di cartone)"""
    n = int(SR*0.10); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    schiocco = (np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(14)/14, mode="same")) * np.exp(-t/0.004)
    tt = np.clip(t - 0.03, 0, None)
    cartone = (np.sin(2*np.pi*150*tt) + 0.6*np.sin(2*np.pi*215*tt + 0.5)) * np.exp(-tt/0.022) * (t >= 0.03) * 0.6
    soffio = np.convolve(z, np.ones(30)/30, mode="same") * np.exp(-tt/0.012) * (t >= 0.03) * 2.0
    return amp * (schiocco + cartone + soffio) * np.minimum(1, t/0.001)

pad = np.zeros(N)
for f, a in ((146.83, .020), (220.00, .015), (369.99, .011)):
    for d in (-0.5, 0.5):
        pad += a*np.sin(2*np.pi*(f+d)*t_all)
env = np.minimum(1, t_all/0.6) * np.clip((DUR - t_all)/0.8, 0, 1)
giu = np.ones(N)                                   # il pad si abbassa mentre si sente lo scotch (2.7 - 4.2 s)
a, b = (t_all >= 2.7) & (t_all < 2.9), (t_all >= 4.05) & (t_all < 4.25)
giu[a] = 1 - (t_all[a]-2.7)/0.2*0.65
giu[(t_all >= 2.9) & (t_all < 4.05)] = 0.35
giu[b] = 0.35 + (t_all[b]-4.05)/0.2*0.65
pad *= env * giu * (0.85 + 0.15*np.sin(2*np.pi*0.25*t_all))
L += pad; R += pad

add(click(), 0.02, pan=-0.2)
for k, s in enumerate((0.0, 1.30, 4.20, 5.70, 7.10)):              # righe parlate
    p = 0.18 if k % 2 == 0 else -0.18
    add(pluck(587.33), s + 0.05, pan=p); add(pluck(880.00), s + 0.125, pan=p)
add(scotch(amp=0.055), 2.78, pan=-0.10)                              # [chiude la scatola con due giri di scotch]:
add(strappo(amp=0.10), 3.19, pan=-0.06)                              #  primo nastro e primo strappo
add(scotch(dur=0.38, amp=0.058, f0=190.0, f1=330.0), 3.40, pan=0.08) #  secondo nastro, un po' piu' veloce
add(strappo(amp=0.11), 3.79, pan=0.10)                               #  secondo strappo
for j, f in enumerate((146.83, 220.00, 293.66, 369.99, 440.00)):    # cartello
    add(pluck(f, amp=0.11, tau=1.1, dur=2.4), 9.35 + j*0.045, pan=(-0.3 + j*0.15))

st = np.stack([L, R], axis=1); st /= np.max(np.abs(st)) / 0.70
wavfile.write("/home/claude/nxty/demo/audio_1111.wav", SR, (st*32767).astype(np.int16))
print("audio ok", DUR, "s")
