#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Domenica 1/11 (id 99): CAROSELLO "Il vocabolario della nonna", ep. 4 (modello caro_1025.py), dentro la campagna
"Per chi verra'" (direttiva 43: le parole della nonna come eredita'). L'1/11 e' Ognissanti: il post resta leggero.
Occhiello di copertina "Episodio 4", voce di copertina nuova ("domenica", s.f.), sottotitolo "Altre sei parole. Un giorno
le dirai tu.". Apostrofi stretti con la classe .ap dentro k(), come in caro_1027.py.
Formato fisso della serie: ogni slide e' una VOCE DI DIZIONARIO. Lemma grande come lo dice lei, categoria
grammaticale in corsivo oro, filetto oro, accezione numerata ("1.") con la definizione di una riga o due.
8 slide 1080x1350 (4:5): copertina notte che e' gia' una voce di dizionario (una voce nuova a ogni episodio), 6 voci su crema,
chiusura notte con il logo ("Nel dizionario non ci sono. / Ci sono nella sua voce. Tienila.").
Solo tipografia: niente sagome umane, niente loghi. Per un nuovo episodio: cambiare VOCI (mai quelle gia' usate,
vedi layout_usati.md) e la voce di copertina."""
from playwright.sync_api import sync_playwright
from PIL import Image
import os, re
BASE = "/home/claude/nxty/demo"
FONTS = f"{BASE}/node_modules/@fontsource/plus-jakarta-sans/files"
REPO = "/home/claude/nxty/repo"
OUTDIR = f"{REPO}/posts/daily"
GOLD, NOTTE, CREMA = "#DCA659", "#0B0B12", "#FDFBF6"
W, H = 1080, 1350
ID = 99
EP = 4
SERIE = "Il vocabolario della nonna"

# voce di copertina: il segno della serie gia' visibile al primo sguardo
COPERTINA = ("domenica", "s.f.", "Il pranzo da lei. Dalle dodici alle&nbsp;cinque.")

# (lemma, categoria, definizione) — mai le diciotto voci degli ep. 1-3 ne' battute dei vocali, del mammese, delle frasi
# giurate, di "Per chi verra'" o delle domande ai nonni (layout_usati.md); l'ultima e' la piu' forte
VOCI = [
    ("Il colpo d&rsquo;aria",   "loc. s.",  "La causa di ogni malanno. Dal&nbsp;torcicollo al mal di&nbsp;pancia."),
    ("L&rsquo;America",         "s.f.",     "Qualsiasi posto dove si&nbsp;arriva in&nbsp;aereo."),
    ("Il motorino",             "s.m.",     "Il mezzo pi&ugrave; pericoloso del&nbsp;mondo. Dopo la&nbsp;bicicletta."),
    ("Il meteo",                "s.m.",     "Lo guarda tre volte al&nbsp;giorno. Non ci crede&nbsp;mai."),
    ("I jeans strappati",       "loc. s.",  "Un lavoro lasciato a met&agrave;. Te li ricuce&nbsp;lei."),
    ("Fai il bravo",            "loc.",     "Il suo modo di salutarti. Anche&nbsp;adesso che sei&nbsp;grande."),
]

def font(w, it=False):
    st = "italic" if it else "normal"
    return (f"@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-{w}-{st}.woff2') "
            f"format('woff2'); font-weight:{w}; font-style:{st}; }}")

HEAD = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
{font(600)} {font(700)} {font(800)} {font(600, True)} {font(700, True)}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; font-family:'PJS',sans-serif; -webkit-font-smoothing:antialiased; overflow:hidden; }}
.slide {{ width:{W}px; height:{H}px; position:relative; overflow:hidden; }}
.wm {{ display:flex; align-items:center; gap:14px; font-weight:800; letter-spacing:.32em; font-size:30px; }}
.wm i {{ color:{GOLD}; font-size:40px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-3px); }}
.kick {{ font-weight:800; letter-spacing:.24em; font-size:24px; color:{GOLD}; text-transform:uppercase; }}
.cat {{ font-style:italic; font-weight:600; color:{GOLD}; }}
.filetto {{ width:132px; height:7px; border-radius:4px; background:{GOLD}; }}
.acc {{ color:{GOLD}; font-weight:800; margin-right:.32em; }}
.pt {{ margin-left:-.075em; }}
.ap {{ margin:0 -.05em; }}
</style></head><body>"""
FOOT = "</body></html>"

def k(t):
    """avvicina punto e virgola alla parola precedente (solo testo, mai attributi)"""
    t = re.sub(r'([.,])(?![^<]*>)', r'<span class="pt">\1</span>', t)
    t = t.replace('&rsquo;', '<span class="ap">&rsquo;</span>')
    return t.replace('&hellip;', '<span class="pt">&hellip;</span>')

def freccia(color):
    return (f'<svg width="92" height="40" viewBox="0 0 92 40" style="display:block">'
            f'<path d="M2 20 H84 M66 4 L86 20 L66 36" fill="none" stroke="{color}" stroke-width="6" '
            f'stroke-linecap="round" stroke-linejoin="round"/></svg>')

def copertina():
    lemma, cat, defin = COPERTINA
    return HEAD + f"""
<div class="slide" style="background:radial-gradient(1000px 820px at 50% 34%, #17162C 0%, #08080E 76%); color:{CREMA};">
  <div class="wm" style="position:absolute; top:92px; left:0; right:0; justify-content:center; color:{CREMA};"><i>&#8734;</i>NXTY</div>
  <div style="position:absolute; left:96px; right:96px; top:236px;">
    <div class="kick" style="margin-bottom:34px;">Episodio {EP}</div>
    <div style="font-size:108px; font-weight:800; line-height:1.02; letter-spacing:-.015em;">
      Il vocabolario<br>della <span style="color:{GOLD};">nonna</span>{k('.')}</div>
    <div style="margin-top:40px; font-size:44px; font-weight:700; line-height:1.25; color:rgba(253,251,246,.62);">
      {k('Altre sei parole. Un giorno le dirai tu.')}</div>
    <div style="margin-top:70px; padding:34px 0 34px 40px; border-left:7px solid {GOLD};">
      <div style="display:flex; align-items:baseline; gap:22px;">
        <span style="font-size:72px; font-weight:800; line-height:1;">{k(lemma)}</span>
        <span class="cat" style="font-size:38px;">{cat}</span>
      </div>
      <div style="margin-top:20px; font-size:38px; font-weight:700; line-height:1.3; color:rgba(253,251,246,.84);">
        <span class="acc">1.</span>{k(defin)}</div>
    </div>
  </div>
  <div style="position:absolute; right:96px; bottom:92px;">{freccia(GOLD)}</div>
</div>""" + FOOT

def voce(n, lemma, cat, defin):
    lung = len(re.sub(r'&\w+;', 'x', lemma))
    size = 150 if lung <= 7 else (128 if lung <= 10 else 112)
    dl = len(re.sub(r'&\w+;', 'x', defin))
    dsize = 58 if dl <= 52 else 52
    return HEAD + f"""
<div class="slide" style="background:{CREMA}; color:{NOTTE};">
  <div class="kick" style="position:absolute; top:96px; left:120px;">{SERIE}</div>
  <div style="position:absolute; top:96px; right:120px; font-size:24px; font-weight:800; letter-spacing:.12em;
    color:rgba(11,11,18,.34);">{n}/6</div>
  <div style="position:absolute; left:120px; right:120px; top:0; bottom:0; display:flex; flex-direction:column; justify-content:center; padding-bottom:70px;">
    <div style="font-size:{size}px; font-weight:800; line-height:1.0; letter-spacing:-.02em;">{k(lemma)}</div>
    <div class="cat" style="margin-top:26px; font-size:46px;">{cat}</div>
    <div class="filetto" style="margin-top:46px;"></div>
    <div style="margin-top:46px; font-size:{dsize}px; font-weight:700; line-height:1.22; letter-spacing:-.005em;">
      <span class="acc">1.</span>{k(defin)}</div>
  </div>
  <div class="wm" style="position:absolute; bottom:88px; left:120px; color:{NOTTE}; font-size:24px;"><i style="font-size:32px;">&#8734;</i>NXTY</div>
</div>""" + FOOT

def chiusura():
    return HEAD + f"""
<div class="slide" style="background:radial-gradient(1000px 820px at 50% 40%, #17162C 0%, #08080E 76%); color:{CREMA};">
  <div style="position:absolute; left:96px; right:96px; top:0; bottom:300px; display:flex; flex-direction:column; justify-content:center;">
    <div style="font-size:100px; font-weight:800; line-height:1.05; letter-spacing:-.015em;">Nel dizionario<br>{k('non ci sono.')}</div>
    <div style="margin-top:52px; font-size:54px; font-weight:800; line-height:1.2; color:{GOLD};">
      {k('Ci sono nella sua voce. Tienila.')}</div>
  </div>
  <div style="position:absolute; left:0; right:0; bottom:104px; display:flex; flex-direction:column; align-items:center; gap:26px;">
    <img src="file://{BASE}/logo_oro.png" style="width:116px;">
    <div style="font-size:26px; font-weight:800; letter-spacing:.3em; color:rgba(253,251,246,.62);">NEXT TO YOU</div>
  </div>
</div>""" + FOOT

SLIDES = [copertina()] + [voce(i + 1, l, c, d) for i, (l, c, d) in enumerate(VOCI)] + [chiusura()]

if __name__ == "__main__":
    os.makedirs(OUTDIR, exist_ok=True)
    out = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        ctx = b.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg = ctx.new_page()
        for i, html in enumerate(SLIDES, 1):
            hp = f"{BASE}/caro_1101_s{i}.html"
            with open(hp, "w", encoding="utf-8") as f: f.write(html)
            pg.goto(f"file://{hp}", wait_until="networkidle"); pg.wait_for_timeout(300)
            tmp = f"{BASE}/_caro_s{i}.png"
            pg.screenshot(path=tmp)
            jp = f"{OUTDIR}/caro_1101_{ID}_s{i}.jpg"
            Image.open(tmp).convert("RGB").save(jp, "JPEG", quality=92, optimize=True)
            out.append(jp)
        b.close()
    for o in out: print(o, os.path.getsize(o)//1024, "KB")
