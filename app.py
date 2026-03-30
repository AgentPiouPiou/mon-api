from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import time
import uuid
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

socketio = SocketIO(app, cors_allowed_origins="*")

devices = {}
TIMEOUT = 3

# Nettoyage automatique
def cleanup():
    while True:
        now = time.time()
        to_remove = []

        for device_id, last_ping in devices.items():
            if now - last_ping > TIMEOUT:
                to_remove.append(device_id)

        for d in to_remove:
            del devices[d]

        # broadcast mise à jour
        socketio.emit("update", {"count": len(devices)})

        socketio.sleep(1)

threading.Thread(target=cleanup, daemon=True).start()

@app.route("/")
def home():
    return "API WebSocket OK"

@socketio.on("connect")
def on_connect():
    print("Client connecté")

@socketio.on("register")
def register():
    device_id = str(uuid.uuid4())
    devices[device_id] = time.time()

    emit("registered", {"device_id": device_id})
    socketio.emit("update", {"count": len(devices)})

@socketio.on("heartbeat")
def heartbeat(data):
    device_id = data.get("device_id")

    if device_id in devices:
        devices[device_id] = time.time()

@socketio.on("disconnect")
def disconnect():
    print("Client déconnecté")

    # Option : supprimer les appareils morts via timeout
    socketio.emit("update", {"count": len(devices)})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
