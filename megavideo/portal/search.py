# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.shortcuts import render_to_response
from django.conf import settings
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string
from django.template import RequestContext
from megavideo.video.models import *

#DiggPaginator
from megavideo.common.DiggPaginator import *

### import dos defs ###
from megavideo.portal.tools import _prepare_page

#cache_page(30)
def search(request, cat_id = 0, sub_id = 0, tag = '', page = 1):

    p = {}

    p['cat_id'] = cat_id
    p['sub_id'] = sub_id

    p['chan'] = request.channel_name
    p['channel_url'] = request.channel_url

    p['channel_prefix'] = settings.MEGAVIDEO_CONF['channel_prefix']

    lastvideos_id = 'corner-listvideos-search'

    #invoca o menu principal
    _prepare_page(request, p, cat_id, sub_id, lastvideos_id = lastvideos_id)

    last_videos = Video.objects.using('megavideo').filter(published = True).order_by('-date')
    if p['chan']:
        last_videos = last_videos.filter(channel__name = p['chan'])

    paginator = DiggPaginator(last_videos, 4, body = 5, padding = 1 , margin = 1, tail = 1)

    try:
        last_videos = paginator.page(1)
    except:
        last_videos = paginator.page(paginator.num_pages)

    p['superlistvideos'] = {'list' : last_videos, 'title' : 'Últimos vistos', 'id' : 'listvideos', 'max' : paginator.num_pages, 'class' : lastvideos_id}

    p['last_videos'] = render_to_string('portal/super_listvideos.html', p)

    p['var_search'] = ''

    if request.REQUEST.get('search', '') != "" and request.REQUEST.get('search', '') != 'Buscar':
        p['var_search'] = '?search=' + unicode(request.REQUEST['search'])
        p['search'] = unicode(request.REQUEST['search'])
        content_list = Video.objects.using('megavideo').filter(videometa__value__icontains = p['search'], published = True).order_by('videocategory__sequence').distinct()
    else:
        content_list = Video.objects.using('megavideo').filter(published = True).order_by('-id')

    if p['chan']:
        content_list = content_list.filter(channel__name = p['chan']).order_by('videocategory__sequence').distinct()

    #if tag != '':
    #    p['search'] = tag
    #    content_list = Video.objects.using('megavideo').filter(videotag__tags__icontains = p['search'], published = True).filter(channel__name = p['chan']).order_by('videocategory__sequence').distinct()

    paginator = DiggPaginator(content_list, 12, body = 5, padding = 1 , margin = 1, tail = 1)

    if content_list.count() == 0:
        #print 'passou'
        p['suggesting'] = Video.objects.using('megavideo').filter(published = True).order_by('-ratesum').filter(channel__name = p['chan']).order_by('videocategory__sequence').distinct()[0:8]

    try:
        p['content_list'] = paginator.page(page)
    except:
        p['content_list'] = paginator.page(paginator.num_pages)

    p['searchpage'] = True

    p['channel_menu'] = Channel.objects.using('megavideo').all().order_by('-name')

    p['combocat'] = render_to_string('portal/combochan.html', p)

    p['pagination_url'] = p['channel_url'] + 'search/page/'

    return render_to_response('portal/list_videos.html', p, context_instance = RequestContext(request))


def ajax_search(request):

     p = {}

     channel = request.REQUEST.get('channel', '')
     search = request.REQUEST.get('search' , '')

     if channel and channel != 'None':
         videos = Video.objects.using('megavideo').filter(channel__name = channel).filter(videometa__value__icontains = search).filter(published = True).distinct()[0:6]
     else:
         videos = Video.objects.using('megavideo').filter(videometa__value__icontains = search).filter(published = True).distinct()[0:6]

     p['videos'] = videos
     p['channel_url'] = request.channel_url

     return render_to_response('portal/ajaxsearch.html', p, context_instance = RequestContext(request))
