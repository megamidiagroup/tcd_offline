# -*- coding: utf-8 -*-
#!/usr/bin/python
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import Library
from django.conf import settings
from megavideo.video.models import Video, Job, VideoMeta, VideoComment
import simplejson
from megavideo.templatetags.miniature import thumbnail
from django.db.models import Q

from django.views.decorators.cache import cache_page
from megavideo.video.models import SearchRate
from django.db.models import Count

def set_metas(request, video_id):
    """ 
        Salva metas de um vídeo 
    """
    metas = simplejson.loads(request.REQUEST.get('metas'))
    v = Video.objects.using('megavideo').get(id=int(video_id))

    for i in metas.keys():
        v.set_meta(i, metas[i])

    r = dict([(i, v.get_meta(i)) for i in v.get_meta_keys()])
    r['id'] = v.id
    r = simplejson.dumps(r)

    return HttpResponse(r)


@cache_page(600)
def embed_js(request):
    """ 
        Gerador de embed js 
    """
    sourceid = request.REQUEST.get('sourceid', '')
    video_id = request.REQUEST.get('video_id', '')
    width = request.REQUEST.get('width', '640')
    height = request.REQUEST.get('height', '360')
    p = {}

    if sourceid:
        try:
            vm = VideoMeta.objects.using('megavideo').filter(value=str(sourceid), metaclass__name='sourceid')[0]
            video_id = vm.video.id
        except:
            return HttpResponse('')

    try:
        video = Video.objects.using('megavideo').get(id=int(video_id))
    except:
        return HttpResponse('')

    p['dimensao'] = {'width' : width, 'height' : height}
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
    p['video'] = video

    ret_value = 'document.write(\'<script type=\'text/javascript\'>%s</script>\');\n' % render_to_string('../../../static/portal/js/video.js')

    play = render_to_string('portal/embed.html', p)
    for i in play.splitlines():
        ret_value += 'document.write(' + simplejson.dumps(i) + ');\n'

    return HttpResponse(ret_value)

def thumb(request, video_id):
    """ 
        Gera uma thumbnail caso ela não exista e retorna sua url
    """
    v = Video.objects.using('megavideo').get(id=int(video_id))
    size = str(v.width) + 'x' + str(v.height)
    size = request.REQUEST.get('size', size)
    url = thumbnail(v, size)
    return HttpResponseRedirect(url)


def comment_search(**kwarg):
    default_chan = getattr('tv_name', 'settings.MEGAVIDEO_CONF', 'portal')

    id = kwarg.get('id', 0)
    value = kwarg.get('value', 0)
    category = kwarg.get('category', 0)
    orderby = kwarg.get('orderby', '-id,-date')
    channel = kwarg.get('channel', default_chan)
    published = kwarg.get('published' , 0)
    video_id = kwarg.get('video_id', 0)

    #create order args
    args_orderby = [x.strip() for x in orderby.split(',')]

    try:
        channel = int(channel)
    except:
        channel = str(channel)


    if type(channel) == str:
       comments = VideoComment.objects.using('megavideo').filter(video__channel__name=channel)
    elif type(channel) == int:
       comments = VideoComment.objects.using('megavideo').filter(video__channel__id=channel)
    else:
       comments = VideoComment.objects.using('megavideo').all()

    if published:
        comments = comments.filter(published=True)
    if id:
        comments = comments.filter(id=id)
    if value:
        comments = comments.filter(Q(content__icontains=value) | Q(name__icontains=value))
    if category:
        comments = comments.filter(Q(video__category__id=category) | Q(video__category__parent=category))
    if video_id:
        comments = comments.filter(video__id=video_id)

    comments = comments.order_by(*args_orderby)

    return comments


def video_search(**kwarg):
    """ 
        Pesquisa default 
        id = kwarg.get('id', 0)
        value = kwarg.get('value', 0)
        channel = kwarg.get('channel', default_chan)
        category = kwarg.get('category', 0)
        orderby = kwarg.get('order_by', ('videocategory__sequence', '-id'))   
    """
    default_chan = getattr('tv_name', 'settings.MEGAVIDEO_CONF', 'portal')

    id = kwarg.get('id', 0)
    value = kwarg.get('value', 0)
    channel = kwarg.get('channel', default_chan)
    category = kwarg.get('category', 0)
    orderby = kwarg.get('orderby', 'videocategory__sequence,-id')
    tags = kwarg.get('tags', 0)
    published = kwarg.get('published' , 0)

    #create order args
    args_orderby = [x.strip() for x in orderby.split(',')]

    try:
        channel = int(channel)
    except:
        channel = str(channel)

    if type(channel) == str:
        video = Video.objects.using('megavideo').filter(channel__name=channel).extra(select={'videocomments':'select Count(id) from video_videocomment where published=1 and video_videocomment.video_id=video_video.id'})
    else:
        video = Video.objects.using('megavideo').extra(select={'videocomments':'select Count(id) from video_videocomment where published=1 and video_videocomment.video_id=video_video.id'})

    #defaul search
    if published:
        video = video.filter(published=True)
    else:
        video = video.filter(channel__name=channel)

    if value and category and id:
        qr = video.filter(id=id).order_by(*args_orderby)
    elif tags:
        search_rate = SearchRate()
        search_rate.add(tags)
        tags = tags.split(',')
        qr = videos.filter(videotag__in=TaggedItem.objects.using('megavideo').get_by_model(VideoTag.objects.using('megavideo').filter(video__published=True, video__channel=default_chan), Tag.objects.using('megavideo').filter(name__in=tags))).distinct().order_by(*args_orderby)
    elif value and category:
        search_rate = SearchRate()
        search_rate.add(value)
        qr = video.filter( ( Q(title__icontains = value) | Q(description__icontains = value) ) & (Q(category=category) | Q(category__parent=category))).distinct().order_by(*args_orderby)
    elif value:
        search_rate = SearchRate()
        search_rate.add(value)
        qr = video.filter( Q(title__icontains = value) | Q(description__icontains = value) ).distinct().order_by(*args_orderby)
    elif category:
        qr = video.filter((Q(category=category) | Q(category__parent=category))).order_by(*args_orderby)
    elif id:
        qr = video.filter(id=id).order_by(*args_orderby)
    else:
        qr = video.distinct().order_by(*args_orderby)

    return qr
