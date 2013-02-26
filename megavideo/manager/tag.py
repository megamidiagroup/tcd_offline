# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from django.shortcuts import render_to_response
from django.template import RequestContext

from megavideo.video.models import *

per_page = 12

#===============================================================================
# Gerencia Tags
#===============================================================================

@login_required
def list_tag(request, video_id = 0):
    #monta os menus
    p = menu_top(request);

    request.breadcrumbs(u'Configurações', "javascript:void(0)")
    request.breadcrumbs(u'Vídeo ', request.channel_url + 'manager/program/')
    request.breadcrumbs(u'TAG', "javascript:void(0)")

    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
    p['tags'] = VideoTag.objects.using('megavideo').filter(video__id = video_id).order_by('initime')
    p['video'] = Video.objects.using('megavideo').get(id = video_id)
    p['video_id'] = video_id

    p['inteiro'] = ''
    p['pontual'] = ''
    p['faixa'] = ''
    p['extra_css'] = 'portal_background'

    p['type'] = ''

    p['selection'] = 'Todas as categorias'

    return render_to_response('manager/tag/list.html', p, context_instance = RequestContext(request))


@login_required
def add_tag(request):

    p = {}

    p['status'] = False
    p['duplic'] = False

    video_id = request.REQUEST.get('id', False)
    tag = request.REQUEST.get('tag', False)
    timer = request.REQUEST.get('timer', False)
    p['form_action'] = request.get_full_path()[1:]

    #t = VideoTag.objects.using('megavideo').filter(tags = tag, video__id = int(video_id)).count()

    #if not t:
    if video_id:

        array = tag.split(',')
        for i in array:
            t = VideoTag()
            t.video_id = int(video_id)
            t.tags = i
            if float(timer) > 0.5:
                t.initime = float(timer)
            else:
                t.initime = float(0.00)
            t.endtime = float(0.00)

            try:
                t.save(using='megavideo')
                p['status'] = True
            except:
                pass
    #else:
        #p['duplic'] = True

    return HttpResponse(json.dumps(p), mimetype = 'application/json')


@login_required
def edit_tag(request):

    p = {}

    p['status'] = False
    p['duplic'] = False

    idtag = request.REQUEST.get('id', False)
    video_id = request.REQUEST.get('video_id', False)
    tag = request.REQUEST.get('tag', False)
    timer = request.REQUEST.get('timer', False)

    #t = VideoTag.objects.using('megavideo').filter(tags = tag, video__id = int(video_id)).exclude(id = int(idtag)).count()

    #if not t:
    if idtag:

        t = VideoTag.objects.using('megavideo').get(id = int(idtag))
        t.tags = tag
        if float(timer) > 0.5:
            t.initime = float(timer)
        else:
            t.initime = float(0.00)
        t.endtime = float(0.00)

        try:
            t.save(using='megavideo')
            p['status'] = True
        except:
            pass
    #else:
        #p['duplic'] = True

    return HttpResponse(json.dumps(p), mimetype = 'application/json')


def ajax_get_tag(request):

    p = {}

    id_tag = int(request.REQUEST.get('id_tag'))

    vt = VideoTag.objects.using('megavideo').get(id = id_tag)

    p['id'] = vt.id
    p['tag'] = vt.tags[1:-1]
    p['timer'] = vt.initime
    p['tempo'] = number2time(vt.initime)

    return HttpResponse(json.dumps(p), mimetype = 'application/json')


def ajax_del_tag(request):

    p = {}

    id_tag = int(request.POST.get('id_tag'))
    vt = VideoTag.objects.using('megavideo').get(id = id_tag)

    try:
        vt.delete()
        p['status'] = True
    except:
        p['status'] = False

    return HttpResponse(json.dumps(p), mimetype = 'application/json')


def ajax_list_tag(request):

    p = {}

    video_id = int(request.REQUEST.get('video_id', False))
    type = request.REQUEST.get('type', '')

    if type == '':
        p['tags'] = VideoTag.objects.using('megavideo').filter(video__id = video_id).order_by('initime')
    elif type == 'inteira':
        p['tags'] = VideoTag.objects.using('megavideo').filter(video__id = video_id, initime = 0.00).order_by('initime')
    elif type == 'pontual':
        p['tags'] = VideoTag.objects.using('megavideo').filter(video__id = video_id).exclude(initime = 0.00).order_by('initime')

    return render_to_response('manager/tag/ajax_list.html', p, context_instance = RequestContext(request))


