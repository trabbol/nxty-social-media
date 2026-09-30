#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_frames.py — renderer ufficiale dei reel NXTY.
Uso: python3 render_frames.py file.html out.mp4 durata_ms

Cattura 30 fps a 1080x1920. Per avere frame precisi senza dipendere dalla velocita'
degli screenshot, la pagina viene rallentata di SLOW volte (setTimeout/setInterval
riscalati + playbackRate sulle animazioni CSS): ogni fotogramma logico dura cosi'
SLOW*33ms di tempo reale, abbastanza per catturarlo con calma. Il video finale e'
a velocita' normale.
Ricostruito il 31/08/2026 dopo l'azzeramento del workspace, e di nuovo il 30/09/2026
(secondo azzeramento) dalla copia letta nella sessione. NON aggiunge audio: l'audio
si genera a parte (audio_MMDD.py) e si unisce con ffmpeg (direttiva 32)."""
import base64, os, shutil, subprocess, sys, time
from playwright.sync_api import sync_playwright

FPS = 30
W, H = 1080, 1920
SLOW = 12  # fattore di rallentamento: deve essere abbastanza alto che ogni screenshot
           # stia dentro il budget di 1000/FPS*SLOW ms, altrimenti il video accelera

INIT = """
(() => {
  const K = %d;
  const st = window.setTimeout, si = window.setInterval;
  window.setTimeout = (fn, d, ...a) => st(fn, (d || 0) * K, ...a);
  window.setInterval = (fn, d, ...a) => si(fn, (d || 0) * K, ...a);
  const tick = () => {
    try { for (const an of document.getAnimations()) { if (an.playbackRate !== 1 / K) an.playbackRate = 1 / K; } } catch (e) {}
    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
})();
"""


def main():
    if len(sys.argv) != 4:
        print("uso: python3 render_frames.py file.html out.mp4 durata_ms"); sys.exit(1)
    html, out, dur_ms = sys.argv[1], sys.argv[2], int(sys.argv[3])
    html = os.path.abspath(html)
    n = int(round(dur_ms / 1000 * FPS))
    frame_real = (1000.0 / FPS) * SLOW / 1000.0  # secondi reali per fotogramma
    tmp = os.path.abspath("_frames")
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--force-color-profile=srgb", "--font-render-hinting=none"])
        ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=1)
        pg = ctx.new_page()
        pg.add_init_script(INIT % SLOW)
        cdp = ctx.new_cdp_session(pg)
        pg.goto(f"file://{html}", wait_until="load")
        t0 = time.monotonic()
        late = 0
        for i in range(n):
            target = t0 + i * frame_real
            d = target - time.monotonic()
            if d > 0:
                time.sleep(d)
            elif i and d < -0.02:
                late += 1
            shot = cdp.send("Page.captureScreenshot", {"format": "jpeg", "quality": 94, "fromSurface": True})
            with open(f"{tmp}/f{i:05d}.jpg", "wb") as fh:
                fh.write(base64.b64decode(shot["data"]))
            if (i + 1) % 120 == 0:
                print(f"frame {i+1}/{n}", flush=True)
        ctx.close(); browser.close()
    if late:
        print(f"ATTENZIONE: {late}/{n} fotogrammi catturati in ritardo — il video risulterebbe accelerato. Alza SLOW.")

    subprocess.run([
        "ffmpeg", "-loglevel", "error", "-y", "-framerate", str(FPS),
        "-i", f"{tmp}/f%05d.jpg",
        "-c:v", "libx264", "-preset", "slow", "-crf", "20",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart", out,
    ], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    print(f"frames ok: {os.path.basename(out)} {os.path.getsize(out)//1024} KB")


if __name__ == "__main__":
    main()
