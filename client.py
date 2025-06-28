import tkinter as tk
import requests
import threading
import time

# === サーバーURL（あなたのRender URL） ===
SERVER_URL = "https://rchat-nca4.onrender.com"

# === ユーザー名入力 ===
username = input("あなたの名前を入力してください: ")

# === メッセージ送信処理 ===
def send_message():
    msg = entry.get()
    if msg:
        data = {"name": username, "msg": msg}
        try:
            requests.post(f"{SERVER_URL}/send", json=data)
            entry.delete(0, tk.END)
        except:
            chatbox.insert(tk.END, "⚠️ サーバーに接続できませんでした。\n")

# === メッセージ受信処理 ===
def receive_messages():
    while True:
        try:
            res = requests.get(f"{SERVER_URL}/messages")
            if res.status_code == 200:
                messages = res.json()
                chatbox.delete(0, tk.END)
                for name, msg, ts in messages:
                    chatbox.insert(tk.END, f"{name}：{msg}")
        except:
            pass
        time.sleep(2)

# === GUI作成 ===
root = tk.Tk()
root.title("Pythonチャット - LINE風")

chatbox = tk.Listbox(root, width=50, height=20)
chatbox.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40)
entry.pack(side=tk.LEFT, padx=10, pady=5)

send_btn = tk.Button(root, text="送信", command=send_message)
send_btn.pack(side=tk.LEFT, padx=5)

# === 別スレッドでメッセージ取得 ===
threading.Thread(target=receive_messages, daemon=True).start()

root.mainloop()
