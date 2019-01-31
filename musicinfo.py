# -*- coding: utf-8 -*-
import eyed3
import os
import dbconnect
import sys
reload(sys)
sys.setdefaultencoding('utf8')

print os.getcwd()
host = "http://39.108.230.41"
def sync_music_in_db():
    musicDir = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), "static/mp3/")   #音乐文件路劲
    for songName in os.listdir(musicDir):
        musicPath = os.path.join(musicDir, songName)
        audiofile = eyed3.load(musicPath)
        seconds = int(audiofile.info.time_secs)  #时长
        size = audiofile.info.size_bytes
        songName = audiofile.tag.title   #歌名
        singerName = audiofile.tag.artist  #歌手
        album = audiofile.tag.album   #专辑
        url = audiofile.__dict__["_path"]
        downloadUrl= "http://{0}/download/{1}".format(host,songName)   #下载地址
        musicinfo= {
            "singerId": 0,
            "seconds": seconds,
            "songName": songName,
            "singerName":singerName,
            "album": album,
            "downloadUrl": downloadUrl,
            "url": url
        }

def insert_info_into_db():
    operation = " insert into test(name,age) values('gergelin',9) "
    dbconnect.insert_execute(operation)

if __name__ == "__main__":
    insert_info_into_db()