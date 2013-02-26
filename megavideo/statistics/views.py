# -*- coding: utf-8 -*-

import re
import simplejson
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.conf import settings
from urlparse import urlparse
import pickle
import os
import os.path
import urllib
import base64
from models import *

#geo IP
from django.contrib.gis.utils import GeoIP
from django.db.models import Count

dominio_re = re.compile('http://(.[^/]*)(.*)')


def register_location(request):
     #recuperation ip 
     ip = request.META['REMOTE_ADDR']
     agent = request.META['HTTP_USER_AGENT']
     try:
         gi = GeoIP.open(settings.MEGAVIDEO_CONF['geoip_dat'], GeoIP.GEOIP_STANDARD)

         if ip == '127.0.0.1':
             gir = None
         else:
             gir = gi.record_by_addr(ip)
     except:
         gir = None

     print 'GEOIP ' , gir

     if gir != None:
         latitude = gir['latitude']
         longitude = gir['longitude']
         location = Location.objects.using('megavideo').filter(longitude=longitude).filter(latitude=latitude)

         #se ja existe alterar o counter e pegar a location
         if location.count() > 0:

             location = location[0]
             location.counter = int(location.counter) + 1
             location.save(using='megavideo')

         else: #criar location

             location = Location()
             latitude = gir['latitude']
             longitude = gir['longitude']

             try:
                 cityname = gir['city'].decode('latin1').encode('utf8')
             except:
                 cityname = ''

             countrycode = gir['country_code']
             countryname = gir['country_name'].decode('latin1').encode('utf8')

             location.latitude = latitude
             location.longitude = longitude
             location.city = LocationCity.objects.using('megavideo').get_or_create(name=cityname)[0]
             location.country = LocationCountry.objects.using('megavideo').get_or_create(name=contryname, code=contrycode)[0]
             location.counter = 1
             location.save(using='megavideo')

     else:
         location = None


     #creation de Visitor   
     visit = Visitor()
     visit.ip = VisitorIp.objects.using('megavideo').get_or_create(ip=ip)[0]
     visit.location = location
     visit.agent = VisitorAgent.objects.using('megavideo').get_or_create(agent=agent)[0]
     visit.save(using='megavideo')
     #add geo data
     visit.geo_register()

     request.COOKIES['visitor_id'] = visit.id

     return visit.id

def _filter_dominio(dominio):
    try:
        dominio = urllib.unquote(dominio)
    except:
        dominio = ''

    du = dominio_re.findall(dominio)

    try:
        real_dominio = du
        domi = { 'dominio': du[0][0] , 'link' : du[0][1]   }
    except:
        domi = { 'dominio': 'null' , 'link' : 'null'   }

    print '_FILTER_DOMINIO: ' , domi
    return domi


def click(request):

    video_key = request.REQUEST.get('videoId', '')
    action_name = request.REQUEST.get('action', 0)
    time = request.REQUEST.get('tempo', 0)
    dom = request.REQUEST.get('dom', 0)
    id = request.REQUEST.get('id', False)

    video_id = Video().deserialize( video_key )

    try:
        time = urllib.unquote(time)
    except:
        pass

    real_dominio = _filter_dominio(dom)

    dominio_id = request.COOKIES.get('dominio_id', 0)
    dominio_name = request.COOKIES.get('dominio_name', 0)

    if not dominio_id:
        #get_or_create
        mydominio = VisitorDomain.objects.using('megavideo').get_or_create(domain=real_dominio['dominio'])[0]
        dominio_id = request.COOKIES['dominio_id'] = mydominio.id
        request.COOKIES['dominio_name'] = mydominio.domain

    visitor_id = request.COOKIES.get('visitor_id' , 0)
    if not visitor_id:
       visitor_id = register_location(request)

    action_id = request.COOKIES.get('action_id'  , 0)
    ses_action = request.COOKIES.get('action_name', 0)

    if not action_id or ses_action != action_name:
        print 'CREATE ACTION ' , action_name
        action = VisitorAction.objects.using('megavideo').get_or_create(name=action_name)[0]
        action_id = request.COOKIES['action_id'] = action.id
        request.COOKIES['action_name'] = action.name

    vlog = VisitorLog()
    vlog.visitor_id = visitor_id
    vlog.video_id = int(video_id)
    vlog.url = VisitorUrl.objects.using('megavideo').get_or_create(url=real_dominio['link'])[0]

    try:
        vlog.channel = Video.objects.using('megavideo').get(pk=int(video_id)).channel_set.all()[0]
    except:
        vlog.channel = Channel.objects.using('megavideo').all()[0]

    vlog.action_id = action_id
    vlog.seek_video = time
    vlog.domain_id = dominio_id
    vlog.save(using='megavideo')

    print 'VLOG ' , vlog

    print 'COOKIES ' , request.COOKIES

    if id:
        action = "var d = document.getElementById('" + id + "');"
        action += "document.body.removeChild(d);"
    else:
        action = "ok";

    return HttpResponse(action)


def geoprocess(request):
#    channel_name = request.channel_name
    p = {}
    channel_name = 'portal'

    states = LocationRegion.objects.using('megavideo').filter(code='BR').order_by('state_name')
    action = VisitorAction.objects.using('megavideo').filter(name='play')

    months_choices = []
    visitorlogs_total = []
    table_line = []
    total_logs = [0 for i in range(0, 14)]


    year = datetime.datetime.today().year

    for j in states:

        total_log = 0
        visitorlogs_log = []
        months_choices = []

        for i in range(1, 13):
            months_choices.append(datetime.date(year, i, 1))

            if not total_logs[i]:
                total_log = VisitorLog.objects.using('megavideo').filter(event_time__month=i, action=action).extra(select={'mdata':'MONTH(event_time)'}).values("mdata").annotate(total=Count('id'))
                if total_log:
                    total_log = total_log[0]['total']
                else:
                    total_log = 0

                total_logs[i] = total_log

            vl = VisitorLog.objects.using('megavideo').filter(event_time__month=i , visitor__region=j, action=action).extra(select={'mdata':'MONTH(event_time)'}).values("mdata").annotate(total=Count('id'))
            if vl:
                visitorlogs_log.append([vl[0], {'total_log': total_logs[i]}])
            else:
                visitorlogs_log.append([vl, {'total_log': total_logs[i]}])


        table_line.append({'state_name':j.state_name , 'state_log':visitorlogs_log })


    #nao identificados
    visitorlogs_log = []
    for i in range(1, 13):
        vl = VisitorLog.objects.using('megavideo').filter(event_time__month=i , visitor__region__isnull=True, action=action).extra(select={'mdata':'MONTH(event_time)'}).values("mdata").annotate(total=Count('id'))
        if vl:
            visitorlogs_log.append([vl[0], {'total_log': total_logs[i]}])
        else:
            visitorlogs_log.append([vl, {'total_log': total_logs[i]}])
   #     visitorlog_log.append([vl[0], {'total_log': total_logs[i]}])

    table_line.append({'state_name': 'Nao identificado' , 'state_log':visitorlogs_log })

    visitor_log_total = VisitorLog.objects.using('megavideo').filter(action=action).extra(select={'mdata':'MONTH(event_time)'}).values("mdata").annotate(total=Count('id'))[0]
    p['visitorlogs_total'] = visitor_log_total

    p['months_choices'] = months_choices
    p['table_line'] = table_line
    p['total_logs'] = total_logs

    return render_to_response("statistics/table.html", p)

