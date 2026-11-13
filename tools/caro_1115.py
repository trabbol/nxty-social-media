#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Domenica 15/11 (id 113): CAROSELLO "L'eredita' che non si divide", ep. 2, dentro la campagna "Per chi verra'"
(direttiva 43). Al presente e con i genitori vivi, niente notaio, niente lutto: ogni slide e' una cosa che i figli
hanno preso da lei, intera, tutti. Generato dal modello caro_1108.py (ep. 1), stesso formato fisso della serie:
8 slide 1080x1350 (4:5).
- Copertina scura: occhiello oro "EPISODIO 2" (dall'ep. 2 al posto di "NUOVA SERIE"), titolo con "non si divide" in
  oro, sottotitolo nuovo («Altre sei. Ognuno di voi le ha prese intere.») e la riga della quota.
- Sei slide su crema: occhiello e contatore N/6, la cosa grande senza caporali, sotto la riga della quota.
- Chiusura notte fissa della serie: «Su queste non si litiga:» / «sono gia' di tutti.» / «La sua voce, tenetela.»
Testi dal documento della campagna (rev 65: ep. 2 scritto il 13/11 sotto la lista dell'ep. 1).
Per un nuovo episodio: cambiare EP, ID, GIORNO, SOTTOTITOLO e COSE (mai quelle gia' usate, vedi layout_usati.md)."""
from playwright.sync_api import sync_playwright
from PIL import Image
import os, re, html
BASE = "/home/claude/nxty/demo"
FONTS = f"{BASE}/node_modules/@fontsource/plus-jakarta-sans/files"
REPO = "/home/claude/nxty/repo"
OUTDIR = f"{REPO}/posts/daily"
GOLD, NOTTE, CREMA = "#DCA659", "#0B0B12", "#FDFBF6"
W, H = 1080, 1350
ID = 113
EP = 2
GIORNO = "1115"
SERIE = "L&rsquo;eredit&agrave; che non si divide"
SOTTOTITOLO = "Altre sei. Ognuno di voi le ha&nbsp;prese&nbsp;intere."
QUOTA = "a ciascuno dei figli, per&nbsp;intero."

# le sei cose, nell'ordine del documento (rev 65); mai quelle dell'ep. 1 ne' la ricetta e la canzone fischiata
COSE = [
    "Lo starnuto che fa tremare i&nbsp;vetri.",
    "La calligrafia della lista della&nbsp;spesa.",
    "Le valigie pronte tre&nbsp;giorni&nbsp;prima.",
    "La mela sbucciata in&nbsp;un&nbsp;solo&nbsp;giro.",
    "La testa&nbsp;dura.",
    "Il saluto dalla finestra fino in fondo alla&nbsp;via.",
]

def font(w, it=False):
    st = "italic" if it else "normal"
    return (f"@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-{w}-{st}.woff2') "
            f"format('woff2'); font-weight:{w}; font-style:{st}; }}")

HEAD = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{font(600)} {font(700)} {font(800)} {font(600, True)}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; font-family:'PJS',sans-serif; -webkit-font-smoothing:antialiased; overflow:hidden; }}
.slide {{ width:{W}px; height:{H}px; position:relative; overflow:hidden; }}
.wm {{ display:flex; align-items:center; gap:14px; font-weight:800; letter-spacing:.32em; font-size:30px; }}
.wm i {{ color:{GOLD}; font-size:40px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-3px); }}
.kick {{ font-weight:800; letter-spacing:.24em; font-size:24px; color:{GOLD}; text-transform:uppercase; }}
/* la riga della quota, come in un atto: etichetta, puntini, valore in corsivo */
.quota {{ display:flex; align-items:baseline; gap:18px; }}
.quota .lab {{ font-weight:800; letter-spacing:.24em; font-size:24px; color:{GOLD}; text-transform:uppercase; flex:0 0 auto; }}
.quota .punti {{ flex:1 1 auto; min-width:60px; border-bottom:5px dotted rgba(220,166,89,.75); transform:translateY(-6px); }}
.quota .val {{ font-weight:600; font-style:italic; font-size:36px; flex:0 0 auto; }}
.pt {{ margin-left:-.075em; }}
.ap {{ margin:0 -.05em; }}
</style></head><body>"""
FOOT = "</body></html>"

def k(t):
    """avvicina punto, virgola e due punti alla parola precedente (solo testo, mai attributi) e stringe l'apostrofo"""
    t = re.sub(r'([.,:])(?![^<]*>)', r'<span class="pt">\1</span>', t)
    t = t.replace('&rsquo;', '<span class="ap">&rsquo;</span>')
    return t.replace('&hellip;', '<span class="pt">&hellip;</span>')

def freccia(color):
    return (f'<svg width="92" height="40" viewBox="0 0 92 40" style="display:block">'
            f'<path d="M2 20 H84 M66 4 L86 20 L66 36" fill="none" stroke="{color}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def riga_quota(colore_val):
    return (f'<div class="quota"><span class="lab">Quota</span><span class="punti"></span>'
            f'<span class="val" style="color:{colore_val};">{k(QUOTA)}</span></div>')

def copertina():
    return HEAD + f"""
<div class="slide" style="background:radial-gradient(1000px 820px at 50% 34%, #17162C 0%, #08080E 76%); color:{CREMA};">
  <div class="wm" style="position:absolute; top:92px; left:0; right:0; justify-content:center; color:{CREMA};"><i>&#8734;</i>NXTY</div>
  <div style="position:absolute; left:96px; right:96px; top:250px;">
    <div class="kick" style="margin-bottom:34px;">Episodio {EP}</div>
    <div style="font-size:108px; font-weight:800; line-height:1.02; letter-spacing:-.015em;">
      {k('L&rsquo;eredit&agrave;')}<br>che <span style="color:{GOLD};">non<br>si divide</span>{k('.')}</div>
    <div style="margin-top:46px; font-size:44px; font-weight:700; line-height:1.25; color:rgba(253,251,246,.62);">
      {k(SOTTOTITOLO)}</div>
    <div style="margin-top:78px;">{riga_quota('rgba(253,251,246,.78)')}</div>
  </div>
  <div style="position:absolute; right:96px; bottom:92px;">{freccia(GOLD)}</div>
</div>""" + FOOT

def cosa(n, testo):
    lung = len(html.unescape(testo))   # lettere vere: le entita' contano uno
    size = 104 if lung <= 22 else (94 if lung <= 32 else (86 if lung <= 38 else 82))
    return HEAD + f"""
<div class="slide" style="background:{CREMA}; color:{NOTTE};">
  <div class="kick" style="position:absolute; top:96px; left:120px;">{k(SERIE)}</div>
  <div style="position:absolute; top:96px; right:120px; font-size:24px; font-weight:800; letter-spacing:.12em;
    color:rgba(11,11,18,.34);">{n}/6</div>
  <div style="position:absolute; left:120px; right:110px; top:0; bottom:0; display:flex; flex-direction:column; justify-content:center; padding-bottom:90px;">
    <div style="font-size:{size}px; font-weight:800; line-height:1.06; letter-spacing:-.012em;">{k(testo)}</div>
    <div style="margin-top:76px;">{riga_quota('rgba(11,11,18,.66)')}</div>
  </div>
  <div class="wm" style="position:absolute; bottom:88px; left:120px; color:{NOTTE}; font-size:24px;"><i style="font-size:32px;">&#8734;</i>NXTY</div>
</div>""" + FOOT

def chiusura():
    return HEAD + f"""
<div class="slide" style="background:radial-gradient(1000px 820px at 50% 40%, #17162C 0%, #08080E 76%); color:{CREMA};">
  <div style="position:absolute; left:96px; right:96px; top:0; bottom:300px; display:flex; flex-direction:column; justify-content:center;">
    <div style="font-size:100px; font-weight:800; line-height:1.05; letter-spacing:-.015em;">Su queste<br>{k('non si litiga:')}</div>
    <div style="margin-top:44px; font-size:56px; font-weight:700; line-height:1.2; color:rgba(253,251,246,.80);">
      {k('sono gi&agrave; di tutti.')}</div>
    <div style="margin-top:44px; font-size:56px; font-weight:800; line-height:1.2; color:{GOLD};">
      {k('La sua voce, tenetela.')}</div>
  </div>
  <div style="position:absolute; left:0; right:0; bottom:104px; display:flex; flex-direction:column; align-items:center; gap:26px;">
    <img src="file://{BASE}/logo_oro.png" style="width:116px;">
    <div style="font-size:26px; font-weight:800; letter-spacing:.3em; color:rgba(253,251,246,.62);">NEXT TO YOU</div>
  </div>
</div>""" + FOOT

SLIDES = [copertina()] + [cosa(i + 1, t) for i, t in enumerate(COSE)] + [chiusura()]

if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg = ctx.new_page()
        for i, pagina in enumerate(SLIDES, 1):
            hp = f"{BASE}/caro_{GIORNO}_s{i}.html"
            with open(hp, "w", encoding="utf-8") as f: f.write(pagina)
            pg.goto(f"file://{hp}", wait_until="networkidle"); pg.wait_for_timeout(300)
            tmp = f"{BASE}/_caro_s{i}.png"
            pg.screenshot(path=tmp)
            jp = f"{OUTDIR}/caro_{GIORNO}_{ID}_s{i}.jpg"
            Image.open(tmp).convert("RGB").save(jp, "JPEG", quality=92, optimize=True)
            out.append(jp)
        b.close()
    for o in out: print(o, os.path.getsize(o)//1024, "KB")
