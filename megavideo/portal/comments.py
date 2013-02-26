# -*- coding: utf-8 -*-
#!/usr/bin/env python

import simplejson as json

from megavideo.video.models import *
from megavideo.common.dlog import LOGGER
from django.shortcuts import render_to_response
from django.http import HttpResponse

### import dos defs ###
from megavideo.portal.tools import is_valid_email, _prepare_comment


def ajax_send_comment(request):
    """ para salvar comentário novo """
    
    p = {}
    
    nome    = request.REQUEST.get('nome'    , '')
    email   = request.REQUEST.get('email'   , '')
    msg     = request.REQUEST.get('msg'     , '')
    video_id = request.REQUEST.get('video_id' , 0)
    
    if not video_id:
        p['msg']    = 'Impossivel enviar, contacte o administrador!'
        p['status'] = False
    elif nome == '':
        p['msg']    = 'Informe seu Nome!'
        p['status'] = False
    elif email == '':
        p['msg']    = 'Informe seu E-mail!'
        p['status'] = False
    elif not is_valid_email(email):
        p['msg']    = 'E-mail está incorreto!'
        p['status'] = False
    elif msg == '':
        p['msg']    = 'Faça seu comentário!'
        p['status'] = False
    elif len(msg) < 10:
        p['msg']    = 'Faça seu comentário, no minimo 10 letras!'
        p['status'] = False
    
    else:
            
        c           = Videocomment()
        c.name      = nome
        c.email     = email
        c.content   = msg
        c.video_id  = int(video_id)
        c.save(using='megavideo')
            
        p['msg']    = 'Comentário enviado com sucesso!'
        p['status'] = True
        
    return HttpResponse(json.dumps(p), mimetype='application/json')


def ajax_itens_comment(request):
    """ pega itens para lista """
    
    p = {}
    
    p['channel_url'] = request.channel_url
    
    video_id  = request.REQUEST.get('video_id'    , 0)
    page     = request.REQUEST.get('page'       , 1)
    position = request.REQUEST.get('position'   , 'bottom')
    limit    = request.REQUEST.get('limit'      , 0)
    
    try:
        if position == 'bottom':
            p = _prepare_comment(p, int(video_id), page=page)
        elif position == 'top':
            p = _prepare_comment(p, int(video_id), page=1, limit=1)
        elif position == 'all':
            p = _prepare_comment(p, int(video_id), page=1, limit=int(limit))
    except:
        return HttpResponse('<script>$(".more").attr("onclick", "").css("opacity", .2).css("cursor", "default");</script>')
    
    return render_to_response('portal/list_comments.html', p)


def ajax_comment_list(request):

    video = int(request.REQUEST.get('video_id'   , 387))
    page  = int(request.REQUEST.get('page'      , 1))
    
    p = _prepare_comment({}, video, page)
	
    p['video'] = {'id': video}
     
    return render_to_response('portal/ajax_commentlist.html', p, context_instance=RequestContext(request))