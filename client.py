import tkinter as tk
from tkinter import simpledialog
import requests
import threading
import time

SERVER_URL = "https://rchat-nca4.onrender.com"

# === メインクラス ===
class ChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Pythonチャット")

        # ユーザー名をGUIで取得
        self.username = simpledialog.askstring("ユーザー名", "あなたの名前を入力してください", parent=root)
        if not self.username:
            self.root.destroy()
            return

        # チャット表示エリア
        self.chatbox = tk.Listbox(root, width=50, height=20)
        self.chatbox.pack(padx=10, pady=10)

        # 入力エリア
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(side=tk.LEFT, padx=10, pady=5)
        self.entry.bind("<Return>", lambda event: self.send_message())

        # 送信ボタン
        self.send_btn = tk.Button(root, text="送信", command=self.send_message)
        self.send_btn.pack(side=tk.LEFT, padx=5)

        # メッセージ取得のループ開始
        self.running = True
        threading.Thread(target=self.receive_messages, daemon=True).start()

    def send_message(self):
        msg = self.entry.get()
        if msg:
            data = {"name": self.username, "msg": msg}
            try:
                requests.post(f"{SERVER_URL}/send", json=data)
                self.entry.delete(0, tk.END)
            except:
                self.chatbox.insert(tk.END, "⚠️ メッセージ送信に失敗しました")

    def receive_messages(self):
        while self.running:
            try:
                res = requests.get(f"{SERVER_URL}/messages")
                if res.status_code == 200:
                    messages = res.json()
                    self.chatbox.delete(0, tk.END)
                    for name, msg, ts in messages:
                        self.chatbox.insert(tk.END, f"{name}：{msg}")
            except:
                pass
            time.sleep(2)

    def close(self):
        self.running = False
        self.root.destroy()


# === 実行部分 ===
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatClient(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
