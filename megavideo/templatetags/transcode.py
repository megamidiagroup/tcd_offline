# -*- coding: utf-8 -*-

from django.template import Library
from django.conf import settings

from megavideo.video.models import Video
from megavideo.statistics.models import VisitorDownload
from megavideo.common.create_url import get_trancode_url, get_thumb_url

register = Library()


def _get_transcode(request, tname, key):
    
    try:
        video_id = Video().deserialize( key )
        v = Video.objects.using('megavideo').get(id = int(video_id))
    except:
        return u'O vídeo selecionado não existe!'

    t = v.videotranscode_set.filter(transcode__name = tname)

    if not t:
        try:
            t = v.videotranscode_set.get(transcode__name = u'Mp4Medium')
        except:
            return u'Transcode %s não está habilitado para o sistema' % tname
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
    
    return url


@register.filter
def get_mp4(key, request):
    
    return _get_transcode(request, 'Mp4Medium', key)

register.filter('get_mp4', get_mp4)


@register.filter
def get_webm(key, request):
        
    return _get_transcode(request, 'WebM', key)
   
register.filter('get_webm', get_webm)


@register.filter
def get_ogv(key, request):
        
    return _get_transcode(request, 'Ogv', key)
   
register.filter('get_ogv', get_ogv)


@register.filter
def get_thumb(key, request):

    video_id = Video().deserialize( key )

    v     = Video.objects.using('megavideo').get(id = int(video_id))
    thumb = '/megavideo/static/manager/images/processando.gif'

    try:
        vt = v.videothumb_set.filter(size = u'M')[0]
    except:
        vt = v.videothumb_set.all()[0]

    thumb = get_thumb_url(vt)

    return thumb


@register.filter
def serialize(id):

    return Video().serialize( id )


@register.filter
def deserialize(key):

    return Video().deserialize( key )
