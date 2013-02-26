# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import Library
from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.contrib.auth.models import User as UserAdmin
from django.template.defaultfilters import date as default_date

from mega.models import *

from datetime import datetime, timedelta

import base64
 
register = Library()


@register.filter()
def count_aluno(rede, user=None):
    
    ua = UserAdmin.objects.filter( Q(is_active = True), Q(is_staff = False), Q(is_superuser = False), Q(infouser__rede = rede), Q(infouser__visible = True) )
    
    if user and user.infouser.filial:
        return ua.filter(infouser__filial = user.infouser.filial).count()
    
    return ua.count()


@register.filter()
def count_treinamento(rede, user=None):
    
    t = Treinamento.objects.filter( Q(category__visible = True) & Q(visible = True) & Q(rede = rede) )
    
    if user and user.infouser.filial:
        return t.filter( Q(category__filial = user.infouser.filial )).count()
    
    return t.count()


@register.filter()
def date_last_user_access(rede, user=None):
    
    ua = UserAdmin.objects.filter( Q(is_active = True), Q(is_staff = False), Q(is_superuser = False), Q(infouser__rede = rede), Q(infouser__visible = True) ).order_by('-last_login')
    
    if user and user.infouser.filial:
        ua = ua.filter(infouser__filial = user.infouser.filial).order_by('-last_login')

    return u'%s (%s)' % ( default_date(ua[0].last_login, 'd/m/Y à\s H:i'), ua[0].username )


@register.filter()
def list_filial(rede, type='<br />'):
    
    f = [i.name.encode('utf8') for i in Filial.objects.filter( Q(visible = True), Q(rede = rede) ).order_by('name')]

    if type == '<br />':
        return ', <br />'.join(f)
    return ', '.join(f)


@register.filter()
def certificadorealizado(user, rede):
    
    parte = 0
    
    try:

        q     = [i.treinamento.id for i in Question.objects.filter( Q(rede = rede), Q(visible = True), Q(relatorioavalicao__isnull = False), Q(relatorioavalicao__user = user) ).distinct()]
        cs    = Certificado.objects.filter( Q(rede = rede), Q(visible = True) )
        cer   = cs.filter( Q(treinamento__id__in = q) ).distinct()
    
        for c in cer:
            count = c.treinamento.all().count()
            tr    = True
            for i in c.treinamento.all():
                tr = q.count(i.id) > 0 and tr
            if tr:
                parte += 1
            
    
        t = int((float(parte) / float(cs.count())) * 100)
    except:
        t = 0

    return str(t) + '%'


@register.filter()
def treinamentorealizado(user, rede):
    
    try:

        cert  = Certificado.objects.filter( Q(rede = rede), Q(visible=True) ).order_by('date')
        count = 0
    
        for i in cert:
            count += i.treinamento.filter(visible=True).count()
    
        ## ver essa parte está errado a lógica
        parte = RelatorioAvalicao.objects.filter( Q(rede = rede), Q(user = user) ).count()
    
        
        t = int((float(parte) / float(count)) * 100)
    except:
        t = 0

    return str(t) + '%'


@register.filter()
def counttreinamentorealizado(user, rede):

    try:
        ## ver essa parte está errado a lógica
        return RelatorioAvalicao.objects.filter( Q(rede = rede), Q(user = user) ).count()
    except:
        return 0