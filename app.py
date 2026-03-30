from flask import Flask
from flask_socketio import SocketIO
import time
import uuid

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

devices = {}
TIMEOUT = 3  # secondes sans signal = supprimé

def cleanup():
    while True:
        now = time.time()

        to_remove = [
            d for d, last in devices.items()
            if now - last > TIMEOUT
        ]

        for d in to_remove:
            devices.pop(d, None)

        # broadcast du compteur
        socketio.emit("update", {"count": len(devices)})

        socketio.sleep(1)

socketio.start_background_task(cleanup)

@app.route("/")
def home():
    return "API OK"

@socketio.on("heartbeat")
def heartbeat(data):
    device_id = data.get("device_id")

    if device_id:
        devices[device_id] = time.time()

    # mise à jour immédiate
    socketio.emit("update", {"count": len(devices)})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
