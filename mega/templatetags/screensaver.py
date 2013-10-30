# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import Library
from django.conf import settings
from django.db.models import Q

from mega.models import *


register  = Library()

@register.inclusion_tag('templatetags/screensaver.html', takes_context=True)
def get_screensaver(context, rede=None):
    
    p = {}
    
    p['screensaver'] = None
    p['rede']        = rede
    p['is_login']    = False
    p['next']        = context['request'].path
    
    if p['next'].count('/login/') > 0:
        p['is_login'] = True
    
    if rede:
        is_offline = getattr(settings, 'OFFLINE', False)
        ss         = ScreenSaver.objects.filter( Q(visible = True) & Q(rede = rede) ).order_by('-date')
        if is_offline:
            ss     = ss.filter(is_offline = True)
        else:
            ss     = ss.filter(is_online  = True)

        if ss.count() > 0:
            ss = ss[0]
            if (p['is_login'] and ss.time_login > 0) or (not p['is_login'] and ss.time_full > 0):
                p['screensaver'] = ss

    return p