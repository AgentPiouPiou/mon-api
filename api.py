from flask import Flask, request, jsonify

app = Flask(__name__)

command = {}

@app.route("/")
def home():
    return "API OK"

@app.route("/set-command", methods=["POST"])
def set_command():
    global command
    data = request.json

    command = {
        "action": data.get("action"),
        "value": data.get("value")
    }

    return jsonify({"status": "ok"})


@app.route("/command")
def get_command():
    global command

    current = command.copy()
    command = {}  # reset après lecture

    return jsonify(current)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
