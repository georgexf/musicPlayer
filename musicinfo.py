# -*- coding: utf-8 -*-
import eyed3
import os
import dbconnect
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf8')


host = "39.108.230.41"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"
filename = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())) , 'log/mysql.log')
logging.basicConfig(filename='mysql.log', level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT)


def sync_music_in_db():
    musicDir = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "static/mp3/")   #音乐文件路径
    musicinfo_list = []
    for song in os.listdir(musicDir):
        musicPath = os.path.join(musicDir, song)
        audiofile = eyed3.load(musicPath)
        seconds = int(audiofile.info.time_secs)  #时长
        #size = audiofile.info.size_bytes
        songName = audiofile.tag.title   #歌名
        singerName = audiofile.tag.artist  #歌手
        album = audiofile.tag.album   #专辑
        downloadUrl = "http://{0}/download/{1}".format(host, song)   #下载地址
        musicinfo = {
            "singerId": 0,
            "seconds": seconds,
            "songName": songName,
            "singerName":singerName,
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
            elif isinstance(musicinfo[key], str):
                values = '{0}\"{1}\",'.format(values, str(musicinfo[key]).encode("unicode_escape"))
        values = '({0})'.format(values.strip(','))
        #print values.decode("unicode_escape")
        values_list.append(values)
    operation = "insert into {0}({1}) values{2}".format(tableName, keys, ",".join(values_list))
    print operation.decode("unicode_escape")
    dbconnect.insert_execute(operation)


if __name__ == "__main__":
    #operation = " insert into test(name,age) values('gergelin',9) "
    #insert_info_into_db(operation)
    sync_music_in_db()