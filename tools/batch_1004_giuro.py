#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Domenica 4/10 — storia "giuro" pubblicata su ordine diretto di Alessandro (ripartenza dopo due giorni fermi).
Annuncia il carosello del pomeriggio con il segno della serie: la promessa con "non" e "mai" barrati in oro,
che si legge "Io queste frasi le diro'"."""
from playwright.sync_api import sync_playwright
from PIL import Image
import os
BASE = "/home/claude/nxty/demo"
FONTS = f"{BASE}/node_modules/@fontsource/plus-jakarta-sans/files"
REPO = "/home/claude/nxty/repo"
GOLD, NOTTE, CREMA = "#DCA659", "#0B0B12", "#FDFBF6"
S = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-600-normal.woff2') format('woff2'); font-weight:600; }}
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-700-normal.woff2') format('woff2'); font-weight:700; }}
@font-face {{ font-family:'PJS'; src:url('file://{FONTS}/plus-jakarta-sans-latin-800-normal.woff2') format('woff2'); font-weight:800; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1920px; font-family:'PJS',sans-serif; -webkit-font-smoothing:antialiased; background:{CREMA}; }}
.wm {{ display:flex; align-items:center; gap:16px; font-weight:800; letter-spacing:.32em; font-size:36px; justify-content:center; color:{NOTTE}; }}
.wm i {{ color:{GOLD}; font-size:48px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-4px); }}
.pt {{ margin-left:-.075em; }}
.barrato {{ position:relative; color:rgba(11,11,18,.40); }}
.barrato::after {{ content:''; position:absolute; left:-10px; right:-10px; top:58%; height:11px; border-radius:6px;
  background:{GOLD}; transform:rotate(-3deg); }}
</style></head><body>
<div style="width:1080px; height:1920px; position:relative; overflow:hidden; color:{NOTTE};">
  <div class="wm" style="position:absolute; top:112px; left:0; right:0;"><i>&#8734;</i>NXTY</div>
  <div style="position:absolute; left:110px; right:96px; top:0; bottom:120px; display:flex; flex-direction:column; justify-content:center;">
    <div style="font-weight:800; letter-spacing:.26em; font-size:30px; color:{GOLD};">LA PROMESSA</div>
    <div style="margin-top:44px; font-size:116px; font-weight:800; line-height:1.08; letter-spacing:-.015em;">
      Io queste frasi<br><span class="barrato">non</span> le dir&ograve;<br><span class="barrato">mai</span><span class="pt">.</span>
    </div>
    <div style="margin-top:96px; font-size:50px; font-weight:800; line-height:1.2; color:{GOLD};">
      Le frasi che giuravi<br>di non dire<span class="pt">.</span></div>
    <div style="margin-top:22px; font-size:38px; font-weight:600; color:rgba(11,11,18,.55);">Oggi pomeriggio, nel feed<span class="pt">.</span></div>
  </div>
  <div style="position:absolute; bottom:96px; left:0; right:0; display:flex; justify-content:center;">
    <img src="file://{BASE}/logo_oro.png" style="width:92px;">
  </div>
</div></body></html>"""
name, out = "1004_1030_giuro", f"{REPO}/stories/daily/1004_1030_giuro.jpg"
with sync_playwright() as p:
    b = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
    with open(f"{BASE}/{name}.html", "w", encoding="utf-8") as f: f.write(S)
    ctx = b.new_context(viewport={"width":1080, "height":1920}, device_scale_factor=1)
    pg = ctx.new_page(); pg.goto(f"file://{BASE}/{name}.html", wait_until="networkidle"); pg.wait_for_timeout(500)
    pg.screenshot(path=f"{BASE}/_tmp1004g.png")
    Image.open(f"{BASE}/_tmp1004g.png").convert("RGB").save(out, "JPEG", quality=92, optimize=True)
    b.close()
print("ok", out, os.path.getsize(out)//1024, "KB")
