# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.shortcuts import render_to_response, HttpResponse
from django.template.context import RequestContext
from django.template.defaultfilters import date as default_date
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User as UserAdmin
from django.utils.encoding import smart_str
from django.views.decorators.cache import cache_page

try:
    from django.core.validators import email_re
except:
    from django.forms.fields import email_re


from models import *
from mega.models import *
from mega.templatetags.relatorio import certificadorealizado, treinamentorealizado, counttreinamentorealizado, \
                                            count_aluno, count_treinamento, list_filial
from datetime import datetime, timedelta

import csv
import operator

### relatórios

def _prepare_vars_admin(request):

    p = {}

    p['rede']  = None
    p['user']  = request.user

    p['title'] = u'TCD - Plataforma de Treinamento e Comunicação a Distância'
    
    try:
        try:
            p['rede'] = Rede.objects.filter( Q(user = p['user']), Q(visible=True) )[0]
        except:
            ## protege contra falha de não incluir super cliente na rede.
            p['rede'] = p['user'].infouser.rede
            
        template  = Template.objects.filter( Q(rede = p['rede']), Q(visible=True) ).order_by('name')

        p['get_template'] = []
        p['get_tipo_template'] = 'mega'

        if template.count() > 0:
            p['get_template']      = template[0]
            p['get_tipo_template'] = template[0].tipo.name
    except:
        pass

    return p


@cache_page(settings.CACHES['default']['TIMEOUT'])
def alunocadastrado(request):

    p  = _prepare_vars_admin(request)

    ac = AlunoCadastrado()

    p['o']              = request.REQUEST.get('o'               , 'username')
    p['ot']             = request.REQUEST.get('ot'              , 'asc')
    p['rede__exact']    = request.REQUEST.get('rede__exact'     , 0)
    p['filial__exact']  = request.REQUEST.get('filial__exact'   , 0)
    p['visible__exact'] = request.REQUEST.get('visible__exact'  , '')

    p['action']           = request.REQUEST.get('action'        , '')
    p['_selected_action'] = request.REQUEST.getlist('_selected_action')
    
    p['q']   = request.REQUEST.get('q'  , '')
    p['de']  = request.REQUEST.get('de' , '')
    p['ate'] = request.REQUEST.get('ate', '')

    p['result_list'] = UserAdmin.objects.filter( Q(is_superuser = False), Q(is_staff = False) )
    
    if len(p['q'].strip()) > 0:
        p['result_list'] = p['result_list'].filter( Q(first_name__in = p['q'].strip().split(' ')) | Q(last_name__in = p['q'].strip().split(' ')) | Q(username__icontains = p['q'].strip()) )
    
    if len(p['de']) >= 10:
        try:
            date = datetime.strptime(p['de'], '%d/%m/%Y')
            p['result_list'] = p['result_list'].filter( Q(infouser__date__gte = date) )
        except:
            pass
        
    if len(p['ate']) >= 10:
        try:
            date = datetime.strptime(p['ate'], '%d/%m/%Y') + timedelta(days=1)
            p['result_list'] = p['result_list'].filter( Q(infouser__date__lte = date) )
        except:
            pass

    if int(p['rede__exact']) > 0:
        p['result_list'] = p['result_list'].filter( Q(infouser__rede__id = int(p['rede__exact'])) )
    elif p['filial__exact'] == 'null':
        p['result_list'] = p['result_list'].filter( Q(infouser__filial__isnull = True) )
    elif int(p['filial__exact']) > 0:
        p['result_list'] = p['result_list'].filter( Q(infouser__filial__id = int(p['filial__exact'])) )
    elif p['visible__exact'] != '':
        p['result_list'] = p['result_list'].filter( Q(is_active = bool(int(p['visible__exact']))) )

    p['result_list'] = p['result_list'].order_by('%s' % p['o'])

    if p['action'] == 'export_selected':

        p['result_list'] = p['result_list'].filter( Q(id__in = p['_selected_action']) ).order_by('%s' % p['o'])

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=relatorio_alunos_cadastrados_%s.csv' % (default_date(datetime.now(), 'd_m_Y'))

        writer = csv.writer(response)
        writer.writerow(['Nome', 'Usuário', 'Rede', 'E-mail', 'Filial', 'Data de Cadastro', 'Habilitado'])

        for i in p['result_list']:
            res    = u'Não'
            filial = u'(nenhum)'
            if i.is_active:
                res    = u'Sim'
            if i.infouser.filial:
                filial = i.infouser.filial.name
            list = ['%s' % i.get_full_name(), '%s' % i.username, '%s' % i.infouser.rede.name, '%s' % i.email, '%s' % filial, '%s' % default_date(i.infouser.date, 'd/m/Y'), '%s' % res]
            writer.writerow( list )

        ac.set_extrato(p)

        return response


    p['list_rede']   = Rede.objects.filter( Q(visible=True) ).order_by('name')
    p['list_filial'] = Filial.objects.filter( Q(visible=True) ).order_by('name')

    if not request.user.is_superuser:
        rede             = request.user.rede_set.filter( Q(visible=True) )
        p['list_rede']   = Rede.objects.filter( Q(user = request.user) ).order_by('name')
        p['list_filial'] = Filial.objects.filter( Q(rede__user = request.user) ).order_by('name')
        p['result_list'] = p['result_list'].filter( (Q(is_superuser = False) & Q(username = request.user.username)) | (Q(is_superuser = False) & Q(infouser__rede__in = rede)) )
        
    if request.rede:
        p['list_rede']   = None
        p['list_filial'] = Filial.objects.filter( Q(rede = request.rede) ).order_by('name')
        p['result_list'] = p['result_list'].filter( Q(infouser__rede = request.rede) )

    ac.set_acesso(p)

    return render_to_response('relatorio/alunocadastrado.html', p, context_instance=RequestContext(request))


@cache_page(settings.CACHES['default']['TIMEOUT'])
def alunocertificado(request, rede=None):

    p  = _prepare_vars_admin(request)

    ac = AlunoCertificado()

    p['o']              = request.REQUEST.get('o'               , 'username')
    p['ot']             = request.REQUEST.get('ot'              , 'asc')
    p['rede__exact']    = request.REQUEST.get('rede__exact'     , 0)
    p['filial__exact']  = request.REQUEST.get('filial__exact'   , 0)
    p['visible__exact'] = request.REQUEST.get('visible__exact'  , '')

    p['action']           = request.REQUEST.get('action'        , '')
    p['_selected_action'] = request.REQUEST.getlist('_selected_action')
    
    p['q']   = request.REQUEST.get('q'  , '')
    p['de']  = request.REQUEST.get('de' , '')
    p['ate'] = request.REQUEST.get('ate', '')

    p['result_list'] = UserAdmin.objects.filter( Q(is_superuser = False), Q(is_staff = False) )
    
    if len(p['q'].strip()) > 0:
        p['result_list'] = p['result_list'].filter( Q(first_name__in = p['q'].strip().split(' ')) | Q(last_name__in = p['q'].strip().split(' ')) | Q(username__icontains = p['q'].strip()) )
    
    if len(p['de']) >= 10:
        try:
            date = datetime.strptime(p['de'], '%d/%m/%Y')
            p['result_list'] = p['result_list'].filter( Q(infouser__date__gte = date) )
        except:
            pass
        
    if len(p['ate']) >= 10:
        try:
            date = datetime.strptime(p['ate'], '%d/%m/%Y') + timedelta(days=1)
            p['result_list'] = p['result_list'].filter( Q(infouser__date__lte = date) )
        except:
            pass

    if int(p['rede__exact']) > 0:
        p['result_list'] = p['result_list'].filter( Q(infouser__rede__id = int(p['rede__exact'])) )
    elif p['filial__exact'] == 'null':
        p['result_list'] = p['result_list'].filter( Q(infouser__filial__isnull = True) )
    elif int(p['filial__exact']) > 0:
        p['result_list'] = p['result_list'].filter( Q(infouser__filial__id = int(p['filial__exact'])) )
    elif p['visible__exact'] != '':
        p['result_list'] = p['result_list'].filter( Q(is_active = bool(int(p['visible__exact']))) )

    p['result_list'] = p['result_list'].order_by('%s' % p['o'])

    if p['action'] == 'export_selected':

        p['result_list'] = p['result_list'].filter( Q(id__in = p['_selected_action']) ).order_by('%s' % p['o'])

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=relatorio_alunos_certificados_%s.csv' % (default_date(datetime.now(), 'd_m_Y'))

        writer = csv.writer(response)
        writer.writerow(['Nome', 'Usuário', 'Rede', 'Filial', 'Certificados realizados (%)', 'Aproveitamento (%)', 'Habilitado'])

        for i in p['result_list']:
            res    = u'Não'
            filial = u'(nenhum)'
            if i.is_active:
                res    = u'Sim'
            if i.infouser.filial:
                filial = i.infouser.filial.name
            list = ['%s' % i.get_full_name(), '%s' % i.username, '%s' % i.infouser.rede.name, '%s' % filial, '%s' % certificadorealizado(i, i.infouser.rede), '%s' % treinamentorealizado(i, i.infouser.rede), '%s' % res]
            writer.writerow( list )

        ac.set_extrato(p)

        return response


    p['list_rede']   = Rede.objects.filter( Q(visible=True) ).order_by('name')
    p['list_filial'] = Filial.objects.filter( Q(visible=True) ).order_by('name')

    if not request.user.is_superuser:
        rede             = request.user.rede_set.filter( Q(visible=True) )
        p['list_rede']   = Rede.objects.filter( Q(user = request.user) ).order_by('name')
        p['list_filial'] = Filial.objects.filter( Q(rede__user = request.user) ).order_by('name')
        p['result_list'] = p['result_list'].filter( (Q(is_superuser = False) & Q(username = request.user.username)) | (Q(is_superuser = False) & Q(infouser__rede__in = rede)) )
        
    if request.rede:
        p['list_rede']   = None
        p['list_filial'] = Filial.objects.filter( Q(rede = request.rede) ).order_by('name')
        p['result_list'] = p['result_list'].filter( Q(infouser__rede = request.rede) )

    ac.set_acesso(p)

    return render_to_response('relatorio/alunocertificado.html', p, context_instance=RequestContext(request))


@cache_page(settings.CACHES['default']['TIMEOUT'])
def treinamentoconcluido(request, rede=None):

    p  = _prepare_vars_admin(request)

    tc = TreinamentoConcluido()

    p['o']              = request.REQUEST.get('o'               , 'username')
    p['ot']             = request.REQUEST.get('ot'              , 'asc')
    p['rede__exact']    = request.REQUEST.get('rede__exact'     , 0)
    p['filial__exact']  = request.REQUEST.get('filial__exact'   , 0)
    p['visible__exact'] = request.REQUEST.get('visible__exact'  , '')

    p['action']           = request.REQUEST.get('action'        , '')
    p['_selected_action'] = request.REQUEST.getlist('_selected_action')
    
    p['q']   = request.REQUEST.get('q'  , '')
    p['de']  = request.REQUEST.get('de' , '')
    p['ate'] = request.REQUEST.get('ate', '')

    p['result_list'] = UserAdmin.objects.filter( Q(is_superuser = False), Q(is_staff = False) )
    
    if len(p['q'].strip()) > 0:
        p['result_list'] = p['result_list'].filter( Q(first_name__in = p['q'].strip().split(' ')) | Q(last_name__in = p['q'].strip().split(' ')) | Q(username__icontains = p['q'].strip()) )
    
    if len(p['de']) >= 10:
        try:
            date = datetime.strptime(p['de'], '%d/%m/%Y')
            p['result_list'] = p['result_list'].filter( Q(infouser__date__gte = date) )
        except:
            pass
        
    if len(p['ate']) >= 10:
        try:
            date = datetime.strptime(p['ate'], '%d/%m/%Y') + timedelta(days=1)
            p['result_list'] = p['result_list'].filter( Q(infouser__date__lte = date) )
        except:
            pass

    if int(p['rede__exact']) > 0:
        p['result_list'] = p['result_list'].filter( Q(infouser__rede__id = int(p['rede__exact'])) )
    elif p['filial__exact'] == 'null':
        p['result_list'] = p['result_list'].filter( Q(infouser__filial__isnull = True) )
    elif int(p['filial__exact']) > 0:
        p['result_list'] = p['result_list'].filter( Q(infouser__filial__id = int(p['filial__exact'])) )
    elif p['visible__exact'] != '':
        p['result_list'] = p['result_list'].filter( Q(is_active = bool(int(p['visible__exact']))) )

    p['result_list'] = p['result_list'].order_by('%s' % p['o'])

    if p['action'] == 'export_selected':

        p['result_list'] = p['result_list'].filter( Q(id__in = p['_selected_action']) ).order_by('%s' % p['o'])

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=relatorio_treinamentos_concluidos_%s.csv' % (default_date(datetime.now(), 'd_m_Y'))

        writer = csv.writer(response)
        writer.writerow(['Nome', 'Usuário', 'Rede', 'Filial', 'Treinamentos Concluidos', 'Habilitado'])

        for i in p['result_list']:
            res    = u'Não'
            filial = u'(nenhum)'
            if i.is_active:
                res    = u'Sim'
            if i.infouser.filial:
                filial = i.infouser.filial.name
            list = ['%s' % i.get_full_name(), '%s' % i.username, '%s' % i.infouser.rede.name, '%s' % filial, '%s' % counttreinamentorealizado(i, i.infouser.rede), '%s' % res]
            writer.writerow( list )

        tc.set_extrato(p)

        return response


    p['list_rede']   = Rede.objects.filter( Q(visible=True) ).order_by('name')
    p['list_filial'] = Filial.objects.filter( Q(visible=True) ).order_by('name')

    if not request.user.is_superuser:
        rede             = request.user.rede_set.filter( Q(visible=True) )
        p['list_rede']   = Rede.objects.filter( Q(user = request.user) ).order_by('name')
        p['list_filial'] = Filial.objects.filter( Q(rede__user = request.user) ).order_by('name')
        p['result_list'] = p['result_list'].filter( (Q(is_superuser = False) & Q(username = request.user.username)) | (Q(is_superuser = False) & Q(infouser__rede__in = rede)) )
        
    if request.rede:
        p['list_rede']   = None
        p['list_filial'] = Filial.objects.filter( Q(rede = request.rede) ).order_by('name')
        p['result_list'] = p['result_list'].filter( Q(infouser__rede = request.rede) )

    tc.set_acesso(p)

    return render_to_response('relatorio/treinamentoconcluido.html', p, context_instance=RequestContext(request))


@cache_page(settings.CACHES['default']['TIMEOUT'])
def pontuacaoaluno(request, rede=None):

    p  = _prepare_vars_admin(request)

    pa = PontuacaoAluno()

    p['o']              = request.REQUEST.get('o'               , 'username')
    p['ot']             = request.REQUEST.get('ot'              , 'asc')
    p['rede__exact']    = request.REQUEST.get('rede__exact'     , 0)
    p['filial__exact']  = request.REQUEST.get('filial__exact'   , 0)
    p['visible__exact'] = request.REQUEST.get('visible__exact'  , '')

    p['action']           = request.REQUEST.get('action'        , '')
    p['_selected_action'] = request.REQUEST.getlist('_selected_action')
    
    p['q']   = request.REQUEST.get('q'  , '')
    p['de']  = request.REQUEST.get('de' , '')
    p['ate'] = request.REQUEST.get('ate', '')

    p['result_list'] = UserAdmin.objects.filter( Q(is_superuser = False), Q(is_staff = False) )
    
    if len(p['q'].strip()) > 0:
        p['result_list'] = p['result_list'].filter( Q(first_name__in = p['q'].strip().split(' ')) | Q(last_name__in = p['q'].strip().split(' ')) | Q(username__icontains = p['q'].strip()) )
    
    if len(p['de']) >= 10:
        try:
            date = datetime.strptime(p['de'], '%d/%m/%Y')
            p['result_list'] = p['result_list'].filter( Q(infouser__date__gte = date) )
        except:
            pass
        
    if len(p['ate']) >= 10:
        try:
            date = datetime.strptime(p['ate'], '%d/%m/%Y') + timedelta(days=1)
            p['result_list'] = p['result_list'].filter( Q(infouser__date__lte = date) )
        except:
            pass

    if int(p['rede__exact']) > 0:
        p['result_list'] = p['result_list'].filter( Q(infouser__rede__id = int(p['rede__exact'])) )
    elif p['filial__exact'] == 'null':
        p['result_list'] = p['result_list'].filter( Q(infouser__filial__isnull = True) )
    elif int(p['filial__exact']) > 0:
        p['result_list'] = p['result_list'].filter( Q(infouser__filial__id = int(p['filial__exact'])) )
    elif p['visible__exact'] != '':
        p['result_list'] = p['result_list'].filter( Q(is_active = bool(int(p['visible__exact']))) )

    p['result_list'] = p['result_list'].order_by('%s' % p['o'])

    if p['action'] == 'export_selected':

        p['result_list'] = p['result_list'].filter( Q(id__in = p['_selected_action']) ).order_by('%s' % p['o'])

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=relatorio_pontuacao_alunos_%s.csv' % (default_date(datetime.now(), 'd_m_Y'))

        writer = csv.writer(response)
        writer.writerow(['Nome', 'Usuário', 'Rede', 'Filial', 'Pontuação', 'Habilitado'])

        for i in p['result_list']:
            res    = u'Não'
            filial = u'(nenhum)'
            if i.is_active:
                res    = u'Sim'
            if i.infouser.filial:
                filial = i.infouser.filial.name
            list = ['%s' % i.get_full_name(), '%s' % i.username, '%s' % i.infouser.rede.name, '%s' % filial, '%s' % i.infouser.pontos, '%s' % res]
            writer.writerow( list )

        pa.set_extrato(p)

        return response


    p['list_rede']   = Rede.objects.filter( Q(visible=True) ).order_by('name')
    p['list_filial'] = Filial.objects.filter( Q(visible=True) ).order_by('name')

    if not request.user.is_superuser:
        rede             = request.user.rede_set.filter( Q(visible=True) )
        p['list_rede']   = Rede.objects.filter( Q(user = request.user) ).order_by('name')
        p['list_filial'] = Filial.objects.filter( Q(rede__user = request.user) ).order_by('name')
        p['result_list'] = p['result_list'].filter( (Q(is_superuser = False) & Q(username = request.user.username)) | (Q(is_superuser = False) & Q(infouser__rede__in = rede)) )
        
    if request.rede:
        p['list_rede']   = None
        p['list_filial'] = Filial.objects.filter( Q(rede = request.rede) ).order_by('name')
        p['result_list'] = p['result_list'].filter( Q(infouser__rede = request.rede) )

    pa.set_acesso(p)

    return render_to_response('relatorio/pontuacaoaluno.html', p, context_instance=RequestContext(request))


@cache_page(settings.CACHES['default']['TIMEOUT'])
def treinamentocadastrado(request, rede=None):

    p  = _prepare_vars_admin(request)

    tc = TreinamentoCadastrado()

    p['o']              = request.REQUEST.get('o'               , 'name')
    p['ot']             = request.REQUEST.get('ot'              , 'asc')
    p['filial__exact']  = request.REQUEST.get('filial__exact'   , 0)
    p['visible__exact'] = request.REQUEST.get('visible__exact'  , '')

    p['action']           = request.REQUEST.get('action'        , '')
    p['_selected_action'] = request.REQUEST.getlist('_selected_action')
    
    p['q']   = request.REQUEST.get('q'  , '')
    p['de']  = request.REQUEST.get('de' , '')
    p['ate'] = request.REQUEST.get('ate', '')

    p['result_list'] = Rede.objects.all().order_by('name')
    
    if len(p['q'].strip()) > 0:
        p['result_list'] = p['result_list'].filter( Q(name__in = p['q'].strip().split(' ')) | Q(link__in = p['q'].strip().split(' ')) )
    
    if len(p['de']) >= 10:
        try:
            date = datetime.strptime(p['de'], '%d/%m/%Y')
            p['result_list'] = p['result_list'].filter( Q(date__gte = date) )
        except:
            pass
        
    if len(p['ate']) >= 10:
        try:
            date = datetime.strptime(p['ate'], '%d/%m/%Y') + timedelta(days=1)
            p['result_list'] = p['result_list'].filter( Q(date__lte = date) )
        except:
            pass

    if p['filial__exact'] == 'null' and p['result_list']:
        p['result_list'] = p['result_list'][0].filter_not_filial(p['result_list'])
    elif int(p['filial__exact']) > 0 and p['result_list']:
        p['result_list'] = p['result_list'][0].filter_in_filial(int(p['filial__exact']))
    elif p['visible__exact'] != '':
        p['result_list'] = p['result_list'].filter( Q(visible = bool(int(p['visible__exact']))) )

    p['result_list'] = p['result_list'].order_by('%s' % p['o'])

    if p['action'] == 'export_selected':

        p['result_list'] = p['result_list'].filter( Q(id__in = p['_selected_action']) ).order_by('%s' % p['o'])

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=relatorio_treinamentos_cadastrados_%s.csv' % (default_date(datetime.now(), 'd_m_Y'))

        writer = csv.writer(response)
        writer.writerow(['Rede', 'Nº Alunos', 'Nº Treinamentos', 'Filiais', 'Data de criação', 'Habilitado'])

        for i in p['result_list']:
            res    = u'Não'
            if i.visible:
                res    = u'Sim'
            
            list = ['%s' % i.name, '%s' % count_aluno(i), '%s' % count_treinamento(i), '%s' % list_filial(i, '\n'), '%s' % i.date, '%s' % res]
            writer.writerow( list )

        tc.set_extrato(p)

        return response


    p['list_filial'] = Filial.objects.filter( Q(visible=True) ).order_by('name')

    if not request.user.is_superuser:
        redes            = [i.id for i in request.user.rede_set.filter( Q(visible=True) )]
        p['list_filial'] = Filial.objects.filter( Q(rede__user = request.user) ).order_by('name')
        p['result_list'] = p['result_list'].filter( Q(id__in = redes) )
        
    if request.rede:
        p['list_filial'] = Filial.objects.filter( Q(rede = request.rede) ).order_by('name')
        p['result_list'] = p['result_list'].filter( Q(id = request.rede.id) )

    tc.set_acesso(p)

    return render_to_response('relatorio/treinamentocadastrado.html', p, context_instance=RequestContext(request))


@cache_page(settings.CACHES['default']['TIMEOUT'])
def relatoriografico(request, rede=None):

    p  = _prepare_vars_admin(request)

    rg = RelatorioGrafico()

    p['rede_id'] = request.REQUEST.get('rede_id' , '')
    p['user_id'] = request.REQUEST.get('user_id' , '')
    p['de']      = request.REQUEST.get('de'      , '')
    p['ate']     = request.REQUEST.get('ate'     , '')
    p['m']       = request.REQUEST.get('m'       , '')
    
    redes        = None

    p['result_list_rede'] = Rede.objects.all().order_by('name')
    
    if not request.user.is_superuser:
        redes                 = [i.id for i in request.user.rede_set.filter( Q(visible=True) )]
        p['result_list_rede'] = p['result_list_rede'].filter( Q(id__in = redes) )
        
    if request.rede:
        p['result_list_rede'] = request.rede

    ############### --------------------- #######################
    
    tmp, tmp_acerto, tmp_erro, tmp_not, i = [], [], [], [], None
    
    q = Question.objects.all()
    
    if request.rede:
        p['rede_id'] = request.rede.id
    
    if p['rede_id'] and int(p['rede_id']) > 0:
        q = q.filter(rede__id = int(p['rede_id']))
        
    if not redes == None:
        q = q.filter(rede__id__in = redes)
        
    if len(p['de']) >= 10:
        try:
            date = datetime.strptime(p['de'], '%d/%m/%Y')
            q = q.filter( Q(date__gte = date) )
        except:
            pass
        
    if len(p['ate']) >= 10:
        try:
            date = datetime.strptime(p['ate'], '%d/%m/%Y') + timedelta(days=1)
            q = q.filter( Q(date__lte = date) )
        except:
            pass
    
    for i in q:
        if tmp.count(i.treinamento_id) == 0:
            retorno = i.treinamento.relatoriotentativa_set.all()
            if len(p['de']) >= 10:
                try:
                    date = datetime.strptime(p['de'], '%d/%m/%Y')
                    retorno = retorno.filter( Q(date__gte = date) )
                except:
                    pass
                
            if len(p['ate']) >= 10:
                try:
                    date = datetime.strptime(p['ate'], '%d/%m/%Y') + timedelta(days=1)
                    retorno = retorno.filter( Q(date__lte = date) )
                except:
                    pass
                
            if retorno.filter(aprovado = True):
                tmp_acerto.append(i.treinamento)
            elif retorno.filter(aprovado = False):
                tmp_erro.append(i.treinamento)
            else:
                tmp_not.append(i.treinamento)
            tmp.append(i.treinamento_id)     
    
    p['erros']      = len(tmp_erro)
    p['acertos']    = len(tmp_acerto)
    p['notfizeram'] = len(tmp_not)
    p['num_q']      = len(tmp)
    
    ra = RelatorioAcoes.objects.filter().order_by('complete')
    
    if p['rede_id'] and int(p['rede_id']) > 0:
        ra = ra.filter(rede__id = int(p['rede_id']))
        
    if not redes == None:
        ra = ra.filter(rede__id__in = redes)
    
    if len(p['de']) >= 10:
        try:
            date = datetime.strptime(p['de'], '%d/%m/%Y')
            ra   = ra.filter( Q(date__gte = date) )
        except:
            pass
        
    if len(p['ate']) >= 10:
        try:
            date = datetime.strptime(p['ate'], '%d/%m/%Y') + timedelta(days=1)
            ra   = ra.filter( Q(date__lte = date) )
        except:
            pass
    
    ############### --------------------- #######################
    
    tmp, list_grafico_acessos, r = [], [], None
    
    raa = ra
    
    if not len(p['de']) >= 10 and not len(p['ate']) >= 10:
        date = datetime.now() - timedelta(days=12)
        raa  = raa.filter( Q(date__gte = date) )

    for r in raa:
        data = default_date(r.date, 'Ymd')
        if tmp.count(data) == 0:
            list_grafico_acessos.append({'data':default_date(r.date, 'd/m'), 'count':1, 'id':data})
            tmp.append(data)
        else:
            for lga in list_grafico_acessos:
                if lga['id'] == data:
                    lga['count'] += 1
                    
    list_grafico_acessos = sorted(list_grafico_acessos, key=operator.itemgetter('id'))

    p['list_grafico_acessos'] = list_grafico_acessos
    
    ############### --------------------- #######################
    
    tmp, list_top_user, r = [], [], None
    
    for r in ra.filter(complete=True):
        if tmp.count(r.user_id) == 0:
            list_top_user.append({'object':r, 'count':1, 'id':r.user_id})
            tmp.append(r.user_id)
        else:
            for ltu in list_top_user:
                if ltu['id'] == r.user_id:
                    ltu['count'] += 1
                    
    list_top_user = sorted(list_top_user, key=operator.itemgetter('count'), reverse=True)

    if p['m'] and p['m'] == 'top_user':
        p['list_top_user'] = list_top_user
        return render_to_response('relatorio/relatoriograficotopuser.html', p, context_instance=RequestContext(request))
    
    p['list_top_user'] = list_top_user[0:10]
    
    p['mais_top_user'] = len(list_top_user) > len(p['list_top_user'])
    
    ################ ------------------------ ##################
    
    tmp, list_top_treinamento, r = [], [], None
    
    for r in ra:
        if tmp.count(r.video_id) == 0:
            list_top_treinamento.append({'object':r, 'count':1, 'id':r.video_id})
            tmp.append(r.video_id)
        else:
            for ltt in list_top_treinamento:
                if ltt['id'] == r.video_id:
                    ltt['count'] += 1
                    
    list_top_treinamento = sorted(list_top_treinamento, key=operator.itemgetter('count'), reverse=True)
    
    if p['m'] and p['m'] == 'top_treinamento':
        p['list_top_treinamento'] = list_top_treinamento
        return render_to_response('relatorio/relatoriograficotoptreinamento.html', p, context_instance=RequestContext(request))

    p['list_top_treinamento'] = list_top_treinamento[0:10]
    p['mais_top_treinamento'] = len(list_top_treinamento) > len(p['list_top_treinamento'])
    
    ################# -------------------------- ##################
    
    result_list_user      = UserAdmin.objects.filter( Q(is_active = True), Q(is_staff = False), Q(is_superuser = False) )
    
    if p['rede_id'] and int(p['rede_id']) > 0:
        result_list_user  = result_list_user.filter(infouser__rede__id = int(p['rede_id']))
        
    if not redes == None:
        result_list_user  = result_list_user.filter(infouser__rede__id__in = redes)
    
    p['result_list_user'] = result_list_user.order_by('username')
    
    ################# -------------------------- ##################
    
    list_statistic      = ra
    if p['user_id'] and int(p['user_id']) > 0:
        list_statistic  = list_statistic.filter(user__id = int(p['user_id']))
        
    if p['m'] and p['m'] == 'statistic':
        p['list_statistic'] = list_statistic.order_by('-date')
        return render_to_response('relatorio/relatoriograficostatistic.html', p, context_instance=RequestContext(request))
    
    p['list_statistic'] = list_statistic.order_by('-date')[0:10]
    p['mais_statistic'] = len(list_statistic) > len(p['list_statistic'])

    rg.set_acesso(p)

    return render_to_response('relatorio/relatoriografico.html', p, context_instance=RequestContext(request))