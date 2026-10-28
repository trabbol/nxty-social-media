#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio ORIGINALE del reel 30/10 "Per chi verra'" ep. 3 «La prima lezione», generato qui senza brani di terzi.
Stesso disegno dell'ep. 2 (audio_1029.py), con quattro righe di risposta e il salto di sessantuno anni: i tic seguono
la curva dell'animazione ma sono diradati a non meno di 14 ms l'uno dall'altro (44 su 61), perche' a meta' salto
sessantuno tic veri, a meno di 9 ms, diventerebbero un ronzio; l'ep. 1 ne aveva 45 a non meno di 12 ms.
Parente del tema della nonna (stesso pad in Re maggiore, stesse due note che salgono sulle righe, stesso
arpeggio sul cartello), con i segni propri della serie:
- un clic di registratore all'inizio (il pallino che pulsa);
- il salto degli anni: i tic di un contatore meccanico (61 anni, 44 tic diradati), con la stessa curva
  cubic-bezier(.65,0,.35,1) dell'animazione, sopra un soffio che sale; il pad passa da Re a Sol;
- le righe della risposta suonano le stesse due note del messaggio, con un'eco: la risposta fa eco.
Tempi = reel_1030.py. Mai suoni presi da altri."""
import numpy as np
from scipy.io import wavfile
SR, DUR = 48000, 15.9
N = int(SR * DUR); t_all = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1030)
SALTO, SALTO_DUR, ANNI = 6.0, 1.5, 61
DISTANZA_MIN = 0.014                # s fra due tic: sotto, a meta' salto, i tic diventano un ronzio

def add(sig, start_s, pan=0.0):
    i0 = int(start_s * SR); i1 = min(N, i0 + len(sig))
    if i1 <= i0: return
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

def tic(amp=0.035):
    """tic di contatore meccanico: un colpetto legnoso breve, due risonanze smorzate"""
    n = int(SR*0.03); t = np.arange(n)/SR
    y = 0.6*np.sin(2*np.pi*1650*t)*np.exp(-t/0.004) + 0.4*np.sin(2*np.pi*2950*t)*np.exp(-t/0.0025)
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(3)/3, mode="same") - np.convolve(z, np.ones(18)/18, mode="same")
    return amp * (y + 0.3*z*np.exp(-t/0.002)) * np.minimum(1, t/0.0008)

def soffio(dur, amp=0.03):
    """soffio che sale: rumore filtrato che passa da scuro a chiaro, inviluppo a campana"""
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n + 400)
    scuro = (np.convolve(z, np.ones(24)/24, mode="same") - np.convolve(z, np.ones(160)/160, mode="same"))[200:200+n]
    chiaro = (np.convolve(z, np.ones(4)/4, mode="same") - np.convolve(z, np.ones(30)/30, mode="same"))[200:200+n]
    w = t / dur
    return amp * ((1-w)*scuro*1.6 + w*chiaro*0.7) * np.sin(np.pi*w)**1.5

def bezier_tempi(n, p1=(0.65, 0.0), p2=(0.35, 1.0)):
    """istanti (0-1) in cui il contatore cambia anno: progresso y = (k-0.5)/n sulla curva cubic-bezier"""
    def xy(s):
        a, b = 3*(1-s)**2*s, 3*(1-s)*s**2
        return a*p1[0] + b*p2[0] + s**3, a*p1[1] + b*p2[1] + s**3
    out = []
    for k in range(1, n+1):
        y_t = (k - 0.5) / n; lo, hi = 0.0, 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if xy(mid)[1] < y_t: lo = mid
            else: hi = mid
        out.append(xy((lo+hi)/2)[0])
    return out

# pad: Re maggiore fino al salto, poi Sol maggiore (passaggio morbido durante il salto)
def accordo(freqs, amps):
    y = np.zeros(N)
    for f, a in zip(freqs, amps):
        for d in (-0.5, 0.5):
            y += a*np.sin(2*np.pi*(f+d)*t_all)
    return y
re_ = accordo((146.83, 220.00, 369.99), (.020, .015, .011))
sol = accordo((196.00, 293.66, 493.88), (.018, .014, .010))
x = np.clip((t_all - SALTO) / SALTO_DUR, 0, 1); x = x*x*(3 - 2*x)
pad = re_*(1 - x) + sol*x
env = np.minimum(1, t_all/0.6) * np.clip((DUR - t_all)/0.8, 0, 1)
pad *= env * (0.85 + 0.15*np.sin(2*np.pi*0.25*t_all))
L += pad; R += pad

add(click(), 0.02, pan=-0.2)                                        # il registratore parte
for k, s in enumerate((0.0, 1.30, 2.90, 4.50)):                     # righe del messaggio
    p = 0.18 if k % 2 == 0 else -0.18
    add(pluck(587.33), s + 0.05, pan=p); add(pluck(880.00), s + 0.125, pan=p)
add(soffio(1.9), SALTO - 0.25, pan=0.0)                             # il salto
tempi = [SALTO + u*SALTO_DUR for u in bezier_tempi(ANNI)]           # i tic con la curva dell'animazione, diradati
tenuti = [tempi[0]]
for x in tempi[1:-1]:
    if x - tenuti[-1] >= DISTANZA_MIN: tenuti.append(x)
if tempi[-1] - tenuti[-1] < DISTANZA_MIN: tenuti[-1] = tempi[-1]
else: tenuti.append(tempi[-1])
for j, x in enumerate(tenuti):
    add(tic(amp=0.030 + 0.006*np.sin(np.pi*j/(len(tenuti)-1))), x, pan=(-0.25 if j % 2 == 0 else 0.25))
add(pluck(783.99, amp=0.10, tau=0.6, dur=1.8), SALTO + SALTO_DUR + 0.02, pan=0.0)   # l'arrivo, in Sol
for k, s in enumerate((7.70, 9.20, 10.40, 11.60)):                  # righe della risposta: stesse note, con eco
    p = -0.18 if k % 2 == 0 else 0.18
    for ritardo, g in ((0.0, 1.0), (0.21, 0.38), (0.42, 0.15)):
        add(pluck(587.33, amp=0.15*g), s + 0.05 + ritardo, pan=p*(1 - ritardo*2))
        add(pluck(880.00, amp=0.15*g), s + 0.125 + ritardo, pan=p*(1 - ritardo*2))
for j, f in enumerate((146.83, 220.00, 293.66, 369.99, 440.00)):    # cartello: l'arpeggio della serie
    add(pluck(f, amp=0.11, tau=1.1, dur=2.4), 13.50 + j*0.045, pan=(-0.3 + j*0.15))

st = np.stack([L, R], axis=1); st /= np.max(np.abs(st)) / 0.70
wavfile.write("/home/claude/nxty/demo/audio_1030.wav", SR, (st*32767).astype(np.int16))
print("audio ok", DUR, "s, tic tenuti", len(tenuti), "su", ANNI, "- distanza minima",
      round(min(b - a for a, b in zip(tenuti, tenuti[1:]))*1000, 1), "ms")
