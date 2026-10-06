#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mercoledi' 7/10 — storia serale "pina" (18:30Z) del reel 74, "Il vocale della nonna" ep. 3.
Ora che i reel escono normali (direttiva 34) la storia puo' rimandare al reel: amplifica scura
che incorpora il fotogramma a 8,6 s del reel 68 (trascrizione completa)."""
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
html,body {{ width:1080px; height:1920px; font-family:'PJS',sans-serif; -webkit-font-smoothing:antialiased; }}
.wm {{ display:flex; align-items:center; gap:16px; font-weight:800; letter-spacing:.32em; font-size:36px; justify-content:center; color:{CREMA}; }}
.wm i {{ color:{GOLD}; font-size:48px; font-style:normal; letter-spacing:0; font-weight:700; transform:translateY(-4px); }}
.kick {{ font-weight:700; letter-spacing:.3em; font-size:29px; color:{GOLD}; text-transform:uppercase; text-align:center; }}
</style></head><body>
<div style="width:1080px; height:1920px; position:relative; overflow:hidden; display:flex; flex-direction:column; align-items:center;
  background:radial-gradient(1100px 900px at 50% 30%, #17162C 0%, #08080E 74%); color:{CREMA}; padding:112px 74px 270px;">
  <div class="wm"><i>&#8734;</i>NXTY</div>
  <div class="kick" style="margin-top:40px;">Episodio 3</div>
  <div style="margin:auto 0; display:flex; flex-direction:column; align-items:center;">
    <div style="width:540px; height:960px; overflow:hidden; border-radius:34px; flex:0 0 auto;
      border:1px solid rgba(220,166,89,.30); box-shadow:0 34px 90px rgba(0,0,0,.55);">
      <img src="file://{BASE}/_frame74.jpg" style="width:540px; height:960px; display:block;">
    </div>
    <div style="margin-top:58px; font-size:44px; font-weight:800; line-height:1.3; text-align:center; color:{CREMA};">
      Il vocale della nonna.<br><span style="color:{GOLD};">Con il telegiornale acceso.</span></div>
  </div>
  <div style="font-size:30px; font-weight:600; text-align:center; color:rgba(253,251,246,.54);">Il reel &egrave; nel feed.</div>
  <div style="position:absolute; bottom:96px; left:0; right:0; display:flex; justify-content:center;">
    <img src="file://{BASE}/logo_oro.png" style="width:92px;">
  </div>
</div></body></html>"""
name, out = "1007_2030_pina", f"{REPO}/stories/daily/1007_2030_pina.jpg"
with sync_playwright() as p:
    b = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
    with open(f"{BASE}/{name}.html", "w", encoding="utf-8") as f: f.write(S)
    ctx = b.new_context(viewport={"width":1080, "height":1920}, device_scale_factor=1)
    pg = ctx.new_page(); pg.goto(f"file://{BASE}/{name}.html", wait_until="networkidle"); pg.wait_for_timeout(500)
    pg.screenshot(path=f"{BASE}/_tmp1007.png")
    Image.open(f"{BASE}/_tmp1007.png").convert("RGB").save(out, "JPEG", quality=92, optimize=True)
    b.close()
print("ok", out, os.path.getsize(out)//1024, "KB")
