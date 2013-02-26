# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Library
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.files import File
from django.core.cache import cache
from django.template.loader import render_to_string
from django.template import defaultfilters
from django.db.models import Q
from django.template.defaultfilters import slugify, linebreaks
from django.db.models import Count, Sum
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.mail import send_mail, EmailMessage
from django.template import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import resolve
from django.views.decorators.cache import never_cache

import time
import urllib
import pickle
import base64
import os
import os.path
import tempfile
import shutil
import Image
import simplejson as json
import random
import math

from hashlib import md5
from urlparse import urlparse
from xml.dom.minidom import Document
from datetime import datetime, timedelta
from urlparse import urlparse
from thumb import *
from menu import *
from category import *
from channel import *
from comment import *
from publicity import *
from tag import *
from user import *
from preroll import *

from megavideo.common.DiggPaginator import *
from megavideo.manager.models import *
from megavideo.video.models import *
from megavideo.async.call import AsyncCall
from megavideo.common.dlog import LOGGER
from megavideo.video.views import get_absolute_url
from megavideo.statistics.models import VisitorAction, VisitorLog, Visitor, Location, VisitorDownload # , Update
from megavideo.templatetags.extra_filter import number2time
from megavideo.templatetags.embeds import video_embed
from megavideo.common.login import login_required, set_login, del_login


def login_view(request):
    """ login de usuário """

    p = {}

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    create_pass = request.POST.get('createpass', 0)
    next = request.REQUEST.get('next', '')

    base_url = settings.MEGAVIDEO_CONF.get('base_url', '')

    if int(create_pass) == 1:

        email = request.POST.get('email', False)
        myuser = User.objects.using('megavideo').filter(email=email)

        if myuser and email:

            myuser = myuser[0]
            md5id  = md5(str(datetime.datetime.now())).hexdigest()[0:8]
            myuser.set_password(md5id)
            myuser.save(using='megavideo')

            content = '<h2>Pedido de nova senha</h2>'
            content += 'Usuário <b>%s</b> <br> ' % str(myuser.username)
            content += 'Sua nova senha é <b>%s</b> <br> ' % md5id
            content += 'Acesse: <a href="' + str(base_url) + 'manager/">MegaVideo Manager</a><br>'

            msg = EmailMessage('Recuperar de senha MegaVideo Manager', content, str(settings.MEGAVIDEO_CONF['email']), [myuser.email])
            msg.content_subtype = "html"
            msg.send()

            p['msg'] = 'Sua nova senha foi enviada para você em seu e-mail'

            return render_to_response('manager/login.html', p, context_instance=RequestContext(request))

        p['msg'] = 'E-mail não encontrado no sistema'

    else:

        if username:

            user = authenticate(username=username, password=password, db='megavideo')

            if user is not None:
                if user.is_active:
                    
                    set_login(request, user)

                    if user.is_superuser:
                        channel = settings.MEGAVIDEO_CONF['default_channel']
                    else:
                        try:
                            channel = user.userchannel_set.all()[0].channel.name
                        except:
                            channel = request.channel_name
                            if not channel:
                                channel = settings.MEGAVIDEO_CONF['default_channel']
                    # Redirect to a success page.
                    if next:
                        url = 'home/%s' % channel
                        return HttpResponseRedirect(base_url + url + next)
                    else:
                        return HttpResponseRedirect(base_url + 'home/%s/manager/program/' % channel)
                else:
                    # Return a 'disabled account' error message
                    p['msg'] = 'Conta desabilitada'
            else:
                # Return an 'invalid login' error message.
                p['msg'] = 'Login inválido'

    p['next'] = next

    return render_to_response('manager/login.html' , p, context_instance=RequestContext(request))


def logout_view(request):
    del_login(request)
    return HttpResponseRedirect(settings.MEGAVIDEO_CONF.get('base_url', '') + 'manager/')


#===============================================================================


per_page = 12
object_types = ['Video', 'Audio', 'Text']


@login_required
def hot_videos(request):

    d = datetime.datetime.now()

    channel_selected = request.channel_name
    video_chan = Video.objects.using('megavideo').filter(channel__name=request.channel_name)
    today = d.date()
    tomorrow = (d + datetime.timedelta(1, 0)).date()

    topvid = video_chan.filter(Q(visitordownload__time__gte=today) & Q(visitordownload__time__lt=tomorrow)).distinct().annotate(play_log=Count('visitorlog')).order_by('-play_log')[0:7]

    return topvid


@login_required
def index(request):
    #monta os menus
    p = menu_top(request)

    request.breadcrumbs('Geral', "")
    request.breadcrumbs('Painel', request.channel_url + 'manager/panel/')

    list_job = Job.objects.using('megavideo').all()
    category = Category.objects.using('megavideo').filter(channel__name=request.channel_name)
    video    = Video.objects.using('megavideo').filter(channel__name=request.channel_name).order_by('-date')
    comment  = VideoComment.objects.using('megavideo').filter(video__channel__name=request.channel_name)

    p['category_list_form'] = category.filter(parent__isnull=True).order_by('-id')

    p['last_videos'] = video.filter().order_by('-id').distinct()[0:10]
    p['last_uploads'] = video.filter(videocategory__isnull=True).order_by('-date').distinct()

    p['last_comments'] = comment.all().order_by('-id').distinct()[0:5]
    p['total_videos'] = video.filter().count()
    p['total_hours'] = int(sum(i.duration for i in video.all()) / 3600)
    p['total_category'] = category.filter(published=True).count()
    p['total_tags'] = VideoTag.objects.using('megavideo').filter(video__channel__name=request.channel_name).count()
    p['total_comment'] = comment.count()

    #p['hot_videos'] = Video.objects.using('megavideo').filter(visitorlog__action__name = 'play').filter(visitorlog__event_time__gte = datetime.datetime.now() - datetime.timedelta(0, 4 * 3600)).annotate(play = Count('visitorlog')).order_by('-play')[0:5]
    p['hot_videos'] = hot_videos(request)
    ms = _main_stats(Channel.objects.using('megavideo').get(name=request.channel_name))

    stat = [
            {
                  'titulo'      : 'Visitantes no canal'
                , 'etiqueta'    : 'Mês'
                , 'valor'       : str(ms['visitor_month'])
                , 'title_total' : 'Total'
                , 'total'       : str(ms['visitor'])
            }
          , {
                  'titulo'      : 'Vídeos visualizados'
                , 'etiqueta'    : 'Mês atual'
                , 'valor'       : str(ms['video_month'])
                , 'title_total' : 'Total'
                , 'total'       : str(ms['video'])
            }
          , {
                  'titulo'      : 'Número de vídeos'
                , 'etiqueta'    : ''
                , 'valor'       : str(video.count())
                , 'title_total' : ''
                , 'total'       : ''
            }
    ]

    p['statistics'] = stat
    p['channel']    = Channel.objects.using('megavideo').get(name=request.channel_name)

    p['vflow_plan'] = settings.VFLOW_PLAN.get('basico', {'data':'100GB','transfer':'170GB'})

    return render_to_response('manager/admin.html', p, context_instance=RequestContext(request))


#===============================================================================

@login_required
def flashimport(request):
    #monta os menus
    p = menu_top(request)
    p['extra_css'] = 'portal_background'

    request.breadcrumbs('Geral', "javascript:void(0)")
    request.breadcrumbs(u'Inserção de vídeos ', request.channel_url + 'manager/import/')

    p['url_setting'] = settings.MEGAVIDEO_CONF['base_url'][:-1]

    list_job = Job.objects.using('megavideo').all()

    p['job'] = list_job.exclude(status='F').filter(channel__name=request.channel_name)
    p['job_end'] = list_job.filter(channel__name=request.channel_name, status='F').order_by('-date')[0:5]

    p['list_job'] = render_to_string('manager/import/list_job.html', p, context_instance=RequestContext(request))

    return render_to_response('manager/import/form.html', p, context_instance=RequestContext(request))


#===============================================================================

def _main_stats(channel=None):
    now = datetime.datetime.now()
    month = datetime.datetime(now.year, now.month, 1)

    action_play = VisitorAction.objects.using('megavideo').get_or_create(name='play')[0]
    flash_web = Transcode.objects.using('megavideo').get_or_create(name='FlashWeb')[0]

    datas = {}

    if channel:
        datas['visitor_month'] = Visitor.objects.using('megavideo').filter(visitorlog__channel=channel, visitorlog__event_time__gte=month).distinct().count()
        datas['visitor'] = Visitor.objects.using('megavideo').filter(visitorlog__channel=channel).distinct().count()

        if not datas['visitor_month']:
            datas['visitor_month'] = 0

        if not datas['visitor']:
            datas['visitor'] = 0

        plays = VisitorDownload.objects.using('megavideo').filter(channel=channel)
        plays_month = VisitorDownload.objects.using('megavideo').filter(channel=channel, time__gte=month)
        videos = Video.objects.using('megavideo').filter(channel=channel)
    else:
        datas['visitor_month'] = Visitor.objects.using('megavideo').filter(visitorlog__event_time__gte=month, visitorlog__action=action_play).distinct().count()
        datas['visitor'] = Visitor.objects.using('megavideo').filter().distinct().count()

        if not datas['visitor_month']:
            datas['visitor_month'] = 0

        if not datas['visitor']:
            datas['visitor'] = 0

        plays = VisitorDownload.objects.using('megavideo').all()
        plays_month = VisitorDownload.objects.using('megavideo').filter(time__gte=month)
        videos = Video.objects.using('megavideo').filter()


    datas['video_month'] = plays_month.count()
    datas['video'] = plays.count()

    s_month = plays_month.aggregate(soma=Sum('total_time'))['soma']
    s = plays.aggregate(soma=Sum('total_time'))['soma']

    if not s_month:
        s_month = 0

    if not s:
        s = 0

    datas['horas_month'] = '%.2dh%.2dm%.2ds' % (int(s_month / 3600), int(s_month % 3600 / 60), int(s_month % 60))
    datas['horas'] = '%.2dh%.2dm%.2ds' % (int(s / 3600), int(s % 3600 / 60), int(s % 60))

    datas['transfert'] = plays.aggregate(soma=Sum('size'))['soma']
    datas['transfert_month'] = plays_month.aggregate(soma=Sum('size'))['soma']
    datas['size'] = videos.aggregate(soma=Sum('total_size'))['soma']

    list_videos = videos.filter(date__gte=month)

    if list_videos.count() > 0:
        datas['size_month'] = list_videos.aggregate(soma=Sum('total_size'))['soma']
    else:
        datas['size_month'] = 0

    if not datas['transfert']:
        datas['transfert'] = 0

    if not datas['transfert_month']:
        datas['transfert_month'] = 0

    if not datas['size']:
        datas['size'] = 0

    return datas


@never_cache
def embed(request, item='audio'):

    if str(item) == 'audio':
        return render_to_response('manager/embed-audio.html')
    else:
        if str(item) == 'video':
            return render_to_response('manager/embed-video.html')


    return HttpResponse('Não existe o embed para template')


def ajax_register_bug(request):
    #from megavideo.api.mantis import Mantis
    p = {}

    bug_msg = request.REQUEST.get('bug_msg', 0)
    bug_url = request.REQUEST.get('bug_url', 0)
    bug_user = request.REQUEST.get('bug_user', 0)
    bug_channel = request.channel_name

    title = u'Registro de bug no manager - %s' % getattr('TV_NAME', 'settings', 'Megavideo')

    content = u"<b>Registro de bug</b> <br>\n"
    content += u"<b>URL:</b> %s <br>\n" % bug_url
    content += u"<b>Usuário:</b> %s <br>\n" % bug_user
    content += u"<b>Rede:</b> %s <br>\n" % bug_channel
    content += u"<p> %s </p> <br>\n" % linebreaks(bug_msg)

    msg = EmailMessage(title, content, str(settings.MEGAVIDEO_CONF['email']), [i[1] for i in settings.ADMINS])
    msg.content_subtype = "html"
    status = msg.send()

    if status:
        p['status'] = 0
        p['msg'] = 'Problema reportado com sucesso'
    else:
        p['status'] = 1
        p['msg'] = 'Erro ao reportar o problema'

    return HttpResponse(json.dumps(p), mimetype='application/json')


def get_media(request, user, key):
    """ download da media para os terminais offline dos restaurantes """
    
    access = False
    
    u = User.objects.using('megavideo').filter( Q(username = user) & Q(is_active = True) )
    
    if u.count() > 0:
        u = u[0]
        if u.check_password(key):
            access = True
            
    if not access:
        return HttpResponse('Sem permissão de acesso')
    
    channel = u.userchannel_set.all()[0].channel
    
    lista   = []
    
    for v in channel.video.all():
        for vt in v.videothumb_set.all():
            lista.append( settings.MEGAVIDEO_CONF.get('video_storage', '') + '/' + v.dir + '/' + 'thumb_' + vt.name )

    for v in channel.video.all():
        for vt in v.videotranscode_set.all():
            lista.append( settings.MEGAVIDEO_CONF.get('video_storage', '') + '/' + v.dir + '/' + 'transcoded_' + vt.name )
            
    local = '/home/redes/' + channel.name
    
    if os.path.isdir(local):
        shutil.rmtree(local)
        
    os.mkdir(local)
        
    for l in lista:
        
        dst = local + '/media/megavideo/storage/videos' + l.replace(settings.MEGAVIDEO_CONF.get('video_storage', ''), '')
        
        dir = os.path.dirname(dst)
        
        if not os.path.exists(dir):
            os.makedirs(dir)
        
        if not os.path.islink(dst):
            os.symlink(l, dst)
            
    o = open(local + '/crossdomain.xml', 'w+')
    o.write('<cross-domain-policy><allow-access-from domain="*"/></cross-domain-policy>')
    o.close()
    
    return HttpResponse(local)

