from flask import Flask, request, jsonify

app = Flask(__name__)

command = {"action": ""}

SECRET = "MON_CODE_SECRET"

@app.route("/")
def home():
    return "API OK"

@app.route("/lancer")
def lancer():
    key = request.args.get("key")
    logiciel = request.args.get("logiciel")

    if key == SECRET:
        command["action"] = logiciel
        return "ok"
    return "refuse"

@app.route("/command")
def get_command():
    global command

    current = command.copy()
    command["action"] = ""  # reset après lecture

    return jsonify(current)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
