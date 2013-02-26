# -*- coding: utf-8 -*-
from django.template import Library
from django.template import Context, Template

register = Library()


@register.filter
def number2time(value):
    try:
        value = int(value)
    except RuntimeError, e:
        return '00:00'

    min = int(value / 60)
    sec = int(value % 60)
    changeTime = '%.2d:%.2d' % (min, sec)

    return changeTime

@register.filter
def time2number(time):
    """ in human, out float """
    arr = time.split(':')
    min = int(arr[0])
    sec = int(arr[1])
    timer = (min * 60) + sec
    return timer
