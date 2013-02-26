#!/usr/bin/python
# -*- coding: utf-8 -*-

from ofc import *
import random
import datetime
import urllib
from megavideo.video.models import *


# django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Library
from django.contrib.auth import authenticate
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.files import File
from django.core.cache import cache
from django.template.loader import render_to_string
from django.template import defaultfilters
from django.db.models import Q , Count, Sum
from django.template.defaultfilters import slugify
from django.template import RequestContext

#python
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
from urlparse import urlparse
from xml.dom.minidom import Document
from datetime import datetime, timedelta
from xml.dom.minidom import Document
from hashlib import md5

# Import lib
from thumb    import *
from menu     import *
from video    import *

#DiggPaginator
from megavideo.common.DiggPaginator import *
from megavideo.common.login import login_required

#Vflow
from megavideo.common.channel import *
from megavideo.manager.models import *
from megavideo.video.models import *
from megavideo.async.call             import AsyncCall
#from megavideo.compatibility.models   import Menu, Menucategory
from megavideo.common.dlog import LOGGER
from megavideo.video.views   import get_absolute_url

from megavideo.manager.views import  hot_videos, _main_stats
from megavideo.api.traffic import get_traffic

from megavideo.statistics.models import VisitorAction, VisitorLog, Visitor, Location, VisitorDomain# , Update
#from megavideo.statistics.views import *

#import simplejson
MEGAVIDEO_CONF = settings.MEGAVIDEO_CONF
OBJECT_TYPE = MEGAVIDEO_CONF['object_type']
base_url = MEGAVIDEO_CONF['base_url']

months = {'Jan':1, 'Fev':2, 'Mar':3, 'Abr':4, 'Mai':5, 'Jun':6, 'Jul':7, 'Ago':8, 'Set':9, 'Out':10, 'Nov':11, 'Dez':12 }


def get_visitorlog(select_month=False, channel_name='White', video_id=0):
    today = False;
    select_year = datetime.datetime.now().year

    if not select_month:
        select_month = datetime.datetime.now().month
        today = datetime.datetime.now().day

    if today:

        if not video_id:
            vdown = VisitorLog.objects.using('megavideo').filter(event_time__month=select_month, event_time__year=select_year , event_time__day=today , channel__name=channel_name).extra(select={'mdata':'HOUR(event_time)'}).values("mdata").annotate(total_download=Count('id')).order_by('event_time')[0:31]
        else:
            vdown = VisitorLog.objects.using('megavideo').filter(video__id=video_id, event_time__month=select_month, event_time__year=select_year , event_time__day=today , channel__name=channel_name).extra(select={'mdata':'HOUR(event_time)'}).values("mdata").annotate(total_download=Count('id')).order_by('event_time')[0:31]


        arydown = [i for i in vdown]
        myDates = [i['mdata'] for i in arydown]

        for x in range(0, 24):
            if not x in myDates:
                arydown.append({'mdata': x , 'total_download':0 })

        arydown.sort()

        return arydown

    else:

        if not video_id:
            vdown = VisitorLog.objects.using('megavideo').filter(event_time__month=select_month, event_time__year=select_year, channel__name=channel_name).extra(select={'mdata':'DATE(event_time)'}).values("mdata").annotate(total_download=Count('id')).order_by('event_time')[0:31]
        else:
            vdown = VisitorLog.objects.using('megavideo').filter(video__id=video_id, event_time__month=select_month, event_time__year=select_year, channel__name=channel_name).extra(select={'mdata':'DATE(event_time)'}).values("mdata").annotate(total_download=Count('id')).order_by('event_time')[0:31]

    return vdown


def get_visitordownload(channel_name='Whitelabel'):
    this_month = datetime.datetime.now().month
    today = datetime.datetime.now().day

    vdown = VisitorDownload.objects.using('megavideo').filter(time__month=this_month, time__day=today , channel__name=channel_name).extra(select={'mdata':'HOUR(time)'}).values("mdata").annotate(total_download=Count('id')).order_by('-event_time')

    if not vdown:
        vdown = VisitorDownload.objects.using('megavideo').filter(channel__name=channel_name).extra(select={'mdata':'HOUR(time)'}).values("mdata").annotate(total_download=Count('id')).order_by('-event_time')[0:11]

    return vdown


def get_meses(channel_name='portal'):
    this_year = datetime.datetime.today().year
    mdata = VisitorLog.objects.using('megavideo').filter(channel__name=channel_name, event_time__year=this_year).extra(select={'mdata_mes':'MONTH(event_time)', 'mdata_ano':'YEAR(event_time)'}).values("mdata_mes", "mdata_ano").annotate(total_download=Count('id')).order_by('event_time')
    new_data = []
    for i in mdata:
        new_data.append(datetime.datetime.strptime(('%s-%s' % (i['mdata_ano'], i['mdata_mes'])) , '%Y-%m'))
    return new_data


@login_required
def index(request, video_id=0):
    """ pagina principal das statisticas """
    p = {}
    stat = {}
    mais = {}

    data1 = 0
    data2 = 0
    ind = 1

    p = menu_top(request)

    request.breadcrumbs('Geral', "javascript:void(0)")
    request.breadcrumbs(u'Estatísticas', request.channel_url + 'manager/statistic/')

    ms = _main_stats(Channel.objects.using('megavideo').get(name=request.channel_name))


    p['visitantes'] = {
                        'month' : str(ms['visitor_month'])
                        , 'year': str(ms['visitor'])
                       }

    p['tempo'] = {
                  'month' : str(ms['video_month'])
                  , 'year' : str(ms['video'])
                  }

    #data padrao
    hoje = datetime.datetime.now().date()
    tomorrow = hoje + datetime.timedelta(1, 0)
    yesterday = hoje - datetime.timedelta(1, 0)
    select_month = request.REQUEST.get('select_mont', 0)

    p['transferencia'] = get_traffic(project='wl', server='v6.vflow.com.br') #pegando portallabel

    p['statistics'] = stat
    p['today'] = hoje
    p['months'] = get_meses(request.channel_name)
    p['graphic'] = get_visitorlog(select_month, channel_name=request.channel_name, video_id=video_id)
    p['last_five'] = Video.objects.using('megavideo').all().order_by('-views')[0:5]
    p['graphic_name'] = 'h'

    if not video_id:

        p['domains'] = VisitorDomain.objects.using('megavideo').filter(visitorlog__isnull=False, \
                                                     visitorlog__event_time__month=hoje.month, \
                                                     visitorlog__event_time__year=hoje.year , \
                                                     visitorlog__channel__name=request.channel_name \
                                                     ).annotate(total_visitorlog=Count('visitorlog') \
                                                                ).values('total_visitorlog', 'domain'\
                                                                         ).order_by('-total_visitorlog')[0:5]

        return render_to_response('manager/statistics/report.html', p, context_instance=RequestContext(request))

    else:

        p['video'] = Video.objects.using('megavideo').get(id=video_id)
        p['domains'] = VisitorDomain.objects.using('megavideo').filter(visitorlog__isnull=False, \
                                                     visitorlog__event_time__month=hoje.month, \
                                                     visitorlog__event_time__year=hoje.year , \
                                                     visitorlog__channel__name=request.channel_name, \
                                                     visitorlog__video__id=video_id \
                                                     ).annotate(total_visitorlog=Count('visitorlog') \
                                                                ).values('total_visitorlog', 'domain'\
                                                                         ).order_by('-total_visitorlog')[0:5]

        return render_to_response('manager/statistics/info.html', p, context_instance=RequestContext(request))




def refresh_maps(request):
    p = {}
    select_month = request.REQUEST.get('month', 0)
    video_id = request.REQUEST.get('video_id', 0)

    if '/' in select_month:
        srtp = select_month.split('/')
        select_month = months.get(srtp[0], 0)
        select_year = srtp[1]
        p['graphic_name'] = ''
    else:
        select_month = months.get(select_month, 0)
        select_year = datetime.datetime.now().year

        if not select_month:
            p['graphic_name'] = 'h'


    p['graphic'] = get_visitorlog(select_month, channel_name=request.channel_name , video_id=video_id)


    return render_to_response('manager/statistics/gp_access.html', p, context_instance=RequestContext(request))


def refresh_maps_domain(request):
    p = {}
    select_month = request.REQUEST.get('month', 0)
    video_id = request.REQUEST.get('video_id', 0)

    if '/' in select_month:
        srtp = select_month.split('/')
        select_month = months.get(srtp[0], 0)
        select_year = srtp[1]
    else:
        select_month = months.get(select_month, datetime.datetime.now().month)
        select_year = datetime.datetime.now().year

    if not video_id:

        p['domains'] = VisitorDomain.objects.using('megavideo').filter(visitorlog__isnull=False, \
                                                     visitorlog__event_time__month=select_month, \
                                                     visitorlog__event_time__year=select_year , \
                                                     visitorlog__channel__name=request.channel_name \
                                                     ).annotate(total_visitorlog=Count('visitorlog')\
                                                                ).values('total_visitorlog', 'domain'\
                                                                         ).order_by('-total_visitorlog')[0:5]

    else:

        p['domains'] = VisitorDomain.objects.using('megavideo').filter(visitorlog__isnull=False, \
                                                     visitorlog__event_time__month=select_month, \
                                                     visitorlog__event_time__year=select_year , \
                                                     visitorlog__channel__name=request.channel_name, \
                                                     visitorlog__video__id=video_id \
                                                     ).annotate(total_visitorlog=Count('visitorlog') \
                                                                ).values('total_visitorlog', 'domain'\
                                                                         ).order_by('-total_visitorlog')[0:5]


    return render_to_response('manager/statistics/gp_domain.html', p, context_instance=RequestContext(request))




