#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audio ORIGINALE del reel 30/11 "Il vocale della nonna" ep. 19, generato qui senza brani di terzi.
Stesso tema della serie: pad in Re maggiore, clic di play, due note che salgono sulle righe parlate,
arpeggio sul cartello. Su [il cucchiaio sul coperchio, poi il barattolo che si apre] il pad si abbassa e si sente il
barattolo di sugo: quattro colpi del cucchiaio sul coperchio di latta, tutto intorno al bordo (lo schiocco del metallo,
le risonanze del coperchio e il colpo sordo del vetro pieno), sempre un poco piu' forti; il cucchiaio che fa leva sotto
il bordo (uno sfregamento metallico a scatti); il toc del coperchio che cede (lo scatto del bottone del sottovuoto, con
il soffio dell'aria che entra); il coperchio che gira sul vetro (un attrito a grani) e il barattolo posato sul tavolo
di legno. Come le barre della forma d'onda «colpi e toc». Suono mai usato nella serie. Mai suoni presi da altri.
Tempi = reel_1130.py."""
import numpy as np
from scipy.io import wavfile
SR, DUR = 48000, 11.8
AMP = {"colpo": 0.097, "leva": 0.028, "toc": 0.100, "soffio": 0.022, "giro": 0.034, "posato": 0.042}
N = int(SR * DUR); t_all = np.arange(N) / SR
L = np.zeros(N); R = np.zeros(N)
rng = np.random.default_rng(1130)

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

def interruttore(amp=0.08):
    """lo scatto dell'interruttore della macchinetta: clac di plastica (rumore medio di pochi millesimi), un tonfo corto
    a 240 Hz e il rimbalzo della levetta"""
    n = int(SR*0.045); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(4)/4, mode="same") - np.convolve(z, np.ones(26)/26, mode="same")
    y = 0.75*z*np.exp(-t/0.0022) + 0.40*np.sin(2*np.pi*240*t)*np.exp(-t/0.008)
    i = int(0.011*SR); m = int(0.004*SR)
    y[i:i+m] += 0.30*z[:m]*np.exp(-np.arange(m)/SR/0.0012)
    return amp * y * np.minimum(1, t/0.0003)

def motorino(dur, amp=0.03, f=208.0, su=0.14, giu=0.16):
    """il motorino della macchinetta: ronzio con le armoniche che calano, che parte da fermo (in su secondi arriva a
    f Hz), gira con un filo di ruvidita' e il fruscio delle spazzole, e si ferma (in giu secondi); piu' forte quando gira
    piu' veloce"""
    n = int(SR*dur); t = np.arange(n)/SR
    v = np.ones(n)
    a = t < su; v[a] = 0.2 + 0.8*np.sin(np.pi/2*t[a]/su)
    b = t > dur - giu; v[b] = 0.2 + 0.8*np.sin(np.pi/2*(dur - t[b])/giu)
    ph = 2*np.pi*np.cumsum(f*v)/SR
    y = sum(c*np.sin(k*ph + 0.4*k) for k, c in ((1, 1.0), (2, .62), (3, .40), (4, .26), (5, .16), (6, .10), (8, .05)))
    r = rng.standard_normal(n)
    r = np.convolve(r, np.ones(240)/240, mode="same"); r /= np.max(np.abs(r)) + 1e-9
    sp = rng.standard_normal(n)
    sp = np.convolve(sp, np.ones(6)/6, mode="same") - np.convolve(sp, np.ones(60)/60, mode="same")
    env = v**1.6 * np.minimum(1, t/0.01) * np.minimum(1, (dur - t)/0.02)
    return amp * (y*(1 + 0.18*r) + 0.35*sp) * env

def fresa(dur, profilo, amp=0.03, f=3100.0):
    """la fresa che taglia la chiave: il fischio dei denti della fresa (f Hz, con l'armonica e un anello metallico
    inarmonico, un filo tremolante) sopra un rumore chiaro di limatura; l'intensita' segue il profilo dei denti della
    chiave: a ogni dente la fresa morde (piu' forte e un poco piu' grave) e poi scorre"""
    n = int(SR*dur); t = np.arange(n)/SR
    k = len(profilo); h = np.array(profilo, float) / max(profilo)
    hv = np.interp(t/dur*k, np.arange(k) + 0.5, h)
    j = rng.standard_normal(n); j = np.convolve(j, np.ones(480)/480, mode="same"); j /= np.max(np.abs(j)) + 1e-9
    fi = f*(1 - 0.045*hv + 0.012*j)
    ph = 2*np.pi*np.cumsum(fi)/SR
    fischio = np.sin(ph) + 0.35*np.sin(2*ph + 0.5) + 0.30*np.sin(1.47*ph + 1.3)
    z = rng.standard_normal(n)
    lima = np.convolve(z, np.ones(3)/3, mode="same") - np.convolve(z, np.ones(14)/14, mode="same")
    env = (0.18 + 0.82*hv**1.3) * np.minimum(1, t/0.015) * np.minimum(1, (dur - t)/0.03)
    return amp * (0.45*fischio*(0.4 + 0.6*hv) + 1.0*lima) * env

def spazzola(dur, amp=0.02):
    """la spazzola che toglie le bave ai denti: fruscio fitto e morbido (banda media e alta) con il tremolio delle
    setole a 38 Hz"""
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n + 400)
    z = (np.convolve(z, np.ones(3)/3, mode="same") - np.convolve(z, np.ones(30)/30, mode="same"))[200:200+n]
    env = np.sin(np.pi*t/dur)**1.2 * (0.72 + 0.28*np.sin(2*np.pi*38*t))
    return amp * z * env

def colpo(amp=0.06, k=1.0):
    """un colpo del cucchiaio sul bordo del coperchio di latta: schiocco metallico brevissimo, quattro risonanze del
    coperchio smorzate dalla guarnizione (k sposta un poco l'altezza: il colpo cade ogni volta in un punto diverso del
    bordo), il tonfo sordo del vetro pieno di sugo e un filo di squillo del cucchiaio"""
    n = int(SR*0.16); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(9)/9, mode="same")
    lat = sum(a*np.sin(2*np.pi*f*k*t + ph)*np.exp(-t/d) for f, a, d, ph in
              ((1460, 1.0, 0.020, 0.0), (2930, .55, 0.014, 0.9), (4610, .32, 0.009, 1.7), (6840, .18, 0.006, 2.3)))
    vetro = np.sin(2*np.pi*410*t)*np.exp(-t/0.018)
    cucchiaio = np.sin(2*np.pi*3260*t + 0.4)*np.exp(-t/0.09)
    y = 0.55*z*np.exp(-t/0.0012) + 0.60*lat + 0.45*vetro + 0.06*cucchiaio
    return amp * y * np.minimum(1, t/0.0002)

def leva(dur=0.16, amp=0.012):
    """il cucchiaio che fa leva sotto il bordo del coperchio: sfregamento di metallo su metallo a scatti (attrito che si
    attacca e si stacca, circa 150 scatti al secondo) con la risonanza chiara del coperchio, sempre piu' forte"""
    n = int(SR*dur); t = np.arange(n)/SR
    out = np.zeros(n)
    k = 0
    while k < n - 240:
        m = 200; tt = np.arange(m)/SR
        z = rng.standard_normal(m)
        z = np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(7)/7, mode="same")
        g = z*np.exp(-tt/0.0009) + 0.5*np.sin(2*np.pi*rng.uniform(2800, 3400)*tt)*np.exp(-tt/0.0025)
        out[k:k+m] += rng.uniform(0.5, 1.0) * g
        k += int(SR/rng.uniform(120, 180))
    env = (0.35 + 0.65*t/dur) * np.minimum(1, t/0.01) * np.minimum(1, (dur - t)/0.012)
    return amp * out * env

def toc(amp=0.07):
    """il toc del coperchio che cede: lo scatto del bottone del sottovuoto (schiocco chiaro e una risonanza di latta a
    1,25 kHz che si spegne subito) e il corpo piu' basso del coperchio che si flette"""
    n = int(SR*0.09); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(2)/2, mode="same") - np.convolve(z, np.ones(12)/12, mode="same")
    y = (0.70*z*np.exp(-t/0.0016) + 0.85*np.sin(2*np.pi*1250*t)*np.exp(-t/0.010)
         + 0.30*np.sin(2*np.pi*2710*t + 0.6)*np.exp(-t/0.006) + 0.55*np.sin(2*np.pi*330*t)*np.exp(-t/0.016))
    return amp * y * np.minimum(1, t/0.0002)

def soffio(dur=0.09, amp=0.016):
    """l'aria che entra nel barattolo quando cede il sottovuoto: un soffio chiaro (rumore alto) che parte di colpo e si
    spegne in pochi centesimi"""
    n = int(SR*dur); t = np.arange(n)/SR
    z = rng.standard_normal(n + 200)
    z = (z[1:] - z[:-1])[100:100+n]
    z = np.convolve(z, np.ones(2)/2, mode="same")
    return amp * z * np.exp(-t/0.022) * np.minimum(1, t/0.002)

def giro(dur=0.20, amp=0.016):
    """il coperchio che gira sul filetto del vetro: attrito a grani irregolari (da 35 a 70 al secondo, ognuno uno
    sfregamento metallico di pochi millesimi) con un filo di risonanza del vetro, forte all'inizio e poi piu' leggero"""
    n = int(SR*dur); t = np.arange(n)/SR
    out = np.zeros(n)
    k = int(SR*0.004)
    while k < n - 400:
        m = int(SR*rng.uniform(0.003, 0.007)); tt = np.arange(m)/SR
        z = rng.standard_normal(m)
        z = np.convolve(z, np.ones(3)/3, mode="same") - np.convolve(z, np.ones(16)/16, mode="same")
        g = z*np.sin(np.pi*tt/(m/SR)) + 0.25*np.sin(2*np.pi*640*tt)*np.exp(-tt/0.004)
        out[k:k+m] += rng.uniform(0.5, 1.0) * g
        k += int(SR/rng.uniform(35, 70))
    env = (1.0 - 0.6*t/dur) * np.minimum(1, t/0.008) * np.minimum(1, (dur - t)/0.02)
    return amp * out * env

def posato(amp=0.05):
    """il barattolo posato sul tavolo di legno: tonfo basso a 120 Hz, il legno a 260 Hz e due risonanze corte del vetro"""
    n = int(SR*0.12); t = np.arange(n)/SR
    z = rng.standard_normal(n)
    z = np.convolve(z, np.ones(5)/5, mode="same") - np.convolve(z, np.ones(40)/40, mode="same")
    y = (0.80*np.sin(2*np.pi*120*t)*np.exp(-t/0.020) + 0.45*np.sin(2*np.pi*260*t)*np.exp(-t/0.012)
         + 0.25*np.sin(2*np.pi*1050*t)*np.exp(-t/0.008) + 0.12*np.sin(2*np.pi*2340*t + 0.8)*np.exp(-t/0.005)
         + 0.35*z*np.exp(-t/0.002))
    return amp * y * np.minimum(1, t/0.0008)

pad = np.zeros(N)
for f, a in ((146.83, .020), (220.00, .015), (369.99, .011)):
    for d in (-0.5, 0.5):
        pad += a*np.sin(2*np.pi*(f+d)*t_all)
env = np.minimum(1, t_all/0.6) * np.clip((DUR - t_all)/0.8, 0, 1)
giu = np.ones(N)                                   # il pad si abbassa mentre si apre il barattolo (2.7 - 4.2 s)
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
# [il cucchiaio sul coperchio, poi il barattolo che si apre]: i quattro colpi tutto intorno al bordo, sempre un poco
# piu' forti (le quattro barre alte della forma d'onda), la leva sotto il bordo, il toc, il coperchio che gira, posato
for s, g, kk, p in ((2.84, 0.70, 1.00, 0.16), (3.05, 0.82, 1.04, 0.06), (3.26, 0.92, 0.97, 0.14), (3.47, 1.00, 1.06, 0.04)):
    add(colpo(amp=AMP["colpo"]*g, k=kk), s, pan=p)
add(leva(0.16, amp=AMP["leva"]), 3.58, pan=0.10)                        #  il cucchiaio fa leva sotto il bordo
add(toc(amp=AMP["toc"]), 3.79, pan=0.08)                                #  toc: il sottovuoto cede
add(soffio(0.09, amp=AMP["soffio"]), 3.792, pan=0.08)                   #  l'aria che entra
add(giro(0.20, amp=AMP["giro"]), 3.88, pan=0.05)                        #  il coperchio che gira
add(posato(amp=AMP["posato"]), 4.12, pan=0.02)                          #  il barattolo posato sul tavolo
for j, f in enumerate((146.83, 220.00, 293.66, 369.99, 440.00)):    # cartello
    add(pluck(f, amp=0.11, tau=1.1, dur=2.4), 9.35 + j*0.045, pan=(-0.3 + j*0.15))

st = np.stack([L, R], axis=1); st /= np.max(np.abs(st)) / 0.70
wavfile.write("/home/claude/nxty/demo/audio_1130.wav", SR, (st*32767).astype(np.int16))
print("audio ok", DUR, "s")
