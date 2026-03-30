from flask import Flask
from flask_socketio import SocketIO
import time

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# état global
connected = False
last_signal_time = 0

TIMEOUT = 2  # secondes


@socketio.on("status")
def status(data):
    global connected, last_signal_time

    if data == "connected":
        connected = True
        last_signal_time = time.time()

    # envoyer au site directement
    socketio.emit("update", {"connected": connected})


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
