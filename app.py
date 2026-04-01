import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
import time

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    max_http_buffer_size=10 * 1024 * 1024,
    ping_timeout=10,
    ping_interval=5
)

connected = False
last_signal_time = 0

TIMEOUT = 2


@socketio.on("status")
def status(data):
    global connected, last_signal_time

    if data == "connected":
        connected = True
        last_signal_time = time.time()

    socketio.emit("update", {"connected": connected})


@socketio.on("frames")
def receive_frames(data):
    socketio.emit("frames", data)


def check_loop():
    global connected, last_signal_time

    while True:
        if time.time() - last_signal_time > TIMEOUT:
            if connected:
                connected = False
                socketio.emit("update", {"connected": False})

        socketio.sleep(0.5)


socketio.start_background_task(check_loop)


@app.route("/")
def home():
    return "API OK"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
