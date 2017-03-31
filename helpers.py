# -*- coding: utf-8 -*-
import logging
import constants
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor

class DBConectionHelper():
    def __init__(self, app):
        app.config['MYSQL_USER'] = constants.DB_USER
        app.config['MYSQL_PASSWORD'] = constants.DB_PASS
        app.config['MYSQL_DB'] = constants.DB_NAME
        app.config['MYSQL_HOST'] = constants.BD_HOST
        self.mysql = MySQL(app)

    def getTableLdap(self):
        try:
            cursor = self.mysql.connect.cursor(cursorclass=DictCursor)
            cursor.execute('''SELECT * FROM ldapRouting''')
            rv = cursor.fetchall()
            return rv

        except Exception as e:
            logging.exception(e)
            raise e

