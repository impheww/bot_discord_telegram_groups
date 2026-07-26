from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.get("/")
def home():
    return "Bot Online"

def run():
    print("Flask Starting...")
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        use_reloader=False
    )

def server_on():
    Thread(target=run, daemon=True).start()
