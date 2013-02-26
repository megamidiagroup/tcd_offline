# -*- coding: utf-8 -*-
from megavideo.video.models import *
from django.template.loader import render_to_string
import os.path

path = getatt('FTP_PATH', 'settings', settings.BASEDIR)


class CounterFile():
    def __init__(self, file, maxsize):
        self.file = file
        self.count = 0
        self.maxsize = maxsize

    def write(self, bytes):
        self.count += len(bytes)
        print "total %d bytes / %d" % (self.count, self.maxsize)
        if self.count == self.maxsize:
            print "   Should be complete"
        self.file.write(bytes)


irList = os.listdir(path)
for fname in dirList:
    print fname
