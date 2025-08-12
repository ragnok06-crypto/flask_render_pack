from flask import Flask, jsonify, make_response
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

app = Flask(__name__)
PARIS = ZoneInfo("Europe/Paris")

def no_cache(resp):
    """Désactive le cache côté client/CDN."""
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

@app.get("/health")
def health():
    """Vérifie que le service répond (texte brut)."""
    r = make_response("OK")
    r.mimetype = "text/plain"
    return no_cache(r)

@app.get("/heure")
def heure_txt():
    """Retourne l'heure actuelle de Paris en texte brut."""
    now = datetime.now(PARIS).isoformat(timespec="seconds")
    r = make_response(f"Heure Paris: {now}")
    r.mimetype = "text/plain"
    return no_cache(r)

@app.get("/api/heure")
def heure_json():
    """Retourne l'heure actuelle en JSON + comparaison avec une source externe."""
    local_now = datetime.now(PARIS)

    # Double vérification via worldtimeapi.org
    ext_iso = None
    delta_sec = None
    source = "worldtimeapi"
    status = "external_unavailable"

    try:
        r = requests.get("https://worldtimeapi.org/api/timezone/Europe/Paris", timeout=4)
        if r.ok:
            data = r.json()
            ext_iso = data.get("datetime")
            ext_dt = datetime.fromisoformat(ext_iso.replace("Z", "+00:00"))
            ext_dt_paris = ext_dt.astimezone(PARIS)
            delta_sec = abs(int((local_now - ext_dt_paris).total_seconds()))
            status = "ok" if delta_sec <= 120 else "drift>120s"
    except Exception:
        status = "external_error"

    r = jsonify({
        "tz": "Europe/Paris",
        "local_iso": local_now.isoformat(timespec="seconds"),
        "local_unix": int(local_now.timestamp()),
        "external_iso": ext_iso,
        "delta_seconds": delta_sec,
        "external_source": source,
        "status": status
    })
    return no_cache(r)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
