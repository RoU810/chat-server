from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    # /loginアクセスはトップページ（ログイン兼チャット画面）にリダイレクト
    return redirect("/")

@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    name = data.get("name")
    msg = data.get("msg")
    room = request.args.get("room", "global")
    filename = f"chat_{room}.txt"

    time_str = datetime.now().strftime("%H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"{name}::{msg}::{time_str}\n")

    return jsonify({"status": "ok"})

@app.route("/messages", methods=["GET"])
def messages():
    room = request.args.get("room", "global")
    filename = f"chat_{room}.txt"

    output = []
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("::")
                if len(parts) == 3:
                    output.append((parts[0], parts[1], parts[2]))
    return jsonify(output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
