# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from megavideo.portal.tools import CaptchaTestForm, Video, VideoVote


def teste(request):
    p = {}
    return render_to_response('portal/teste.html', p, context_instance=RequestContext(request))


def ajax_captcha(request):

    p = {}

    p['id_video'] = int(request.REQUEST.get('id_video', 1))
    p['value'] = int(request.REQUEST.get('value', 5))
    p['human'] = False
    p['voto'] = 'false'

    if 'captcha_1' in request.POST:
        p['human'] = True
        p['message'] = 'Autenticação inválida'
        p['voto'] = 'false'
        v = Video.objects.using('megavideo').get(id=p['id_video'])

        p['voted'] = v.get_vote()
        form = CaptchaTestForm(request.POST)
        # Validate the form: the captcha field will automatically 
        # check the input
        if form.is_valid():
            p['message'] = 'Seu voto já foi enviado'

            vt = VideoVote()
            vt.video_id = p['id_video']
            vt.ip = request.META['REMOTE_ADDR']
            vt.agent = request.META['HTTP_USER_AGENT']
            vt.vote = p['value']
            vt.save(using='megavideo')
            v.ratenum += 1
            v.ratesum += p['value']
            v.save(using='megavideo')

            p['message'] = 'O cadastro de seu voto <br> foi efetuado com sucesso'
            p['voto'] = 'true'

            v = Video.objects.using('megavideo').get(id=p['id_video'])
            p['voted'] = v.get_vote()

    else:

        p['form'] = CaptchaTestForm()

    return render_to_response('portal/ajaxcaptcha.html', p, context_instance=RequestContext(request))


def option_embed(request):

    width = request.REQUEST.get('width', '640')
    height = request.REQUEST.get('height', '360')
    video_id = request.REQUEST.get('video_id', 0)

    p = {}

    p['video_id'] = video_id
    p['playAuto'] = 'false'
    p['dimensao'] = {'width': width, 'height': height}
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']

    v = Video.objects.using('megavideo').get(id = int(video_id))

    return HttpResponse( v.get_embed(width, height) )
