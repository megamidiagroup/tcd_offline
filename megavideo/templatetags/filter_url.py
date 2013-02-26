from django.template import Library
from django.template import Context, Template

register = Library()

import re

@register.filter
def show_url(value):
    a = re.compile('(?P<url>http://.[^\ ]*)')
    b = value
    return a.sub('<a href=\'\g<url>\' target="_blank">&gt; link</a>'  , b)

@register.filter
def clear_url(url1 = '', url2 = ''):
    """
        Remove '//' from URLs 
    """
    url = ''.join([url1, url2]).replace('//', '/')
    return url

@register.filter
def crop_page(url):
    links = ['page', 'add' , 'update' , 'info' , 'preroll' , 'publicity' , 'tag' , 'list']
    if url:
        for i in links:
            if i in url:
                url = url.split(i)[0]

        return url
