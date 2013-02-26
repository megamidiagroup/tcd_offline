# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import Library
from django.conf import settings

from datetime import datetime as dt

register = Library()


@register.filter()
def get_days(date, now=None):
    
    if not now:
        now = dt.now()
        
    data = (now - date)
    
    return '%s dias' % data.days