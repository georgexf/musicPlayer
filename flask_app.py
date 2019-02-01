# -*-coding:utf-8 -*-
from flask import Flask, jsonify,abort
from flask import send_file, send_from_directory
import os
from flask import make_response
import musicinfo
import logging
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)


LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logfile = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), '/log/flask-{0}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d")))
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


@app.route('/')
def hello_world():
    return 'Hello Music!'


@app.route('/api/music/info/<pageid>')
def get_music_info(pageid):
    return jsonify(musicinfo.get_music_info_by_pageid(pagesize=20, pageid=pageid))


@app.route('/api/music/info/singer/<singer>')
def get_music_info_by_singer(singer):
    logging.info("get singer {0} music".format(singer))
    if len(musicinfo.get_music_info_by_singer(singer=singer)) == 0:
        abort(404)
    return jsonify(musicinfo.get_music_info_by_singer(singer=singer))


@app.route('/api/music/info/songname/<songname>')
def get_music_info_by_songname(songname):
    logging.info("get sing {0} music".format(songname))
    if len(musicinfo.get_music_info_by_songName(songname=songname)) == 0:
        abort(404)
    return jsonify(musicinfo.get_music_info_by_songName(songname=songname))


@app.route("/api/music/download/<filename>", methods=['GET'])
def download_music(filename):
    directory = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'static/mp3/')
    logging.info("download {0} from {1}".format(filename, directory))
    response = make_response(send_from_directory(directory, filename, as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('utf-8'))
    return response


#@app.route("/download/<filepath>", methods=['GET'])
#def download_file(filepath):
#return app.send_static_file(filepath)


if __name__ == '__main__':
    app.run(host='0.0.0.0')