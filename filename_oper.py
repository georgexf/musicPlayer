# -*-coding:utf-8 -*-
#替换掉文件名的空格
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

musicdir = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'static/mp3/')
for songname in os.listdir(musicdir):
    print songname
    os.rename(os.path.join(musicdir, songname),os.path.join(musicdir, songname.replace(' ', '')))