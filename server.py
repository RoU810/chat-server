from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import time

app = Flask(__name__)
CORS(app)

def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, name TEXT, msg TEXT, timestamp REAL)")
    conn.commit()
    conn.close()

@app.route("/send", methods=["POST"])
def send():
    data = request.json
    name = data["name"]
    msg = data["msg"]
    timestamp = time.time()

    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("INSERT INTO messages (name, msg, timestamp) VALUES (?, ?, ?)", (name, msg, timestamp))
    conn.commit()
    conn.close()
    return jsonify({"status": "ok"})

@app.route("/messages", methods=["GET"])
def get_messages():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute("SELECT name, msg, timestamp FROM messages ORDER BY timestamp DESC LIMIT 20")
    messages = c.fetchall()
    conn.close()
    messages.reverse()
    return jsonify(messages)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
