#!/usr/bin/env python

import sys
import os.path
from django.conf import settings
import time, hashlib

def get_trancode_url(t):
    path = os.path.join(t.video.dir, 'transcoded_' + t.name)
    return settings.STORAGE_URL + 'videos/' + path


def get_video_url(v):
    path = os.path.join('/', v.dir, v.name)
    return gen_sec_link(path)


def get_thumb_url(t):
    path = os.path.join(t.video.dir, 'thumb_' + t.name)
    return settings.STORAGE_URL + 'videos/' + path


def gen_sec_link(rel_path, iphone = False):
    conf = settings.MEGAVIDEO_CONF
    uri_prefix = '/mediacontent/videos/'
    if 'sec_link' in conf and conf['sec_link'] == False:
        if iphone:
            return settings.MEDIA_URL_IPHONE + 'videos/' + rel_path
        else:
            return settings.MEDIA_URL + 'videos/' + rel_path
    else:
        secret = 'vflowSuperSikret'
        hextime = "%08x" % time.time()
        token = hashlib.md5(secret + rel_path + hextime).hexdigest()
    return '%s%s/%s%s' % (uri_prefix, token, hextime, rel_path)


def get_thumb_path(t):
    base = settings.VFLOW['video_storage']
    path = os.path.join(base, t.video.dir, 'thumb_' + t.name)
    return path
