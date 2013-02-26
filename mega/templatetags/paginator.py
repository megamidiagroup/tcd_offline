# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import Library
from django.conf import settings
 
register = Library()

@register.inclusion_tag('templatetags/digg_paginator.html')
def digg_paginator(content, url):
    """ paginação """
    
    p = {'content_list' : content , 'url' : url}
    return p