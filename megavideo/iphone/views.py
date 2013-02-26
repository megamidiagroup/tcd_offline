#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render_to_response
from megavideo.common.create_url import get_thumb_url
from megavideo.video.models import *
from django.conf import settings
from megavideo.common.channel import *
    
def index(request):
    p = {'vlist': []}
    chan = get_current_channel(request)
    v = Video.objects.using('megavideo').filter(published = True, channel = chan).order_by('-id')[0:9]
    p['vlist'] = v
    return render_to_response('iphone/base.html', p)

def index_app(request):
    p = {'vlist': []}
    chan = get_current_channel(request)
    v = Video.objects.using('megavideo').filter(published = True, channel = chan).order_by('-id')[0:9]
    p['vlist'] = v
    p['app'] = True
    return render_to_response('iphone/app.html', p)


if __name__ == '__main__':
    test()
