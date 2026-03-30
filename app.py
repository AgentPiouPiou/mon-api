from flask import Flask
from flask_socketio import SocketIO
import time

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# {device_id: timestamp}
devices = {}

TIMEOUT = 2  # suppression rapide


def get_active_devices():
    now = time.time()

    # suppression directe
    to_delete = [
        device_id for device_id, last_seen in devices.items()
        if now - last_seen > TIMEOUT
    ]

    for device_id in to_delete:
        del devices[device_id]

    return len(devices)


def broadcast():
    socketio.emit("update", {"count": get_active_devices()})


@socketio.on("heartbeat")
def heartbeat(data):
    device_id = data.get("device_id")

    if not device_id:
        return

    # mise à jour du device
    devices[device_id] = time.time()

    # envoi immédiat
    broadcast()


# backup nettoyage
def cleanup_loop():
    while True:
        broadcast()
        socketio.sleep(1)


socketio.start_background_task(cleanup_loop)


@app.route("/")
def home():
    return "API OK"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
