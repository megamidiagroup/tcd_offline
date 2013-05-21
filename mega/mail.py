# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.template.defaultfilters import date as default_date
from django.core.urlresolvers import reverse

try:
    from django.core.validators import email_re
except:
    from django.forms.fields import email_re

from django.core.mail import send_mail, EmailMessage, BadHeaderError

from templatetags.util import encode_object

from datetime import datetime

from sql_offline import set_mail


def _is_valid_email(email):
    if email_re.match(email):
        return True
    else:
        return False
    

def _send_email_user(p, request):

    from_email   = settings.LIST_VARS.get('from_email', '')
    
    subject      = u'O TCD comunica mudanças nas informações do cadastro'
    
    if not 'get_tipo_template' in p:
        p['get_tipo_template'] = 'mega'
    elif p['get_tipo_template'] == 'sala4':
        subject  = u'Sala#04 comunica mudanças nas informações do cadastro'
        
    p['host']    = request.get_host()

    html_msg     = render_to_string('%s/mail/send_email_user.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))

    text_content = strip_tags(html_msg)
    html_content = html_msg
    msg          = EmailMultiAlternatives(subject, text_content, from_email, [p['to_mail']])
    msg.attach_alternative(html_content, "text/html")
    
    if getattr(settings, 'OFFLINE', False):
        set_mail(to=p['to_mail'], subject=subject, text=html_content)
        return 'offline'
    else:
        try:
            msg.send()
            return True
        except BadHeaderError:
            return False
    
    
def _send_email_free_question_responsavel(p, request):
    
    from_email   = settings.LIST_VARS.get('from_email', '')
    
    subject      = u'O TCD comunica que há um questionário para ser avaliado'
    
    if not 'get_tipo_template' in p:
        p['get_tipo_template'] = 'mega'
    elif p['get_tipo_template'] == 'sala4':
        subject  = u'Sala#04 comunica que há um questionário para ser avaliado'
        
    p['host']    = request.get_host()

    html_msg     = render_to_string('%s/mail/send_email_free_question_responsavel.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))

    text_content = strip_tags(html_msg)
    html_content = html_msg
    msg          = EmailMultiAlternatives(subject, text_content, from_email, [p['to_mail']])
    msg.attach_alternative(html_content, "text/html")
    
    if getattr(settings, 'OFFLINE', False):
        set_mail(to=p['to_mail'], subject=subject, text=html_content)
        return 'offline'
    else:
        try:
            msg.send()
            return True
        except BadHeaderError:
            return False
    

def _send_email_free_question_user(p, request, aprovado):

    from_email    = settings.LIST_VARS.get('from_email', '')
    
    subject       = u'O TCD comunica que seu questionário foi avaliado'
    
    if not 'get_tipo_template' in p:
        p['get_tipo_template'] = 'mega'
    elif p['get_tipo_template'] == 'sala4':
        subject   = u'Sala#04 comunica que seu questionário foi avaliado'
        
    p['host']     = request.get_host()
    
    p['aprovado'] = aprovado

    html_msg      = render_to_string('%s/mail/send_email_free_question_user.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))

    text_content  = strip_tags(html_msg)
    html_content  = html_msg
    msg           = EmailMultiAlternatives(subject, text_content, from_email, [p['to_mail']])
    msg.attach_alternative(html_content, "text/html")
    
    if getattr(settings, 'OFFLINE', False):
        set_mail(to=p['to_mail'], subject=subject, text=html_content)
        return 'offline'
    else:
        try:
            msg.send()
            return True
        except BadHeaderError:
            return False
    

def _send_email_pontos(p, request):

    from_email   = settings.LIST_VARS.get('from_email', '')
    
    if not 'get_tipo_template' in p:
        p['get_tipo_template'] = 'mega'

    html_msg     = render_to_string('%s/mail/send_email_pontos.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))

    subject      = u'Solicitação dos seus pontos por email.'
    text_content = strip_tags(html_msg)
    html_content = html_msg
    msg          = EmailMultiAlternatives(subject, text_content, from_email, [p['to_mail']])
    msg.attach_alternative(html_content, "text/html")

    if getattr(settings, 'OFFLINE', False):
        set_mail(to=p['to_mail'], subject=subject, text=html_content)
        return 'offline'
    else:
        try:
            msg.send()
            return True
        except BadHeaderError:
            return False


def _send_email_extrato(p, request):

    from_email   = settings.LIST_VARS.get('from_email', '')
    
    if not 'get_tipo_template' in p:
        p['get_tipo_template'] = 'mega'

    html_msg     = render_to_string('%s/mail/send_email_extrato.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))

    subject      = u'Extrato do certificado de treinamento.'
    text_content = strip_tags(html_msg)
    html_content = html_msg
    msg          = EmailMultiAlternatives(subject, text_content, from_email, [p['to_mail']])
    msg.attach_alternative(html_content, "text/html")

    if getattr(settings, 'OFFLINE', False):
        set_mail(to=p['to_mail'], subject=subject, text=html_content)
        return 'offline'
    else:
        try:
            msg.send()
            return True
        except BadHeaderError:
            return False
        
        
def _send_email_extrato_pdf(p, request):

    from_email   = settings.LIST_VARS.get('from_email', '')
    
    if not 'get_tipo_template' in p:
        p['get_tipo_template'] = 'mega'
        
    p['link']    = 'https://www.treinandoequipes.com.br/%s/get_certificado/%s/?id=%s&key=%s' % (p['rede'].link, p['tipo'], encode_object(request.user.username), p['key'])

    html_msg     = render_to_string('%s/mail/send_email_extrato_pdf.html' % p['get_tipo_template'], p, context_instance=RequestContext(request))

    subject      = u'TCD - Certificado para download.'
    text_content = strip_tags(html_msg)
    html_content = html_msg
    msg          = EmailMultiAlternatives(subject, text_content, from_email, [p['to_mail']])
    msg.attach_alternative(html_content, "text/html")

    if getattr(settings, 'OFFLINE', False):
        set_mail(to=p['to_mail'], subject=subject, text=html_content)
        return 'offline'
    else:
        try:
            msg.send()
            return True
        except BadHeaderError:
            return False
    
    
def _send_email_suggestion(s, p):
    
    content = u'<h2>Olá %s, segue abaixo a sugestão ou dúvida:</h2>' % p['rede'].name
    
    content += u'Usuário          : <b>%s, %s</b> <br /> '                  % (s.user.get_full_name(), s.user.email)
    content += u'Treinamento      : <b><a href="%s%s">%s</a></b> <br /> '   % (settings.LIST_VARS.get('base_url', '')[:-1], reverse('treinamento', args=(p['rede'].link, s.treinamento.id,)), s.treinamento.name)
    content += u'Mensagem         : <b>%s</b> <br /> '                      % s.mensagem
    content += u'Data da mensagem : <b>%s</b> <br /> '                      % default_date(s.date, 'd/m/Y à\s H:i')
    content += u'<br />'
    
    s.enviado   = True
    s.date_send = datetime.now()
    s.save()

    content += u'-------------------------------------------------------------------------------- <br /><br />'

    content += u'<h6>Caso deseje modificar o envio desse e-mail ou cancelar <a href="%s%s?key=%s">clique aqui</a></h6>' % ( settings.LIST_VARS.get('base_url', '')[:-1], reverse('agendamento', args=(p['rede'].link,)), encode_object(p['rede'].email) )
    
    em = EmailMessage(u'Você acaba de receber novas mensagens de Sugestão e Dúvidas - %s' % default_date(datetime.now(), 'd/m/Y'), content, str(settings.MEGAVIDEO_CONF['email']), [p['rede'].email], [settings.ADMINS[0][1]])
    em.content_subtype = "html"
    
    if getattr(settings, 'OFFLINE', False):
        set_mail(to=settings.ADMINS[0][1], subject=u'Você acaba de receber novas mensagens de Sugestão e Dúvidas - %s' % default_date(datetime.now(), 'd/m/Y'), text=content)
        return 'offline'
    else:
        try:
            em.send()
            return True
        except BadHeaderError:
            return False
    
    
def _send_email_faq(s, p):
    
    content = u'<h2>Olá %s, segue abaixo a pergunta sobre o treinamento:</h2>' % p['rede'].name
    
    content += u'Usuário          : <b>%s, %s</b> <br /> '                  % (s.user.get_full_name(), s.user.email)
    content += u'Treinamento      : <b><a href="%s%s">%s</a></b> <br /> '   % (settings.LIST_VARS.get('base_url', '')[:-1], reverse('treinamento', args=(p['rede'].link, s.treinamento.id,)), s.treinamento.name)
    content += u'Mensagem         : <b>%s</b> <br /> '                      % s.mensagem
    content += u'Data da mensagem : <b>%s</b> <br /> '                      % default_date(s.date, 'd/m/Y à\s H:i')
    content += u'<br />'
    
    s.enviado   = True
    s.date_send = datetime.now()
    s.save()

    content += u'-------------------------------------------------------------------------------- <br /><br />'

    content += u'<h6>Caso deseje você mesmo modificar ou adicionar o faq do treinamento <a href="%s%s?key=%s">clique aqui</a></h6>' % ( settings.LIST_VARS.get('base_url', '')[:-1], reverse('faq_edit', args=(p['rede'].link, s.treinamento.id,)), encode_object(p['rede'].email) )

    content += u'<h6>Caso deseje modificar o envio desse e-mail ou cancelar <a href="%s%s?key=%s">clique aqui</a></h6>' % ( settings.LIST_VARS.get('base_url', '')[:-1], reverse('agendamento', args=(p['rede'].link,)), encode_object(p['rede'].email) )
    
    em = EmailMessage(u'Você acaba de receber novas mensagens de perguntas sobre treinamentos - %s' % default_date(datetime.now(), 'd/m/Y'), content, str(settings.MEGAVIDEO_CONF['email']), [p['rede'].email], [settings.ADMINS[0][1]])
    em.content_subtype = "html"
    
    if getattr(settings, 'OFFLINE', False):
        set_mail(to=settings.ADMINS[0][1], subject=u'Você acaba de receber novas mensagens de perguntas sobre treinamentos - %s' % default_date(datetime.now(), 'd/m/Y'), text=content)
        return 'offline'
    else:
        try:
            em.send()
            return True
        except BadHeaderError:
            return False



def _send_email_robot(p, request, to, subject, text):
    
    if not _is_valid_email( to ):
        return False

    from_email   = settings.LIST_VARS.get('from_email', '')
    html_msg     = text

    text_content = strip_tags(html_msg)
    html_content = html_msg
    msg          = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        return True
    except BadHeaderError:
        pass
        
    return False