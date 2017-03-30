import os
from flask import Flask
from flask.ext.restful import Api
import logging

app = Flask(__name__)
app.config.from_object('config')

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run()

