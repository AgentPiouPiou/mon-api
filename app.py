from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Stockage simple en mémoire (⚠️ reset si redémarrage)
user_count = 0

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"})

@app.route("/connect", methods=["POST"])
def connect():
    global user_count
    user_count += 1
    return jsonify({"message": "connected", "users": user_count})

@app.route("/disconnect", methods=["POST"])
def disconnect():
    global user_count
    user_count = max(0, user_count - 1)
    return jsonify({"message": "disconnected", "users": user_count})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "users": user_count
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
