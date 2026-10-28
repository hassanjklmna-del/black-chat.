
import os
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "black-chat-key")
socketio = SocketIO(app, cors_allowed_origins="*")

ROOMS = {"عام", "تجارة", "تيمات"}

@app.get("/")
def home():
    return "BLACK CHAT server is running!"

@socketio.on("join")
def on_join(data):
    username = str(data.get("username", "مجهول"))[:30]
    room = str(data.get("room", "عام"))
    if room not in ROOMS:
        return
    join_room(room)
    emit("message", {
        "username": "النظام",
        "text": username + " دخل الشات",
        "room": room
    }, to=room)

@socketio.on("chat_message")
def on_message(data):
    username = str(data.get("username", "مجهول"))[:30]
    room = str(data.get("room", "عام"))
    message = str(data.get("message", ""))[:500].strip()

    if room not in ROOMS or not message:
        return

    emit("message", {
        "username": username,
        "text": message,
        "room": room
    }, to=room)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    socketio.run(app, host="0.0.0.0", port=port)
  
