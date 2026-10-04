#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pubblicazione automatica su Instagram per @nxty_app, eseguita da GitHub Actions
(.github/workflows/pubblica.yml).

Regole:
- Il token Meta sta SOLO nel secret META_TOKEN del repository. Non si stampa e non entra mai in un URL:
  viaggia nell'intestazione Authorization.
- Si pubblica solo cio' che e' in posts.json con "pubblica_auto": true e la data di oggi (UTC).
  Slot "post" (15:30Z): reel o carosello. Slot "storia" (18:30Z): le storie con un "file", solo se il
  post del giorno e' gia' uscito.
- Anti-doppione: prima di pubblicare un post si confronta la didascalia con gli ultimi media
  dell'account; prima di una storia si controlla che oggi non ne sia gia' uscita una.
- Questo script non modifica posts.json (lo scrive solo la regia). Scrive due file suoi:
  pubblicati.json (id -> permalink, media_id, ora, storie) e stato_pubblicazione.json (esito dell'ultimo giro,
  follower e numero di post, che sono dati pubblici del profilo).
- DRY_RUN=true: legge tutto e dice cosa farebbe, senza nessuna chiamata che pubblica. Un push e' sempre una
  prova, TRANNE quando nel repository c'e' richiesta.json valida (ordine diretto di Alessandro, eseguito una
  volta sola): {"rid": "...", "id": 72, "slot": "storia", "entro": "2026-10-04T11:30:00Z"}.
- Le entry con "solo_su_richiesta": true non escono mai dai giri programmati, solo da richiesta.json o da
  un avvio manuale con post_id. Le entry "tipo": "storia" sono storie da sole, senza post da aspettare.
- Storie: mai la stessa due volte (id registrato) e al massimo MAX_STORIE al giorno.
"""
import datetime as dt
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

VERSIONE = "2026-10-04e"  # cambiarla insieme a richiesta.json fa partire il workflow su push
API = os.environ.get("API_BASE", "https://graph.facebook.com/v21.0").rstrip("/")
RAW = os.environ.get("RAW_BASE", "https://raw.githubusercontent.com/trabbol/nxty-social-media/main").rstrip("/") + "/"
IG = os.environ.get("IG_USER_ID", "17841480193943878")
TOKEN = os.environ.get("META_TOKEN", "").strip()
EVENTO = os.environ.get("EVENTO", "manuale")
CRON = os.environ.get("CRON", "").strip()
SLOT_IN = os.environ.get("SLOT", "").strip()
ID_IN = os.environ.get("POST_ID", "").strip()
DRY = os.environ.get("DRY_RUN", "false").strip().lower() == "true" or EVENTO == "push"
RADICE = os.environ.get("REPO_DIR", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASSO_POLL = float(os.environ.get("PASSO_POLL", "8"))
ADESSO = (dt.datetime.fromisoformat(os.environ["ADESSO_TEST"].replace("Z", "+00:00"))
          if os.environ.get("ADESSO_TEST") else dt.datetime.now(dt.timezone.utc))

# finestre (UTC) entro cui un giro programmato puo' ancora pubblicare: GitHub a volte parte in ritardo,
# ma un post non deve uscire a mezzanotte. Un avvio manuale (workflow_dispatch) e' un ordine diretto: niente finestra.
FINESTRE = {"post": (15.25, 19.5), "storia": (18.25, 22.0)}
MAX_STORIE = 3
CRON_SLOT = {"30 15 * * *": "post", "30 18 * * *": "storia"}

stato = {"ultimo_giro": ADESSO.strftime("%Y-%m-%dT%H:%M:%SZ"), "evento": EVENTO, "slot": None,
         "dry_run": DRY, "token_ok": False, "account": None, "azioni": [], "errori": []}


class ApiError(Exception):
    pass


def call(method, path, params=None):
    url = f"{API}/{path}"
    data = None
    if method == "GET" and params:
        url += "?" + urllib.parse.urlencode(params)
    elif params is not None:
        data = urllib.parse.urlencode(params).encode()
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Authorization": f"Bearer {TOKEN}"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            err = json.loads(e.read().decode()).get("error", {})
        except Exception:
            err = {}
        raise ApiError(f"{err.get('message', 'HTTP ' + str(e.code))} "
                       f"(code {err.get('code')}, subcode {err.get('error_subcode')})") from None
    except urllib.error.URLError as e:
        raise ApiError(f"rete: {e.reason}") from None


def leggi(nome, vuoto):
    p = os.path.join(RADICE, nome)
    if not os.path.exists(p):
        return vuoto
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def scrivi(nome, obj):
    with open(os.path.join(RADICE, nome), "w", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False, indent=1) + "\n")


def norm(testo):
    return " ".join((testo or "").split())[:80]


def attendi(cid, max_s, passo=None):
    passo = passo or PASSO_POLL
    t0 = time.time()
    while True:
        s = call("GET", cid, {"fields": "status_code"})
        sc = s.get("status_code")
        if sc in ("FINISHED", "PUBLISHED"):
            return
        if sc in ("ERROR", "EXPIRED"):
            raise ApiError(f"container {cid}: {sc}")
        if time.time() - t0 > max_s:
            raise ApiError(f"container {cid}: ancora {sc} dopo {max_s}s (non pubblicato)")
        time.sleep(passo)


def pubblica_e_permalink(cid):
    m = call("POST", f"{IG}/media_publish", {"creation_id": cid})
    info = call("GET", m["id"], {"fields": "permalink,timestamp"})
    return m["id"], info.get("permalink"), info.get("timestamp")


def pubblica_post(p):
    if p["tipo"] == "reel":
        c = call("POST", f"{IG}/media", {"media_type": "REELS", "video_url": RAW + p["video"],
                                          "caption": p["caption"], "share_to_feed": "true"})
        attendi(c["id"], max_s=900)
        return pubblica_e_permalink(c["id"])
    if p["tipo"] == "carosello":
        figli = []
        for f in p["slide"]:
            figli.append(call("POST", f"{IG}/media", {"image_url": RAW + f, "is_carousel_item": "true"})["id"])
        for cid in figli:
            attendi(cid, max_s=300)
        c = call("POST", f"{IG}/media", {"media_type": "CAROUSEL", "children": ",".join(figli),
                                          "caption": p["caption"]})
        attendi(c["id"], max_s=300)
        return pubblica_e_permalink(c["id"])
    raise ApiError(f"tipo non gestito: {p['tipo']}")


def pubblica_storia(file):
    c = call("POST", f"{IG}/media", {"media_type": "STORIES", "image_url": RAW + file})
    attendi(c["id"], max_s=300)
    m = call("POST", f"{IG}/media_publish", {"creation_id": c["id"]})
    return m["id"]


def slot_del_giro():
    if SLOT_IN in ("post", "storia"):
        return SLOT_IN
    if CRON in CRON_SLOT:
        return CRON_SLOT[CRON]
    return "post" if EVENTO == "push" else None


def leggi_richiesta(pubblicati):
    """Ordine diretto via richiesta.json: valido solo su push, entro la scadenza e una volta sola."""
    if EVENTO != "push":
        return None
    r = leggi("richiesta.json", None)
    if not r or not r.get("rid") or r.get("slot") not in ("post", "storia") or not r.get("id"):
        return None
    if r["rid"] in pubblicati.get("_richieste", {}):
        stato["azioni"].append(f"richiesta {r['rid']} gia' eseguita, la ignoro")
        return None
    try:
        entro = dt.datetime.fromisoformat(str(r.get("entro", "")).replace("Z", "+00:00"))
    except ValueError:
        return None
    if ADESSO > entro:
        stato["azioni"].append(f"richiesta {r['rid']} scaduta ({r.get('entro')}), la ignoro")
        return None
    return r


def allinea_al_remoto():
    """Su GitHub Actions porta il checkout all'ultimo main prima di decidere: un giro partito in ritardo
    (o in coda dietro un altro) vede cosi' il registro aggiornato e non ripubblica."""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    r = subprocess.run(["git", "-C", RADICE, "pull", "--ff-only", "--quiet", "origin", "main"],
                       capture_output=True, text=True, timeout=90)
    stato["allineato"] = r.returncode == 0
    if r.returncode != 0:
        stato["azioni"].append("attenzione: allineamento a origin/main non riuscito, uso il checkout dell'evento")


def main():
    global DRY, ID_IN
    allinea_al_remoto()
    pubblicati = leggi("pubblicati.json", {})
    slot = slot_del_giro()
    richiesta = leggi_richiesta(pubblicati)
    if richiesta:
        DRY, ID_IN, slot = False, str(richiesta["id"]), richiesta["slot"]
        stato["richiesta"] = richiesta["rid"]
        stato["dry_run"] = False
    stato["slot"] = slot
    if not TOKEN:
        stato["errori"].append("META_TOKEN mancante: va aggiunto nei secret del repository")
        return 1
    try:
        acc = call("GET", IG, {"fields": "username,followers_count,media_count"})
        stato["token_ok"] = True
        stato["account"] = {k: acc.get(k) for k in ("username", "followers_count", "media_count")}
    except ApiError as e:
        stato["errori"].append(f"token non valido o scaduto: {e}")
        return 1
    if slot is None:
        stato["errori"].append(f"slot sconosciuto (evento {EVENTO}, cron '{CRON}')")
        return 1
    if EVENTO == "schedule":
        ora = ADESSO.hour + ADESSO.minute / 60
        lo, hi = FINESTRE[slot]
        if not lo <= ora < hi:
            stato["azioni"].append(f"giro fuori finestra ({ADESSO:%H:%M}Z): non pubblico niente")
            return 0

    posts = leggi("posts.json", {"posts": []})["posts"]
    oggi = ADESSO.date().isoformat()
    if richiesta:
        pubblicati.setdefault("_richieste", {})[richiesta["rid"]] = {"eseguita": stato["ultimo_giro"],
                                                                     "id": richiesta["id"], "slot": slot}

    if ID_IN:
        cand = [p for p in posts if str(p.get("id")) == ID_IN]
    else:
        cand = [p for p in posts if p.get("data") == oggi and p.get("pubblica_auto") is True
                and not p.get("solo_su_richiesta")]
    if not cand:
        stato["azioni"].append(f"nessun contenuto con pubblica_auto per {oggi}" if not ID_IN
                               else f"id {ID_IN} non trovato in posts.json")
        return 0

    if slot == "post":
        recenti = call("GET", f"{IG}/media", {"fields": "id,caption,permalink,timestamp", "limit": "15"}).get("data", [])
        for p in cand:
            if p.get("tipo") not in ("reel", "carosello"):
                continue
            pid = str(p["id"])
            if p.get("permalink") or pubblicati.get(pid, {}).get("permalink"):
                stato["azioni"].append(f"{pid}: gia' pubblicato, salto")
                continue
            gemello = next((m for m in recenti if norm(m.get("caption")) == norm(p["caption"])), None)
            if gemello:
                pubblicati.setdefault(pid, {}).update({"media_id": gemello["id"], "permalink": gemello.get("permalink"),
                                                       "pubblicato": gemello.get("timestamp"),
                                                       "nota": "trovato gia' online dall'anti-doppione"})
                stato["azioni"].append(f"{pid}: gia' online ({gemello.get('permalink')}), registrato senza ripubblicare")
                continue
            if DRY:
                quanti = len(p.get("slide", [])) if p["tipo"] == "carosello" else 1
                stato["azioni"].append(f"{pid}: PROVA, pubblicherei il {p['tipo']} ({quanti} file) con la didascalia dell'entry")
                continue
            try:
                mid, link, ts = pubblica_post(p)
                pubblicati.setdefault(pid, {}).update({"media_id": mid, "permalink": link, "pubblicato": ts,
                                                       "pubblicato_da": "GitHub Actions"})
                stato["azioni"].append(f"{pid}: pubblicato {link}")
            except ApiError as e:
                stato["errori"].append(f"{pid}: {e}")

    if slot == "storia":
        try:
            storie_oggi = [s for s in call("GET", f"{IG}/stories", {"fields": "id,timestamp"}).get("data", [])
                           if (s.get("timestamp") or "").startswith(oggi)]
        except ApiError as e:
            stato["errori"].append(f"lettura storie: {e}")
            storie_oggi = None
        for p in cand:
            pid = str(p["id"])
            uscito = (p.get("tipo") == "storia" or p.get("permalink")
                      or pubblicati.get(pid, {}).get("permalink"))
            for i, s in enumerate(p.get("storie", [])):
                if not s.get("file"):
                    continue
                gia = s.get("story_id") or pubblicati.get(pid, {}).get("storie", {}).get(str(i))
                if gia:
                    stato["azioni"].append(f"{pid}: storia {i} gia' pubblicata, salto")
                    continue
                if not uscito:
                    stato["azioni"].append(f"{pid}: il post non e' uscito, la storia {i} aspetta")
                    continue
                if storie_oggi is None:
                    stato["azioni"].append(f"{pid}: non riesco a leggere le storie di oggi, non ne aggiungo")
                    continue
                if len(storie_oggi) >= MAX_STORIE:
                    stato["azioni"].append(f"{pid}: oggi ci sono gia' {len(storie_oggi)} storie, non ne aggiungo")
                    continue
                if DRY:
                    stato["azioni"].append(f"{pid}: PROVA, pubblicherei la storia {s['file']}")
                    continue
                try:
                    sid = pubblica_storia(s["file"])
                    pubblicati.setdefault(pid, {}).setdefault("storie", {})[str(i)] = sid
                    stato["azioni"].append(f"{pid}: storia pubblicata ({sid})")
                    storie_oggi.append({"id": sid})
                except ApiError as e:
                    stato["errori"].append(f"{pid} storia {i}: {e}")

    if not DRY:
        scrivi("pubblicati.json", pubblicati)
    return 1 if stato["errori"] else 0


if __name__ == "__main__":
    try:
        codice = main()
    except Exception as e:  # nessun dettaglio che possa contenere intestazioni
        stato["errori"].append(f"errore imprevisto: {type(e).__name__}: {e}")
        codice = 1
    scrivi("stato_pubblicazione.json", stato)
    print(json.dumps(stato, ensure_ascii=False, indent=1))
    sys.exit(codice)
