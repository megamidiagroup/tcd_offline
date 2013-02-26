#-*- coding: utf8 -*-
#!/usr/bin/python 
from django.utils.http import urlquote
from django.conf import settings
import simplejson


def convert_to_utf8(value):
    """
       Converte caracteres
    """
    encodings = ('utf-8' , 'windows-1253', 'iso-8859-7', 'iso-8859-1', 'macgreek', 'latin1')

    for enc in encodings:
        try:
            f = value.decode(enc)
            return f
        except StandardError, e:
            print u'Erro ao usar o encode %s value: %s' % (enc , e)

    return value


def out_js(text):
    """
       Saída em js das informações
    """
    a = u''
    for i in text.splitlines():
        if len(i) > 0:
            a += u'document.write(%s);' % simplejson.dumps(i)
    return a


def remove_pagenumber(querystring, search):

     if search:
         querystring += u'?search=%s&page=' % search
     else:
         querystring += u'?page='

     return querystring


def convert_to_utf8(value):
    """
       Converte caracteres
    """
    encodings = ('utf-8' , 'windows-1253', 'iso-8859-7', 'iso-8859-1', 'macgreek', 'latin1')

    for enc in encodings:
        try:
            f = value.decode(enc)
            return f
        except StandardError, e:
            print u'Erro ao usar o encode %s value: %s' % (enc , e)

    return value
