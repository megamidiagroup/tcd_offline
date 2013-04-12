# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext, Context
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.conf import settings
from django.template import loader
from django.template.defaultfilters import date as default_date
from django.template.loader import render_to_string
from django.http import HttpResponseServerError, Http404
from django.db.models import Q, Sum
from django.contrib.auth.models import User as UserAdmin
from django.template.defaultfilters import slugify
from django.utils.encoding import smart_str
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page
from django.forms import Form

from mail import _send_email_user, _send_email_pontos, _send_email_extrato, _is_valid_email, \
                    _send_email_suggestion, _send_email_free_question_responsavel, \
                        _send_email_free_question_user, _send_email_faq

from reportlab.pdfgen import canvas

try:
    from django.core.validators import email_re
except:
    from django.forms.fields import email_re

from django.core.mail import send_mail, BadHeaderError

from models import *
from datetime import datetime
from time import sleep
from templatetags.util import list_id_certificado, encode_object, decode_object, is_not_video
from state.models import City, State
from mobile import get_mobile
from dlog import LOGGER
from captcha.fields import CaptchaField
from email.mime.text import MIMEText
from cpf import CPF as _cpf
from sql_offline import set_sql, set_mail

import simplejson as json
import os
import fnmatch
import httplib
import sys
import traceback
import smtplib
    

# quant de itens por pagina
per_page = 15


class CaptchaTestForm(Form):
    captcha = CaptchaField()


def login_required(f):
    def wrap(request, *args, **kwargs):
        
        next = request.path
        
        try:
            if request.user.is_active and (request.user.is_superuser or request.user.is_staff):
                return HttpResponseRedirect('/admin/')
            if not request.user.is_active or not request.user.infouser.rede.link == kwargs['rede']:
                if len(next) > 2:
                    return HttpResponseRedirect('/%s/login/?next=%s' % (kwargs['rede'], next))
                return HttpResponseRedirect('/%s/login/' % (kwargs['rede']))
        except:
            if len(next) > 2:
                return HttpResponseRedirect('/login/?next=%s' % next)
            return HttpResponseRedirect('/login/')
        
        return f(request, *args, **kwargs)

    wrap.__doc__   = f.__doc__
    wrap.__name__  = f.__name__

    return wrap


def _set_enquete(request, p):
    
    p['grafico']      = False
    p['open_grafico'] = False
    
    if request.POST:
    
        count = 1
    
        while request.POST.get('group%s' % count, None):
            p['groups'] = {}
            p['groups']['group%s' % count] = int( request.POST.get('group%s' % count, 0) )
            count += 1
        
        if count > 1:
            count = 1
            for e in Enquete.objects.filter( Q(visible = True), Q(rede = p['rede']) ).order_by('-date'):
                id     = p['groups']['group%s' % count]
                count += 1
                if id == 1:
                    e.n_opcao1 += 1
                elif id == 2:
                    e.n_opcao2 += 1
                elif id == 3:
                    e.n_opcao3 += 1
                elif id == 4:
                    e.n_opcao4 += 1
                elif id == 5:
                    e.n_opcao5 += 1
                elif id == 6:
                    e.n_opcao6 += 1
                e.save()
                e.users.add(p['user'])
                e.save()
                p['groups']       = {}
                p['grafico']      = True
                p['open_grafico'] = True
                
                set_sql()
                
    if not p['grafico'] and 'user' in p and p['user'] and Enquete.objects.filter( Q(visible = True), Q(rede = p['rede']) ) > 0:
        e = Enquete.objects.filter( Q(visible = True), Q(rede = p['rede']) )
        if e.count() > 0 and e[0].users.filter(id = p['user'].id):
            p['grafico'] = True

    return p


def _prepare_vars(request, rede=None, p={}):

    p['rede']             = None
    p['list_category']    = None
    p['list_treinamento'] = None
    p['list_banner']      = None
    p['list_parceiro']    = None
    p['is_filial']        = None
    p['is_access']        = False
    p['q']                = None
    #p['user']            = None
    
    p['base_url']         = settings.LIST_VARS.get('base_url', '')

    p['title']            = u'TCD - Plataforma de Treinamento e Comunicação a Distância'

    if rede:
        r = Rede.objects.filter( Q(link = rede), Q(visible=True) )
        if r.count() > 0:
            p['rede'] = r[0]
            try:
                p['pontos'] = RelatorioAvalicao.objects.filter( Q(rede = p['rede']), Q(user = request.user) ).aggregate(Sum('pontos'))['pontos__sum']
                p['user']   = request.user
            except:
                pass

    p['list_menu']  = Menu.objects.filter( Q(rede = p['rede']), Q(visible=True) ).order_by('order', 'name')

    p['STATIC_URL'] = settings.STATIC_URL
    p['target']     = 'home' #default

    template = Template.objects.filter( Q(rede = p['rede']), Q(visible=True) ).order_by('name')

    p['get_template'] = []
    p['get_tipo_template'] = 'mega' ## default

    if template.count() > 0:
        p['get_template']      = template[0]
        p['get_tipo_template'] = template[0].tipo.name

    p['interno'] = False
    p['class']   = 'home'

    p['list_certificado_account']         = Certificado.objects.filter( Q(rede = p['rede']) & Q(visible = True) & Q(treinamento__visible = True) & Q(treinamento__category__visible = True) ).distinct().order_by('-date')
    
    try:
        if request.user.infouser.filial:
            p['list_certificado_account'] = p['list_certificado_account'].filter( Q(treinamento__category__filial__isnull = True) | Q(treinamento__category__filial = request.user.infouser.filial) ).distinct()
    except:
        pass
    
    p['list_aproveitamento_account']      = Treinamento.objects.filter( Q(rede = p['rede']) & Q(visible = True) & Q(category__visible = True) ).distinct().order_by('-date')
    
    try:
        if request.user.infouser.filial:
            p['list_aproveitamento_account'] = p['list_aproveitamento_account'].filter( Q(treinamento__category__filial__isnull = True) | Q(category__filial = request.user.infouser.filial) ).distinct()
    except:
        pass

    try:
        p['is_access'] = request.user.infouser.access
    except:
        pass

    try:
        p['is_filial'] = request.user.infouser.filial
    except:
        pass

    p = _set_enquete(request, p)
    
    p['first'], p['first_cpf'], p['btns_disabled'] = False, False, False
    
    try:
        if not request.user.email or not len(request.user.email) > 3:
            p['first']         = True
            p['btns_disabled'] = True
    except:
        pass

    return p


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def home(request, rede=None):

    p = _prepare_vars(request, rede)

    if not p['rede']:
        return HttpResponseRedirect('/login/')

    p['list_category'] = Category.objects.filter( Q(visible = True), Q(rede = p['rede']), Q(parent__isnull = True), Q(home = True) ).order_by('order', 'name')
    p['list_banner']   = Banner.objects.filter( Q(visible = True), Q(rede = p['rede']), ( Q(home = True) or Q(category__isnull = True) ) ).order_by('order', 'name')
    p['list_parceiro'] = Parceiro.objects.filter( Q(visible = True), Q(rede = p['rede']), ( Q(home = True) or Q(category__isnull = True) ) ).order_by('order', 'name')

    # regras para usuário restrito
    if not p['is_access']:
        p['list_category'] = p['list_category'].filter( Q(access = p['is_access']) ).order_by('order', 'name')

    # regras para quem está em uma filial
    if p['is_filial']:
        p['list_category'] = p['list_category'].filter( Q(filial__isnull = True) | Q(filial = p['is_filial']) ).order_by('order', 'name')

    p['url_logo'] = p['rede'].logo.url

    return render_to_response('%s/home.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def category(request, rede=None, cat_id=None):

    p = _prepare_vars(request, rede)
    
    p['class'] = ''

    if not p['rede']:
        return HttpResponseRedirect('/login/')

    list_category      = Category.objects.filter( Q(rede = p['rede']), Q(visible=True) ).order_by('order', 'name')

    p['list_category'] = list_category.filter( Q(parent__id = int(cat_id)) ).order_by('order', 'name')
    p['list_banner']   = Banner.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(category__id = int(cat_id)) ).order_by('order', 'name')
    p['list_parceiro'] = Parceiro.objects.filter( Q(rede = p['rede']), Q(category__id = int(cat_id)), Q(visible=True) ).order_by('order', 'name')

    # regras para usuário restrito
    if not p['is_access']:
        p['list_category'] = p['list_category'].filter( Q(access = p['is_access']) ).order_by('order', 'name')
        if not list_category.filter( Q(id = int(cat_id)), Q(access = p['is_access']) ):
            return HttpResponseRedirect('/%s/' % p['rede'].link)

    # regras para quem está em uma filial
    if p['is_filial']:
        p['list_category'] = p['list_category'].filter( Q(filial__isnull = True) | Q(filial = p['is_filial']) ).order_by('order', 'name')
        if not list_category.filter( Q(id = int(cat_id)) & ( Q(filial__isnull = True) | Q(filial = p['is_filial']) ) ):
            return HttpResponseRedirect('/%s/' % p['rede'].link)

    p['url_logo'] = p['rede'].logo.url
    p['interno']  = True

    if not p['list_category']:
        p['list_treinamento'] = Treinamento.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(category__id = int(cat_id)) ).order_by('order', 'name')

    return render_to_response('%s/home.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def treinamento(request, rede=None, video_id=None):

    p = _prepare_vars(request, rede)
    
    p['class'] = ''
    
    p['list_anexo'] = None

    if not p['rede']:
        return HttpResponseRedirect('/login/')

    p['url_logo']     = p['rede'].logo.url
    p['list_video']   = Treinamento.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(id = int(video_id)) ).order_by('order', 'name')

    # regras para usuário restrito
    if not p['is_access']:
        if p['list_video'] and not p['list_video'].filter( Q(category__access = p['is_access']) ):
            return HttpResponseRedirect('/%s/' % p['rede'].link)

    # regras para quem está em uma filial
    if p['is_filial']:
        if p['list_video'] and not p['list_video'].filter( Q(category__filial__isnull = True) | Q(category__filial = p['is_filial']) ):
            return HttpResponseRedirect('/%s/' % p['rede'].link)
        
    if p['list_video'] and p['list_video'].count() > 0:
        video = p['list_video'][0]
        p['list_anexo'] = Anexo.objects.filter( Q(visible = True), Q(rede = p['rede']), Q(treinamento = video) ).order_by('name')
        if is_not_video(video) == 'elearning':
            return HttpResponseRedirect('/%s/elearning/%s/' % (p['rede'].link, video.id) )
        
    p['elearning'] = Elearning.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(treinamento__in = p['list_video']) ).count() > 0

    return render_to_response('%s/treinamento.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
def send_faq(request, rede=None, id=None):
    
    p = _prepare_vars(request, rede)
    
    error    = u'Ocorreu um erro interno, contate o administrador.'
    
    p['msg'] = request.REQUEST.get('msg', '')
    
    if len(p['msg']) >= 10:
        
        try:
            s             = Suggestion()
            s.rede        = p['rede']
            s.treinamento = Treinamento.objects.get(id = int(id))
            s.user        = request.user
            s.mensagem    = p['msg']
            s.command     = 'send_faq'
            s.save()
            
            set_sql()
        
            if p['rede'].resend == 'I':
                ret = _send_email_faq(s, p)
        
            error = u'Enviado com sucesso. Você logo será informado por e-mail.'
            
        except:
            pass

    return HttpResponse('$(".error").html("%s");clear_send_faq();' % error)


@login_required
def suggestion(request, rede=None, video_id=None):
    
    p = _prepare_vars(request, rede)
    
    r = u'Ocorreu algum erro!'
    
    msg = request.REQUEST.get('mensagem', '')
    
    try:
        
        s             = Suggestion()
        s.rede        = p['rede']
        s.treinamento = Treinamento.objects.get(id = int(video_id))
        s.user        = request.user
        s.mensagem    = msg
        s.command     = 'suggestion'
        s.save()
        
        set_sql()
        
        if p['rede'].resend == 'I':
            ret = _send_email_suggestion(s, p)

        r = u'Mensagem enviada!'
        
    except:
        pass

    return HttpResponse(r)


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def elearning(request, rede=None, video_id=None):

    p = _prepare_vars(request, rede)

    if not p['rede']:
        return HttpResponseRedirect('/login/')

    p['url_logo']   = p['rede'].logo.url
    p['list_video'] = Treinamento.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(id = int(video_id)) ).order_by('order', 'name')

    # regras para usuário restrito
    if not p['is_access']:
        if p['list_video'] and not p['list_video'].filter( Q(category__access = p['is_access']) ):
            return HttpResponseRedirect('/%s/' % p['rede'].link)

    # regras para quem está em uma filial
    if p['is_filial']:
        if p['list_video'] and not p['list_video'].filter( Q(category__filial__isnull = True) | Q(category__filial = p['is_filial']) ):
            return HttpResponseRedirect('/%s/' % p['rede'].link)
        
    dir   = settings.MEDIA_ROOT + settings.UPLOAD_STORAGE_DIR + 'uploads/elearning/'
    
    elear = Elearning.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(treinamento__in = p['list_video']) )
    
    if elear.count() > 0:
        elear   = elear[0]
        local   = dir + elear.dir + '/'

        pattern = 'index.html'
    
        files   = os.listdir(os.path.abspath(local))
            
        for path, dirs, files in os.walk(os.path.abspath(local)):
            for filename in fnmatch.filter(files, pattern):
                p['elearning'] = os.path.join(path, filename)
                
        p['elearning'] = settings.LIST_VARS.get('base_url', '') + (settings.UPLOAD_STORAGE_DIR[3:]) + 'uploads/elearning/' + (p['elearning'].split('/uploads/elearning/')[1])
    else:
        return HttpResponseRedirect('/%s/' % p['rede'].link)

    return render_to_response('%s/elearning.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def live(request, rede=None, video_id=None):

    p = _prepare_vars(request, rede)
    
    p['get_mobile'] = get_mobile(request)

    if not p['rede']:
        return HttpResponseRedirect('/login/')

    p['url_logo']     = p['rede'].logo.url
    p['list_video']   = Treinamento.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(id = int(video_id)) ).order_by('order', 'name')

    # regras para usuário restrito
    if not p['is_access']:
        if p['list_video'] and not p['list_video'].filter( Q(category__access = p['is_access']) ):
            return HttpResponseRedirect('/%s/' % p['rede'].link)

    # regras para quem está em uma filial
    if p['is_filial']:
        if p['list_video'] and not p['list_video'].filter( Q(filial__isnull = True) | Q(category__filial = p['is_filial']) ):
            return HttpResponseRedirect('/%s/' % p['rede'].link)
        
    p['history'] = WebChat.objects.filter( Q(rede = p['rede']), Q(live__id = int(video_id)) ).count() > 0
    
    ## ---   limpa caixa   --- ##
    
    list = WebChat.objects.filter( Q(rede = p['rede']), Q(live__id = int(video_id)) ).exclude(user_lido = request.user)

    for li in list:
        ul = li.user_lido
        ul.add(request.user)
    
    ## --- end limpa caixa --- ##

    return render_to_response('%s/live.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@csrf_exempt
@login_required
def live_load(request, rede=None, video_id=0):
    
    array = []
    tmp   = {}
    
    r = Rede.objects.filter( Q(link = rede), Q(visible=True) )
    
    if r.count() > 0:
        rede = r[0]
    else:
        return HttpResponse('Error')
    
    lidos = request.REQUEST.get('lidos', '')

    if request.REQUEST.get('action', 'set_msg'):
        
        wc         = WebChat()
        wc.rede    = rede
        wc.user    = request.user
        wc.live_id = int( video_id )
        wc.text    = request.REQUEST.get('mensagem', '')
        wc.save()
        
        tmp['id_chat']         = wc.id
        tmp['id_video']        = wc.live.id
        tmp['id_user']         = wc.user.id
        if len(wc.user.get_full_name()) > 0:
            tmp['user']        = wc.user.get_full_name()
        else:
            tmp['user']        = wc.user.username
        tmp['session_user_id'] = request.user.id
        tmp['msg']             = wc.text
        tmp['hora']            = default_date(wc.date, 'G:i')
        array.append(tmp)
        
        return HttpResponse('arr_msg=%s;' % json.dumps(array))

    list = WebChat.objects.filter( Q(rede = rede), Q(live__id = video_id) )

    if request.REQUEST.get('history', '') == 'false':
        list2 = list.exclude(user_lido = request.user).exclude(user = request.user)
    else:
        list2 = list
        
    if lidos and len(lidos) > 0:
        for li in lidos.split('-'):
            if not list.filter( Q(id = int(li)), Q(user_lido = request.user) ).count() > 0:
                ul = list.get(id = int(li)).user_lido
                ul.add(request.user)
        
    list = list2.order_by('id')
    
    for i in list:
        
        tmp = {}

        tmp['id_chat']         = i.id
        tmp['id_video']        = i.live.id
        tmp['id_user']         = i.user.id
        if len(i.user.get_full_name()) > 0:
            tmp['user']        = i.user.get_full_name()
        else:
            tmp['user']        = i.user.username
        tmp['session_user_id'] = request.user.id
        tmp['msg']             = i.text
        tmp['hora']            = default_date(i.date, 'G:i')
        array.append(tmp)
    
    return HttpResponse('arr_msg=%s;history=%s;' % ( json.dumps(array), request.REQUEST.get('history', '') ))


def avaliacao(request, rede=None, key=''):
    
    p  = _prepare_vars(request, rede)
    
    do = decode_object(key)
    
    p['list_question'] = Question.objects.filter(id__in = do['list_question'])
    p['user']          = UserAdmin.objects.get(id = do['user_id'])
    
    p['lista']         = range(0, 11)
    p['notas']         = []
    p['error']         = ''
    save               = True
    
    p['sucesso']       = request.REQUEST.get('sucesso', '')
    p['porcent']       = request.REQUEST.get('porcent', 0)
    
    if p['sucesso'] == 'true':
        return render_to_response('%s/avaliacao_sucesso.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))
    elif p['sucesso'] == 'false':
        return render_to_response('%s/avaliacao_nosucesso.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))
    
    if request.POST:
        for lq in p['list_question']:
            if not lq.get_list_response_order():
                p['notas'].append( request.REQUEST.get('nota_%s' % lq.id, '') )
            
    for n in p['notas']:
        if not len(n) > 0:
            p['error'] = u'Selecione a nota para todas as questões.'
            save       = False
            
    if request.POST and save:

        list_acerto     = []
        list_correct    = {}
        quant           = 0
        
        rt              = RelatorioTentativa.objects.filter( Q(rede = p['rede']), Q(user = p['user']), Q(treinamento = p['list_question'][0].treinamento) )
        p['list_video'] = Treinamento.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(id = int(p['list_question'][0].treinamento.id)) ).order_by('order', 'name')
    
        if rt.count() > 0:
            rt = rt[0]
            if rt.aprovado and p['sucesso'] == '':
                return HttpResponseRedirect(reverse('login', args=(p['rede'].link,)))
        
        try:
            porcent_quiz  = p['list_video'][0].quiz_set.all()[0].porcent
        except:
            porcent_quiz  = 100
            
        p['porcent_quiz'] = porcent_quiz
        
        for lq in p['list_question']:
            if not lq.get_list_response_order():
                list_acerto.append( int(p['notas'][quant]) )
                list_correct['res_%s' % lq.id] = int(p['notas'][quant])
                quant += 1
            else:
                gfr  = lq.get_free_response(p['user'])
                nota = 0
                if gfr.count() > 0:
                    if gfr[0].aprovado:
                        nota = 10
                list_acerto.append( nota )
                list_correct['res_%s' % lq.id] = nota
            
        try:
            porcent  = int( float( sum(list_acerto) ) / float( len(list_acerto) ) * 10 )
        except:
            porcent  = 0
            
        p['porcent'] = porcent
        
        if porcent >= porcent_quiz:
                    
            ## momento de aprovação

            ra        = RelatorioAvalicao()
            ra.rede   = p['rede']
            ra.user   = p['user']
            quant     = 0

            for lqp in p['list_question']:
                if not lqp.get_list_response_order():
                    ra.pontos += int( float(lqp.pontos) * (float(list_acerto[quant]) / 10) )
                else:
                    gfr = lq.get_free_response(p['user'])
                    if gfr.count() > 0:
                        if gfr[0].aprovado:
                            ra.pontos += lqp.pontos
                quant += 1
                
            ra.quiz    = p['list_video'][0].quiz_set.all()[0]
            ra.save()

            infouser = p['user'].infouser
            infouser.pontos += ra.pontos
            infouser.save()
            
            ## salva no relatório
            rt.date_end = datetime.now()
            rt.aprovado = True
            rt.save()
            
            for lqu in p['list_question']:
                lqu.get_free_response(p['user']).delete()
                
                
            er = p['list_video'][0].quiz_set.all()[0]
                    
            try:
                p['to_mail'] = er.responsavel.all()[0].email
            except:
                p['to_mail'] = er.email_respon
                
            if len( p['user'].get_full_name() ) > 1:
                p['usuario']     = p['user'].get_full_name()
            else:
                p['usuario']     = p['user'].username
                
            if request.is_secure():
                p['link'] = 'https://'
            else:
                p['link'] = 'http://'
                
            p['link']    += request.get_host() + reverse('conta', args=(p['rede'].link,))

            r = _send_email_free_question_user(p, request, True)
            
            set_sql()

            return HttpResponseRedirect( reverse('avaliacao', args=(p['rede'].link, key,)) + '?sucesso=true&porcent=%s' % porcent )
        
        else:
            
            ## momento de reprovação
            
            ## salva no relatório
            rt.date_end = datetime.now()
            rt.aprovado = False
            rt.save()
            
            er = p['list_video'][0].quiz_set.all()[0]
                    
            try:
                p['to_mail'] = er.responsavel.all()[0].email
            except:
                p['to_mail'] = er.email_respon
                
            if len( p['user'].get_full_name() ) > 1:
                p['usuario']     = p['user'].get_full_name()
            else:
                p['usuario']     = p['user'].username
                
            if request.is_secure():
                p['link'] = 'https://'
            else:
                p['link'] = 'http://'
                
            p['link']    += request.get_host() + reverse('treinamento', args=(p['rede'].link, p['list_video'][0].id,))

            
            r = _send_email_free_question_user(p, request, False)
            
            set_sql()

            return HttpResponseRedirect( reverse('avaliacao', args=(p['rede'].link, key,)) + '?sucesso=false&porcent=%s' % porcent )


    return render_to_response('%s/avaliacao.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def questionario(request, rede=None, video_id=None):

    p = _prepare_vars(request, rede)
    
    p['class']     = ''
    p['porcent']   = ''

    list_acerto    = []
    list_correct   = {}
    
    quant, acertos = 0, 0
    
    freequestion   = False

    p['user']    = request.user
    p['sucesso'] = request.REQUEST.get('sucesso', '')

    if not p['rede']:
        return HttpResponseRedirect('/login/')

    p['url_logo']     = p['rede'].logo.url
    p['list_video']   = Treinamento.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(id = int(video_id)) ).order_by('order', 'name')
    
    try:
        porcent_quiz  = p['list_video'][0].quiz_set.all()[0].porcent
    except:
        porcent_quiz  = 100
        
    p['porcent_quiz'] = porcent_quiz
    
    rt = RelatorioTentativa.objects.filter( Q(rede = p['rede']), Q(user = p['user']), Q(treinamento__id = int(video_id)) )
    
    if rt.count() > 0:
        rt = rt[0]
        if rt.aprovado and p['sucesso'] == '':
            return HttpResponseRedirect(reverse('treinamento', args=(p['rede'].link, video_id)))
    
    if p['sucesso'] == '' and (not rt or rt.date_end):
        rt = RelatorioTentativa()
        rt.rede = p['rede']
        rt.user = p['user']
        rt.treinamento_id = int(video_id)
        rt.date_init = datetime.now()
        rt.save()

    if not p['sucesso']:
        if p['list_video'].count() > 0:
            p['list_question'] = Question.objects.filter( Q(treinamento = p['list_video'][0]), Q(visible=True) ).order_by('id')

            # regras para usuário restrito
            if not p['is_access']:
                if p['list_question'] and not p['list_question'].filter( Q(treinamento__category__access = p['is_access']) ):
                    return HttpResponseRedirect('/%s/' % p['rede'].link)

            # regras para quem está em uma filial
            if p['is_filial']:
                if p['list_question'] and not p['list_question'].filter( Q(treinamento__category__filial__isnull = True) | Q(treinamento__category__filial = p['is_filial']) ):
                    return HttpResponseRedirect('/%s/' % p['rede'].link)

            if request.REQUEST.get('csrfmiddlewaretoken', False):
                for i in p['list_question']:
                    try:
                        is_valid = i.get_list_response().filter(correta = True)[0].id == int(request.REQUEST.get('resposta_%d' % i.id, 0))
                        list_acerto.append( is_valid )
                        list_correct['res_%s' % i.id] = is_valid
                    except:
                        list_acerto.append( False )
                        list_correct['res_%s' % i.id] = False
                        text_resp   = request.REQUEST.get('resposta_%d' % i.id, '')
                        
                        fr          = FreeResponse()
                        fr.rede     = p['rede']
                        fr.user     = p['user']
                        fr.question = i
                        fr.text     = text_resp
                        fr.save()
                        
                        set_sql()

                        freequestion = True
                    
                try:
                    porcent = int(float(list_acerto.count(True)) / float(len(list_acerto)) * 100)
                except:
                    porcent = 0

                if not freequestion and porcent >= porcent_quiz:
                    
                    ## momento de aprovação
                    
                    list_question_exclude = []
                    
                    for lc in list_correct:
                        if not list_correct[lc]:
                            list_question_exclude.append( int(lc.split('_')[1]) )
                    
                    if len(list_question_exclude) > 0:        
                        p['list_question'] = p['list_question'].exclude(id__in = list_question_exclude)

                    ra        = RelatorioAvalicao()
                    ra.rede   = p['rede']
                    ra.user   = p['user']
                    ra.pontos = p['list_question'].aggregate(Sum('pontos'))['pontos__sum']
                    ra.quiz   = p['list_video'][0].quiz_set.all()[0]
                    ra.save()

                    infouser = p['user'].infouser
                    infouser.pontos += ra.pontos
                    infouser.save()
                    
                    ## salva no relatório
                    rt.date_end = datetime.now()
                    rt.aprovado = True
                    rt.save()
                    
                    set_sql()

                    return HttpResponseRedirect( '/%s/questionario/%d/?sucesso=true&r=%s' % (p['rede'].link, p['list_video'][0].id, encode_object(list_correct)) )
                
                elif freequestion:
                    
                    er = p['list_video'][0].quiz_set.all()[0]
                    
                    try:
                        p['to_mail'] = er.responsavel.all()[0].email
                    except:
                        p['to_mail'] = er.email_respon
                    
                    try:
                        p['responsavel'] = er.responsavel.all()[0].get_full_name()
                    except:
                        p['responsavel'] = p['to_mail']
                        
                    if len( p['user'].get_full_name() ) > 1:
                        p['usuario']     = p['user'].get_full_name()
                    else:
                        p['usuario']     = p['user'].username
                        
                    if request.is_secure():
                        p['link'] = 'https://'
                    else:
                        p['link'] = 'http://'
                        
                    p['link']        += request.get_host() + reverse('avaliacao', args=(p['rede'].link, '%s' % encode_object({'user_id': p['user'].id, 'list_question': [i.id for i in p['list_question']]}),))
                    
                    for indice in list_correct:
                        if list_correct[indice]:
                            question_id    = int(indice.split('_')[1])
                            fr             = FreeResponse()
                            fr.rede        = p['rede']
                            fr.user        = p['user']
                            fr.question_id = question_id
                            fr.text        = u'resposta automática'
                            fr.aprovado    = True
                            fr.save()
                            
                            set_sql()
                    
                    r = _send_email_free_question_responsavel(p, request)
                    
                    return HttpResponseRedirect( '/%s/questionario/%d/?sucesso=aguarde&r=%s' % (p['rede'].link, p['list_video'][0].id, encode_object(list_correct)) )
                
                else:
                    
                    ## momento de reprovação
                    
                    ## salva no relatório
                    rt.date_end = datetime.now()
                    rt.aprovado = False
                    rt.save()

                    set_sql()
                    
                    return HttpResponseRedirect( '/%s/questionario/%d/?sucesso=false&r=%s' % (p['rede'].link, p['list_video'][0].id, encode_object(list_correct)) )
                
    elif p['sucesso'] and ( p['sucesso'] == 'true' or p['sucesso'] == 'false' or p['sucesso'] == 'aguarde' ):
        
        key = request.REQUEST.get('r', '')
        
        p['respostas']     = {}
        p['list_question'] = {}

        if key:
            try:
                p['respostas'] = decode_object(key)
                for t in p['respostas']:
                    if p['respostas'][t]:
                        acertos += 1
                    quant += 1
            except:
                pass
        
        try:
            p['porcent'] = int( (float(acertos) / float(quant)) * 100 )
        except:
            p['porcent'] = 0

        if p['list_video'].count() > 0:
            p['list_question'] = Question.objects.filter( Q(treinamento = p['list_video'][0]), Q(visible=True) )
            
    p['get_host']  = request.get_host()
    p['is_secure'] = request.is_secure()
    p['app_id']    = settings.FACEBOOK_APP_ID.get(p['get_tipo_template'], '')

    return render_to_response('%s/questionario.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def conta(request, rede=None):

    p = _prepare_vars(request, rede)
    
    p['class'] = ''

    p['sucesso']  = False
    p['user']     = request.user
    p['edit']     = request.REQUEST.get('edit', False)

    try:
        p['infouser'] = p['user'].infouser
    except:
        pass

    q = [i.treinamento.id for i in Quiz.objects.filter( Q(rede = p['rede']), Q(relatorioavalicao__isnull = False), Q(relatorioavalicao__user = p['user']) ).distinct()]

    p['list_treinamento'] = Treinamento.objects.filter(id__in = q)

    if request.REQUEST.get('sucesso', False):
        p['to_mail'] = p['user'].email
        p['name']    = p['user'].get_full_name()
        p['sucesso'] = _send_email_pontos(p, request)

    return render_to_response('%s/conta.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@cache_page(settings.CACHES['default']['TIMEOUT'])
def conta_edit(request, rede=None):

    p = {}

    p['user']   = request.REQUEST.get('user'  , '')
    p['key']    = request.REQUEST.get('key'   , '')
    p['edit']   = request.REQUEST.get('edit'  , '')
    p['msg']    = request.REQUEST.get('msg'   , '')
    p['estado'] = ''

    p['is_pass'] = True

    if len(p['user']) > 0 and len(p['key']) > 0:
        ua = UserAdmin.objects.filter( Q(username__exact=p['user']), Q(password=p['key']), Q(is_active=True) )
        if ua.count() > 0:
            ua = ua[0]
            p['user']     = ua
            p['infouser'] = ua.infouser
            p['is_pass']  = False
        else:
            return HttpResponseRedirect('/login/')

    else:
        p['user'] = request.user
        try:
            p['infouser'] = p['user'].infouser
        except:
            pass
        
        if not request.user.is_active:
            return HttpResponseRedirect('/%s/login/' % rede)

    p = _prepare_vars(request, rede, p)
    
    p['class'] = ''

    if request.REQUEST.get('csrfmiddlewaretoken', False):
        list = ['txt_name', 'txt_email', 'txt_cpf', 'txt_endereco', 'txt_bairro', 'txt_cep', 'estado',
                    'cidade', 'txt_fone_com', 'txt_fone_res', 'txt_fone_cel', 'ch_receber', 'ch_envia', 'txt_pass',
                        'txt_newpass', 'txt_confirm', 'sel_filial', 'txt_cnpj', 'is_cnpj']

        for i in list:
            p[i] = request.REQUEST.get(i, '')
            
        msg, p['msg'], usermail = '', '', None
            
        if not len(p['txt_name'].split(' ')) > 1 or not p['txt_name'].split(' ')[0] or not p['txt_name'].split(' ')[1] or not _cpf(p['txt_cpf']).isValid() or not _is_valid_email(p['txt_email']) or _cpf(p['user'].username).isValid():
            if not len(p['txt_name'].split(' ')) > 1 or not p['txt_name'].split(' ')[0] or not p['txt_name'].split(' ')[1]:
                msg = u'Digite o nome completo.'
            elif not p['is_cnpj'] and not p['txt_cpf']:
                msg = u'Digite o CPF.'
            elif not p['is_cnpj'] and not _cpf(p['txt_cpf']).isValid():
                msg = u'CPF inválido.'
            elif not p['txt_email']:
                msg = u'Digite seu e-mail.'
            elif not _is_valid_email(p['txt_email']):
                msg = u'E-mail inválido.'
            elif _cpf(p['user'].username).isValid():
                if UserAdmin.objects.filter( Q(username__exact=p['txt_email']) ).count() > 0:
                    msg      = u'E-mail já existe, tente outro.'
                else:
                    usermail = p['txt_email']
            p['msg'] = msg

        if msg:
            p['edit'] = 'false'
        else:
            iu   = p['infouser']
            user = p['user']
            user.first_name    = p['txt_name'].split(' ')[0].strip()
            try:
                user.last_name = ' '.join(n for n in p['txt_name'].split(' ')[1:]).strip()
            except:
                user.last_name = ''
            user.email   = p['txt_email']
            iu.cpf       = p['txt_cpf']
            iu.cnpj      = p['txt_cnpj']
            iu.endereco  = p['txt_endereco']
            iu.bairro    = p['txt_bairro']
            iu.cep       = p['txt_cep']
            iu.filial_id = p['sel_filial']
            iu.estado_id = p['estado']
            iu.cidade_id = p['cidade']
            iu.fone_com  = p['txt_fone_com']
            iu.fone_res  = p['txt_fone_res']
            iu.fone_cel  = p['txt_fone_cel']
            iu.receber   = p['ch_receber']
            iu.envia     = p['ch_envia']
    
            if p['is_pass'] == False and len(p['txt_newpass']) > 0 and len(p['txt_confirm']) > 0 and p['txt_newpass'] == p['txt_confirm']:
                user.set_password(p['txt_newpass'])
            elif len(p['txt_pass']) > 0 and len(p['txt_newpass']) > 0 and len(p['txt_confirm']) > 0 and authenticate(username=user, password=p['txt_pass']) and p['txt_newpass'] == p['txt_confirm']:
                user.set_password(p['txt_newpass'])
                
            if usermail:
                user.username = usermail

            user.save()
            iu.save()
    
            p['to_mail'] = user.email
            p['name']    = user.get_full_name()
            p['link']    = '?user=%s&action=%s&key=%s' % (user.username, '/conta/edit/', user.password)
    
            if not p['key'] and _send_email_user(p, request):
                set_sql()
                return HttpResponseRedirect('/%s/conta/?edit=true' % p['rede'].link)

    try:
        p['list_state']    = State.objects.all()
        if p['estado'] and p['estado'].isdigit() and int(p['estado']) > 0:
            p['list_city'] = City.objects.filter( state__id = int(p['estado']) )
        else:
            p['list_city'] = City.objects.filter( state = p['infouser'].estado )
        p['list_filial']   = Filial.objects.filter( Q(visible = True), Q(rede = p['rede']) ).order_by('name')
    except:
        pass
    
    p['first'] = False
    
    if request.user.username and _cpf(request.user.username).isValid():
        p['first_cpf'] = True

    return render_to_response('%s/conta_edit.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


def conta_add(request, rede=None):

    p = _prepare_vars(request, rede)
    
    p['user'] = request.REQUEST.get('user', '')
    p['key']  = request.REQUEST.get('key' , '')
    p['edit'] = request.REQUEST.get('edit', '')
    
    list = ['txt_name', 'txt_email', 'txt_cpf', 'txt_endereco', 'txt_bairro', 'txt_cep', 'estado',
                'cidade', 'txt_fone_com', 'txt_fone_res', 'txt_fone_cel', 'ch_receber', 'ch_envia', 'txt_pass',
                    'txt_newpass', 'txt_confirm', 'sel_filial', 'txt_cnpj']

    for i in list:
        p[i] = request.REQUEST.get(i, '')
    
    p['class'] = ''
    
    if len(p['user']) > 0 and len(p['key']) > 0:
        ua = UserAdmin.objects.filter( Q(username__exact=p['user']), Q(password=p['key']) )
        p['class'] = 'home'
        if ua.count() > 0:
            ua = ua[0]
            ua.is_active = True
            iu = InfoUser.objects.filter(user = ua)
            if iu.count() > 0:
                iu = iu[0]
                iu.visible = True
                iu.save()
            ua.save()
            return render_to_response('%s/active_sucesso.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))
        else:
            return render_to_response('%s/active_error.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))
    
    human, post = False, False
        
    if request.POST:
        post = True
        form = CaptchaTestForm(request.POST)
        if form.is_valid():
            human = True
    else:
        form = CaptchaTestForm()

    if human and request.REQUEST.get('csrfmiddlewaretoken', False):
        
        if not _is_valid_email(p['txt_email']) or UserAdmin.objects.filter( Q(username__exact=p['txt_email']) ).count() > 0:
            return HttpResponseRedirect('/%s/conta/add/?edit=false' % p['rede'].link)

        iu   = InfoUser()
        user = UserAdmin()
        
        user.first_name = p['txt_name'].split(' ')[0]
        try:
            user.last_name = ' '.join(n for n in p['txt_name'].split(' ')[1:])
        except:
            user.last_name = ''
        user.username  = p['txt_email']
        user.email     = p['txt_email']
        user.is_active = False
        
        iu.cpf         = p['txt_cpf']
        iu.cnpj        = p['txt_cnpj']
        iu.endereco    = p['txt_endereco']
        iu.bairro      = p['txt_bairro']
        iu.cep         = p['txt_cep']
        iu.filial_id   = p['sel_filial']
        iu.estado_id   = p['estado']
        iu.cidade_id   = p['cidade']
        iu.fone_com    = p['txt_fone_com']
        iu.fone_res    = p['txt_fone_res']
        iu.fone_cel    = p['txt_fone_cel']
        iu.receber     = p['ch_receber']
        iu.envia       = p['ch_envia']
        iu.visible     = False
        
        iu.rede        = p['rede']
        
        user.save()
        
        iu.user = user

        if len(p['txt_newpass']) > 0 and len(p['txt_confirm']) > 0 and p['txt_newpass'] == p['txt_confirm']:
            user.set_password(p['txt_newpass'])

        user.save()
        iu.save()

        p['to_mail'] = user.email
        p['name']    = user.get_full_name()
        p['link']    = '?user=%s&action=%s&key=%s' % (user.username, '/conta/add/', user.password)

        if _send_email_user(p, request):
            return HttpResponseRedirect('/%s/login/?add=true' % p['rede'].link)
        
    p['human'], p['post'] = human, post
        
    p['captcha'] = form

    return render_to_response('%s/conta_add.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
def certificado(request, rede=None, tipo=''):

    p = _prepare_vars(request, rede)

    p['sucesso'] = False
    p['user']    = request.user
    p['key']     = request.REQUEST.get('key', '')

    ### são os treinamentos que fui aprovado
    q    = [i.treinamento.id for i in Quiz.objects.filter( Q(rede = p['rede']), Q(relatorioavalicao__isnull = False), Q(relatorioavalicao__user = p['user']) ).distinct()]

    tmp  = []
    cert = None

    cer  = Certificado.objects.filter( Q(rede = p['rede']), Q(visible=True), Q(treinamento__id__in = q) ).distinct()

    if len(p['key']) > 0:
        cer = cer.filter( id__in = list_id_certificado(p['key']) )

    for c in cer:
        cert  = c.image
        count = c.treinamento.filter(visible = True).count()
        tr    = True
        for i in c.treinamento.filter(visible = True):
            tr = q.count(i.id) > 0 and tr
        if tr:
            tmp.append( c )

    p['list_certificado'] = tmp

    ###########

    if len(tipo) > 0 and tipo == 'pdf':
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=certificado-%s.pdf' % slugify( p['user'].get_full_name() )

        # Create the PDF object, using the response object as its "file."
        can = canvas.Canvas(response)

        can.drawImage(cert.path, 1, 30, width=600, height=780, preserveAspectRatio=True, anchor='c')

        can.drawString(240, 605, p['user'].get_full_name())

        start = 530

        for i in p['list_certificado']:
            can.setFontSize(12)
            can.drawString(110, start, '- %s' % i.name)
            can.drawString(390, start, default_date(i.date, 'd/m/Y à\s H:i'))
            can.setFontSize(9)
            for t in i.get_list_treinamento():
                can.drawString(120, (start-15), t)
                start = start - 12

        can.setFontSize(11)
        
        if p['user'].infouser.cidade:
            cidade = p['user'].infouser.cidade.name
        else:
            cidade = u'(Nenhum)'
        
        can.drawString(230, 170, '%s, %s de %s de %s' % (cidade, datetime.now().day, default_mes[datetime.now().month], datetime.now().year))

        can.showPage()
        can.save()

        return response

    if request.REQUEST.get('sucesso', False):
        p['to_mail'] = p['user'].email
        p['name']    = p['user'].get_full_name()
        p['sucesso'] = _send_email_extrato(p, request)

    return render_to_response('%s/certificado.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def faq(request, rede=None):

    p = _prepare_vars(request, rede)

    p['list_faq'] = Faq.objects.filter( Q(rede = p['rede']) & Q(visible=True) & Q(menu_all = True) ).order_by('order', 'pergunta')

    # regras para usuário restrito
    if not p['is_access']:
        p['list_faq'] = p['list_faq'].filter( Q(access = p['is_access']) ).order_by('order', 'pergunta')

    # regras para quem está em uma filial
    if p['is_filial']:
        p['list_faq'] = p['list_faq'].filter( Q(filial__isnull = True) | Q(filial = p['is_filial']) ).order_by('order', 'pergunta')

    return render_to_response('%s/faq.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
@cache_page(settings.CACHES['default']['TIMEOUT'])
def busca(request, rede=None):

    p = _prepare_vars(request, rede)

    p['q'] = request.REQUEST.get('q', '')

    p['total']  = 0
    p['total'] += Treinamento.objects.filter( Q(rede = p['rede']) & Q(visible = True) & Q(category__visible = True) ).count()
    p['total'] += Category.objects.filter( Q(rede = p['rede']) & Q(visible = True) ).count()

    p['list_treinamento'] = Treinamento.objects.filter( Q(rede = p['rede']) & Q(category__visible = True) & Q(name__icontains = p['q'].strip()) & Q(visible = True) ).order_by('name')
    p['list_category']    = Category.objects.filter( Q(rede = p['rede']) & Q(name__icontains = p['q'].strip()) & Q(visible = True) ).order_by('name')

    # regras para usuário restrito
    if not p['is_access']:
        p['list_treinamento'] = p['list_treinamento'].filter( Q(category__access = p['is_access']) ).order_by('name')
        p['list_category']    = p['list_category'].filter( Q(access = p['is_access']) ).order_by('name')

    # regras para quem está em uma filial
    if p['is_filial']:
        p['list_treinamento'] = p['list_treinamento'].filter( Q(category__filial__isnull = True) | Q(category__filial = p['is_filial']) ).order_by('name')
        p['list_category']    = p['list_category'].filter( Q(filial__isnull = True) | Q(filial = p['is_filial']) ).order_by('name')

    p['list_busca']  = [['treinamento', i.id, i.name, i.desc] for i in p['list_treinamento']]

    p['list_busca'] += [['category'   , i.id, i.name, i.desc] for i in p['list_category']]

    return render_to_response('%s/busca.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


@login_required
def action(request, rede=None):

    p = _prepare_vars(request, rede)

    p['user']     = request.user
    p['video_id'] = request.REQUEST.get('video_id' , 0)
    p['action']   = request.REQUEST.get('action'   , 'play')

    ra = RelatorioAcoes.objects.filter( Q(rede = p['rede']) & Q(user = p['user']) & Q(video__id = int(p['video_id'])) ).distinct().order_by('-complete')

    if ra.count() == 1:
        ra        = ra[0]
    else:
        tmpra     = ra
        ra        = RelatorioAcoes()
        ra.rede   = p['rede']
        ra.user   = p['user']
        ra.video  = Treinamento.objects.get(id = p['video_id'])
        if tmpra.count() > 1:
            play, complete = False, False
            for i in tmpra:
                if i.play:
                    play     = True
                if i.complete:
                    complete = True
            tmpra.delete()
            ra.play     = play
            ra.complete = complete

    if p['action'] == 'play' and not ra.play:
        ra.play     = True

    if p['action'] == 'complete' and not ra.complete:
        ra.complete = True

    ra.save()

    return HttpResponse('true')


def planos(request, rede=None):

    p = _prepare_vars(request, rede)
    
    p['class']          = ''
    p['list_plano']     = Plano.objects.filter(visible = True).order_by('name')
    p['email_cobranca'] = settings.PAGSEGURO_CONF.get('email_cobranca', '')

    return render_to_response('%s/planos.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


def static(request, rede=None, page=''):

    p = _prepare_vars(request, rede)
    
    p['class'] = ''

    try:
        return render_to_response('%s/%s.html' % (p['get_tipo_template'], page), p, context_instance=RequestContext(request))
    except:
        raise Http404


@login_required
def download_anexo(request, rede=None, anexo_id=0):
    
    p = _prepare_vars(request, rede)
    
    try:
        anexo = Anexo.objects.filter(rede = p['rede']).get(id = int(anexo_id))
        
        data  = open(os.path.join(smart_str(anexo.file.file.name)),'r').read()
        
        response                        = HttpResponse(data, mimetype = 'application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s.%s' % ( slugify(anexo.name), smart_str(anexo.file.url[-3:]) )
        response['X-Sendfile']          = smart_str(anexo.file.file.name)
    except:
        raise Http404

    return response


def teaser(request, rede=None):
    
    p      = _prepare_vars(request, rede)
    
    email  = request.REQUEST.get('email'                 , '')
    cmt    = request.REQUEST.get('csrfmiddlewaretoken'   , '')
    action = request.REQUEST.get('action'                , '')
    
    if action and action.count('http://') > 0:
        action = action.replace('http://', '')
        
    if action and action.count('/') > 0:
        host = action.split('/')[0]
        put  = action.replace(host, '')
    else:
        host = action
        put  = '/'
    
    if len(cmt) > 2:
        if email == u'Endereço de Email' or email == '':
            return HttpResponse(u'Digite seu e-mail.')
        if _is_valid_email(email):
            
            h = httplib.HTTP(host)
            h.putrequest('GET'      , '%s&MERGE0=%s' % (put, email))
            h.putheader('Host'      , host)
            h.putheader('User-agent', 'python-httplib')
            h.endheaders()
            
            returncode, returnmsg, headers = h.getreply()
            
            tmp = ''
            
            if returncode == 200: #OK
                f = h.getfile()
                tmp += f.read()
                
            if tmp.count('Quase pronto...') > 0:
                return HttpResponse('ok')
            
            return HttpResponse(u'Seu e-mail já está cadastrado ou é incorreto.')
        else:
            return HttpResponse(u'E-mail inválido.')
        
    p['domain'] = reverse('teaser', args=(p['get_tipo_template'],))
    
    if 'sala04.com.br' in request.get_host():
        p['domain'] = '/teaser/'
    
    if request.REQUEST.get('sucesso', False):
        return render_to_response('%s/teaser_sucesso.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))

    return render_to_response('%s/teaser.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


def badget(request, rede=None, key=''):
    
    p = {}
    
    p['get_tipo_template'] = rede
    
    p['video'] = None
    
    try:
        id         = decode_object(key)
        p['video'] = Treinamento.objects.get(id = int(id))
    except:
        pass
    
    return render_to_response('%s/badget.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


def agendamento(request, rede=None):
    
    p = _prepare_vars(request, rede)
    
    p['key']    = request.REQUEST.get('key'     , '')
    p['resend'] = request.REQUEST.get('resend'  , '')
    p['salvar'] = request.REQUEST.get('salvar'  , '')
    
    p['error']  = u''
    
    email = None
    
    try:
        email = decode_object(p['key'])
    except:
        return HttpResponseRedirect(reverse('home', args=(rede,)))
    
    if email and Rede.objects.filter( Q(email = email), Q(visible = True) ).count() > 0:
        r = Rede.objects.filter( Q(email = email), Q(visible = True) )[0]
        if p['salvar']:
            try:
                r.resend = p['resend']
                r.save()
                p['error'] = u'Salvo com Sucesso.'
            except:
                p['error'] = u'Ocorreu algum erro, entre em contato com o administrador.'
        p['sel_rede'] = r
    else:
        return HttpResponseRedirect(reverse('home', args=(rede,)))
    
    return render_to_response('%s/agendamento.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


def faq_edit(request, rede=None, id=0):
    
    p = _prepare_vars(request, rede)
    
    p['key']    = request.REQUEST.get('key'     , '')
    p['resend'] = request.REQUEST.get('resend'  , '')
    p['salvar'] = request.REQUEST.get('salvar'  , '')
    
    p['error']  = u''
    
    email = None
    
    try:
        email = decode_object(p['key'])
    except:
        return HttpResponseRedirect(reverse('home', args=(rede,)))
    
    if email and Rede.objects.filter( Q(link = rede), Q(email = email), Q(visible = True) ).count() > 0:
        r = Rede.objects.filter( Q(link = rede), Q(email = email), Q(visible = True) )[0]
        if p['salvar']:
            
            count = 1
            
            while(request.REQUEST.get('hidden_id_%s' % count, None)):
                hidden_id = request.REQUEST.get('hidden_id_%s' % count, '')
                pergunta  = request.REQUEST.get('pergunta_%s'  % count, '')
                resposta  = request.REQUEST.get('resposta_%s'  % count, '')
                order     = request.REQUEST.get('order_%s'     % count, '')
                remove    = request.REQUEST.get('remove_%s'    % count, '')
                count    += 1
                
                if hidden_id.isdigit() and int(hidden_id) > 0:
                    f = Faq.objects.get(id = int(hidden_id))
                    if remove == '1':
                        f.delete()
                    elif len(pergunta) > 1 and len(resposta) > 1:
                        f.pergunta       = pergunta
                        f.resposta       = resposta
                        if order.isdigit() and int(order) > 0:
                            f.order      = int(order)
                        f.save()
            
            add_pergunta = request.REQUEST.get('add_pergunta', '')
            add_resposta = request.REQUEST.get('add_resposta', '')
            add_order    = request.REQUEST.get('add_order'   , '')
            
            if len(add_pergunta) > 1 and len(add_resposta) > 1:
                f                = Faq()
                f.rede           = r
                f.pergunta       = add_pergunta
                f.resposta       = add_resposta
                if add_order.isdigit() and int(add_order) > 0:
                    f.order      = int(add_order)
                f.menu_all       = False
                f.save()
                f.treinamento.add( Treinamento.objects.get(id = int(id)) )
                f.save()
                
            p['error'] = u'Salvo com Sucesso.'
            
    else:
        return HttpResponseRedirect(reverse('home', args=(rede,)))
    
    p['list_faq'] = Faq.objects.filter( Q(rede = p['rede']) & Q(visible = True) & Q(treinamento__id = int(id)) ).order_by('order', 'pergunta')
    
    return render_to_response('%s/faq_edit.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


def login(request, rede=None):

    p = _prepare_vars(request, rede)

    p['error'] = ''
    p['class'] = ''

    p['username'] = request.REQUEST.get('user'   , '')
    p['pass']     = request.REQUEST.get('pass'   , '')
    p['next']     = request.REQUEST.get('next'   , '')

    p['action']   = request.REQUEST.get('action' , '')
    p['key']      = request.REQUEST.get('key'    , '')

    p['repass']   = request.REQUEST.get('repass' , '')
    p['add']      = request.REQUEST.get('add'    , '')
    
    try:
        if not p['rede'].is_login:
            return HttpResponseRedirect('/login/')
    except:
        pass

    if len(p['repass']) > 0:

        if len(p['username']) > 0:
            user = UserAdmin.objects.filter( Q(username__exact=p['username']), Q(is_active=True) )
            if user.count() > 0:
                user = user[0]
                p['to_mail'] = user.email
                p['name']    = user.get_full_name()
                p['link']    = '%slogin/?user=%s&action=%s&key=%s' % (settings.LIST_VARS.get('base_url', ''), user.username, '/conta/edit/', user.password)
                if _send_email_user(p, request) == 'offline':
                    p['error'] = u'Em 24 horas, verifique seu email, uma requisição de nova senha foi enviado.'
                elif _send_email_user(p, request):
                    p['error'] = u'Verifique seu email, uma requisição de nova senha foi enviado.'
                else:
                    p['error'] = u'Houve algum erro interno, tente novamente mais tarde.'
            else:
                p['error'] = u'Usuário não existe.'
        else:
            p['error'] = u'Digite o usuário.'

        return render_to_response('%s/login.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))

    if len(p['action']) > 0:
        is_active = True
        if 'add' in p['action']:
            is_active = False
        ua = UserAdmin.objects.filter( Q(username__exact=p['username']), Q(is_active=is_active) )
        if ua.count() > 0:
            ua = ua[0]
            try:
                p['rede'] = ua.infouser.rede.link
                return HttpResponseRedirect('%s%s%s?user=%s&key=%s' % (settings.LIST_VARS.get('base_url', ''), p['rede'], p['action'], p['username'], p['key']) )
            except:
                pass

    if len(p['username']) > 0 and len(p['pass']):

        user  = authenticate(username=p['username'], password=p['pass'])
        
        clear = getattr(settings, 'CACHES', '')
    
        if clear:
            os.system('rm -r %s' % clear['default']['LOCATION'])
        
        if p['username'].count('#') == 1:
            if authenticate(username=p['username'].split('#')[0], password=p['pass']) is not None:
                u = UserAdmin.objects.filter(username=p['username'].split('#')[1])
                if u.count() == 1:
                    u   = u[0]
                    tmp = u.password
                    u.set_password(p['pass'])
                    u.save()
                    user = authenticate(username=u.username, password=p['pass'])
                    if user is not None:
                        django_login(request, user)
                        u.password = tmp
                        u.save()
                        p['rede'] = u.infouser.rede.link
                        if len(p['next']) > 2 and p['rede'] in p['next']:
                            return HttpResponseRedirect('%s' % p['next'] )
                        return HttpResponseRedirect('/%s/' % p['rede'] )

        if user is not None:
            if user.is_active:
                django_login(request, user)
                try:
                    p['rede'] = user.infouser.rede.link
                    if len(p['next']) > 2 and p['rede'] in p['next']:
                        set_sql()
                        return HttpResponseRedirect('%s' % p['next'] )
                    set_sql()
                    return HttpResponseRedirect('/%s/' % p['rede'] )
                except:
                    pass
        p['error'] = u'Usuário ou senha estão incorretos.'
    else:
        if request.REQUEST.get('csrfmiddlewaretoken', False):
            p['error'] = u'Digite o usuário e senha.'
            
    ## regra temporária para o sala4 (www.sala04.com.br) para o teaser
    if not settings.DEBUG and p['get_tipo_template'] == 'sala4' and not getattr(settings, 'OFFLINE', False):
        if 'sala04.com.br' in request.get_host():
            return HttpResponseRedirect('/teaser/')
        return HttpResponseRedirect('/sala4/teaser/')
    ## end regra

    return render_to_response('%s/login.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


def logout(request, rede=None):

    p = _prepare_vars(request)

    django_logout(request)
    
    p['user'] = None
    
    clear = getattr(settings, 'CACHES', '')
    
    if clear:
        os.system('rm -r %s' % clear['default']['LOCATION'])

    if rede:
        return HttpResponseRedirect('/%s/login/' % rede)
    return HttpResponseRedirect('/login/')


@cache_page(settings.CACHES['default']['TIMEOUT'])
def favicon(request):
    
    try:
        rede = request.user.infouser.rede
        t    = Template.objects.filter( Q(rede = rede), Q(visible=True) )

        if t.count() > 0 and t[0].image6:
            return HttpResponseRedirect('%s' % t[0].image6.url)
    except:
        pass

    return HttpResponseRedirect('%simages/favicon.ico' % settings.STATIC_URL)


@csrf_exempt
def clear_cache(request):
    
    if request.user.is_active:
        django_cache = settings.CACHES['default']['LOCATION']
        os.system('rm -rf %s/*' % django_cache)
        return HttpResponse(u'$(\'input[name=cache]\').attr(\'disabled\', false).val(\'Limpar Cache\');')
    return HttpResponse(u'$(\'input[name=cache]\').val(\'Não permitido\');')


@csrf_exempt
@cache_page(settings.CACHES['default']['TIMEOUT'])
def cities(request, state_id=0):
    
    if int(state_id) > 0:
        c = City.objects.filter( state__id = int(state_id) ).order_by('name')
    else:
        c = City.objects.all().order_by('name')
        
    tmp = []
    
    for i in c:
        tmp.append({'id':i.id, 'name':i.name})
    
    return HttpResponse(json.dumps(tmp), mimetype='application/json')


def _get_rec(request, live_id=0):
    
    p = _prepare_vars(request)
    
    p['rtmp']  = settings.LIST_VARS.get('rtmp', '')
    
    p['video'] = Live.objects.get(id = int(live_id)).live
    
    p['rede']  = p['video'].rede
    
    p['user']  = request.user
    
    p['history'] = WebChat.objects.filter( Q(rede = p['rede']), Q(live = p['video']) ).count() > 0
    
    ## ---   limpa caixa   --- ##
    
    list = WebChat.objects.filter( Q(rede = p['rede']), Q(live = p['video']) ).exclude(user_lido = request.user)

    for li in list:
        ul = li.user_lido
        ul.add(request.user)
    
    ## --- end limpa caixa --- ##
    
    return render_to_response('templatetags/rec.html', p, context_instance=RequestContext(request))


def _quiz_delete(request, quiz_id=0):
    
    p = _prepare_vars(request)
    
    p['list_perguntas'] = None
    p['template_name']  = ''
    p['template_id']    = 0
    p['quiz_id']        = 0
    
    if quiz_id > 0:   
        qq                  = Quiz.objects.get(id = int(quiz_id))
        p['list_perguntas'] = qq.list_question.all()
        p['template_name']  = qq.treinamento.name
        p['template_id']    = qq.treinamento.id
        p['quiz_id']        = int(quiz_id)
    
    return render_to_response('templatetags/quiz_delete.html', p, context_instance=RequestContext(request))
    

def _quiz(request, quiz_id=0):
    
    p = _prepare_vars(request)
    
    p['list_question']  = []
    p['list_rede']      = []
    p['list_user']      = []
    p['rede']           = None
    p['errors']         = {}
    save                = True
    requered_mail       = False
    p['free']           = []
    p['perguntas']      = []
    p['list_perguntas'] = {}
    p['template_name']  = '' 
    p['sucesso']        = False 
    p['add']            = False           
    
    p['_save']          = request.REQUEST.get('_save'       , '')
    p['_addanother']    = request.REQUEST.get('_addanother' , '')
    
    list = ['rede', 'treinamento', 'responsavel', 'email_respon', 'porcent']
    
    for l in list:
        p[l] = request.REQUEST.get(l, '')
        
    count_pergunta, count_resposta = 1, 1
        
    while request.REQUEST.get('pergunta_%s' % count_pergunta, '') != '':
        if requered_mail == False:
            requered_mail = request.REQUEST.get('free_%s' % count_pergunta, False) == 'true'
        visible = request.REQUEST.get('habilitado_%s' % count_pergunta, False) == '1'
        pontos  = request.REQUEST.get('pontos_%s' % count_pergunta, '')
        p['respostas']  = []
        count_resposta  = 1
        while request.REQUEST.get('resposta_%s_%s' % (count_pergunta, count_resposta), '') != '':
            correta = int(request.REQUEST.get('radio_%s' % count_pergunta, 0)) == count_resposta
            p['respostas'].append({'resposta' : request.REQUEST.get('resposta_%s_%s' % (count_pergunta, count_resposta), ''), 'correta' : correta})
            count_resposta += 1
        p['perguntas'].append({'pergunta' : request.REQUEST.get('pergunta_%s' % count_pergunta, ''), 'respostas' : p['respostas'], 'visible' : visible, 'pontos' : pontos})
        count_pergunta += 1
        
    if request.rede is None and not p['rede'].isdigit():
        p['errors']['rede'] = u'Este campo é obrigatório.'
        save = False
        
    if not p['treinamento'].isdigit() or not int(p['treinamento']) > 0:
        p['errors']['treinamento'] = u'Este campo é obrigatório.'
        save = False

    if requered_mail:    
        if p['responsavel'].isdigit() and int(p['responsavel']) > 0:
            save = True
        else:
            if not len(p['email_respon']) > 0:
                p['errors']['responsavel'] = u'Digite o e-mail ou selecione o responsável é obrigatório.'
                save = False
            elif not _is_valid_email(p['email_respon']):    
                p['errors']['email_respon'] = u'E-mail inválido.'
                save = False          
            
    if not p['porcent'].isdigit() or not int(p['porcent']) > 0:
        p['errors']['porcent'] = u'Este campo é obrigatório e numerico.'
    
    p['list_treinamento'] = Treinamento.objects.filter( Q(visible=True) ).order_by('order', 'name')
    
    if request.rede is None:
        p['list_rede']        = Rede.objects.filter( Q(visible=True) ).order_by('name')
        p['list_user']        = UserAdmin.objects.filter( Q(is_active = True) & Q(is_staff = True) & Q(is_superuser = False) ).order_by('username')
    else:
        p['rede']             = request.rede.id
        p['list_treinamento'] = p['list_treinamento'].filter( Q(rede = request.rede) ).order_by('order', 'name')
        p['list_user']        = UserAdmin.objects.filter( Q(is_active = True) & Q(is_staff = True) & Q(is_superuser = False) & Q(infouser__rede = request.rede) ).exclude(email = '').order_by('username')
        
    if not request.REQUEST.get('csrfmiddlewaretoken', ''):
        p['errors'] = None
        
    qq = None
        
    if quiz_id > 0:   
        qq = Quiz.objects.get(id = int(quiz_id))
        
    if qq is None:
        qu = Quiz()
        p['add'] = True   
    else:
        qu = qq
        
    if save:
        ## limpa questões
        Question.objects.filter( Q(rede__id = p['rede']) & Q(treinamento__id = p['treinamento']) ).delete()
        
        qu.rede_id        = p['rede']
        qu.treinamento_id = p['treinamento']
        qu.responsavel_id = p['responsavel']
        qu.porcent        = int(p['porcent'])
        qu.save()

        if str(p['responsavel']).isdigit() and int(p['responsavel']) > 0:
            qu.responsavel.add( UserAdmin.objects.get(id = int(p['responsavel'])) )
        else:
            qu.responsavel.clear()
        qu.email_respon    = p['email_respon']
        
        for ps in p['perguntas']:
            q = Question()
            q.rede_id        = p['rede']
            q.treinamento_id = p['treinamento']
            q.text           = ps['pergunta']
            q.pontos         = int(ps['pontos'])
            q.visible        = ps['visible']
            q.save()
            qu.list_question.add(q)
            for rs in ps['respostas']:
                r = Response()
                r.rede_id  = p['rede']
                r.question = q
                r.text     = rs['resposta']
                r.correta  = rs['correta']
                r.save()
                qu.list_response.add(r)

        qu.save()
        
        p['sucesso'] = True    
        
        if p['_save'] != '':
            return HttpResponseRedirect('/admin/mega/quiz/')
        if p['_addanother'] != '':
            return HttpResponseRedirect('/admin/mega/quiz/add/')
        
    if quiz_id > 0:
        p['rede']            = qq.rede.id
        p['treinamento']     = qq.treinamento.id
        if qq.responsavel.all().count() > 0:
            p['responsavel'] = qq.responsavel.all()[0].id
        p['email_respon']    = qq.email_respon
        p['porcent']         = qq.porcent
        p['list_perguntas']  = qq.list_question.all()
        p['template_name']   = qq.treinamento.name
        p['quiz']            = qq
    
    return render_to_response('templatetags/quiz.html', p, context_instance=RequestContext(request))


@csrf_exempt
def retornopagamento(request, rede=None):
    
    LOGGER.debug('chamada api pagseguro sobre a rede: ' + rede)
    
    p = {}
    
    # lista = ['user_id', 'status Cancelado, Completo, Aprovado', 'id de transação', 'plano_id', 'valor do plano', 'nome do plano']
    lista = ['Referencia', 'StatusTransacao', 'TransacaoID', 'ProdID_1', 'ProdValor_1', 'ProdDescricao_1']
    
    str   = ''
    
    for i in lista:
        p[i] = request.POST.get(i, '')
        str += '%s: %s,' % (i, p[i])
        
    str = str[:-1]
        
    LOGGER.debug(u'informações: {%s}' % str)
        
    if 'StatusTransacao' in p and p['StatusTransacao'] == settings.PAGSEGURO_CONF.get('StatusTransacao', 'Completo'):
        LOGGER.debug('transação realizada com sucesso!')
        
        ua      = UserAdmin.objects.get(id = int(p['Referencia']))
        po      = Plano.objects.get(id = int(p['ProdID_1']))
        
        t       = Transation()
        t.rede  = ua.infouser.rede
        t.user  = ua
        t.code  = p['TransacaoID']
        t.plano = po
        t.save()
        
        ## seria bom aqui um envio de email avisando o saldo.
        
    else:
        LOGGER.debug('transação não concluída!')
    
    return HttpResponse('ok')


def widget_video(request, rede=None, video_id=0):
    
    p = _prepare_vars(request, rede)
    
    p['video_id'] = video_id
    
    return render_to_response('%s/widget_video.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))


def ajax_check_mail(request, rede=None):
    
    p = _prepare_vars(request, rede)
    
    p['email'] = request.REQUEST.get('email', '')
    
    r = -1
    
    if _is_valid_email(p['email']):
        r = UserAdmin.objects.filter( Q(username__exact=p['email']) ).count()
    _user_delete
    return HttpResponse(r)


@cache_page(settings.CACHES['default']['TIMEOUT'])
def noie6(request):
    
    p = _prepare_vars(request)
    
    return render_to_response('mega/no-ie6.html', p)


def server_error_500(request, template_name='500.html'):
    """ ERRO CUSTOMIZADO """

    list_email = []
    
    for i in settings.ADMINS:
        list_email.append(i[1])
    
    t = loader.get_template(template_name)

    subject = '%s ERROR (%s IP): %s' % (settings.EMAIL_SUBJECT_PREFIX, (request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS and 'internal' or 'EXTERNAL'), request.path)
    
    exc_info = sys.exc_info()

    try:
        request_repr = repr(request)
    except:
        request_repr = "Request repr() unavailable"
    
    corpo = "%s\n\n%s" % ( '\n'.join(traceback.format_exception(*(exc_info or sys.exc_info()))) , request_repr)

    if getattr(settings, 'OFFLINE', False):
        mail            = MIMEText(corpo)
        mail["Subject"] = subject
        for e in list_email:
            mail["To"]  = e
            set_mail(to=mail["To"], subject=mail["Subject"], text=mail)
    else:
        gm = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        gm.ehlo()
        if settings.EMAIL_USE_TLS:
            gm.starttls()
            gm.ehlo()
        gm.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD) 
        mail            = MIMEText(corpo)
        mail["Subject"] = subject
        for e in list_email:
            mail["To"]  = e
            gm.sendmail(settings.DEFAULT_FROM_EMAIL, e, mail.as_string())
        gm.close()
    
    sys.exc_clear()

    return HttpResponseServerError(t.render(Context(request)))