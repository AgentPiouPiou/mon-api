from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet"
)

# état global (1 = actif, 0 = aucun signal)
last_signal = 0


# réception du signal
@socketio.on("ping")
def ping():
    global last_signal
    last_signal = 1

    socketio.emit("status", {"connected": True})


def loop():
    global last_signal

    while True:
        # si aucun signal reçu récemment → offline
        if last_signal == 0:
            socketio.emit("status", {"connected": False})
        else:
            # reset pour attendre le prochain signal
            last_signal = 0

        socketio.sleep(0.3)  # 🔥 très rapide


socketio.start_background_task(loop)


@app.route("/")
def home():
    return "API OK"


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
