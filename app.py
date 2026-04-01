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
    max_http_buffer_size=20 * 1024 * 1024,  # buffer plus grand pour les images
    ping_timeout=10,
    ping_interval=5
)

# État global du client
connected = False
last_signal_time = 0
TIMEOUT = 2  # secondes

# ------------------ événements ------------------

@socketio.on("status")
def handle_status(data):
    global connected, last_signal_time
    if data == "connected":
        connected = True
        last_signal_time = time.time()
    socketio.emit("update", {"connected": connected})

@socketio.on("frames")
def handle_frames(data):
    # data : { "0": base64, "1": base64, ... }
    socketio.emit("frames", data)

# ------------------ boucle de vérification ------------------

def check_loop():
    global connected, last_signal_time
    while True:
        if connected and (time.time() - last_signal_time > TIMEOUT):
            connected = False
            socketio.emit("update", {"connected": False})
        socketio.sleep(0.5)

socketio.start_background_task(check_loop)

# ------------------ route simple ------------------

@app.route("/")
def home():
    return "API OK"

# ------------------ lancement ------------------

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
