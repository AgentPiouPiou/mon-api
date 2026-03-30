from flask import Flask, request, jsonify
import time

app = Flask(__name__)

SECRET = "MON_CODE_SECRET"

# Stockage des clients connectés
clients = {}

@app.route("/")
def home():
    return "API OK"

# 🔻 CLIENT → API (heartbeat)
@app.route("/ping")
def ping():
    key = request.args.get("key")
    pc_id = request.args.get("id")

    if key != SECRET:
        return "refuse"

    clients[pc_id] = time.time()
    return "ok"

# 🔻 VOIR LES CLIENTS CONNECTÉS
@app.route("/clients")
def get_clients():
    now = time.time()

    # On garde seulement ceux actifs < 10 sec
    actifs = {
        pc: round(now - last_seen, 1)
        for pc, last_seen in clients.items()
        if now - last_seen < 10
    }

    return jsonify(actifs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
