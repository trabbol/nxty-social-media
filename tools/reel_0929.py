#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reel di martedi 29 settembre (id 67) — "Dal mammese all'italiano", ep. 1. MODELLO DELLA SERIE.
Interfaccia piatta di traduttore: pill MAMMESE -> ITALIANO, scheda bianca con la frase fra caporali,
scheda oro chiaro con la traduzione, cursore oro prima della traduzione; la battuta gira la scheda in notte.
Ricostruito il 30/9 dopo l'azzeramento del container, identico alla versione pubblicata (posizioni finali).
Per un nuovo episodio: cambiare FRASI (mai le sei gia' usate, vedi layout_usati.md) e il numero di ep."""
BASE = "/home/claude/nxty/demo"
FONTS = f"{BASE}/node_modules/@fontsource/plus-jakarta-sans/files"
GOLD, NOTTE, CREMA = "#DCA659", "#0B0B12", "#FDFBF6"
EP = 1
FRASI = [
    ("Copriti.",                 "Ti voglio bene.",       False),
    ("Hai mangiato?",            "Ti voglio bene.",       False),
    ("Chiamami quando arrivi.",  "Ti voglio bene.",       False),
    ("Fa&rsquo; come vuoi.",     "<span style='color:%s'>Non</span> fare come vuoi." % GOLD, True),
    ("Lascia, faccio io.",       "Ti voglio bene.",       False),
]
PASSO, TRAD = 1700, 550
PAUSA_BATTUTA = 600
TEMPI = []
t = 0
for src, tgt, battuta in FRASI:
    durata = PASSO + (PAUSA_BATTUTA if battuta else 0)
    TEMPI.append((t, t + TRAD, t + durata - 60))
    t += durata
VIA   = t - 20
FINE  = VIA + 200
DURATA = FINE + 2300

src_html, tgt_html, car_html, notte_anim = [], [], [], ""
for i, ((src, tgt, battuta), (ts, tt, tu)) in enumerate(zip(FRASI, TEMPI)):
    if i == 0:
        a_src, st0 = f"esci 140ms {tu}ms forwards", "opacity:1;"
    else:
        a_src, st0 = f"entra 160ms {ts}ms forwards, esci 140ms {tu}ms forwards", ""
    src_html.append(f'<div class="frase" style="{st0}animation:{a_src};">&laquo;{src}&raquo;</div>')
    col = f"color:{CREMA};" if battuta else ""
    tgt_html.append(f'<div class="frase trad" style="{col}animation:pop 260ms {tt}ms forwards, esci 140ms {tu}ms forwards;">{tgt}</div>')
    car_html.append(f'<div class="caret" style="animation:c_on 1ms {ts}ms forwards, pulsa 270ms {ts}ms 2 alternate, c_off 1ms {tt-10}ms forwards;"></div>')
    if battuta:
        notte_anim = f"entra 200ms {tt-40}ms forwards, esci 180ms {tu}ms forwards"

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
@keyframes pop   {{ 0% {{ opacity:0; transform:translateY(18px); }} 100% {{ opacity:1; transform:translateY(0); }} }}
@keyframes c_on  {{ to {{ opacity:1; }} }}
@keyframes c_off {{ to {{ opacity:0; }} }}
@keyframes pulsa {{ from {{ opacity:1; }} to {{ opacity:.12; }} }}
.main {{ position:absolute; inset:0; animation:esci 380ms {VIA}ms forwards; }}
.wmd {{ position:absolute; top:236px; left:0; right:0; display:flex; align-items:center; justify-content:center;
  gap:16px; font-weight:800; letter-spacing:.32em; font-size:34px; color:{NOTTE}; }}
.wmd i {{ color:{GOLD}; font-size:46px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-4px); }}
.lingue {{ position:absolute; top:392px; left:0; right:0; display:flex; align-items:center; justify-content:center; gap:26px; }}
.pill {{ font-size:30px; font-weight:800; letter-spacing:.16em; padding:18px 34px; border-radius:999px; }}
.pill.da {{ color:{GOLD}; border:3px solid {GOLD}; }}
.pill.a  {{ color:{CREMA}; background:{NOTTE}; border:3px solid {NOTTE}; }}
.scheda {{ position:absolute; left:76px; right:76px; height:340px; border-radius:40px; overflow:hidden; }}
.scheda.src {{ top:522px; background:#FFFFFF; border:2px solid rgba(11,11,18,.08); box-shadow:0 18px 50px rgba(11,11,18,.06); }}
.scheda.tgt {{ top:898px; background:rgba(220,166,89,.16); border:2px solid rgba(220,166,89,.38); }}
.etichetta {{ position:absolute; top:42px; left:56px; font-size:25px; font-weight:800; letter-spacing:.22em; }}
.src .etichetta {{ color:{GOLD}; }}
.tgt .etichetta {{ color:rgba(11,11,18,.50); }}
.frase {{ position:absolute; top:112px; left:56px; right:56px; font-size:74px; font-weight:800; line-height:1.08;
  color:{NOTTE}; opacity:0; z-index:2; }}
.caret {{ position:absolute; top:122px; left:58px; width:7px; height:74px; background:{GOLD}; border-radius:4px; opacity:0; z-index:2; }}
.notte {{ position:absolute; inset:0; background:{NOTTE}; opacity:0; z-index:1; animation:{notte_anim}; }}
.notte .etichetta {{ color:rgba(253,251,246,.55); }}
.serie {{ position:absolute; top:1298px; left:0; right:0; text-align:center; font-size:30px; font-weight:700;
  color:rgba(11,11,18,.46); letter-spacing:.02em; }}
.fine {{ position:absolute; inset:0; z-index:5; display:flex; flex-direction:column; align-items:center;
  justify-content:center; background:{CREMA}; opacity:0; animation:entra 600ms {FINE}ms forwards; padding-bottom:120px; }}
.fine .riga {{ font-size:66px; font-weight:800; line-height:1.16; text-align:center; color:{NOTTE}; }}
.fine .marchio {{ display:flex; align-items:center; gap:16px; font-weight:800; letter-spacing:.34em; font-size:40px; color:{NOTTE}; }}
.fine .marchio i {{ color:{GOLD}; font-size:52px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-4px); }}
</style></head><body>
<div class="scena">
  <div class="main">
    <div class="wmd"><i>&#8734;</i>NXTY</div>
    <div class="lingue">
      <div class="pill da">MAMMESE</div>
      <svg width="64" height="30" viewBox="0 0 64 30"><path d="M2 15 H56 M44 3 L58 15 L44 27" fill="none" stroke="{GOLD}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div class="pill a">ITALIANO</div>
    </div>
    <div class="scheda src"><div class="etichetta">MAMMESE</div>{''.join(src_html)}</div>
    <div class="scheda tgt"><div class="etichetta">ITALIANO</div><div class="notte"><div class="etichetta">ITALIANO</div></div>{''.join(car_html)}{''.join(tgt_html)}</div>
    <div class="serie">Dal mammese all&rsquo;italiano &middot; ep. {EP}</div>
  </div>
  <div class="fine">
    <div class="riga">Certe lingue<br>le parla<br><span style="color:{GOLD};">una persona sola.</span></div>
    <img src="file://{BASE}/logo_oro.png" style="width:118px; margin-top:92px;">
    <div class="marchio" style="margin-top:34px;"><i>&#8734;</i>NXTY</div>
    <div style="margin-top:30px; font-size:29px; font-weight:600; color:rgba(11,11,18,.50);">Link in bio</div>
  </div>
</div>
</body></html>"""
with open(f"{BASE}/reel_0929.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print("tempi:", TEMPI, f"| via {VIA} · cartello {FINE} · durata {DURATA} ms")
