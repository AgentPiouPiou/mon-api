from flask import Flask
from flask_socketio import SocketIO
import time
import uuid
import threading

app = Flask(__name__)

# IMPORTANT : eventlet
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

devices = {}
TIMEOUT = 3

# Nettoyage automatique
def cleanup():
    while True:
        now = time.time()
        to_remove = []

        for device_id, last_ping in list(devices.items()):
            if now - last_ping > TIMEOUT:
                to_remove.append(device_id)

        for d in to_remove:
            devices.pop(d, None)

        socketio.emit("update", {"count": len(devices)})
        socketio.sleep(1)

threading.Thread(target=cleanup, daemon=True).start()

@app.route("/")
def home():
    return "API OK"

@socketio.on("connect")
def connect():
    print("Client connecté")

@socketio.on("register")
def register():
    device_id = str(uuid.uuid4())
    devices[device_id] = time.time()

    socketio.emit("update", {"count": len(devices)})
    return {"device_id": device_id}

@socketio.on("heartbeat")
def heartbeat(data):
    device_id = data.get("device_id")
    if device_id in devices:
        devices[device_id] = time.time()

@socketio.on("disconnect")
def disconnect():
    socketio.emit("update", {"count": len(devices)})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
