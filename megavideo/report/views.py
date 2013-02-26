# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.core.context_processors import request
from django.db.models import Q, Count, Sum , Max , Min
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.conf import settings

#vflow
from megavideo.video.models import *
from megavideo.statistics.models import *

import datetime
import urllib2
import simplejson
from django.http import HttpRequest

this_year = datetime.datetime.now().year
this_month = datetime.datetime.now().month
last_month = datetime.datetime.now().month - 1

def read_content(_project, _year = this_year, _month = this_month):
    open_to = 'http://adm.vflow.com.br/traffic/by_customer/in_json/%s/%d/%d/' % (_project, _year, _month)
    #print open_to
    _url = urllib2.urlopen(open_to)
    print 'URL ' , open_to
    try:
        _decode = simplejson.loads(_url.read())[0]
    except:
        _decode = False

    return _decode


def index(request):
    p = {}

    this_video = Video.objects.using('megavideo').filter(published = True, date__month = this_month).annotate(max_date = Max('date'), min_date = Min('date')).order_by('-views')[0:7]
    last_video = Video.objects.using('megavideo').filter(published = True, date__month = last_month).annotate(max_date = Max('date'), min_date = Min('date')).order_by('-views')[0:7]

    p['date_pub'] = datetime.datetime.now()

    p['group'] = []
    p['group'].append({ 'inicio' : this_video[0] , 'content' : this_video[1:7] , 'brandwidth' : read_content('tvsebrae', this_year, this_month) })
    p['group'].append({ 'inicio' : last_video[0] , 'content' : last_video[1:7] , 'brandwidth' : read_content('tvsebrae', this_year, last_month) })

    return render_to_response('report/base.html', p, context_instance = RequestContext(request))


def send_test(request):

    _email = request.REQUEST.get('email', 'valder@vflow.com.br')

    p = {}

    this_video = Video.objects.using('megavideo').filter(published = True, date__month = this_month).annotate(max_date = Max('date'), min_date = Min('date')).order_by('-views')[0:7]
    last_video = Video.objects.using('megavideo').filter(published = True, date__month = last_month).annotate(max_date = Max('date'), min_date = Min('date')).order_by('-views')[0:7]

    p['date_pub'] = datetime.datetime.now()

    p['group'] = []
    p['group'].append({ 'inicio' : this_video[0] , 'content' : this_video[1:7] , 'brandwidth' : read_content('tvsebrae', this_year, this_month) })
    p['group'].append({ 'inicio' : last_video[0] , 'content' : last_video[1:7] , 'brandwidth' : read_content('tvsebrae', this_year, last_month) })

    content = render_to_string('report/base.html', p, context_instance = RequestContext(request))

    msg = EmailMessage('Teste de relatório', content, 'valder@vflow.com.br', [_email])
    msg.content_subtype = "html"
    msg.send()

    rt = 'Mensagem enviada com sucesso - %s' % _email

    return HttpResponse(rt)
