#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reel di venerdi' 9 ottobre (id 76) — "Il vocale della nonna", ep. 4. Generato dal modello reel_1007.py.
Stessa forma della serie: intestazione di chat, bolla del vocale con la forma d'onda che si riempie d'oro
seguendo i minuti della trascrizione, scheda TRASCRIZIONE riga per riga. Vocale da 3:08 in cui la nonna
fa vedere tutte le tue foto alla Franca: il tratto "a pettine" (barre alte e basse alternate, regolari) e'
il dito che scorre le foto. Battute nuove, mai usate (vedi layout_usati.md). Chiusura «sono fiera di te»."""
import random, re
BASE = "/home/claude/nxty/demo"
FONTS = f"{BASE}/node_modules/@fontsource/plus-jakarta-sans/files"
GOLD, NOTTE, CREMA = "#DCA659", "#0B0B12", "#FDFBF6"

def k(t):
    """avvicina punto e virgola alla parola precedente (Plus Jakarta Sans 800 li stacca; solo testo, mai attributi)"""
    t = re.sub(r'([.,])(?![^<]*>)', r'<span class="pt">\1</span>', t)
    return t.replace('&hellip;', '<span class="pt">&hellip;</span>')

# (ms di comparsa, minuto del vocale, testo, e' silenzio?)
RIGHE = [
    (0,    "0:00", "&laquo;Ciao tesoro,<br>sono la nonna.&raquo;", False),
    (1300, "0:06", "&laquo;Sono qui con la Franca,<br>ti saluta.&raquo;", False),
    (2700, "0:11", "[le fa vedere<br>tutte le tue foto]", True),
    (4200, "1:43", "&laquo;Anche quella<br>nella vasca.&raquo;", False),
    (5700, "2:22", "&laquo;Dice che hai gli occhi<br>di tuo nonno.&raquo;", False),
    (7100, "2:55", "&laquo;Mandami una foto nuova,<br>queste le ha gi&agrave; viste.&raquo;", False),
]
DUR_VOCALE = 188
ONDA_MS = 9000
VIA = 9150
FINE = 9350
DURATA = FINE + 2450          # 11800

# forma d'onda: 40 barre; fra 0:11 e 1:43 il pettine regolare delle foto che scorrono, poi parlato
random.seed(1009)
N_BARRE = 40
barre = []
for i in range(N_BARRE):
    sec = (i + 0.5) / N_BARRE * DUR_VOCALE
    if 11 <= sec < 103:                      # scorre le foto: pettine regolare, alto/basso alternati
        h = 58 if i % 2 == 0 else 14
    else:                                    # parlato
        h = random.choice([18, 26, 34, 44, 52, 40, 30])
    barre.append(h)
def ONDA(col):
    return "".join(f'<i style="height:{h}px; background:{col};"></i>' for h in barre)

# il riempimento segue i tempi della trascrizione, non una retta
stops = [(0, 0), (1300, 6), (2700, 11), (4200, 103), (5700, 142), (7100, 175), (ONDA_MS, 188)]
kf = " ".join(f"{t/ONDA_MS*100:.2f}% {{ clip-path: inset(0 {100 - s/DUR_VOCALE*100:.2f}% 0 0); }}" for t, s in stops)

righe_html = []
for t, minuto, testo, silenzio in RIGHE:
    anim = "opacity:1; max-height:160px; margin-top:22px;" if t == 0 else f"animation:cresce 380ms {t}ms both;"
    cls = "riga silenzio" if silenzio else "riga"
    righe_html.append(f'<div class="{cls}" style="{anim}"><span class="min">{minuto}</span><span class="txt">{k(testo)}</span></div>')

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-600-normal.woff2') format('woff2'); font-weight:600; }}
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-700-normal.woff2') format('woff2'); font-weight:700; }}
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-800-normal.woff2') format('woff2'); font-weight:800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1920px; font-family:'PJS',sans-serif; -webkit-font-smoothing:antialiased;
  background:{CREMA}; color:{NOTTE}; overflow:hidden; }}
.scena {{ position:absolute; inset:0; background:{CREMA}; }}
@keyframes entra {{ to {{ opacity:1; }} }}
@keyframes esci  {{ to {{ opacity:0; }} }}
@keyframes cresce {{ 0% {{ opacity:0; max-height:0; margin-top:0; }} 55% {{ opacity:0; }} 100% {{ opacity:1; max-height:160px; margin-top:22px; }} }}
@keyframes riempi {{ {kf} }}
.main {{ position:absolute; inset:0; animation:esci 380ms {VIA}ms forwards; }}

.wmd {{ position:absolute; top:186px; left:0; right:0; display:flex; align-items:center; justify-content:center;
  gap:16px; font-weight:800; letter-spacing:.32em; font-size:34px; color:{NOTTE}; }}
.wmd i {{ color:{GOLD}; font-size:46px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-4px); }}

.testata {{ position:absolute; top:340px; left:76px; display:flex; align-items:center; gap:24px; }}
.avatar {{ width:88px; height:88px; border-radius:50%; background:{GOLD}; color:{CREMA}; display:flex; align-items:center;
  justify-content:center; font-size:42px; font-weight:800; }}
.nome {{ font-size:42px; font-weight:800; color:{NOTTE}; line-height:1.1; }}
.sotto {{ font-size:26px; font-weight:600; color:rgba(11,11,18,.48); margin-top:6px; }}

.bolla {{ position:absolute; top:464px; left:76px; width:840px; height:150px; background:#FFFFFF;
  border:2px solid rgba(11,11,18,.08); border-radius:44px 44px 44px 12px; box-shadow:0 18px 50px rgba(11,11,18,.06); }}
.play {{ position:absolute; left:32px; top:31px; width:88px; height:88px; border-radius:50%; background:{GOLD}; }}
.play:after {{ content:""; position:absolute; left:34px; top:25px; border-left:30px solid {CREMA};
  border-top:19px solid transparent; border-bottom:19px solid transparent; }}
.onda {{ position:absolute; left:150px; top:0; height:150px; width:560px; display:flex; align-items:center; gap:6px; }}
.onda i {{ display:block; width:8px; border-radius:4px; flex:0 0 auto; }}
.onda.letta {{ clip-path:inset(0 100% 0 0); animation:riempi {ONDA_MS}ms linear forwards; }}
.durata {{ position:absolute; right:36px; top:55px; font-size:30px; font-weight:700; color:rgba(11,11,18,.46); }}

.scheda {{ position:absolute; top:660px; left:76px; right:76px; border-radius:40px;
  background:rgba(220,166,89,.12); border:2px solid rgba(220,166,89,.36); padding:42px 50px 46px; }}
.etichetta {{ font-size:25px; font-weight:800; letter-spacing:.22em; color:{GOLD}; }}
.riga {{ display:grid; grid-template-columns:96px 1fr; column-gap:18px; margin-top:0; max-height:0; overflow:hidden; opacity:0; }}
.min {{ font-size:28px; font-weight:700; color:rgba(11,11,18,.42); padding-top:11px; }}
.txt {{ font-size:46px; font-weight:800; line-height:1.18; color:{NOTTE}; }}
.silenzio .txt {{ font-size:40px; font-weight:600; color:rgba(11,11,18,.42); }}
.pt {{ margin-left:-.075em; }}

.serie {{ position:absolute; top:264px; left:0; right:0; text-align:center; font-size:26px; font-weight:800;
  letter-spacing:.20em; color:{GOLD}; }}

.fine {{ position:absolute; inset:0; z-index:5; display:flex; flex-direction:column; align-items:center; justify-content:center;
  background:{CREMA}; opacity:0; animation:entra 600ms {FINE}ms forwards; padding-bottom:120px; }}
.fine .riga-f {{ font-size:66px; font-weight:800; line-height:1.16; text-align:center; color:{NOTTE}; }}
.fine .marchio {{ display:flex; align-items:center; gap:16px; font-weight:800; letter-spacing:.34em; font-size:40px; color:{NOTTE}; }}
.fine .marchio i {{ color:{GOLD}; font-size:52px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-4px); }}
</style></head><body>
<div class="scena">
  <div class="main">
    <div class="wmd"><i>&#8734;</i>NXTY</div>
    <div class="testata">
      <div class="avatar">N</div>
      <div><div class="nome">Nonna</div><div class="sotto">messaggio vocale</div></div>
    </div>
    <div class="bolla">
      <div class="play"></div>
      <div class="onda">{ONDA("rgba(11,11,18,.16)")}</div>
      <div class="onda letta">{ONDA(GOLD)}</div>
      <div class="durata">3:08</div>
    </div>
    <div class="scheda">
      <div class="etichetta">TRASCRIZIONE</div>
      {''.join(righe_html)}
    </div>
    <div class="serie">IL VOCALE DELLA NONNA &middot; EP. 4</div>
  </div>
  <div class="fine">
    <div class="riga-f">Tre minuti e otto secondi<br>per dire<br><span style="color:{GOLD};">&laquo;sono fiera di te&raquo;{k('.')}</span></div>
    <img src="file://{BASE}/logo_oro.png" style="width:118px; margin-top:92px;">
    <div class="marchio" style="margin-top:34px;"><i>&#8734;</i>NXTY</div>
    <div style="margin-top:30px; font-size:29px; font-weight:600; color:rgba(11,11,18,.50);">Link in bio</div>
  </div>
</div>
</body></html>"""

with open(f"{BASE}/reel_1009.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"scritto reel_1009.html — righe a {[r[0] for r in RIGHE]} ms, onda {ONDA_MS} ms, via {VIA}, cartello {FINE}, durata {DURATA} ms")
