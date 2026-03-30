from flask import Flask
from flask_socketio import SocketIO
import time

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# stockage des appareils
# {device_id: last_seen}
devices = {}

# ⚡ TTL ultra court
TTL = 2  # secondes


def get_active_devices():
    now = time.time()

    # supprimer immédiatement les appareils morts
    dead_devices = [
        device_id
        for device_id, last_seen in devices.items()
        if now - last_seen > TTL
    ]

    for device_id in dead_devices:
        del devices[device_id]

    return len(devices)


def send_update():
    count = get_active_devices()
    socketio.emit("update", {"count": count})


@socketio.on("heartbeat")
def handle_heartbeat(data):
    device_id = data.get("device_id")

    if not device_id:
        return

    # mise à jour du timestamp
    devices[device_id] = time.time()

    # 🔥 envoi instantané
    send_update()


# petit fallback (sécurité)
def background_check():
    while True:
        send_update()
        socketio.sleep(1)


socketio.start_background_task(background_check)


@app.route("/")
def index():
    return "API OK"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
