# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template.loader import render_to_string
from django.template import RequestContext
from megavideo.common.channel import *
from megavideo.common.dlog import LOGGER
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect

import time

### import dos defs ###
from megavideo.portal.tools import _prepare_page, _prepare_comment


def index(request, cat_id = 0, video_id = 0):

    return HttpResponseRedirect(settings.MEGAVIDEO_CONF.get('base_url', '') + 'manager/')

    try:
        if request.META['HTTP_USER_AGENT'].find('iPhone') > 0:
            return HttpResponseRedirect('./iphone/')
    except:
        return HttpResponse(u'Não é possível acessar essa página sem navegador. Permissão negada!')

    start = time.time()
    p = {'vlist': []}

    p['cat_id'] = int(cat_id)

    p['chan'] = request.channel_name
    p['channel_url'] = request.channel_url

    try:
        p['current_category'] = Category.objects.using('megavideo').get(id = p['cat_id'])
    except:
        pass

    p['digg_url'] = 'manager/channel/'
    p['channel_url'] = request.channel_url

    #invoca o menu principal
    _prepare_page(request, p, cat_id, video_id)


    #pega a categoria    
    if cat_id > 0 and video_id == 0:
        p['playAuto'] = 'false'
        try:
            #print 'VIDEO DIRETO ------------------------------------------------------------------------------'
            p['video'] = Video.objects.using('megavideo').filter(category__id = cat_id, published = True, channel__name = p['chan']).order_by('videocategory__sequence')[0]
        except:
             try:
                #print 'VIDEO COM FILTRO POR CATEGORIA------------------------------------------------------------------------------' 
                p['video'] = p['last_video'][0]
             except:
                #print 'VIDEO SEM NADA ------------------------------------------------------------------------------' 
                pass

    if video_id > 0:
        #print 'VIDEO SELECIONADO POR URL   ------------------------------------------------------------------------------'
        try:
            p['video'] = Video.objects.using('megavideo').get(id = video_id)
        except:
            return HttpResponse(u'O vídeo não existe.')
        p['playAuto'] = 'true'

    elif video_id == 0:

        try:
            video_id = p['video'].id
        except:
            video_id = 0

        p['playAuto'] = 'false'


    # pega videos e categorias em destaque
    vf = VideoFeatured.objects.using('megavideo').filter(channel__name = p['chan'])

    if 'video' not in p:
        #video de destaque
        vfvideo = vf.filter(typevideofeatured__name = 'v').order_by('-id')
        if vfvideo.count() > 0:
            p['video'] = vfvideo[0].video
        else:
            #sem video de destaque
            try:
                if 'last_video' in p:
                    if len(p['last_video']) > 0:
                        p['video'] = p['last_video'][0]
                    else:
                        p['video'] = Video.objects.using('megavideo').filter(published = True, channel__name = p['chan']).order_by('videocategory__sequence')[0]
                else:
                    p['video'] = Video.objects.using('megavideo').filter(published = True, channel__name = p['chan']).order_by('videocategory__sequence')[0]
            except:
                p['video'] = []

    try:
        p = _prepare_comment(p, p['video'].id, 1)
    except:
        pass

    p['dimensao'] = {'width': 640, 'height': 360}
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
    p['flash'] = render_to_string('white/embed.html', p)

    try:
        p['absolute_url'] = get_absolute_url(request, 'FlashWeb', p['video'].id)
    except:
        p['absolute_url'] = ''

    try:
        soma = p['video'].ratesum / 5
    except:
        soma = 0

    if soma < 5:
        p['safe_voted'] = soma
    else:
        p['safe_voted'] = 5

    p['vote'] = [1, 2, 3, 4, 5]

    if 'tag' in request.REQUEST:
        p['search'] = request.REQUEST['tag']

    if 'ajax_search' in request.REQUEST:
        p['search'] = request.REQUEST['ajax_search']


    try:
        vt = p['video']
    except:
        vt = None

    if vt:
        p['videotag'] = [ x.name for i in vt.videotag_set.all().order_by('-id') for x in i.get_tags() ][:10]
    else:
        p['videotag'] = []

    #{{ base_url }}/video/{{ video.id }}/{{ video.get_name|slugify }}
    try:
        request.session['selected_video'] = p['base_url'] + "video/" + str(p['video'].id) + "/" + defaultfilters.slugify(p['video'].get_name())
    except:
        request.session['selected_video'] = p['base_url'] + "video/" + str(0) + "/"

    p['selected_video'] = request.session['selected_video']

    request.session['video_id'] = video_id

    p['urlplayer'] = settings.STATIC_URL + "{{STATIC_URL}}/static/white/swf/megaplayer.swf"

    return render_to_response('white/main.html', p, context_instance = RequestContext(request))


def vast(request, video_id = 637):

    p = {}

    p['chan'] = request.channel_name
    p['channel_url'] = request.channel_url
    p['digg_url'] = 'manager/channel/'

    #invoca o menu principal
    _prepare_page(request, p, 0, video_id)

    p['video'] = Video.objects.using('megavideo').filter(published = True).order_by('videocategory__sequence')
    if video_id:
        try:
            p['video'] = p['video'].filter(id = int(video_id))[0]
        except:
            p['video'] = p['video'][0]
    else:
        p['video'] = p['video'][0]
    p['playAuto'] = 'false'
    p['dimensao'] = {'width': 640, 'height': 360}
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']

    p['urlplayer'] = settings.STATIC_URL + "{{STATIC_URL}}/static/white/swf/newplayer_vast.swf"

    return render_to_response('white/main.html', p, context_instance = RequestContext(request))
