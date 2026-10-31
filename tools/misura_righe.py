#!/usr/bin/env python3
"""Misura gli a capo delle righe di un reel prima del render (rifatto il 31/10/2026 dopo l'azzeramento del container).
Uso: python3 misura_righe.py file.html
- «Il vocale della nonna»: altezza di ogni .riga .txt a scheda aperta (46 px su due righe = 109 px; la riga del suono,
  40 px, su due righe = 94 px), larghezza del cartello finale e fondo della scheda.
- «Per chi verra'»: numero di righe di ogni .msg .t, fondo delle due schede e cartello."""
import sys
from playwright.sync_api import sync_playwright

html = sys.argv[1]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920})
    pg.goto("file://" + html, wait_until="load"); pg.wait_for_timeout(400)
    r = pg.evaluate("""() => { document.getAnimations().forEach(a => a.cancel());
      const out = [];
      document.querySelectorAll('.riga').forEach(m => { m.style.opacity = 1; m.style.maxHeight = 'none'; m.style.animation = 'none'; });
      document.querySelectorAll('.riga .txt').forEach(t => out.push(['riga', Math.round(t.getBoundingClientRect().height), Math.round(t.getBoundingClientRect().width), t.textContent]));
      document.querySelectorAll('.msg .t').forEach(t => { const rr = Array.from(t.getClientRects());
        out.push(['msg', rr.length + ' righe', Math.round(Math.max(...rr.map(x => x.width))), t.textContent.slice(0, 60)]); });
      for (const sel of ['.scheda', '.sopra', '.basso']) { const e = document.querySelector(sel);
        if (e) { const q = e.getBoundingClientRect(); out.push(['fondo ' + sel, Math.round(q.bottom), '', '']); } }
      document.querySelectorAll('.fine .riga-f').forEach(f => { const q = f.getBoundingClientRect();
        out.push(['fine', Math.round(q.height), Math.round(q.width), f.textContent]); });
      return out; }""")
    for x in r: print(*x)
    b.close()
