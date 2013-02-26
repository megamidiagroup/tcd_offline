#!/usr/bin/python 
#-*- coding: utf8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.http import urlquote
from django.conf import settings
import urllib

import simplejson

from megavideo.common.channel import get_current_channel
from megavideo.video.models import *
from megavideo.api.video import video_search
from django.template.defaultfilters import slugify
import datetime
#from megavideo.record.aes_python import AESMessage


def _out_js(text):
    """
       Saída em js das informações
    """
    a = u''
    for i in text.splitlines():
        if len(i) > 0:
            a += u'document.write(%s);' % simplejson.dumps(i)
    return a


def index(request):
    """
        Função padrão para pesquisa e retorno de widget
    """
    p = {}

    #a = AESMessage(settings.VFLOW_REC['key'])
    
    category_id = request.REQUEST.get('category', 0)

    if category_id:
        p['cat_id'] = category_id

    p['url'] = request.REQUEST.get('url' , settings.MEGAVIDEO_CONF['base_url'])
    p['types'] = request.REQUEST.get('types' , 'Video:mp4|mpg|wmv|avi|mov|flv|f4v|3gp|3GP')
    p['videoBasename'] = 'tvt_' + str(slugify(datetime.datetime.now()))
    #p['token'] = a.encode(p['videoBasename'])
    p['upstreamUrl'] = settings.VFLOW_REC.get('rtmp_url', "rtmp://tvt.vflow.tv/vflowopen")

    values = ''
    for i in p.keys():
        values += "%s=%s&" % (i , p[i])

    p['values'] = values

    render = request.REQUEST.get('render', 'js')

    player = request.REQUEST.get('player', 'upload_widget.swf')

    #configuração
    p['width'] = request.REQUEST.get('width'     , '215')
    p['height'] = request.REQUEST.get('height'    , '275')

    p['player'] = request.REQUEST.get('player'    , settings.MEGAVIDEO_CONF['base_url'] + 'static/portal/swf/' + player)

    text = render_to_string('api/record.html', p, context_instance = RequestContext(request))


    if render == 'html':
        return HttpResponse(text)

    text = _out_js(text)

    return HttpResponse(text)


def test(request):
    return render_to_response('api/testjs.html', {'script' : '/api/record.js', 'values': request.META['QUERY_STRING'] })
