import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_socketio import SocketIO
import time
import pyautogui

app = Flask(__name__)

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    max_http_buffer_size=20 * 1024 * 1024,
    ping_timeout=10,
    ping_interval=5
)

connected = False
last_signal_time = 0
TIMEOUT = 2
frames_data = {}

# ---------------- STATUS ----------------
@socketio.on("status")
def status(data):
    global connected, last_signal_time
    if data == "connected":
        connected = True
        last_signal_time = time.time()
    socketio.emit("update", {"connected": connected})

# ---------------- FRAMES ----------------
@socketio.on("frames")
def receive_frames(data):
    global frames_data
    frames_data = data
    socketio.emit("frames", data)

# ---------------- MOUSE ----------------
@socketio.on("mouse_move")
def mouse_move(data):
    try:
        dx = data.get("dx", 0)
        dy = data.get("dy", 0)
        x, y = pyautogui.position()
        pyautogui.moveTo(x + dx, y + dy, duration=0)
    except Exception as e:
        print("Erreur mouse_move:", e)

# ---------------- CHECK ----------------
def check_loop():
    global connected, last_signal_time
    while True:
        if connected and (time.time() - last_signal_time > TIMEOUT):
            connected = False
            socketio.emit("update", {"connected": False})
        socketio.sleep(0.5)

socketio.start_background_task(check_loop)

@app.route("/")
def home():
    return "API OK"

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
