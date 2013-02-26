# -*- coding: utf-8 -*-
#django
from django.template import Library
from django.conf import settings
from django.template import defaultfilters

register = Library()

@register.filter
def hasin(lib, value):
    try:
            if value in lib:
                return True
            return False
    except:
            return False


@register.filter
def return_selected(lib, value):
    if hasin(lib, value):
        return ' selected '
    return ''

@register.filter
def lt(value, lt):
    if int(value) < int(lt):
        return True
    return False


@register.filter
def lte(value, lt):
    if int(value) <= int(lt):
        return True
    return False


@register.filter
def gt(value, gt):
    if int(value) > int(gt):
        return True
    return False


@register.filter
def gte(value, gt):
    if int(value) >= int(gt):
        return True
    return False
