import os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from flask import Flask, render_template, jsonify, make_response

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ping")
def ping():
    return jsonify(status="OK")

def _paris_now():
    tz = ZoneInfo("Europe/Paris")
    now = datetime.now(tz)
    return {
        "iso": now.isoformat(timespec="seconds"),
        "unix": int(now.timestamp()),
        "tz": "Europe/Paris",
        "offset": now.strftime("%z"),     # ex: +0200
        "human": now.strftime("%A %d %B %Y • %H:%M:%S")
    }

@app.route("/api/heure")
def api_heure():
    data = _paris_now()
    data["source"] = "server/zoneinfo"
    resp = jsonify(data)
    resp.headers["Cache-Control"] = "no-store"
    return resp

@app.route("/heure")
def heure():
    data = _paris_now()
    html = f"""
    <html lang="fr"><meta charset="utf-8">
    <title>Heure de Paris</title>
    <body style="font-family:system-ui,Segoe UI,Roboto,Arial">
      <h1>Heure de Paris</h1>
      <p><b>{data['human']}</b></p>
      <p>ISO : <code>{data['iso']}</code> — UNIX : <code>{data['unix']}</code></p>
      <p>Fuseau : <code>{data['tz']}</code> (offset {data['offset']})</p>
    </body></html>
    """
    resp = make_response(html)
    resp.headers["Cache-Control"] = "no-store"
    return resp

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

