#!/usr/bin/env python3
"""Prova di tools/pubblica.py contro una finta Graph API locale (nessuna chiamata a Meta)."""
import json, os, shutil, subprocess, sys, threading, urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

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
            mid = f"m{STATE['n']}"
            if body["creation_id"] and STATE.get("story_mode"):
                STATE["stories"].append({"id": mid, "timestamp": "2026-10-04T18:31:00+0000"})
            return self._send(200, {"id": mid})
        return self._send(404, {"error": {"message": "unknown", "code": 100}})

srv = HTTPServer(("127.0.0.1", 0), H); port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()

SRC = "/home/claude/nxty/repo"
W = "/tmp/claude-0/-home-claude/396d5fe2-c946-568d-88e5-7c0343336e5d/scratchpad/repo_test"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W + "/tools")
shutil.copy(SRC + "/tools/pubblica.py", W + "/tools/")
posts = json.load(open(SRC + "/posts.json", encoding="utf-8"))
for p in posts["posts"]:
    if p["id"] == 71:
        p["data"] = "2026-10-04"; p["pubblica_auto"] = True
        p["storie"] = [{"ora": "20:30", "nome": "test", "file": "stories/daily/x.jpg"}]
    if p["id"] == 70:
        p["data"] = "2026-10-05"; p["pubblica_auto"] = True
posts["posts"].append({"id": 72, "data": "2026-10-04", "tipo": "storia", "pubblica_auto": True, "solo_su_richiesta": True,
                       "storie": [{"nome": "giuro", "file": "stories/daily/1004_1030_giuro.jpg"}]})
json.dump(posts, open(W + "/posts.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def run(env, label):
    LOG.clear()
    e = dict(os.environ, API_BASE=f"http://127.0.0.1:{port}/v21.0", REPO_DIR=W, PASSO_POLL="0.05", **env)
    r = subprocess.run([sys.executable, W + "/tools/pubblica.py"], env=e, capture_output=True, text=True)
    st = json.load(open(W + "/stato_pubblicazione.json"))
    posts_calls = [(m, p) for m, p, _ in LOG if m == "POST"]
    print(f"--- {label}: exit {r.returncode} | azioni={st['azioni']} | errori={st['errori']} | POST={len(posts_calls)}")
    assert TOK not in r.stdout and TOK not in r.stderr, "TOKEN NELL'OUTPUT!"
    assert TOK not in open(W + "/stato_pubblicazione.json").read()
    return r.returncode, st

# 1 token mancante
c, st = run({"META_TOKEN": "", "EVENTO": "schedule", "CRON": "30 15 * * *"}, "1 senza token")
assert c == 1 and "META_TOKEN mancante" in st["errori"][0]
# 2 token sbagliato
c, st = run({"META_TOKEN": "sbagliato", "EVENTO": "schedule", "CRON": "30 15 * * *"}, "2 token sbagliato")
assert c == 1 and "token non valido" in st["errori"][0]
# 3 push = prova
c, st = run({"META_TOKEN": TOK, "EVENTO": "push", "ADESSO_TEST": "2026-10-04T10:00:00Z"}, "3 push (prova)")
assert c == 0 and st["dry_run"] and "PROVA" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
assert not os.path.exists(W + "/pubblicati.json")
# 4 giro programmato fuori finestra
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 15 * * *", "ADESSO_TEST": "2026-10-04T20:10:00Z"}, "4 fuori finestra")
assert c == 0 and "fuori finestra" in st["azioni"][0]
# 5 storia prima del post: aspetta
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 18 * * *", "ADESSO_TEST": "2026-10-04T18:31:00Z"}, "5 storia senza post")
assert c == 0 and "aspetta" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
# 6 carosello vero
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 15 * * *", "ADESSO_TEST": "2026-10-04T15:33:00Z"}, "6 carosello")
assert c == 0 and "pubblicato" in st["azioni"][0]
figli = [b for m, p, b in LOG if m == "POST" and b.get("is_carousel_item") == "true"]
padre = [b for m, p, b in LOG if m == "POST" and b.get("media_type") == "CAROUSEL"]
assert len(figli) == 8 and figli[0]["image_url"].endswith("posts/daily/caro_1003_71_s1.jpg") and figli[7]["image_url"].endswith("_s8.jpg")
assert len(padre) == 1 and len(padre[0]["children"].split(",")) == 8 and padre[0]["caption"].startswith("A quindici anni")
pub = json.load(open(W + "/pubblicati.json")); assert pub["71"]["permalink"]
print("   figli in ordine:", [f["image_url"].rsplit("/", 1)[1] for f in figli])
# 7 stesso giro ripetuto: niente doppione
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 15 * * *", "ADESSO_TEST": "2026-10-04T15:40:00Z"}, "7 ripetuto")
assert c == 0 and "gia' pubblicato" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
# 8 storia dopo il post
STATE["story_mode"] = True
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 18 * * *", "ADESSO_TEST": "2026-10-04T18:32:00Z"}, "8 storia")
assert c == 0 and "storia pubblicata" in st["azioni"][0]
sto = [b for m, p, b in LOG if m == "POST" and b.get("media_type") == "STORIES"]; assert len(sto) == 1
# 9 storia ripetuta
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 18 * * *", "ADESSO_TEST": "2026-10-04T18:40:00Z"}, "9 storia ripetuta")
assert c == 0 and "gia' pubblicata" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
STATE["story_mode"] = False
# 10 reel del 5/10 gia' online (pubblicato a mano): anti-doppione sulla didascalia
cap70 = [p for p in posts["posts"] if p["id"] == 70][0]["caption"]
STATE["recent"] = [{"id": "999", "caption": cap70, "permalink": "https://www.instagram.com/reel/MANUALE/", "timestamp": "2026-10-05T15:00:00+0000"}]
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 15 * * *", "ADESSO_TEST": "2026-10-05T15:31:00Z"}, "10 anti-doppione")
assert c == 0 and "gia' online" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
assert json.load(open(W + "/pubblicati.json"))["70"]["permalink"].endswith("MANUALE/")
# 11 reel vero (didascalia diversa in griglia)
STATE["recent"] = []
pj = json.load(open(W + "/pubblicati.json")); pj.pop("70"); json.dump(pj, open(W + "/pubblicati.json", "w"))
c, st = run({"META_TOKEN": TOK, "EVENTO": "workflow_dispatch", "SLOT": "post", "POST_ID": "70", "DRY_RUN": "false"}, "11 reel a mano")
reel = [b for m, p, b in LOG if m == "POST" and b.get("media_type") == "REELS"]
assert c == 0 and len(reel) == 1 and reel[0]["share_to_feed"] == "true" and reel[0]["video_url"].endswith("posts/daily/reel_1002_70.mp4")
# 12 workflow_dispatch in prova
pj = json.load(open(W + "/pubblicati.json")); pj.pop("70"); json.dump(pj, open(W + "/pubblicati.json", "w"))
c, st = run({"META_TOKEN": TOK, "EVENTO": "workflow_dispatch", "SLOT": "post", "POST_ID": "70", "DRY_RUN": "true"}, "12 prova a mano")
assert c == 0 and "PROVA" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
# 13 richiesta.json valida su push: storia 72 pubblicata davvero
STATE["recent"] = []; STATE["stories"] = []; STATE["story_mode"] = True
for f in ("pubblicati.json",):
    if os.path.exists(W + "/" + f): os.remove(W + "/" + f)
json.dump({"rid": "2026-10-04-giuro", "id": 72, "slot": "storia", "entro": "2026-10-04T11:30:00Z"}, open(W + "/richiesta.json", "w"))
c, st = run({"META_TOKEN": TOK, "EVENTO": "push", "ADESSO_TEST": "2026-10-04T10:20:00Z"}, "13 richiesta storia")
sto = [b for m, p, b in LOG if m == "POST" and b.get("media_type") == "STORIES"]
assert c == 0 and not st["dry_run"] and st.get("richiesta") == "2026-10-04-giuro" and len(sto) == 1
assert sto[0]["image_url"].endswith("stories/daily/1004_1030_giuro.jpg")
pj = json.load(open(W + "/pubblicati.json")); assert "2026-10-04-giuro" in pj["_richieste"] and pj["72"]["storie"]["0"]
# 14 stesso push ripetuto: niente doppione
c, st = run({"META_TOKEN": TOK, "EVENTO": "push", "ADESSO_TEST": "2026-10-04T10:25:00Z"}, "14 richiesta ripetuta")
assert c == 0 and st["dry_run"] and "gia' eseguita" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
# 15 richiesta scaduta
json.dump({"rid": "altra", "id": 72, "slot": "storia", "entro": "2026-10-04T09:00:00Z"}, open(W + "/richiesta.json", "w"))
c, st = run({"META_TOKEN": TOK, "EVENTO": "push", "ADESSO_TEST": "2026-10-04T10:30:00Z"}, "15 richiesta scaduta")
assert c == 0 and st["dry_run"] and "scaduta" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
os.remove(W + "/richiesta.json")
# 16 giro delle 15:30Z: carosello 71 (la 72 e' solo su richiesta e non c'entra)
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 15 * * *", "ADESSO_TEST": "2026-10-04T15:32:00Z"}, "16 carosello dopo la storia")
assert c == 0 and len(st["azioni"]) == 1 and "71: pubblicato" in st["azioni"][0]
# 17 giro delle 18:30Z: la storia del carosello esce anche se oggi c'e' gia' la storia 72 (tetto 3)
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 18 * * *", "ADESSO_TEST": "2026-10-04T18:33:00Z"}, "17 seconda storia del giorno")
sto = [b for m, p, b in LOG if m == "POST" and b.get("media_type") == "STORIES"]
assert c == 0 and len(sto) == 1 and "storia pubblicata" in st["azioni"][0] and len(st["azioni"]) == 1
# 18 tetto: con 3 storie oggi non ne aggiunge
pj = json.load(open(W + "/pubblicati.json")); pj["71"].pop("storie"); json.dump(pj, open(W + "/pubblicati.json", "w"))
STATE["stories"] += [{"id": "x1", "timestamp": "2026-10-04T12:00:00+0000"}]
c, st = run({"META_TOKEN": TOK, "EVENTO": "schedule", "CRON": "30 18 * * *", "ADESSO_TEST": "2026-10-04T18:40:00Z"}, "18 tetto 3 storie")
assert c == 0 and "non ne aggiungo" in st["azioni"][0] and not any(m == "POST" for m, _, _ in LOG)
STATE["story_mode"] = False
print("TUTTE LE PROVE PASSATE")
