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
from megavideo.api.video import comment_search

#DiggPaginator
from megavideo.common.DiggPaginator import *
from megavideo.api.filters import *

def add_comment(request):
    p = {}
    video_id = request.REQUEST.get('video_id', 0)
    name = request.REQUEST.get('name', 0)
    email = request.REQUEST.get('email', 0)
    comment = request.REQUEST.get('comment', 0)
    callback = request.REQUEST.get('callback')

    new_comment = VideoComment()
    new_comment.name = name
    new_comment.email = email
    new_comment.content = comment
    new_comment.video_id = video_id

    try:
        new_comment.save(using='megavideo')
        p['msg'] = 'Comentário cadastrado com sucesso'
    except:
        p['msg'] = 'Erro ao adicionar um comentário'

    #return HttpResponse(simplejson.dumps(p), mimetype = 'application/json')

    callme = "%s(%s)" % (callback, simplejson.dumps(p))

    return HttpResponse(callme, mimetype='text/plain')



def index(request):
    """
        Função padrão para pesquisa e retorno de widget
    """
    #filter
    p = {}
    category = request.REQUEST.get('category', 0)
    search = request.REQUEST.get('search', 0)
    order = request.REQUEST.get('order', 0)

    url = remove_pagenumber(request.REQUEST.get('link', 'todos_os_videos.php'), search)

    #list 
    page = int(request.REQUEST.get('page', 1))
    limit = int(request.REQUEST.get('limit', 4))
    paginate = int(request.REQUEST.get('paginate', 0))
    page_link = request.REQUEST.get('page_link', 'watch.php')

    #style 
    video_id = request.REQUEST.get('video_id', 0)
    truncate_title = request.REQUEST.get('truncate_title', '5-10')
    truncate_desc = request.REQUEST.get('truncate_desc', '10-15')
    render = request.REQUEST.get('render', 'js')
    list_as = str(request.REQUEST.get('list_as', 'ul'))
    id = request.REQUEST.get('id', 'vflow_list')
    classname = request.REQUEST.get('class', 'vflow_list')
    simple = request.REQUEST.get('simple', False)
    channel_name = request.REQUEST.get('channel', request.channel_name)


    if order:
        comments = comment_search(value=search, channel=channel_name, category=category , video_id=video_id , orderby=order , published=True)
    else:
        comments = comment_search(value=search, channel=channel_name , category=category , video_id=video_id , published=True)

    paginator = DiggPaginator(comments, limit, body=5, padding=1 , margin=1, tail=1)

    try:
        content_list = paginator.page(page)
    except:
        content_list = []

    p.update({
         'conf' : {
                   'list_as' : list_as ,
                   'video_id' : video_id,
                   'id' : id ,
                   'classname' : classname ,
                   'truncate_title' : truncate_title ,
                   'truncate_desc' : truncate_desc ,
                   'page_link' : page_link,
                   },
         'content_list' : content_list,
         'simple' : simple,
         'base_url' : settings.MEGAVIDEO_CONF['base_url'][:-1],
         'paginate' : paginate ,
         'url': url,
         })

    text = render_to_string('api/block_comment.html', p, context_instance=RequestContext(request))

    if render == 'html':
        return HttpResponse(text)

    if render == 'json':
        return HttpResponse(simplejson.dumps({'text': text}), mimetype='application/json')

    text = out_js(text)

    return HttpResponse(text)


def test(request):
    return render_to_response('api/testjs.html', {'script' : '/api/comment.js', 'values': request.META['QUERY_STRING'] })
