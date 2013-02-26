# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.conf import settings

def get_mobile(request):
    
    user_agent, type = '', ''
    
    if request.META.has_key('HTTP_USER_AGENT'):
        user_agent = request.META['HTTP_USER_AGENT']
         
    if 'android' in user_agent.lower():
        type = 'Android'
        #print 'Android - %s' % request.flavour
        
    if 'iphone' in user_agent.lower():
        type = 'Iphone'
        #print 'Iphone - %s' % request.flavour
        
    if 'windows' in user_agent.lower():
        type = 'Windows'
        #print 'Windows - %s' % request.flavour

    return {'type': request.flavour, 'navegator': type}