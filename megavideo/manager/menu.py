# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
import simplejson as json
from megavideo.video.models   import *
from megavideo.common.channel import *
from django.conf import settings
from lxml import etree
import os

menu_xml = settings.STATIC_ROOT + 'manager/menu.xml'

def find_xml(element, node , attrib, value):
    return element.findall('%s[%s="%s"]', (node, attirb, value))

def menu_top(request):
    
    p = {}
    e = etree.ElementTree()

    p['xml_menu']     = e.parse(menu_xml)
    p['user_channel'] = Channel.objects.using('megavideo').all().order_by('name')

    if not request.user.is_authenticated():
        p['user_channel'] = ''
        
    p['select_channel'] = ''

    try:
        for j in request.user.userchannel_set.all():
            p['select_channel'] = j.channel.name
            p['user_channel']   = ''
    except:
        pass

    #channel_url
    return p