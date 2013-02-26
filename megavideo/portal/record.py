# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.contrib.sessions.models import *
from django.template import RequestContext
from megavideo.async.call import AsyncCall
from megavideo.common.dlog import LOGGER
from megavideo.video.models import Channel, Category, Job
from megavideo.record.views import _prepare_recorder, _decode_dict

import os
import simplejson as json
import tempfile

### import dos defs ###
from megavideo.portal.tools import _prepare_page, is_valid_email
from megavideo.video.models import *
from megavideo.common.DiggPaginator import *


def _prepare_last_videos(request, p, page = 1, lastvideos_id = ''):

    last_videos = Video.objects.using('megavideo').filter(published = True, channel__name = request.channel_name).order_by('-ratesum')
    paginator = DiggPaginator(last_videos, 4, body = 5, padding = 1 , margin = 1, tail = 1)

    try:
        last_videos = paginator.page(1)
    except:
        last_videos = paginator.page(paginator.num_pages)

    #print 'lastvideos_id: ' , lastvideos_id
    p['superlistvideos'] = {'list' : last_videos, 'title' : 'Últimos vistos', 'id' : 'listvideos', 'max' : paginator.num_pages, 'class' : lastvideos_id}
    p['last_videos'] = render_to_string('portal/super_listvideos.html', p)

    return p

def _prepare_featured(request, p , page = 1, cat_id = 0 , lastvideos_id = ''):
    vf = VideoFeatured.objects.using('megavideo').filter(channel__name = request.channel_name, video__isnull = True, typevideofeatured__name = 'v')

    if vf.count() > 0:
        #p['featured_exists'] = True
        print 'HAVE VIDEO FEATURED'
        superlistvideos = vf.filter(video__published = True).order_by('-views')
    else:
        if int(cat_id):
            print 'HAVE IDCAT ' , cat_id
            superlistvideos = Video.objects.using('megavideo').filter(published = True, channel__name = request.channel_name, category__id = cat_id).order_by('videocategory__sequence')
        else:
            print 'DEFAULT SEACH'
            superlistvideos = Video.objects.using('megavideo').filter(published = True, channel__name = request.channel_name).order_by('-id')

    if superlistvideos.count() > 0:
        slv = superlistvideos[0].category.filter(published = True)
        if slv.count() == 0:
            subtitle = superlistvideos.filter(published = True)[0].name
        else:
            subtitle = ''
    else:
        subtitle = ''

    paginator = DiggPaginator(superlistvideos, 4, body = 5, padding = 1 , margin = 1, tail = 1)

    try:
        superlistvideospage = paginator.page(1)
    except:
        superlistvideospage = paginator.page(paginator.num_pages)

    p['superlistvideos'] = {'list' : superlistvideospage, 'title' : 'Destaques', 'subtitle' : subtitle, 'id' : 'featured', 'max' : paginator.num_pages}
    p['featured'] = render_to_string('portal/super_listvideos.html', p)

    return p


def form_record(request, cat_id = 0):
    """ para captar os dados do usuario que envia o video """

    p = {}

    p['cat_id'] = int(cat_id)
    p['channel_url'] = request.channel_url

    lastvideos_id = 'corner-listvideos-search'
    p['record'] = True
    p['chan'] = request.channel_name

    p['channel_url'] = request.channel_url

    #invoca o menu principal
    _prepare_page(request, p, cat_id)

    name = request.REQUEST.get('name' , '')
    email = request.REQUEST.get('email' , '')
    title = request.REQUEST.get('title' , '')
    description = request.REQUEST.get('description' , '')
    destino_url = request.REQUEST.get('destino_url' , False)

    print 'DESTINO URL --------------------------------------------------->'
    print destino_url

    if 'addValue' in request.REQUEST:

        filtered = {}
        filtered['name'] = unicode(name)
        filtered['title'] = unicode(title)
        filtered['email'] = email
        filtered['description'] = unicode(description)

        p['form_error'] = ''

        if filtered['name'] == '':
            p['form_error'] = 'O nome é um campo obrigatório'

        if filtered['email'] == '':
            p['form_error'] = 'O e-mail é um campo obrigatório'
        elif not is_valid_email(filtered['email']):
            p['form_error'] = 'O e-mail é inválido!'

        if filtered['title'] == '':
            p['form_error'] = 'O título vídeo é um campo obrigatório'

        #if filtered['description'] == '':
        #    p['form_error'] = 'A descrição é um campo obrigatório'

        if len(p['form_error']) == 0:
            #armazena para o envio pegar
            filtered["chan_id"] = Channel.objects.using('megavideo').get(name = p['chan']).id
            if p['cat_id'] != 0:
                filtered["cat_id"] = cat_id

            request.session['values_form'] = filtered
            request.session['values_rec'] = filtered
            request.session['destino_url'] = destino_url

            if   destino_url == "upload":
                return HttpResponseRedirect(p['channel_url'] + 'uploadvideo/category/' + str(cat_id) + '/?values=' + str(request.session.session_key))
            elif destino_url == "rec":
                return HttpResponseRedirect(p['channel_url'] + 'recvideo/category/' + str(cat_id) + '/?values=' + str(request.session.session_key))
            else:
                p['form_error'] = 'error: não existe o destino_url, para onde devo ir?'


    print 'CREATE FEATURED '
    p = _prepare_featured(request, p , page = 1, cat_id = cat_id)


    return render_to_response('portal/form.html', p, context_instance = RequestContext(request))


def rec_video(request, cat_id = 0):
    """ formulario para gravar o video pela webcam """

    p = {}

    p['cat_id'] = cat_id
    p['chan'] = request.channel_name

    p['destino_url'] = request.REQUEST.get('destino_url' , 'rec')
    p['record'] = True

    p['channel_url'] = request.channel_url

    lastvideos_id = 'corner-listvideos-search'

    r = _prepare_recorder(request, p, 0, p['cat_id'])

    #invoca o menu principal
    #_prepare_page(request, p, cat_id = 0, lastvideos_id = lastvideos_id)
    _prepare_page(request, p, cat_id)


    p['flash_metas'] = {
                            'values'        : request.REQUEST.get('values', ''),
                            'videoBasename' : r['url']['videoBasename'],
                            'savingUrl'     : request.channel_url + (r['url']['savingUrl'])[1:],
                            'token'         : r['url']['token'],
                            'upstreamUrl'   : settings.VFLOW_REC['rtmp_url']
                        }


    p['metas'] = {
                       'validate' : 'flash',
                       'name'     : '',
                       'id'       : 'player',
                       'width'    : '539',
                       'height'   : '309',
                       'base_url' :  settings.MEGAVIDEO_CONF['base_url'],
                       'swf'      : settings.STATIC_URL + '/megavideo/static/portal/swf/rec_public.swf',
                   }



    return render_to_response('portal/form.html', p, context_instance = RequestContext(request))



def upload_video(request, cat_id = 0):
    """ preparando para enviar o arquivo e seus devidos parametros """

    p = {}

    p['cat_id'] = int(cat_id)
    p['chan'] = request.channel_name

    p['destino_url'] = 'upload'
    p['record'] = True

    p['channel_url'] = request.channel_url

    values = request.REQUEST.get('values', '')

    try:
        sess = Session.objects.using('megavideo').get(pk = values)
        session = sess.get_decoded()
    except:
        return HttpResponseRedirect(p['channel_url'] + 'record/category/' + str(cat_id) + '/')

    if not session['values_form']['name']:
        return HttpResponseRedirect(p['channel_url'] + 'record/category/' + str(cat_id) + '/')

    #invoca o menu principal
    _prepare_page(request, p, p['cat_id'])

    p['flash_metas'] = {
                        'values'            : values,
                        'types'             : 'Video:mp4|wmv|avi|flv|3gp|mov',
                        'url'               : settings.MEGAVIDEO_CONF['base_url'] + request.channel_url,
                        'expressInstall'    : settings.STATIC_URL + '/megavideo/static/portal/swf/expressInstall.swf'
                    }

    p['metas'] = {
                    'validate'  : 'flash',
                    'id'        : 'flashupload' ,
                    'width'     : '614' ,
                    'height'    : '158' ,
                    'swf'       : settings.STATIC_URL + '/megavideo/static/portal/swf/upload_public.swf',
                    'base_url'  : settings.MEGAVIDEO_CONF['base_url']
                 }

    return render_to_response('portal/form.html', p, context_instance = RequestContext(request))



def upload_public(request):
    """ para envio de arquivo publico """

    LOGGER.debug('upload starts ' + str(request.FILES.keys()))
    LOGGER.debug('before')

    chan = request.channel_name

    r = {}
    msg = {}

    values      = request.REQUEST.get('values' , '')
    channel_str = request.REQUEST.get('channel', '')

    if values:
        # ********** create methodo ************* #
        s = Session.objects.using('megavideo').get(pk = values)
        session = s.get_decoded()
        # ********** end ************************ #
        r = session.get('values_form', '')
        try:
            del(session['values_form'])
        except:
            pass
    else:
        r = {}

        LOGGER.debug('values_rec: ' + str(r))

    if 'chan_id' in r:
        chan_id = r['chan_id']
        channel = Channel.objects.using('megavideo').get(id = chan_id)
    else:
        if channel_str != '':
            channel = Channel.objects.using('megavideo').get(name = channel_str)
        else:
            channel = Channel.objects.using('megavideo').get(name = chan)
        chan_id = channel.id

    LOGGER.debug('receive post')

    if 'Filedata' in request.FILES:
        LOGGER.debug('insider')

        file_uploaded = request.FILES['Filedata']

        # ver
        if 'name' in r and r['name'] == '':
            r['name'] = file_uploaded.name

        conf = settings.MEGAVIDEO_CONF
        tmp = tempfile.mktemp('_' + conf['tv_name'])
        tmp = conf['tmp'] + os.path.basename(tmp)
        fd = open(tmp, 'wb')

        LOGGER.debug('opened')

        for chunk in file_uploaded.chunks():
            fd.write(chunk)
        fd.close()

        LOGGER.debug('insider3')

        LOGGER.debug('channel: ' + str(channel))

        job = Job()
        job.channel = channel
        job.ip = request.META['REMOTE_ADDR']
        job.status = 'A'
        job.original_name = file_uploaded.name
        job.message = 'inserting upload/vflow interface'
        job.save(using='megavideo')

        LOGGER.debug('insider4')

        try:
            acall = AsyncCall(conf['dispatch'], conf['tv_name'], channel_id = chan_id)

            kargs = {
                    'metadatas' :-1, #create metadatas from scratch
                    'transcode' : True,
                    'keep_video' : True,
                    'chan_id' : chan_id,
                    'metas': r
                    }

            if 'publish' in settings.VFLOW_REC:
                kargs['publish'] = settings.VFLOW_REC['publish']

            if 'cat_id' in r:
                kargs['cat_id'] = r['cat_id']

            LOGGER.debug('Push video async ' + str(kargs))

            LOGGER.debug('insider5')

            acall.set_job(job)
            acall.set_insert(tmp, **kargs)
            acall.call()

            LOGGER.debug('after calling')

        except StandardError, e:
            LOGGER.debug('error : ')
            LOGGER.debug(str(e))


        if 'redirect' in request.REQUEST:
            return HttpResponseRedirect(request.channel_url + 'manager/jobs/%d/' % (job.id))
        #return HttpResponse( str(job.id) )
        msg = {'error' : 0, 'job' : job.id}
        return HttpResponse(json.dumps(msg), mimetype = 'application/json')

    msg = {'error' : 1, 'job' : 0}

    return HttpResponse(json.dumps(msg), mimetype = 'application/json')


def upload(request):
    """ old """

    LOGGER.debug('upload starts ' + str(request.FILES.keys()))
    LOGGER.debug('before')
    r = {}

    if 'cat_id' in request.REQUEST:
        cat_id = request.REQUEST['cat_id']
    else:
        cat_id = 1

    r = {'name' : '', 'description' : ''}
    for i in ['name', 'description', 'author']:
        if i in request.POST:
            r[i] = request.POST[i]

    LOGGER.debug('receive post')

    if 'Filedata' in request.FILES:
        LOGGER.debug('insider')

        file_uploaded = request.FILES['Filedata']
        if r['name'] == '':
            r['name'] = file_uploaded.name

        conf = settings.MEGAVIDEO_CONF
        tmp = tempfile.mktemp('_' + conf['tv_name'])
        tmp = conf['tmp'] + os.path.basename(tmp)
        fd = open(tmp, 'wb')

        LOGGER.debug('opened')

        for chunk in file_uploaded.chunks():
            fd.write(chunk)
        fd.close()

        LOGGER.debug('insider3')

        job = Job()
        job.ip = request.META['REMOTE_ADDR']
        job.status = 'A'
        job.original_name = file_uploaded.name
        job.message = 'inserting upload/vflow interface'
        job.channel = chan.id
        job.save(using='megavideo')

        LOGGER.debug('insider4')
        try:
            acall = AsyncCall(conf['dispatch'], conf['tv_name'], channel_id = chan.id)

            chan = request.session.get('channel')
            kargs = {
                    'metadatas' :-1, #create metadatas from scratch
                    'transcode' : True,
                    'keep_video' : True,
                    'chan_id' : chan.id,
                    'metas': r
                    }

            if cat_id:
                kargs['cat_id'] = cat_id
            LOGGER.debug('insider5')

            acall.set_job(job)
            acall.set_insert(tmp, **kargs)
            acall.call()

            LOGGER.debug('after calling')

        except StandardError, e:
             LOGGER.debug(str(e))


        if 'redirect' in request.REQUEST:
            return HttpResponseRedirect('/manager/jobs/%d/' % (job.id))
        return HttpResponse(str(job.id))

    return HttpResponse(str(False))
