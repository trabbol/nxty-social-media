#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sabato 10/10 (id 77): CAROSELLO "Le frasi che giuravi di non dire", ep. 2. Generato dal modello caro_1003.py.
Formato fisso: frase fra caporali oro, firma sotto con il genitore barrato in oro e "tu." accanto.
8 slide 1080x1350 (4:5): copertina notte con il segno della serie gia' visibile (occhiello EPISODIO 2,
sottotitolo "Ne sono uscite altre sei."), 6 frasi su crema, chiusura notte con il logo (testo fisso della serie).
Per un nuovo episodio: cambiare FRASI (mai quelle gia' usate, vedi layout_usati.md)."""
from playwright.sync_api import sync_playwright
from PIL import Image
import os, sys
BASE = "/home/claude/nxty/demo"
FONTS = f"{BASE}/node_modules/@fontsource/plus-jakarta-sans/files"
REPO = "/home/claude/nxty/repo"
OUTDIR = f"{REPO}/posts/daily"
GOLD, NOTTE, CREMA = "#DCA659", "#0B0B12", "#FDFBF6"
W, H = 1080, 1350
ID = 77
EP = 2

# (frase, chi la diceva) — nessuna delle sei dell'ep. 1, delle ventuno del mammese o delle battute della nonna
FRASI = [
    ("Questa casa non &egrave; un&nbsp;albergo.",               "pap&agrave;"),
    ("Ne parliamo a&nbsp;casa.",                                "mamma"),
    ("Ti sembra questa l&rsquo;ora?",                           "pap&agrave;"),
    ("Vedremo.",                                                "mamma"),
    ("Se si buttano dal ponte, ti butti anche&nbsp;tu?",        "pap&agrave;"),
    ("Un giorno mi ringrazierai.",                              "mamma"),
]

HEAD = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-600-normal.woff2') format('woff2'); font-weight:600; }}
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-700-normal.woff2') format('woff2'); font-weight:700; }}
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-800-normal.woff2') format('woff2'); font-weight:800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; font-family:'PJS',sans-serif; -webkit-font-smoothing:antialiased; overflow:hidden; }}
.slide {{ width:{W}px; height:{H}px; position:relative; overflow:hidden; }}
.wm {{ display:flex; align-items:center; gap:14px; font-weight:800; letter-spacing:.32em; font-size:30px; }}
.wm i {{ color:{GOLD}; font-size:40px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-3px); }}
.kick {{ font-weight:800; letter-spacing:.24em; font-size:24px; color:{GOLD}; text-transform:uppercase; }}
/* la firma: genitore barrato in oro, poi "tu." */
.firma {{ display:flex; align-items:baseline; gap:22px; font-weight:800; }}
.firma .tratto {{ color:rgba(11,11,18,.36); }}
.barrato {{ position:relative; color:rgba(11,11,18,.40); }}
.barrato::after {{ content:''; position:absolute; left:-8px; right:-8px; top:58%; height:8px; border-radius:4px;
  background:{GOLD}; transform:rotate(-3deg); }}
.tu {{ color:{GOLD}; }}
.pt {{ margin-left:-.075em; }}
</style></head><body>"""
FOOT = "</body></html>"

import re
def k(t):
    """avvicina punto e virgola alla parola precedente (solo testo, mai attributi)"""
    t = re.sub(r'([.,])(?![^<]*>)', r'<span class="pt">\1</span>', t)
    return t.replace('&hellip;', '<span class="pt">&hellip;</span>')

def freccia(color):
    return (f'<svg width="92" height="40" viewBox="0 0 92 40" style="display:block">'
            f'<path d="M2 20 H84 M66 4 L86 20 L66 36" fill="none" stroke="{color}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def copertina():
    return HEAD + f"""
<div class="slide" style="background:radial-gradient(1000px 820px at 50% 34%, #17162C 0%, #08080E 76%); color:{CREMA};">
  <div class="wm" style="position:absolute; top:92px; left:0; right:0; justify-content:center; color:{CREMA};"><i>&#8734;</i>NXTY</div>
  <div style="position:absolute; left:96px; right:96px; top:250px;">
    <div class="kick" style="margin-bottom:34px;">Episodio {EP}</div>
    <div style="font-size:112px; font-weight:800; line-height:1.02; letter-spacing:-.015em;">
      Le frasi che<br><span style="color:{GOLD};">giuravi</span><br>di non dire{k('.')}</div>
    <div style="margin-top:46px; font-size:46px; font-weight:700; line-height:1.25; color:rgba(253,251,246,.62);">
      {k('Ne sono uscite altre sei.')}</div>
    <div class="firma" style="margin-top:86px; font-size:56px;">
      <span class="tratto" style="color:rgba(253,251,246,.34);">&mdash;</span>
      <span class="barrato" style="color:rgba(253,251,246,.42);">mamma</span>
      <span class="barrato" style="color:rgba(253,251,246,.42);">pap&agrave;</span>
      <span class="tu">tu{k('.')}</span>
    </div>
  </div>
  <div style="position:absolute; right:96px; bottom:92px;">{freccia(GOLD)}</div>
</div>""" + FOOT

def frase(n, testo, chi):
    lung = len(testo.replace('&nbsp;', ' ').replace('&hellip;', '.').replace('&rsquo;', "'"))
    size = 104 if lung <= 22 else (94 if lung <= 32 else 86)
    return HEAD + f"""
<div class="slide" style="background:{CREMA}; color:{NOTTE};">
  <div class="kick" style="position:absolute; top:96px; left:120px;">Le frasi che giuravi di non dire</div>
  <div style="position:absolute; top:96px; right:120px; font-size:24px; font-weight:800; letter-spacing:.12em;
    color:rgba(11,11,18,.34);">{n}/6</div>
  <div style="position:absolute; left:120px; right:110px; top:0; bottom:0; display:flex; flex-direction:column; justify-content:center; padding-bottom:90px;">
    <div style="position:relative; font-size:{size}px; font-weight:800; line-height:1.06; letter-spacing:-.012em;">
      <span style="position:absolute; left:-0.66em; color:{GOLD};">&laquo;</span>{k(testo)}<span style="color:{GOLD};">&raquo;</span>
    </div>
    <div class="firma" style="margin-top:64px; font-size:58px;">
      <span class="tratto">&mdash;</span><span class="barrato">{chi}</span><span class="tu">tu{k('.')}</span>
    </div>
  </div>
  <div class="wm" style="position:absolute; bottom:88px; left:120px; color:{NOTTE}; font-size:24px;"><i style="font-size:32px;">&#8734;</i>NXTY</div>
</div>""" + FOOT

def chiusura():
    return HEAD + f"""
<div class="slide" style="background:radial-gradient(1000px 820px at 50% 40%, #17162C 0%, #08080E 76%); color:{CREMA};">
  <div style="position:absolute; left:96px; right:96px; top:0; bottom:300px; display:flex; flex-direction:column; justify-content:center;">
    <div style="font-size:100px; font-weight:800; line-height:1.05; letter-spacing:-.015em;">{k('Le frasi, ormai,')}<br>{k('sono tue.')}</div>
    <div style="margin-top:52px; font-size:54px; font-weight:800; line-height:1.2; color:{GOLD};">
      {k('La voce con cui te le dicevano, tienila.')}</div>
  </div>
  <div style="position:absolute; left:0; right:0; bottom:104px; display:flex; flex-direction:column; align-items:center; gap:26px;">
    <img src="file://{BASE}/logo_oro.png" style="width:116px;">
    <div style="font-size:26px; font-weight:800; letter-spacing:.3em; color:rgba(253,251,246,.62);">NEXT TO YOU</div>
  </div>
</div>""" + FOOT

SLIDES = [copertina()] + [frase(i + 1, t, c) for i, (t, c) in enumerate(FRASI)] + [chiusura()]

if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg = ctx.new_page()
        for i, html in enumerate(SLIDES, 1):
            hp = f"{BASE}/caro_1010_s{i}.html"
            with open(hp, "w", encoding="utf-8") as f: f.write(html)
            pg.goto(f"file://{hp}", wait_until="networkidle"); pg.wait_for_timeout(300)
            tmp = f"{BASE}/_caro_s{i}.png"
            pg.screenshot(path=tmp)
            jp = f"{OUTDIR}/caro_1010_{ID}_s{i}.jpg"
            Image.open(tmp).convert("RGB").save(jp, "JPEG", quality=92, optimize=True)
            out.append(jp)
        b.close()
    for o in out: print(o, os.path.getsize(o)//1024, "KB")
