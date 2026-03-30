from flask import Flask
from flask_socketio import SocketIO
import time

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

devices = {}
TIMEOUT = 3  # si pas de signal → déconnecté


def is_connected():
    now = time.time()

    # nettoyage
    for device_id in list(devices.keys()):
        if now - devices[device_id] > TIMEOUT:
            del devices[device_id]

    return len(devices) > 0


def broadcast():
    socketio.emit("status", {"connected": is_connected()})


@socketio.on("heartbeat")
def heartbeat(data):
    device_id = data.get("device_id")

    if device_id:
        devices[device_id] = time.time()

    broadcast()


def loop():
    while True:
        broadcast()
        socketio.sleep(1)


socketio.start_background_task(loop)


@app.route("/")
def home():
    return "API OK"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
