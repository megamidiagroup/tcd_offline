# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import Library
from django.conf import settings

 
register  = Library()

@register.inclusion_tag('templatetags/keyboard.html')
def set_keyboard(get_tipo_template, target='', clear=0, classe='keyboard0'):
    
    p = {}
    p['get_tipo_template'] = get_tipo_template
    p['STATIC_URL']        = settings.STATIC_URL
    p['target']            = target
    p['clear']             = clear
    p['classe']            = classe

    return p


@register.inclusion_tag('templatetags/keyboard_buttom.html')
def set_keyboard_buttom(get_tipo_template, css='', classe='keyboard0'):

    p = {}
    p['get_tipo_template'] = get_tipo_template
    p['STATIC_URL']        = settings.STATIC_URL
    p['css']               = css
    p['classe']            = classe

    return p