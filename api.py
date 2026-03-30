from flask import Flask, request, jsonify
import time

app = Flask(__name__)

SECRET = "MON_CODE_SECRET"

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
    return "ok"

# 🔻 Nombre de clients actifs
@app.route("/count")
def count_clients():
    now = time.time()

    actifs = [
        pc for pc, last_seen in clients.items()
        if now - last_seen < 10
    ]

    return jsonify({"count": len(actifs)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
