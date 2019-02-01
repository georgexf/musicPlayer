#coding=utf-8
import logging
import os
import datetime
from mysql.connector import (connection)
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

socket = "/tmp/mysql.sock"
host = "127.0.0.1"
port = 3306
db = "music_db"
user = "root"
password = "george@123"

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
filename = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'log/mysql-{0}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d")))
logging.basicConfig(filename=filename, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
logger = logging.getLogger()


def get_connection():
    global host
    global user
    global password
    global db
    cnx = connection.MySQLConnection(user=user, password=password, host=host, database=db, charset='utf8')
    return cnx


def query_execute(operation):
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute(operation)
        d = cursor.fetchall()
        cnx.commit()
        cursor.close()
        cnx.close()
        return d
    except Exception as e:
        logger.error(e)


def insert_execute(operation):
    try:
        cnx = get_connection()
        cursor = cnx.cursor()
        cursor.execute(operation)
        cnx.commit()
        cursor.close()
        cnx.close()
    except Exception as e:
        print e
        logger.error(e)


def get_all_musicinfo():
    opetation = "select * from test"
    res = query_execute(operation=opetation)
    return res


def close_cur_cnx(cursor, cnx):
    cursor.close()
    cnx.close()


if __name__ == "__main__":
    get_all_musicinfo()


