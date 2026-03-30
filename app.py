from flask import Flask, jsonify, request
from flask_cors import CORS
import time
import uuid

app = Flask(__name__)
CORS(app)

# Stockage des appareils : {id: last_ping}
devices = {}

TIMEOUT = 10  # secondes avant suppression

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})

@app.route("/register", methods=["POST"])
def register():
    device_id = str(uuid.uuid4())
    devices[device_id] = time.time()
    return jsonify({"device_id": device_id})

@app.route("/heartbeat", methods=["POST"])
def heartbeat():
    data = request.json
    device_id = data.get("device_id")

    if device_id in devices:
        devices[device_id] = time.time()

    return jsonify({"status": "ok"})

@app.route("/status", methods=["GET"])
def status():
    now = time.time()

    # Supprimer les appareils morts
    to_delete = []
    for device_id, last_ping in devices.items():
        if now - last_ping > TIMEOUT:
            to_delete.append(device_id)

    for d in to_delete:
        del devices[d]

    return jsonify({
        "count": len(devices),
        "devices": list(devices.keys())
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
