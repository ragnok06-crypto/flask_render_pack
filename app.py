import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    # Remplace le contenu du template templates/index.html selon ton besoin
    return render_template("index.html")

@app.route("/ping")
def ping():
    return jsonify(status="OK")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
