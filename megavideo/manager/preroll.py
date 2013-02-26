# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from django.shortcuts import render_to_response
from django.template import RequestContext

from megavideo.video.models import *

per_page = 12


def prerolldemo(request, video_id):
    p = menu_top(request);

    request.breadcrumbs(u'Configurações', "javascript:void(0)")
    request.breadcrumbs(u'Vídeo ', request.channel_url + 'manager/program/')
    request.breadcrumbs(u'Preroll', "javascript:void(0)")


    video = Video.objects.using('megavideo').get(pk = int(video_id))
    if 'roll_id' in request.REQUEST:
        video.rolls.all().delete()
        roll_id = int(request.REQUEST.get('roll_id', 0))
        if roll_id != 0:
            vr = VideoRoll()
            vr.video = video
            vr.roll_id = roll_id
            vr.published = int(request.REQUEST.get('published', True))
            vr.title = request.REQUEST.get('title', 'sem nome')
            vr.position = request.REQUEST.get('position', 0)
            vr.save(using='megavideo')
            p['roll'] = vr.roll
    p['videos'] = Video.objects.using('megavideo').filter(channel__name = request.channel_name, duration__lte = 30)

    p['video'] = video

    return render_to_response('manager/preroll/prerolldemo.html', p, context_instance = RequestContext(request))
