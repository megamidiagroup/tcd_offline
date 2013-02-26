# -*- coding: utf-8 -*-

#django
from django.template import Library
import re
from templatetags.extra_filter import time2number

register = Library()

def points(texto):
    """ função para criar ponteiros em um texto '00:00' """
    
    try:
        
         r = re.compile(r'(?P<time>[0-9]+:[0-5][0-9])')
         texto = r.sub('<a href="javascript:void(0);" onclick="getTime(\'\\1\');" class="timecomment">\\1</a>', texto)
       
    except:
        pass
        
    return texto
   
register.filter('points', points)
