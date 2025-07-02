from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

USER_FILE = "users.json"

# ユーザー登録
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "ユーザ名とパスワードは必須です。"}), 400

    # ファイルがなければ空のdict
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r", encoding="utf-8") as f:
            users = json.load(f)

    if username in users:
        return jsonify({"error": "このユーザ名は既に使われています。"}), 400

    users[username] = password  # パスワードそのまま保存（暗号化は後でも追加可）

    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

    return jsonify({"status": "registered"})


# ログイン処理
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not os.path.exists(USER_FILE):
        return jsonify({"error": "アカウントが登録されていません。"}), 400

    with open(USER_FILE, "r", encoding="utf-8") as f:
        users = json.load(f)

    if users.get(username) == password:
        return jsonify({"status": True, "username": username})
    else:
        return jsonify({"status": False, "error": "ユーザ名またはパスワードが間違っています。"})


# ログアウト（今回は使わないが一応）
@app.route("/logout", methods=["POST"])
def logout():
    return jsonify({"status": "ok"})


# トップページ
@app.route("/")
def home():
    return render_template("index.html")


# メッセージ送信
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


# メッセージ取得
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
