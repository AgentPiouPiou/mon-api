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
    max_http_buffer_size=100 * 1024 * 1024,
    ping_timeout=10,
    ping_interval=5
)

connected = False
last_signal_time = 0
TIMEOUT = 2  # secondes


# ------------------ STATUS ------------------

@socketio.on("status")
def status(data):
    global connected, last_signal_time

    if data == "connected":
        connected = True
        last_signal_time = time.time()

    socketio.emit("update", {"connected": connected})


# ------------------ STREAM VIDEO ------------------

@socketio.on("frames")
def receive_frames(data):
    socketio.emit("frames", data)


# ------------------ MOUVEMENT SOURIS ------------------

@socketio.on("move_mouse")
def move_mouse(data):
    socketio.emit("move_mouse", data)


# ------------------ CHECK CONNECTION ------------------

def check_loop():
    global connected, last_signal_time

    while True:
        if connected and time.time() - last_signal_time > TIMEOUT:
            connected = False
            socketio.emit("update", {"connected": False})

        socketio.sleep(0.5)


socketio.start_background_task(check_loop)


# ------------------ ROUTE ------------------

@app.route("/")
def home():
    return "API OK"


# ------------------ RUN ------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
