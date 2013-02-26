# -*- coding: utf-8 -*-

from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime
import settings

register = template.Library()

def number2time(value):
    format = '%H:%M:%S'

    min = int(value / 60)
    sec = int(value % 60)

    changeTime = '%.2d:%.2d' % (min, sec)

    return changeTime


def time2number(time):
    """ in human, out float """

    arr = time.split(':')

    min = int(arr[0])
    sec = int(arr[1])

    timer = (min * 60) + sec

    return timer


def is_in(value, list):
    if value in list:
        return True
    else:
        return False


def strip_tag(value):
    if value:
        if value[0] == '"':
            value = value[1:]

        if value[-1] == '"':
            value = value[:-1]

    return value


def is_channel(value, user):
    for i in value.userchannel_set.all():
        if user in i.user.username:
            return True
    return False

def crop_str(value, num=1):
    return value[0:int(num)]

def tagfilter(list, filtro='T'):
    if filtro == 'T':#todas
        return list.order_by('-id')
    elif filtro == 'P':#pontual
        return list.exclude(initime=0.0).order_by('tags')
    elif filtro == 'I':#inteira
        return list.filter(initime=0.0).order_by('tags')
    else:
        return []

def get_meta(video, name, limit=0):
    try:
        value = video.get_meta(name)
    except:
        value = ''
    if limit != 0:
        value = value[0:limit]
    return value


def get_embed(video, xy='640x360'):

    xy = xy.split('x')

    base_url = settings.MEGAVIDEO_CONF['base_url']

    try:
        str = "<object width=\"" + xy[0] + "\" height=\"" + xy[1] + "\">"
        str += "<param name=\"movie\" value=\"" + unicode(base_url) + "static/portal/swf/megaplayer.swf?idContent=" + unicode(video.id) + "&playAuto=false&base_url=" + unicode(base_url) + "\"></param>"
        str += "<param name=\"allowFullScreen\" value=\"true\"></param>"
        str += "<param name=\"allowscriptaccess\" value=\"always\"></param>"
        str += "<embed src=\"" + unicode(base_url) + "static/portal/swf/megaplayer.swf?idContent=" + unicode(video.id) + "&playAuto=false&base_url=" + unicode(base_url) + "\" type=\"application/x-shockwave-flash\" allowscriptaccess=\"always\" allowfullscreen=\"true\" width=\"" + xy[0] + "\" height=\"" + xy[1] + "\"></embed>"
        str += "</object>"
    except:
        str = ""

    return str


def zero_left(str, quant=0):

    num = int(str)
    q = int(quant)

    if q:
        if num <= 9:
            return '0' * q + unicode(num)

    return str


@register.filter
def date_time(value):
    try:
        r = value.day
    except:
        r = value

    return r

register.filter('crop_str', crop_str)
register.filter('strip_tag', strip_tag)
register.filter('is_channel', is_channel)
register.filter('is_in', is_in)
register.filter('number2time', number2time)
register.filter('tagfilter', tagfilter)
register.filter('get_meta', get_meta)
register.filter('get_embed', get_embed)
register.filter('zeroleft', zero_left)
