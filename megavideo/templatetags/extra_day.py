# -*- coding: utf-8 -*-

#django
from django.template import Library
from django.conf import settings
from django.template import defaultfilters
#vflow
from megavideo.video.models import *

register = Library()

def diffDays(obj_datetime):
    """ função para mostrar quanto tempo desde a data está relacionado """
    
    from datetime import datetime
    today = datetime.now()
    
    try:
        value = today - obj_datetime
    except:
        return "Erro: o objeto não é data!"   
    
    if int(value.days) > 1:
        return "Enviado há " + str(value.days) + " dias " 
    elif int(value.days) == 1:
        return "Enviado há " + str(value.days) + " dia"
    elif int(value.days) == 0:
        
        seconds  = float(value.seconds)
        minutes  = float(seconds) / 60
        minutos  = int(minutes)
        horas    = int(minutos / 60) 
        segundos = int( (minutes - minutos) * 60 )
        
        if segundos < 10:
            org_seg  = "0" + str(segundos)
        else:
            org_seg  = str(segundos)
                
        if horas > 1:
              return "Enviado há " + str(horas) + " horas"
        elif horas == 1:
              return "Enviado há " + str(horas) + " hora"
        elif horas == 0:
              return "Enviado há " + str( minutos ) + ":" + str(org_seg) + " minutos"
        
    return "Não é possível exibir!"  
        
        
register.filter('diffdays', diffDays)
