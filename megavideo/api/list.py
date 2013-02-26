#-*- coding: utf8 -*-
#!/usr/bin/python 

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.http import urlquote
from django.conf import settings

import simplejson

from tagging.models import *

from megavideo.common.channel import get_current_channel
from megavideo.video.models import *
from megavideo.api.video import video_search

#DiggPaginator
from megavideo.common.DiggPaginator import *
from megavideo.api.filters import *


def index(request):
    """
        Função padrão para pesquisa e retorno de widget
    """
    #filter
    p = {}
    category = request.REQUEST.get('category', 0)
    tags = request.REQUEST.get('tags', 0)
    search = request.REQUEST.get('search', 0)
    order = request.REQUEST.get('order', 0)

    url = remove_pagenumber(request.REQUEST.get('link', 'todos_os_videos.php'), search)

    #list 
    page = int(request.REQUEST.get('page', 1))
    limit = int(request.REQUEST.get('limit', 10))
    paginate = int(request.REQUEST.get('paginate', 0))

    #style 
    truncate_title = request.REQUEST.get('truncate_title', '5-10')
    truncate_desc = request.REQUEST.get('truncate_desc', '10-15')
    render = request.REQUEST.get('render', 'js')
    thumb_size = request.REQUEST.get('thumb_size', '177x100')
    list_as = str(request.REQUEST.get('list_as', 'ul'))
    id = request.REQUEST.get('id', 'vflow_list')
    classname = request.REQUEST.get('class', 'vflow_list')
    simple = request.REQUEST.get('simple', False)
    channel_name = request.REQUEST.get('channel', request.channel_name)

    if list_as == 'cloud_video':
        if channel_name:
            p.update({ 'cloud' :  Tag.objects.using('megavideo').cloud_for_model(VideoTag, filters={'video__channel__name' : channel_name }, min_count=5) })
        else:
            p.update({ 'cloud' :  Tag.objects.using('megavideo').cloud_for_model(VideoTag, min_count=5) })
        videos = False

    if list_as == 'cloud_search':
        se = SearchRate()
        p.update({ 'cloud' :  se.get_cloud(steps=5, limit=limit) })
        videos = False

    else:

        if order:
            videos = video_search(value=search, channel=channel_name, tags=tags, category=category, orderby=order , published=True)
        else:
            videos = video_search(value=search, channel=channel_name , tags=tags, category=category , published=True)


    width, height = thumb_size.split('x')

    paginator = DiggPaginator(videos, limit, body=5, padding=1 , margin=1, tail=1)

    try:
        content_list = paginator.page(page)
    except:
        content_list = []

    p.update({
         'conf' : {'thumb_size' : thumb_size ,
                   'width': width,
                   'height' : height ,
                   'list_as' : list_as ,
                   'id' : id ,
                   'classname' : classname ,
                   'truncate_title' : truncate_title ,
                   'truncate_desc' : truncate_desc ,
                   },
         'content_list' : content_list,
         'simple' : simple,
         'base_url' : settings.MEGAVIDEO_CONF['base_url'][:-1],
         'paginate' : paginate ,
         'url': url,
         })

    text = render_to_string('api/block_list.html', p, context_instance=RequestContext(request))

    if render == 'html':
        return HttpResponse(text)

    if render == 'json':
        return HttpResponse(simplejson.dumps({'text': text}), mimetype='application/json')

    text = out_js(text)

    return HttpResponse(text)


def test(request):
    return render_to_response('api/testjs.html', {'script' : '/api/list.js', 'values': request.META['QUERY_STRING'] })
