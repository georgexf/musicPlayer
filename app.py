# -*-coding:utf-8 -*-
from flask import Flask, jsonify, request
from flask import send_file, send_from_directory
from werkzeug.utils import secure_filename
import os
import re
from flask import make_response
import musicinfo
import logging
import datetime
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
logfile = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), '/log/flask-{0}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d")))
logging.basicConfig(filename=logfile, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)
logger = logging.getLogger()

UPLOAD_PATH = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'static/mp3/')
VERSION_PATH = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'static/apk/')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
app.config['ALLOWED_EXTENSIONS'] = set(['mp3'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/')
def hello_world():
    return 'Hello Music!'


@app.route('/api/music/info/', methods=['GET'])
def get_music_list():
    return jsonify(musicinfo.get_music_list())


@app.route('/api/music/info/<int:pageid>/', methods=['GET'])
def get_music_info(pageid):
    return jsonify(musicinfo.get_music_info_by_pageid(pagesize=20, pageid=pageid))


@app.route('/api/music/info/singer/<singer>/', methods=['GET'])
def get_music_info_by_singer(singer):
    logger.info("get singer {0} music".format(singer))
    return jsonify(musicinfo.get_music_info_by_singer(singer=singer))


@app.route('/api/music/info/songname/<songname>/', methods=['GET'])
def get_music_info_by_songname(songname):
    logger.info("get sing {0} music".format(songname))
    return jsonify(musicinfo.get_music_info_by_songName(songname=songname))


@app.route('/api/music/info/version/', methods=['GET'])
def get_version():
    logger.info("get version")
    apk_list = os.listdir(VERSION_PATH)
    if len(apk_list) != 1:
        return jsonify({
            "msgStr": "get version error",
            "msgCode": 500
        })
    else:
        mat = re.search(r'[0-9]+.[0-9]+.[0-9]+',str(apk_list[0]))
        if mat:
            return jsonify({
                "msgStr": mat.group(),
                "msgCode": 200
            })
        else:
            return jsonify({
                "msgStr": "get version error",
                "msgCode": 500
            })


@app.route("/api/music/download/<filename>", methods=['GET'])
def download_music(filename):
    directory = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'static/mp3/')
    if os.path.exists(os.path.join(directory,filename)):
        logger.info("download {0} from {1}".format(filename, directory))
        response = make_response(send_from_directory(directory, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('utf-8'))
        return response
    else:
        return jsonify({
            "msgStr": "Can not find mp3 file {0}".format(filename),
            "msgCode": 200
        })


@app.route('/api/music/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        upload_file = request.files['music']
        if upload_file and allowed_file(upload_file.filename):
            filename = secure_filename(upload_file.filename)
            if filename in os.listdir(UPLOAD_PATH):
                return jsonify({
                    "msgStr": "file already existed",
                    "msgCode": 200
                })
            else:
                upload_file.save(os.path.join(UPLOAD_PATH, filename))
                return jsonify({
                    "msgStr": "upload success",
                    "msgCode": 200
                })

        else:
            return jsonify({
                "msgStr": "not a mp3 file",
                "msgCode": 500
            })


@app.route("/package/download/<filename>", methods=['GET'])
def download_package(filename):
    directory = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'static/package/')
    if os.path.exists(os.path.join(directory,filename)):
        logger.info("download {0} from {1}".format(filename, directory))
        response = make_response(send_from_directory(directory, filename, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('utf-8'))
        return response
    else:
        return jsonify({
            "msgStr": "Can not find mp3 file {0}".format(filename),
            "msgCode": 404
        })



if __name__ == '__main__':
    logger.info("flask app start")
    app.run(host='0.0.0.0')