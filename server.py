from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)      # ← これが必要！！
CORS(app)

# Web画面の表示
@app.route("/")
def home():
    return render_template("index.html")

# メッセージ送信（POST）
@app.route("/send", methods=["POST"])
def send():
    data = request.get_json()
    name = data.get("name")
    msg = data.get("msg")
    with open("chat.txt", "a", encoding="utf-8") as f:
        f.write(f"{name}::{msg}\n")
    return jsonify({"status": "ok"})

# メッセージ取得（GET）
@app.route("/messages", methods=["GET"])
def messages():
    output = []
    try:
        with open("chat.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split("::")
                if len(parts) == 2:
                    output.append((parts[0], parts[1], ""))
    except:
        pass
    return jsonify(output)

# アプリを実行
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
