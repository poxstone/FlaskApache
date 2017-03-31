# -*- coding: utf-8 -*-

import logging
from flask import Flask
from helpers import DBConectionHelper
from tasks import udpadeNAT

app = Flask(__name__)

try:
    mysql = DBConectionHelper(app)
except Exception as e:
    logging.exception("errror on connect database")
    mysql = False
    raise e

app.config.from_object('config')


@app.route("/updateNAT/", methods=['GET'])
def update():
    if mysql:
        rv = mysql.getTableLdap()
        udpadeNAT(rv)
        return "OK"
    else:
        return "ERROR"


if __name__ == '__main__':
    app.run()

