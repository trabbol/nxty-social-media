#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio ORIGINALE del reel 23/11 "Il vocale della nonna" ep. 17, generato qui senza brani di terzi.
Stesso tema della serie: pad in Re maggiore, clic di play, due note che salgono sulle righe parlate,
arpeggio sul cartello. Su [la padella bucata che scoppietta sul fuoco] il pad si abbassa e si sente la padella delle
castagne: sotto, il crepitio fitto del fuoco; sopra, tre scoppi secchi di castagna (schiocco chiaro, colpo sordo, due
crepitii che seguono), poi la padella scossa due volte (le castagne che rotolano e battono sul ferro, con un fruscio
basso), poi altri due scoppi. Suono mai usato nella serie. Mai suoni presi da altri. Tempi = reel_1123.py."""
import numpy as np
from scipy.io import wavfile
SR, DUR = 48000, 11.8
N = int(SR * DUR); t_all = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1123)

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

def ferro(amp=0.05, f1=3300.0, f2=5150.0):
    """un tocco dei ferri da maglia: due risonanze chiare che si spengono in due o tre millesimi, piu' un filo di rumore"""
    n = int(SR*0.022); t = np.arange(n)/SR
    y = 0.65*np.sin(2*np.pi*f1*t)*np.exp(-t/0.0022) + 0.35*np.sin(2*np.pi*f2*t + 0.7)*np.exp(-t/0.0015)
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(10)/10, mode="same")
    return amp * (y + 0.25*z*np.exp(-t/0.0008)) * np.minimum(1, t/0.0004)

def scatto(amp=0.05):
    """uno scatto della chiavetta del carillon: rumore chiaro brevissimo con una risonanza metallica a 4,1 kHz"""
    n = int(SR*0.018); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(8)/8, mode="same")
    y = np.sin(2*np.pi*4100*t)*np.exp(-t/0.0018)
    return amp * (0.55*z*np.exp(-t/0.0012) + 0.45*y) * np.minimum(1, t/0.0003)

def lamella(f, amp=0.05, dur=0.9):
    """una nota del carillon: lamella metallica, fondamentale con due armonici inarmonici (5,4 e 8,9) brevissimi"""
    t = np.arange(int(SR*dur)) / SR
    y = (np.sin(2*np.pi*f*t)*np.exp(-t/0.32) + 0.22*np.sin(2*np.pi*f*5.4*t)*np.exp(-t/0.03)
         + 0.08*np.sin(2*np.pi*f*8.9*t)*np.exp(-t/0.012))
    return amp * y * np.minimum(1, t/0.0015)

def lana(dur=0.13, amp=0.03):
    """la lana tirata dal gomitolo: rumore morbido (banda media), inviluppo a campana con un leggero tremolio"""
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n + 200)
    z = (np.convolve(z, np.ones(6)/6, mode="same") - np.convolve(z, np.ones(40)/40, mode="same"))[100:100+n]
    env = np.sin(np.pi*t/dur)**2 * (0.8 + 0.2*np.sin(2*np.pi*31*t))
    return amp * z * env

def scoppio(amp=0.06):
    """uno scoppio di castagna nella padella: schiocco secco (rumore chiaro brevissimo), un colpo sordo sotto e due
    crepitii che seguono"""
    n = int(SR*0.12); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    hi = np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(14)/14, mode="same")
    y = 0.75*hi*np.exp(-t/0.0035) + 0.5*np.sin(2*np.pi*170*t)*np.exp(-t/0.018)
    for d, a in ((0.028, 0.35), (0.061, 0.2)):
        i = int(d*SR); m = int(SR*0.006)
        y[i:i+m] += a * hi[:m] * np.exp(-np.arange(m)/SR/0.0015)
    return amp * y * np.minimum(1, t/0.0003)

def rotola(amp=0.02):
    """una castagna che rotola e batte sulla padella di ferro: clic corto con due risonanze metalliche"""
    n = int(SR*0.03); t = np.arange(n)/SR
    f1, f2 = rng.uniform(1700, 2100), rng.uniform(2800, 3300)
    y = 0.6*np.sin(2*np.pi*f1*t)*np.exp(-t/0.006) + 0.4*np.sin(2*np.pi*f2*t)*np.exp(-t/0.004)
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(3)/3, mode="same") - np.convolve(z, np.ones(16)/16, mode="same")
    return amp * (y + 0.4*z*np.exp(-t/0.002)) * np.minimum(1, t/0.0005)

def crepitio(dur, amp=0.008):
    """il fuoco sotto la padella: tanti crepitii minuscoli a caso, circa trenta al secondo"""
    n = int(SR*dur); out = np.zeros(n)
    k = int(rng.exponential(SR/30))
    while k < n - 300:
        m = 200; tt = np.arange(m)/SR
        z = rng.standard_normal(m)
        z = np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(10)/10, mode="same")
        out[k:k+m] += rng.uniform(0.4, 1.0) * z * np.exp(-tt/0.0008)
        k += int(rng.exponential(SR/30)) + 1
    tt = np.arange(n)/SR
    return amp * out * np.minimum(1, tt/0.08) * np.minimum(1, (dur-tt)/0.1)

def scossa(inizio, colpi=14, amp=0.02, swoosh=0.010):
    """la padella scossa una volta: le castagne che rotolano (colpi fitti al centro) e il fruscio basso del ferro"""
    dur = 0.17
    for s in np.sort(rng.uniform(0, dur - 0.02, colpi)):
        add(rotola(amp=amp * (0.55 + 0.45*np.sin(np.pi*s/dur))), inizio + s, pan=rng.uniform(-0.15, 0.25))
    n = int(SR*dur); tt = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(14)/14, mode="same") - np.convolve(z, np.ones(110)/110, mode="same")
    add(swoosh * z * np.sin(np.pi*tt/dur)**2, inizio, pan=0.05)

pad = np.zeros(N)
for f, a in ((146.83, .020), (220.00, .015), (369.99, .011)):
    for d in (-0.5, 0.5):
        pad += a*np.sin(2*np.pi*(f+d)*t_all)
env = np.minimum(1, t_all/0.6) * np.clip((DUR - t_all)/0.8, 0, 1)
giu = np.ones(N)                                   # il pad si abbassa mentre scoppietta la padella (2.7 - 4.2 s)
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
add(crepitio(1.35, amp=0.020), 2.80, pan=0.08)                                 # [la padella bucata che scoppietta sul fuoco]
for s, a in ((2.86, 0.125), (3.12, 0.108), (3.31, 0.116)):         #  tre scoppi radi
    add(scoppio(amp=a), s, pan=0.12)
for inizio in (3.46, 3.66):                                         #  la padella scossa due volte
    scossa(inizio, amp=0.045, swoosh=0.025)
for s, a in ((3.93, 0.125), (4.08, 0.099)):                        #  altri due scoppi
    add(scoppio(amp=a), s, pan=0.12)
for j, f in enumerate((146.83, 220.00, 293.66, 369.99, 440.00)):    # cartello
    add(pluck(f, amp=0.11, tau=1.1, dur=2.4), 9.35 + j*0.045, pan=(-0.3 + j*0.15))

st = np.stack([L, R], axis=1); st /= np.max(np.abs(st)) / 0.70
wavfile.write("/home/claude/nxty/demo/audio_1123.wav", SR, (st*32767).astype(np.int16))
print("audio ok", DUR, "s")
