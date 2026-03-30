from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)

# 🔥 Autorise ton site à accéder à l'API
CORS(app)

SECRET = "MON_CODE_SECRET"

# Stockage des clients
clients = {}

@app.route("/")
def home():
    return "API OK"

# 🔻 Ping client
@app.route("/ping")
def ping():
    key = request.args.get("key")
    pc_id = request.args.get("id")

    if key != SECRET:
        return "refuse"

    clients[pc_id] = time.time()
    print("PING :", pc_id)

    return "ok"

# 🔻 Nombre de clients actifs
@app.route("/count")
def count_clients():
    now = time.time()

    actifs = [
        pc for pc, last_seen in clients.items()
        if now - last_seen < 10
    ]

    print("ACTIFS :", actifs)

    return jsonify({"count": len(actifs)})
