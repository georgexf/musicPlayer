import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

musicdir = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'static/mp3/')
print musicdir
for songname in os.listdir(musicdir):
    print songname
    os.rename(os.path.join(musicdir, songname),os.path.join(musicdir, songname.replace(' ', '')))