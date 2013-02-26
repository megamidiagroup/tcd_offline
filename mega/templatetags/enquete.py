# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import Library
from django.conf import settings
from django.db.models import Q, Count

# import de todos os models da aplicação
from django.db.models import get_apps, get_models
for app in get_apps(): 
    for model in get_models(app): 
        locals()[model.__name__] = model

 
register = Library()

@register.inclusion_tag('templatetags/enquete.html', takes_context=True)
def enquete(context, rede=None):
    
    context['list_enquete'] = Enquete.objects.filter( Q(visible = True), Q(rede = rede) ).order_by('-date')
    
    return context


@register.inclusion_tag('templatetags/grafico.html', takes_context=True)
def grafico(context, rede=None):
    
    context['list_enquete'] = Enquete.objects.filter( Q(visible = True), Q(rede = rede) ).order_by('-date')
    
    return context