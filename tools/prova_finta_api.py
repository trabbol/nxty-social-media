#!/usr/bin/env python3
"""Prova di tools/pubblica.py contro una finta Graph API locale (nessuna chiamata a Meta, token finto).
Rifatto il 30/10/2026 dopo l'azzeramento del container, dal modello sim93.py dello scratchpad, perche' la prova
sopravviva ai prossimi azzeramenti. Uso:
  python3 prova_finta_api.py ID AAAA-MM-GG RID PUBBLICATI.json CARTELLA_DI_LAVORO
Esempio: python3 prova_finta_api.py 99 2026-11-01 2026-11-01-caro99 /tmp/x/pubblicati_gh.json /tmp/x/repo_sim99
Fa tre giri: slot post alle 16:31Z (DRY_RUN), slot storia alle 19:31Z (DRY_RUN, deve aspettare il post),
riserva via richiesta.json alle 16:33Z (finta API: pubblica davvero solo sul finto server)."""
import json, os, shutil, subprocess, sys, threading, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

ID, DATA, RID, PUBBLICATI, W = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
TOK = "TESTTOKEN-XYZ"
IG = "17841480193943878"
LOG = []
STATE = {"recent": [], "stories": [], "n": 0, "polls": {}}

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def _auth(self):
        assert TOK not in self.path, "TOKEN NELL'URL!"
        return self.headers.get("Authorization") == f"Bearer {TOK}"
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); q = dict(urllib.parse.parse_qsl(u.query))
        path = u.path.replace("/v21.0/", "")
        LOG.append(("GET", path, q))
        if not self._auth():
            return self._send(400, {"error": {"message": "Invalid OAuth access token.", "code": 190}})
        if path == IG:
            return self._send(200, {"id": IG, "username": "nxty_app", "followers_count": 53, "media_count": 60})
        if path == f"{IG}/media":
            return self._send(200, {"data": STATE["recent"]})
        if path == f"{IG}/stories":
            return self._send(200, {"data": STATE["stories"]})
        if q.get("fields") == "status_code":
            n = STATE["polls"].get(path, 0); STATE["polls"][path] = n + 1
            return self._send(200, {"status_code": "IN_PROGRESS" if n == 0 else "FINISHED", "id": path})
        if q.get("fields") == "permalink,timestamp":
            return self._send(200, {"permalink": f"https://www.instagram.com/p/{path}/", "timestamp": "2026-10-04T15:31:00+0000"})
        return self._send(404, {"error": {"message": "unknown", "code": 100}})
    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0)); body = dict(urllib.parse.parse_qsl(self.rfile.read(n).decode()))
        path = urllib.parse.urlparse(self.path).path.replace("/v21.0/", "")
        LOG.append(("POST", path, body))
        assert TOK not in json.dumps(body), "TOKEN NEL CORPO!"
        if not self._auth():
            return self._send(400, {"error": {"message": "Invalid OAuth access token.", "code": 190}})
        STATE["n"] += 1
        if path == f"{IG}/media":
            return self._send(200, {"id": f"c{STATE['n']}"})
        if path == f"{IG}/media_publish":
            return self._send(200, {"id": f"m{STATE['n']}"})
        return self._send(404, {"error": {"message": "unknown", "code": 100}})

srv = HTTPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

SRC = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
shutil.rmtree(W, ignore_errors=True); os.makedirs(W + "/tools")
shutil.copy(SRC + "/tools/pubblica.py", W + "/tools/")
shutil.copy(SRC + "/posts.json", W + "/posts.json")
shutil.copy(PUBBLICATI, W + "/pubblicati.json")

def run(env, label):
    LOG.clear()
    e = dict(os.environ, API_BASE=f"http://127.0.0.1:{port}/v21.0", REPO_DIR=W, PASSO_POLL="0.05", META_TOKEN=TOK, **env)
    r = subprocess.run([sys.executable, W + "/tools/pubblica.py"], env=e, capture_output=True, text=True)
    st = json.load(open(W + "/stato_pubblicazione.json"))
    print(f"--- {label}: exit {r.returncode} | azioni={st['azioni']} | errori={st['errori']} | POST={sum(1 for m,_,_ in LOG if m=='POST')}")
    if r.returncode != 0: print(r.stderr[-1500:])
    return st

run({"EVENTO": "schedule", "CRON": "30 15 * * *", "ADESSO_TEST": f"{DATA}T16:31:00Z", "DRY_RUN": "true"}, f"{DATA} slot post {ID} (16:31Z, prova)")
run({"EVENTO": "schedule", "CRON": "30 18 * * *", "ADESSO_TEST": f"{DATA}T19:31:00Z", "DRY_RUN": "true"}, f"{DATA} slot storia {ID} (19:31Z, prova)")
json.dump({"rid": RID, "id": int(ID), "slot": "post", "entro": f"{DATA}T19:00:00Z", "ordine": "prova"}, open(W + "/richiesta.json", "w"), indent=1)
run({"EVENTO": "push", "ADESSO_TEST": f"{DATA}T16:33:00Z", "DRY_RUN": "true"}, f"{DATA} riserva {ID} alle 16:33Z via richiesta.json (finta API)")
print("    POST:", [(p, {k: (v[:60] if isinstance(v, str) else v) for k, v in b.items()
                      if k in ("media_type", "video_url", "image_url", "is_carousel_item", "children", "share_to_feed", "creation_id")})
                  for m, p, b in LOG if m == "POST"])
print(f"    pubblicati {ID}:", json.load(open(W + "/pubblicati.json")).get(str(ID)))
