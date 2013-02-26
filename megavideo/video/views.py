# -*- coding: utf-8 -*-
# Create your views here.
# 
from megavideo.common.create_url import get_trancode_url
from megavideo.common.channel import get_video_url
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from models import *
from django.http import HttpResponseRedirect
import datetime
import os.path
from django.conf import settings

from megavideo.async.call import AsyncCall
from megavideo.statistics.models import VisitorDownload
from megavideo.common.create_url import get_thumb_url

def player(request, key=''):
    video_id = Video().deserialize( key )
    return HttpResponseRedirect('/megavideo/static/portal/swf/megaplayer.swf?idContent=' + str(video_id))

def index(request):

       p = {}

       p = {'logger':'false',
            'tagger':'false',
            'idCategory':'false',
            'tag':'false',
            'idContent':'false',
            'repeat':'false',
            'playAuto':'false'}

       if 'logger' in request.GET:
           p['logger'] = str(request.GET.get('logger'))

       if 'tagger' in request.GET:
           p['tagger'] = str(request.GET.get('tagger'))

       if 'idCategory' in request.GET:
           p['idCategory'] = str(request.GET.get('idCategory'))

       if 'tag' in request.GET:
           p['tag'] = unicode(request.GET.get('tag'))

       if 'idContent' in request.GET:
           p['idContent'] = str(request.GET.get('idContent'))

       if 'repeat' in request.GET:
           p['repeat'] = str(request.GET.get('repeat'))

       if 'playAuto' in request.GET:
           p['playAuto'] = str(request.GET.get('playAuto'))

       p['base_url'] = settings.MEGAVIDEO_CONF['base_url']

       return render_to_response('index.html', p)


def embed(request):

       p = {}

       p = {'idCategory':False,
            'idContent':False,
            }

       if 'idCategory' in request.GET:
           p['idCategory'] = str(request.GET.get('idCategory'))

       if 'idContent' in request.GET:
           p['idContent'] = str(request.GET.get('idContent'))

       p['base_url'] = settings.MEGAVIDEO_CONF['base_url']

       return render_to_response('embed.html', p)

def redirect(request, video_id):
    try:
        v = Video.objects.using('megavideo').get(id = int(video_id))
    except:
        return HttpResponse(u'O video solicitado não existe!')

    return HttpResponseRedirect(get_video_url(request, v))

def get_original_url(request, video):
    url = os.path.join('/storage/videos/_', video.dir, video.name)
    return HttpResponseRedirect(url)


def get_transcode(request, tname, key=''):

    try:
        video_id = Video().deserialize( key )
        v = Video.objects.using('megavideo').get(id = int(video_id))
    except:
        return HttpResponse(u'O vídeo selecionado não existe!')

    if tname == 'Original':
        return get_original_url(request, v)

    t = v.videotranscode_set.filter(transcode__name = tname)

    if not t:
	try:
	    t = v.videotranscode_set.get(transcode__name = 'Mp4Medium')
	except:
            return HttpResponse(u'Transcode %s não está habilitado para o sistema' % tname)
    else:
        t = t[0]

    vd = VisitorDownload(video = v, transcode = t.transcode, channel = v.channel_set.all()[0])

    url = get_trancode_url(t)

    if 'start' in request.REQUEST:
        url += '?start=' + request.REQUEST['start']
        vd.start_time = float(request.REQUEST['start'])
        vd.size = (t.size / v.duration) * (v.duration - vd.start_time)
        vd.total_time = v.duration - vd.start_time
    else:
        vd.start_time = 0
        vd.size = t.size
        vd.total_time = v.duration

    vd.visitor_id = request.session.get('id_visitor', None)

    if request.REQUEST.get('views', 'true') == 'true':
        v.views += 1
        v.save(using='megavideo')
        vd.save(using='megavideo')
        if url.find('?start') >= 0:
            url += '&download_id=' + str(vd.id)
        else:
            url += '?download_id=' + str(vd.id)

    return HttpResponseRedirect(url)


def get_absolute_url(request, tname, video_id):

    if video_id == 0:
        return ''

    v = Video.objects.using('megavideo').get(pk = int(video_id))
    if tname == 'Original':
        return get_original_url(request, v)
    t = v.videotranscode_set.filter(transcode__name = tname)
    if t:
        url = settings.MEGAVIDEO_CONF['base_url'][0:-1] + get_trancode_url(t[0])
    else:
        url = settings.MEGAVIDEO_CONF['base_url'][0:-1]

    return str(url)


def get_thumb(request, key='', tsize = 'M'):

    video_id = Video().deserialize( key )

    v     = Video.objects.using('megavideo').get(id = int(video_id))
    thumb = settings.MEDIA_STATIC + 'megavideo/static/manager/images/processando.jpg'

    try:
        vt = v.videothumb_set.filter(size = tsize)[0]
    except:
        vt = v.videothumb_set.all()[0]

    thumb = get_thumb_url(vt)

    return HttpResponseRedirect(thumb)
