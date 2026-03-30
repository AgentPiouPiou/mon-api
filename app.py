from flask import Flask
from flask_socketio import SocketIO
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

devices = {}
TIMEOUT = 3  # secondes sans ping = supprimé

def cleanup():
    while True:
        now = time.time()

        # supprimer appareils inactifs
        to_remove = [
            d for d, last in devices.items()
            if now - last > TIMEOUT
        ]

        for d in to_remove:
            del devices[d]

        # envoyer MAJ en live
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

    # MAJ instantanée
    socketio.emit("update", {"count": len(devices)})

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
