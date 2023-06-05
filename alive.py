from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
  return "Deployed"


def run():
  app.run(host='0.0.0.0', port=9090)


def alive():
  t = Thread(target=run)
  t.start()
