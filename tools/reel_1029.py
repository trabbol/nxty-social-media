#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reel di giovedi' 29 ottobre (id 96) — "Per chi verra'", ep. 2 «La prima parolaccia». Generato dal modello
reel_1023.py (ep. 1), stessa forma fissa della serie (campagna "Per chi verra'": chi lascia e chi riceve in dialogo).
Paolo, 38 anni, registra per suo figlio Tommaso, 3 anni, il giorno della sua prima parolaccia; trent'anni dopo Tommaso
risponde con le stesse parole: la risposta fa eco. Quattro righe di risposta invece di tre: tempi allungati a 15,9 s.
Forma fissa della serie: in alto la scheda REGISTRATO (bianca), con data, chi parla e per chi; le righe del
messaggio ci sono gia' tutte come barre grigie della loro forma e si scrivono una alla volta. Sotto, l'anno
in oro fra due fili. In basso, gia' dal primo fotogramma, la scheda ASCOLTATO tratteggiata: «Non ancora
ascoltato». Poi l'anno corre da 2026 a 2056 come un contachilometri, il fondo passa dal crema al notte e la
scheda in basso si accende: la risposta si scrive e fa eco. Cartello notte «Ci ha messo trent'anni ad arrivare. /
Per chi verra'.», con l'apostrofo tipografico stretto dalla classe .ap dentro k(). Personaggi inventati, dichiarati
dalla riga «UNA STORIA IMMAGINATA» sotto il titolo; nessun apostrofo nelle righe; caporale di chiusura con .gc; punto e
virgola avvicinati con k(). Impaginazione tutta in flusso (niente misure in JS)."""
import re
BASE = "/home/claude/nxty/demo"
FONTS = f"{BASE}/node_modules/@fontsource/plus-jakarta-sans/files"
GOLD, NOTTE, CREMA = "#DCA659", "#0B0B12", "#FDFBF6"

def k(t):
    """avvicina punto e virgola alla parola precedente (Plus Jakarta Sans 800 li stacca; solo testo, mai attributi)"""
    t = re.sub(r'([.,])(?![^<]*>)', r'<span class="pt">\1</span>', t)
    t = t.replace('&rsquo;', '<span class="ap">&rsquo;</span>')     # apostrofo stretto, come in caro_1027.py
    return t.replace('&hellip;', '<span class="pt">&hellip;</span>')

def q(t):
    return f"&laquo;{t}<span class='gc'>&raquo;</span>"

EP = 2
ANNO_DA, ANNO_A = 2026, 2056
DATA_DA, DATA_A = "Registrato il 29 ottobre 2026", "Ascoltato il 29 ottobre 2056"
CHI_DA, PER_DA = "Paolo, 38 anni", "per suo figlio Tommaso, 3&nbsp;anni"
CHI_A, PER_A = "Tommaso, 33 anni", "suo figlio"
# (ms in cui la riga si scrive, testo)
MESSAGGIO = [
    (0,    q("Oggi hai detto la tua prima&nbsp;parolaccia.")),
    (1300, q("A tavola, davanti alla nonna.")),
    (2900, q("Ho fatto la faccia seria.")),
    (4500, q("Poi sono andato in bagno a&nbsp;ridere.")),
]
SALTO, SALTO_DUR = 6000, 1500        # l'anno corre
NOTTE_DA, NOTTE_DUR = 6100, 900      # il fondo passa al notte
ACCESA = 7000                        # la scheda in basso si accende
RISPOSTA = [
    (7700,  q("Pap&agrave;, oggi mia figlia ha detto la sua prima&nbsp;parolaccia.")),
    (9200,  q("A tavola, davanti alla nonna.")),
    (10400, q("Ho fatto la faccia seria.")),
    (11600, q("Poi sono andato in bagno a&nbsp;ridere.")),
]
VIA, FINE = 13300, 13500
DURATA = FINE + 2400                 # 15900
ANNI = ANNO_A - ANNO_DA
CHIUSURA = "Ci ha messo<br>trent&rsquo;anni<br>ad arrivare."
ALT_ANNO = 124

def righe(lista):
    out = []
    for t, testo in lista:
        stato = ' style="color:inherit; --sk:transparent;"' if t == 0 else f' style="animation:scrivi 520ms {t}ms both;"'
        out.append(f'<div class="msg"><span class="t"{stato}>{k(testo)}</span></div>')
    return "".join(out)

anni_html = "".join(f"<div>{a}</div>" for a in range(ANNO_DA, ANNO_A + 1))

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-600-normal.woff2') format('woff2'); font-weight:600; }}
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-700-normal.woff2') format('woff2'); font-weight:700; }}
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-800-normal.woff2') format('woff2'); font-weight:800; }}
@property --sk {{ syntax:'<color>'; inherits:false; initial-value:rgba(11,11,18,.075); }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1920px; font-family:'PJS',sans-serif; -webkit-font-smoothing:antialiased;
  background:{CREMA}; color:{NOTTE}; overflow:hidden; }}
.scena {{ position:absolute; inset:0; background:{CREMA}; animation:anotte {NOTTE_DUR}ms ease-in-out {NOTTE_DA}ms forwards; }}
@keyframes anotte {{ to {{ background:{NOTTE}; }} }}
@keyframes entra {{ to {{ opacity:1; }} }}
@keyframes esci  {{ to {{ opacity:0; }} }}
@keyframes scrivi {{ 0% {{ color:transparent; }} 100% {{ color:var(--testo); --sk:transparent; }} }}
@keyframes rolla {{ to {{ transform:translateY(-{ANNI * ALT_ANNO}px); }} }}
@keyframes chiaro {{ to {{ color:{CREMA}; }} }}
@keyframes pulsa {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.2; }} }}
.main {{ position:absolute; inset:0; animation:esci 380ms {VIA}ms forwards; }}

.wmd {{ position:absolute; top:138px; left:0; right:0; display:flex; align-items:center; justify-content:center;
  gap:16px; font-weight:800; letter-spacing:.32em; font-size:32px; color:{NOTTE};
  animation:chiaro {NOTTE_DUR}ms ease-in-out {NOTTE_DA}ms forwards; }}
.wmd i {{ color:{GOLD}; font-size:44px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-4px); }}
.serie {{ position:absolute; top:206px; left:0; right:0; text-align:center; font-size:25px; font-weight:800;
  letter-spacing:.20em; color:{GOLD}; }}

.immaginata {{ position:absolute; top:250px; left:0; right:0; text-align:center; font-size:21px; font-weight:800;
  letter-spacing:.22em; color:rgba(220,166,89,.72); }}
.colonna {{ position:absolute; top:300px; left:72px; right:72px; display:flex; flex-direction:column; }}
.scheda {{ border-radius:40px; padding:36px 46px 42px; }}
.sopra {{ background:#FFFFFF; border:2px solid rgba(11,11,18,.07); box-shadow:0 18px 50px rgba(11,11,18,.07); --testo:{NOTTE}; }}
.etichetta {{ display:flex; align-items:center; gap:14px; font-size:26px; font-weight:800; letter-spacing:.14em;
  text-transform:uppercase; color:{GOLD}; }}
.rec {{ width:18px; height:18px; border-radius:50%; background:{GOLD}; flex:0 0 auto; animation:pulsa 1000ms ease-in-out 0ms 6; }}
.tri {{ width:0; height:0; flex:0 0 auto; border-left:18px solid {GOLD}; border-top:11px solid transparent; border-bottom:11px solid transparent; }}
.chi {{ margin-top:14px; font-size:33px; font-weight:800; line-height:1.22; }}
.chi span {{ font-weight:600; opacity:.55; }}
.msg {{ margin-top:20px; font-size:44px; font-weight:800; line-height:1.17; }}
.t {{ color:transparent; border-radius:12px; -webkit-box-decoration-break:clone; box-decoration-break:clone;
  background-image:linear-gradient(transparent 14%, var(--sk) 14%, var(--sk) 90%, transparent 90%); }}

.salto {{ margin-top:28px; height:{ALT_ANNO}px; display:flex; align-items:center; justify-content:center; gap:34px; }}
.filo {{ width:190px; height:2px; background:rgba(220,166,89,.55); }}
.anno {{ height:{ALT_ANNO}px; overflow:hidden; }}
.striscia {{ animation:rolla {SALTO_DUR}ms cubic-bezier(.65,0,.35,1) {SALTO}ms forwards; }}
.striscia div {{ height:{ALT_ANNO}px; line-height:{ALT_ANNO}px; font-size:100px; font-weight:800; color:{GOLD};
  font-variant-numeric:tabular-nums; letter-spacing:.02em; text-align:center; }}
.dopo {{ position:relative; height:34px; margin-top:2px; text-align:center; font-size:26px; font-weight:800; letter-spacing:.18em;
  color:{GOLD}; }}
.dopo span {{ position:absolute; left:0; right:0; top:0; }}
.dopo .ora {{ animation:esci 300ms {SALTO}ms forwards; }}
.dopo .poi {{ opacity:0; animation:entra 400ms {SALTO + SALTO_DUR}ms forwards; }}

.basso {{ position:relative; margin-top:24px; }}
.accesa {{ background:#15151F; border:2px solid rgba(220,166,89,.38); opacity:0; animation:entra 500ms {ACCESA}ms forwards;
  --testo:{CREMA}; }}
.accesa .chi {{ color:{CREMA}; }}
.accesa .t {{ --sk:rgba(253,251,246,.09); }}
.attesa {{ position:absolute; inset:0; border:3px dashed rgba(11,11,18,.22); animation:esci 450ms {NOTTE_DA + 250}ms forwards; }}
.attesa .etichetta {{ color:rgba(11,11,18,.45); }}
.attesa .tri {{ border-left-color:rgba(11,11,18,.45); }}
.attesa .chi {{ color:rgba(11,11,18,.45); }}
.attesa .vuoto {{ margin-top:26px; font-size:34px; font-weight:700; color:rgba(11,11,18,.36); }}
.attesa .barra {{ height:38px; border-radius:12px; background:rgba(11,11,18,.05); margin-top:26px; }}
.pt {{ margin-left:-.075em; }}
.gc {{ margin-left:-.06em; }}
.ap {{ margin:0 -.05em; }}

.fine {{ position:absolute; inset:0; z-index:5; display:flex; flex-direction:column; align-items:center; justify-content:center;
  background:{NOTTE}; opacity:0; animation:entra 600ms {FINE}ms forwards; padding-bottom:120px; }}
.fine .riga-f {{ font-size:64px; font-weight:800; line-height:1.16; text-align:center; color:{CREMA}; }}
.fine .marchio {{ display:flex; align-items:center; gap:16px; font-weight:800; letter-spacing:.34em; font-size:40px; color:{CREMA}; }}
.fine .marchio i {{ color:{GOLD}; font-size:52px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-4px); }}
</style></head><body>
<div class="scena">
  <div class="main">
    <div class="wmd"><i>&#8734;</i>NXTY</div>
    <div class="serie">PER CHI VERR&Agrave; &middot; EP. {EP}</div>
    <div class="immaginata">UNA STORIA IMMAGINATA</div>
    <div class="colonna">
      <div class="scheda sopra">
        <div class="etichetta"><span class="rec"></span>{DATA_DA}</div>
        <div class="chi">{CHI_DA} <span>&middot; {PER_DA}</span></div>
        {righe(MESSAGGIO)}
      </div>
      <div class="salto"><div class="filo"></div><div class="anno"><div class="striscia">{anni_html}</div></div><div class="filo"></div></div>
      <div class="dopo"><span class="ora">OGGI</span><span class="poi">{ANNI} ANNI DOPO</span></div>
      <div class="basso">
        <div class="scheda accesa">
          <div class="etichetta"><span class="tri"></span>{DATA_A}</div>
          <div class="chi">{CHI_A} <span>&middot; {PER_A}</span></div>
          {righe(RISPOSTA)}
        </div>
        <div class="scheda attesa">
          <div class="etichetta"><span class="tri"></span>{DATA_A}</div>
          <div class="chi">{CHI_A} &middot; {PER_A}</div>
          <div class="vuoto">Non ancora ascoltato</div>
          <div class="barra" style="width:72%;"></div>
          <div class="barra" style="width:48%; margin-top:16px;"></div>
          <div class="barra" style="width:63%; margin-top:16px;"></div>
        </div>
      </div>
    </div>
  </div>
  <div class="fine">
    <div class="riga-f">{k(CHIUSURA)}</div>
    <div class="riga-f" style="color:{GOLD}; margin-top:34px;">{k("Per chi verr&agrave;.")}</div>
    <img src="file://{BASE}/logo_oro.png" style="width:118px; margin-top:92px;">
    <div class="marchio" style="margin-top:34px;"><i>&#8734;</i>NXTY</div>
    <div style="margin-top:30px; font-size:29px; font-weight:600; color:rgba(253,251,246,.55);">Link in bio</div>
  </div>
</div>
</body></html>"""

with open(f"{BASE}/reel_1029.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"scritto reel_1029.html — messaggio a {[r[0] for r in MESSAGGIO]} ms, salto {SALTO}-{SALTO + SALTO_DUR}, "
      f"risposta a {[r[0] for r in RISPOSTA]} ms, via {VIA}, cartello {FINE}, durata {DURATA} ms")
