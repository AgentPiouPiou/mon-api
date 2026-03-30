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
devices = {}

TIMEOUT = 3  # secondes sans signal = supprimé


# 🔁 nettoyage automatique
def cleanup():
    while True:
        now = time.time()

        before = len(devices)

        # suppression des appareils inactifs
        for device_id in list(devices.keys()):
            if now - devices[device_id] > TIMEOUT:
                del devices[device_id]

        after = len(devices)

        # envoie seulement si changement
        if after != before:
            socketio.emit("update", {"count": after})

        socketio.sleep(1)


socketio.start_background_task(cleanup)


@app.route("/")
def home():
    return "API OK"


# 📡 heartbeat reçu chaque seconde
@socketio.on("heartbeat")
def heartbeat(data):
    device_id = data.get("device_id")

    if device_id:
        devices[device_id] = time.time()

    # mise à jour immédiate
    socketio.emit("update", {"count": len(devices)})


# ▶️ lancement
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
