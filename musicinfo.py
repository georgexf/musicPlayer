#coding=utf-8
import eyed3
import os
import dbconnect
import logging
import datetime
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


host = "39.108.230.41"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
filename = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'log/mysql-{0}.log'.format(datetime.datetime.now().strftime("%Y-%m-%d")))
logging.basicConfig(filename=filename, level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def sync_music_in_db():
    musicDir = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "static/mp3/")   #音乐文件路径
    musicinfo_list = []
    for song in os.listdir(musicDir):
        musicPath = os.path.join(musicDir, song)
        audiofile = eyed3.load(musicPath)
        seconds = int(audiofile.info.time_secs)  # 时长
        #size = audiofile.info.size_bytes
        songName = audiofile.tag.title   # 歌名
        singerName = audiofile.tag.artist  # 歌手
        album = audiofile.tag.album   # 专辑
        downloadUrl = "http://{0}/download/{1}".format(host, song)   # 下载地址
        musicinfo = {
            "singerId": 0,
            "seconds": seconds,
            "songName": songName,
            "singerName": singerName,
            "album": album,
            "downUrl": downloadUrl
        }
        musicinfo_list.append(musicinfo)
    insert_info_into_db("musicinfo", musicinfo_list)


def insert_info_into_db(tableName, musicinfo_list):
    values_list = []
    for musicinfo in musicinfo_list:
        keys = ",".join(musicinfo.keys())
        values = ""
        for key in musicinfo.keys():
            if isinstance(musicinfo[key], int):
                values = '{0}{1},'.format(values, musicinfo[key])
            else:
                values = '{0}\"{1}\",'.format(values, str(musicinfo[key]).encode("unicode_escape"))

        values = '({0})'.format(values.strip(','))
        values_list.append(values)
    operation = "replace into {0}({1}) values{2}".format(tableName, keys, ",".join(values_list)).decode("unicode_escape")
    print operation
    dbconnect.insert_execute(operation)


def get_music_info_by_pageid(pagesize, pageid):
    start_position = int(pagesize) * (int(pageid) - 1)
    end_position = int(pagesize) * int(pageid)
    operation = 'select * from musicinfo limit {0},{1}'.format(start_position, end_position)
    res = dbconnect.query_execute(operation)
    music_info_list = parse_res(res)
    print music_info_list
    return {"musicInfoList": music_info_list}


def get_music_info_by_singer(singer):
    operation = 'select * from musicinfo where singerName= \"{0}\"'.format(singer)
    logging.info(operation)
    res = dbconnect.query_execute(operation)
    music_info_list = parse_res(res)
    print music_info_list
    return {"musicInfoList": music_info_list}


def get_music_info_by_songName(songname):
    operation = 'select * from musicinfo where songName like \"%{0}%\"'.format(songname)
    logging.info(operation)
    res = dbconnect.query_execute(operation)
    music_info_list = parse_res(res)
    print music_info_list
    return {"musicInfoList": music_info_list}


def parse_res(res):
    music_info_list = []
    if len(res) > 0:
        for info in res:
            musicinfo = {
                "songId": info[0],
                "seconds": info[2],
                "songName": info[3].decode("unicode_escape").encode("utf-8"),
                "singerName": info[4].decode("unicode_escape").encode("utf-8"),
                "album": info[5].decode("unicode_escape").encode("utf-8"),
                "downUrl": info[9].decode("unicode_escape").encode("utf-8")
            }
            music_info_list.append(musicinfo)
    return music_info_list


if __name__ == "__main__":
    sync_music_in_db()