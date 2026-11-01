#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Martedi' 3/11 (id 101): CAROSELLO "Le domande da fare ai nonni", ep. 2, campagna "Per chi verra'" (direttiva 43:
chi riceve chiede, chi lascia racconta). Stesso modello di caro_1027.py (ep. 1), cambiano EP, ID, SOTTOTITOLO e DOMANDE.
Formato fisso della serie: 8 slide 1080x1350 (4:5).
- Copertina su crema: occhiello oro "PER CHI VERRA' · EPISODIO 2", titolo con "nonni" in oro, sottotitolo nuovo
  («Altre sei domande. Ognuna dura un pomeriggio.») e la fila dei sei numeri in cerchi oro (per «Rispondi con il numero»).
- Sei slide su crema: numero grande in oro, domanda grande fra caporali oro, filetto oro, "E POI:" e la domanda che viene dopo.
- Chiusura fissa su fondo scuro: «Non serve un'intervista.» / «Basta una domanda e il telefono sul tavolo.» /
  «La sua voce, per chi verra'.» in oro, logo e NEXT TO YOU.
Sei domande nuove (mai le dodici dell'ep. 1, vedi layout_usati.md), da fare a un nonno o una nonna vivi e in salute,
tutte senza genere (vanno bene per lui e per lei), niente lutto. Apostrofi stretti con .ap dentro k()."""
from playwright.sync_api import sync_playwright
from PIL import Image
import os, re
BASE = "/home/claude/nxty/demo"
FONTS = f"{BASE}/node_modules/@fontsource/plus-jakarta-sans/files"
REPO = "/home/claude/nxty/repo"
OUTDIR = f"{REPO}/posts/daily"
GOLD, NOTTE, CREMA = "#DCA659", "#0B0B12", "#FDFBF6"
W, H = 1080, 1350
ID = 101
EP = 2
SERIE = "Le domande da fare ai nonni"
SOTTOTITOLO = "Altre sei domande. Ognuna dura un&nbsp;pomeriggio."

# (domanda, la domanda che viene dopo)
DOMANDE = [
    ("Qual &egrave; il tuo primo&nbsp;ricordo?",                 "Quanti anni&nbsp;avevi?"),
    ("A cosa si giocava in&nbsp;cortile?",                       "Chi vinceva&nbsp;sempre?"),
    ("Che marachella non&nbsp;hai&nbsp;mai confessato?",         "Me la racconti&nbsp;adesso?"),
    ("Che mestiere sognavi di fare da&nbsp;grande?",             "E com&rsquo;&egrave; andata?"),
    ("Qual &egrave; stato il tuo primo&nbsp;viaggio?",           "Con chi&nbsp;eri?"),
    ("Cosa hai fatto di pi&ugrave; coraggioso?",                 "Chi lo sa, oltre a&nbsp;te?"),
]

def font(w, it=False):
    st = "italic" if it else "normal"
    return (f"@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-{w}-{st}.woff2') "
            f"format('woff2'); font-weight:{w}; font-style:{st}; }}")

HEAD = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{font(600)} {font(700)} {font(800)}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; font-family:'PJS',sans-serif; -webkit-font-smoothing:antialiased; overflow:hidden; }}
.slide {{ width:{W}px; height:{H}px; position:relative; overflow:hidden; }}
.wm {{ display:flex; align-items:center; gap:14px; font-weight:800; letter-spacing:.32em; font-size:30px; }}
.wm i {{ color:{GOLD}; font-size:40px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-3px); }}
.kick {{ font-weight:800; letter-spacing:.24em; font-size:24px; color:{GOLD}; text-transform:uppercase; }}
.filetto {{ width:132px; height:7px; border-radius:4px; background:{GOLD}; }}
.cerchio {{ width:74px; height:74px; border-radius:50%; border:4px solid {GOLD}; color:{GOLD}; display:flex;
  align-items:center; justify-content:center; font-size:36px; font-weight:800; }}
.pt {{ margin-left:-.075em; }}
.gc {{ margin-left:-.07em; }}
.ap {{ margin:0 -.05em; }}
</style></head><body>"""
FOOT = "</body></html>"

def k(t):
    """avvicina punto e virgola alla parola precedente (solo testo, mai attributi) e stringe l'apostrofo,
    che in Plus Jakarta Sans ha spalle larghe («vent' anni» -> «vent'anni»)"""
    t = re.sub(r'([.,])(?![^<]*>)', r'<span class="pt">\1</span>', t)
    t = t.replace('&rsquo;', '<span class="ap">&rsquo;</span>')
    return t.replace('&hellip;', '<span class="pt">&hellip;</span>')

def freccia(color):
    return (f'<svg width="92" height="40" viewBox="0 0 92 40" style="display:block">'
            f'<path d="M2 20 H84 M66 4 L86 20 L66 36" fill="none" stroke="{color}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def copertina():
    cerchi = "".join(f'<div class="cerchio">{n}</div>' for n in range(1, 7))
    return HEAD + f"""
<div class="slide" style="background:{CREMA}; color:{NOTTE};">
  <div class="wm" style="position:absolute; top:92px; left:0; right:0; justify-content:center; color:{NOTTE};"><i>&#8734;</i>NXTY</div>
  <div style="position:absolute; left:96px; right:96px; top:250px;">
    <div class="kick" style="margin-bottom:36px;">Per chi verr&agrave; &middot; Episodio {EP}</div>
    <div style="font-size:112px; font-weight:800; line-height:1.02; letter-spacing:-.015em;">
      Le domande<br>da fare<br>ai <span style="color:{GOLD};">nonni</span>{k('.')}</div>
    <div style="margin-top:44px; font-size:46px; font-weight:700; line-height:1.25; color:rgba(11,11,18,.58);">{k(SOTTOTITOLO)}</div>
    <div style="margin-top:72px; display:flex; gap:22px;">{cerchi}</div>
  </div>
  <div style="position:absolute; right:96px; bottom:92px;">{freccia(GOLD)}</div>
</div>""" + FOOT

def domanda(n, testo, dopo):
    lung = len(re.sub(r'&\w+;', 'x', testo))
    size = 100 if lung <= 26 else (88 if lung <= 40 else 78)
    return HEAD + f"""
<div class="slide" style="background:{CREMA}; color:{NOTTE};">
  <div class="kick" style="position:absolute; top:96px; left:120px;">{SERIE}</div>
  <div style="position:absolute; top:96px; right:120px; font-size:24px; font-weight:800; letter-spacing:.12em;
    color:rgba(11,11,18,.34);">{n}/6</div>
  <div style="position:absolute; left:120px; right:110px; top:0; bottom:0; display:flex; flex-direction:column; justify-content:center; padding-bottom:80px;">
    <div class="cerchio" style="width:104px; height:104px; font-size:54px; border-width:5px; margin-bottom:48px;">{n}</div>
    <div style="position:relative; font-size:{size}px; font-weight:800; line-height:1.07; letter-spacing:-.012em;">
      <span style="position:absolute; left:-0.66em; color:{GOLD};">&laquo;</span>{k(testo)}<span class="gc" style="color:{GOLD};">&raquo;</span>
    </div>
    <div class="filetto" style="margin-top:56px;"></div>
    <div class="kick" style="margin-top:40px; font-size:26px;">E poi:</div>
    <div style="margin-top:16px; font-size:52px; font-weight:700; line-height:1.2; color:rgba(11,11,18,.72);">&laquo;{k(dopo)}<span class="gc">&raquo;</span></div>
  </div>
  <div class="wm" style="position:absolute; bottom:88px; left:120px; color:{NOTTE}; font-size:24px;"><i style="font-size:32px;">&#8734;</i>NXTY</div>
</div>""" + FOOT

def chiusura():
    return HEAD + f"""
<div class="slide" style="background:radial-gradient(1000px 820px at 50% 40%, #17162C 0%, #08080E 76%); color:{CREMA};">
  <div style="position:absolute; left:96px; right:96px; top:0; bottom:300px; display:flex; flex-direction:column; justify-content:center;">
    <div style="font-size:96px; font-weight:800; line-height:1.05; letter-spacing:-.015em;">Non serve<br>{k('un&rsquo;intervista.')}</div>
    <div style="margin-top:44px; font-size:52px; font-weight:700; line-height:1.22; color:rgba(253,251,246,.80);">
      {k('Basta una domanda e il telefono sul&nbsp;tavolo.')}</div>
    <div style="margin-top:44px; font-size:54px; font-weight:800; line-height:1.2; color:{GOLD};">
      {k('La sua voce, per chi verr&agrave;.')}</div>
  </div>
  <div style="position:absolute; left:0; right:0; bottom:104px; display:flex; flex-direction:column; align-items:center; gap:26px;">
    <img src="file://{BASE}/logo_oro.png" style="width:116px;">
    <div style="font-size:26px; font-weight:800; letter-spacing:.3em; color:rgba(253,251,246,.62);">NEXT TO YOU</div>
  </div>
</div>""" + FOOT

SLIDES = [copertina()] + [domanda(i + 1, t, d) for i, (t, d) in enumerate(DOMANDE)] + [chiusura()]

if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg = ctx.new_page()
        for i, html in enumerate(SLIDES, 1):
            hp = f"{BASE}/caro_1103_s{i}.html"
            with open(hp, "w", encoding="utf-8") as f: f.write(html)
            pg.goto(f"file://{hp}", wait_until="networkidle"); pg.wait_for_timeout(300)
            tmp = f"{BASE}/_caro_s{i}.png"
            pg.screenshot(path=tmp)
            jp = f"{OUTDIR}/caro_1103_{ID}_s{i}.jpg"
            Image.open(tmp).convert("RGB").save(jp, "JPEG", quality=92, optimize=True)
            out.append(jp)
        b.close()
    for o in out: print(o, os.path.getsize(o)//1024, "KB")
