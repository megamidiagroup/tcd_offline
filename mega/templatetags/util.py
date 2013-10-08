# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import Library
from django.conf import settings
from django.conf.urls.defaults import include, patterns, url
from django.db.models import Q, Sum
from django.utils.safestring import mark_safe
from django.utils.safestring import SafeString
from django.template.defaultfilters import striptags, stringfilter
from django.utils.html import strip_spaces_between_tags

try:
    from django.core.validators import email_re
except:
    from django.forms.fields import email_re

from mega.models import *

from datetime import datetime, timedelta
from math import ceil

import base64
import pickle
import os
import re

RE_MULTISPACE = re.compile(r"\s{2,}")
RE_NEWLINE = re.compile(r"\n")

register  = Library()

def _is_valid_email(email):
    if email_re.match(email):
        return True
    else:
        return False
    
    
@register.filter()
@stringfilter
def trim(value):
    return value.strip()


@register.filter()
@stringfilter
def compress_html(value, html=1):
    ssbt = strip_spaces_between_tags(value.strip())
    ssbt = RE_MULTISPACE.sub(" ", ssbt)
    ssbt = RE_NEWLINE.sub("", ssbt)
    if html == 0:
        ssbt = striptags( ssbt )
    return ssbt


@register.filter()
def get_image(obj):
    ''' Get image para testes '''

    try:
        if obj[0].image:
            return '%s../%s' % (settings.STATIC_URL, str(obj[0].image))
    except:
        try:
            if obj.image:
                return '%s../%s' % (settings.STATIC_URL, str(obj.image))
        except:
            pass
    
    return ''


@register.filter()
def get_image_crop(images, size=''):

    try:
        return settings.MEDIA_STATIC + str(images[0].image)
    except:
        try:
            return settings.MEDIA_STATIC + str(images.image)
        except:
            return ''
        return ''


@register.filter()
def get_image_crop_small(images, size=''):

    try:
        return settings.MEDIA_STATIC + str(images[0].image_small)
    except:
        try:
            return settings.MEDIA_STATIC + str(images.image_small)
        except:
            return ''
        return ''


@register.filter()
def get_image_crop_thumb(images, size=''):

    try:
        if images[0].image_thumb:
            return settings.MEDIA_STATIC + str(images[0].image_thumb)
        else:
            return settings.MEDIA_STATIC + str(images[0].image)
    except:
        try:
            if images.image_thumb:
                return settings.MEDIA_STATIC + str(images.image_thumb)
            else:
                return settings.MEDIA_STATIC + str(images.image)
        except:
            return ''
        return ''


@register.filter()
def super_truncatewords(word, num):
    """ o super_truncatewords limita palavras como o truncatewords do django + limitador de caracter máximo """

    max_words = ''
    count = trunc = char = 0

    try:
        if num.count('-') > 0:
            trunc = int(num.split('-')[0])
            char  = int(num.split('-')[1])
        else:
            trunc = int(num)
    except:
        pass

    if word.count(' ') > 0:
        for i in word.split(' '):
            if count < trunc:
                max_words += i + ' '
                count += 1
            else:
                break
    else:
        max_words = word


    if char > 0 and len(max_words) > char:
        max_words = max_words[0:char] + ' ...'
    else:
        if len(word) > len(max_words):
            max_words += ' ...'

    return max_words


@register.filter()
def logo(rede, tipo_template='mega'):
    ''' Retorna a imagem da rede ou a imagem default do sistema. '''

    try:
        return '%s%s/../../%s' % (settings.STATIC_URL, tipo_template, str(rede.logo))
    except:
        pass

    return '%s%s/%s' % (settings.STATIC_URL, tipo_template, str('images/logo.png'))


@register.filter()
def logo_log(rede, tipo_template='mega'):
    ''' Retorna a imagem da rede ou a imagem default do sistema. '''

    try:
        if rede.logo_log:
            return '%s%s/../../%s' % (settings.STATIC_URL, tipo_template, str(rede.logo_log))
    except:
        pass

    return logo(rede, tipo_template=tipo_template)


@register.inclusion_tag('templatetags/sub_menu.html')
def sub_menu(list_category, rede, list_treinamento=None, list_anexo=None, last_item=1):

    p = {}

    p['rede']     = rede
    p['atual']    = {'id' : 0}

    list_link = []

    if list_category and list_category.count() > 0:
        reverse_category(list_category, list_link)
        if len(list_link) > 0:
            p['atual'] = list_category[0].parent
        list_link = list_link[1:]
    elif list_treinamento and list_treinamento.count() > 0:
        reverse_category(list_treinamento[0].category, list_link)
        if len(list_link) > 0:
            p['atual'] = list_treinamento[0].category
    elif list_anexo and list_anexo.count() > 0:
        reverse_category(list_anexo[0].category, list_link)
        if len(list_link) > 0:
            p['atual'] = list_anexo[0].category

    if last_item == 3:
        last_item = 1
    else:
        list_link += [{'name' : 'Home'}]

    if not p['atual'] and getattr(list_treinamento, 'count', False) and list_treinamento.count() > 0:
        p['atual'] = list_treinamento[0].category

    list_link.reverse()

    p['list_link'] = list_link
    p['last_item'] = last_item

    return p


@register.inclusion_tag('templatetags/sub_menu.html')
def sub_menu_treinamento(list_video, rede):

    p = {}

    p['rede']     = rede
    p['atual']    = None

    list_link     = []
    list_category = None

    if list_video.count() > 0:
        list_category = Category.objects.filter( id = list_video[0].category_id )

    if list_category.count() > 0:
        list_link.append(list_category[0])
        reverse_category(list_category, list_link)
        if len(list_link) > 0:
            p['atual'] = list_video[0]
        list_link = list_link

    list_link += [{'name' : 'Home'}]

    list_link.reverse()

    p['list_link'] = list_link

    return p


@register.inclusion_tag('templatetags/videos_relacionados.html')
def videos_relacionados(list_video, rede, user=None):

    p = {'rede' : rede, 'user' : user}

    if list_video.count():
        list_video      = list_video[0]
        p['list_video'] = Treinamento.objects.filter( Q(visible = True) & Q(rede = rede) & Q(category = list_video.category) ).exclude(id = list_video.id).order_by('order', 'name')

    return p


@register.inclusion_tag('templatetags/brightcove.html')
def brightcove(rede, code, id, w='640', h='360'):

    return {'rede' : rede, 'code' : code, 'id' : id, 'w' : w, 'h' : h}


@register.inclusion_tag('templatetags/kaltura.html')
def kaltura(rede, code, id, w='640', h='360'):

    return {'rede' : rede, 'code' : code, 'id' : id, 'w' : w, 'h' : h}


@register.inclusion_tag('templatetags/megavideo.html', takes_context = True)
def megavideo(context, rede, code, id, w='640', h='360', logo_url='', logo_link=''):

    base_url = [settings.MEGAVIDEO_CONF.get('base_url', ''), 'https://www.treinandoequipes.com.br/megavideo/'][settings.DEBUG]

    if len(logo_url) > 1 and logo_url.count('http') == 0:
        logo_url = settings.STATIC_URL + logo_url

    return {'rede' : rede, 'code' : code, 'id' : id, 'w' : w, 'h' : h, 'base_url' : base_url, 'logo_url' : logo_url, 'logo_link' : logo_link}


@register.inclusion_tag('templatetags/live.html')
def live(rede, get_tipo_template, code, video, gm):

    return {'rede' : rede, 'get_tipo_template' : get_tipo_template, 'code' : code, 'id' : video.id, 'STATIC_URL' : settings.STATIC_URL, 'rtmp': settings.LIST_VARS.get('rtmp', ''), 'get_mobile': gm, 'image': video.image}


def reverse_category(cat, list_link):

    try:
        cat = cat[0]
    except:
        pass
    
    try:
        if cat:
            list_link.append(cat.parent)
        return reverse_category(cat.parent, list_link)
    except:
        pass

    return False



@register.filter()
def is_question(video, user):

    q = Quiz.objects.filter( Q(treinamento = video) & Q(relatorioavalicao__isnull = False) & Q(relatorioavalicao__user = user) ).distinct()

    if q.count() > 0:
        return False

    return Quiz.objects.filter( Q(treinamento = video) )


@register.filter()
def datetreinamento(video, user):

    q = Quiz.objects.filter( Q(treinamento = video) & Q(relatorioavalicao__isnull = False) & Q(relatorioavalicao__user = user) ).distinct()

    return q[0].relatorioavalicao_set.all()[0].date


@register.filter()
def pontostreinamento(video, user):

    q = Quiz.objects.filter( Q(treinamento = video) & Q(relatorioavalicao__isnull = False) & Q(relatorioavalicao__user = user) ).distinct()

    return q[0].relatorioavalicao_set.all()[0].pontos


@register.filter()
def base64encode(value):

    bs = base64.urlsafe_b64encode(str(value))
    bs = base64.urlsafe_b64encode(str(bs))

    return bs


@register.filter()
def base64decode(value):

    bs = base64.urlsafe_b64decode(str(value))
    bs = base64.urlsafe_b64decode(str(bs))

    return bs


def list_id_certificado(key):

    c = []

    if not key[:-1]:
        return []

    for i in key[:-1].split('-'):
        try:
            c.append(base64decode(i))
        except:
            return []

    return c


@register.filter()
def favicon(rede):

    try:
        return Template.objects.filter( Q(rede = rede) & Q(visible=True) )[0].image6.url
    except:
        return settings.STATIC_URL + '/images/favicon.ico'


@register.filter()
def list_treinamento(c):

    return c.treinamento.filter(visible=True)


@register.filter()
def get_is_treinamento_check(t, user):

    return RelatorioAvalicao.objects.filter( Q(user = user) & Q(quiz__treinamento = t) ).count()


@register.filter()
def porcent_certificado(c, user):

    total = c.treinamento.filter( Q(visible=True) ).count()
    parte = RelatorioAvalicao.objects.filter( Q(rede = c.rede) & Q(user = user) & Q(quiz__treinamento__visible = True) & Q(quiz__treinamento__certificado = c) ).distinct().count()

    try:
        return int((float(parte) / float(total)) * 100)
    except:
        return 0


@register.filter()
def porcent_aproveitamento(list, user, complete=True):

    porcent = 0.0
    total   = list.count()

    for l in list:
        porcent    += float( 1.0 / total )
        is_question = Question.objects.filter( Q(visible = True) & Q(treinamento = l) ).count() > 0
        if is_question:
            if complete:
                div = float(1) / 3
            else:
                div = float(1) / 2
        else:
            if complete:
                div = float(1) / 2
            else:
                div = float(1)

        ## verifica se passou
        lista = l.relatoriotentativa_set.filter( Q(rede = l.rede) & Q(user = user) ).distinct()
        for i in lista:
            if i.aprovado:
                porcent -= float( float(div) / total )

        ## verifica se viu até o fim
        ra = l.relatorioacoes_set.filter( Q(rede = l.rede) & Q(user = user) ).distinct().order_by('-complete')

        if ra.count() > 0:
            ra = ra[0]
            if ra.play:
                porcent -= float( float(div) / total )
            if ra.complete and complete:
                porcent -= float( float(div) / total )

    try:
        return int( float(1 - porcent) * 100)
    except:
        return 0


@register.filter()
def porcent_aproveitamento_not_complete(list, user):
    """ criado especialmente para o projeto sala4 """

    return porcent_aproveitamento(list, user, complete=False)


@register.filter()
def aproveitamento_append(treinamento, user):

    is_question = Question.objects.filter( Q(visible = True) & Q(treinamento = treinamento) ).count() > 0

    if is_question:
        ## verifica se passou
        list = treinamento.relatoriotentativa_set.filter( Q(rede = treinamento.rede) & Q(user = user) ).distinct()
        for i in list:
            if i.aprovado:
                return False
        return True
    else:
        ## verifica se viu até o fim
        try:
            is_ra = treinamento.relatorioacoes_set.filter( Q(rede = treinamento.rede) & Q(user = user) ).distinct().order_by('-complete')
            if is_ra:
                return treinamento.relatorioacoes_set.filter( Q(rede = treinamento.rede) & Q(user = user) & ( Q(play = False) | Q(complete = False) ) ).distinct().count() > 0
            else:
                return True
        except:
            pass

    return True


@register.inclusion_tag('templatetags/aproveitamento_status.html')
def aproveitamento_status(treinamento, user, title=0):

    play, complete, question = False, False, False

    q_count = Question.objects.filter( Q(rede = treinamento.rede) & Q(visible = True) & Q(treinamento = treinamento) ).count()

    if q_count == 0:
        question = True

    ## verifica se viu até o fim
    trei = treinamento.relatorioacoes_set.filter( Q(rede = treinamento.rede) & Q(user = user) ).distinct().order_by('-complete')

    if trei.count() > 0:
        trei     = trei[0]
        play     = trei.play
        complete = trei.complete

    str_title = ''

    if title == 1:
        if not play:
            str_title += u'Você não visualizou o vídeo. Visualize o vídeo até o fim para melhor aproveitamento.'
        elif not complete:
            str_title += u'Você não visualizou o vídeo até o fim. Visualize o vídeo até o fim para melhor aproveitamento.'
        elif not question:
            str_title += u'Você não realizou o teste, visualize o video até o fim que o botão (fazer o teste) irá aparecer.'

    return {'play' : play, 'view' : complete, 'question' : question, 'title' : str_title}


@register.inclusion_tag('templatetags/aproveitamento_count_append.html')
def aproveitamento_count_append(list_treinamento, user):

    count = 0

    for treinamento in list_treinamento:

        if aproveitamento_append(treinamento, user):
            count += 1

    return {'count' : count}


@register.filter()
def tipobusca(obj):

    return obj.filter(tipo = 'S').count() > 0


@register.filter()
def sexo(obj):

    try:
        return dict(CHOICE_SEXO)[obj.sexo]
    except:
        pass

    return ''


@register.filter()
def humanizeboolean(bool):

    if bool == True:
        return u'Sim'
    elif bool == False:
        return u'Não'

    return ''


@register.filter()
def lenght(value):

    try:
        return len(value.strip())
    except:
        pass

    return 0


@register.filter()
def css_hiraquia_cat(cat):

    list_link = []

    reverse_category(cat, list_link)

    return 'custom-category%d' % len(list_link)


@register.filter()
def css_hiraquia_video(video):

    list_link = []

    reverse_category(video.category, list_link)

    return 'custom-category%d' % ( len(list_link) + 1 )


@register.filter()
def filter_menu(list_menu, name='sair'):

    return list_menu.filter( Q(visible = True) & Q(name = name) ).count() > 0


@register.filter()
def get_icone(rede, tipo):

    path = '%s/%s/media/%s/images/icone_%s.png' % (settings.MODPATH, tipo, tipo, rede.link)

    if os.path.exists(path):
        return '%s%s/images/icone_%s.png' % (settings.STATIC_URL, tipo, rede.link)

    return ''


@register.filter()
def count_video_category(category):

    return Treinamento.objects.filter( Q(category = category) & Q(visible = True) ).count()


@register.filter()
def count_videos_per_user_assistido(rede, user):

    return RelatorioAcoes.objects.filter( Q(rede = rede) & Q(user = user) & ( Q(play = True) | Q(complete = True) ) ).distinct().count()


@register.filter()
def count_videos_per_rede(rede):

    return Treinamento.objects.filter( Q(rede = rede) ).count()


@register.filter()
def list_category_treinamentos(c):

    return Treinamento.objects.filter( Q(category = c) & Q(visible = True) ).order_by('order', 'name')


@register.filter()
def count_category_category(category):

    return category.category_set.filter(visible = True).count()


@register.filter()
def list_category_category(category):

    return category.category_set.filter(visible = True).order_by('order', 'name')


@register.filter()
def encode_object(obj):

    return base64.b64encode( pickle.dumps(obj) )

@register.filter()
def decode_object(string):

    return pickle.loads( base64.b64decode(string) )


@register.filter()
def is_responder(obj, respostas):

    try:
        return respostas['res_%s' % obj.id]
    except:
        pass

    return False


@register.filter()
def total_pontos(obj):

    return obj.aggregate(total=Sum('pontos'))['total']


@register.filter()
def is_not_video(obj):

    if obj.tipo_t == 1:
        return 'elearning'

    return 'treinamento'


@register.inclusion_tag('templatetags/bloco_home_sala4.html')
def bloco_home_sala4(cats, rede=None, limit=0):

    if cats.count() > 0:
        cats = cats[0]

    categorias = cats.category_set.filter(visible = True).order_by('order')

    if limit > 0:
        try:
            categorias = categorias[0:limit]
        except:
            categorias = categorias

    return {'list' : categorias, 'rede' : rede, 'STATIC_URL' : settings.STATIC_URL}


@register.inclusion_tag('templatetags/bloco_list_videos_sala4.html')
def bloco_list_videos_sala4(video=None, rede=None, get_tipo_template='', video_id=0, user=None):

    list_videos = Treinamento.objects.filter( Q(rede = rede) & Q(visible=True) & Q(category = video.category) ).order_by('order', 'name')

    return {'list_videos' : list_videos, 'rede' : rede, 'STATIC_URL' : settings.STATIC_URL, 'get_tipo_template' : get_tipo_template, 'video_id' : video_id, 'user' : user}


@register.filter()
def alphanumeric(id):

    alphabetic = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    try:
        return alphabetic[id].lower()
    except:
        pass

    return u'Error'


@register.filter()
def category_master(rede):

    list_category = Category.objects.filter( Q(visible = True) & Q(rede = rede) & Q(parent__isnull = True) ).order_by('order', 'name')

    if list_category.count() > 0:
        return list_category[0].id

    return 0


@register.filter()
def duration_time_resume(time):

    try:
        if time.count('minuto') > 0:
            time = time.split('uto')[0] + '.'
    except:
        pass

    return time


@register.filter()
def is_aprovado(treinamento, user=None):

    rt = RelatorioTentativa.objects.filter( Q(treinamento = treinamento) & Q(user = user) )

    if rt.count() > 0:
        rt = rt[0]
        return rt.aprovado

    return False


@register.filter()
def date_assistido(treinamento, user=None):

    ra = treinamento.relatorioacoes_set.filter( Q(user = user) & ( Q(play = True) | Q(complete = True) ) ).distinct().order_by('-complete')

    if ra.count() > 0:
        ra = ra[0]
        return ra.date

    return False


@register.filter()
def count_videos_assistido(treinamento, user=None):

    return RelatorioAcoes.objects.filter( Q(video__in = treinamento) & Q(user = user) & ( Q(play = True) | Q(complete = True) ) ).distinct().count()


@register.inclusion_tag('templatetags/dashboard.html')
def dashboard(rede, user, get_tipo_template):

    p = {}

    p['user']              = user
    p['rede']              = rede
    p['get_tipo_template'] = get_tipo_template
    p['STATIC_URL']        = settings.STATIC_URL

    p['list_category']     = Category.objects.filter( Q(visible = True) & Q(rede = rede) & Q(parent__isnull = True) ).order_by('order', 'name')

    p['list_pagamento']    = Transation.objects.filter( Q(rede = rede) & Q(user = user) & Q(visible = True) )

    return p


@register.filter()
def is_quiz(treinamento, user):

    try:
        if treinamento.count() > 0:
            treinamento = treinamento.order_by('order', 'name')[0]
    except:
        pass

    if treinamento:
        if treinamento.relatoriotentativa_set.filter( Q(user = user) & Q(aprovado = True) ).count() > 0:
            return False

        try:
            if Response.objects.filter( question = Question.objects.filter( Q(treinamento = treinamento) & Q(visible = True) )[0] ).count() > 0:
                return True
        except:
            pass

    return False


@register.filter()
def barran(value):

    try:
        return SafeString( re.sub('\s+', ' ', mark_safe(value).replace('\n', '')) )
    except:
        pass

    return re.sub('\s+', ' ', mark_safe(value).replace('\n', ''))


@register.filter()
def get_certificado(treinamento, image=False):

    cers = treinamento.certificado_set.filter(visible = True)

    if cers.count() > 0:
        if image:
            return '%s../%s' % (settings.STATIC_URL, str(cers[0].image))
        return cers[0]

    return cers


@register.filter()
def filter_search(value, rep=''):

    try:
        return value.replace('%s', '%s' % rep)
    except:
        pass

    return value


@register.filter()
def replace(value, rep=''):

    try:
        return value.replace('%s' % rep, '')
    except:
        pass

    return value


@register.filter()
def get_free_response(question, user):

    fr = FreeResponse.objects.filter( Q(rede = question.rede) & Q(question = question) & Q(user = user) )

    if fr.count() > 0:
        return fr[0].text

    return ''


@register.filter()
def nota(count, notas):

    try:
        return notas[count]
    except:
        pass

    return []


@register.filter()
def list_option_enquete(le, obj=0):

    lista        = []
    lista_object = []

    if len(le.opcao1) > 1:
        lista.append(le.opcao1)
        lista_object.append({'opcao' : le.opcao1, 'n_opcao' : le.n_opcao1})
    if len(le.opcao2) > 1:
        lista.append(le.opcao2)
        lista_object.append({'opcao' : le.opcao2, 'n_opcao' : le.n_opcao2})
    if len(le.opcao3) > 1:
        lista.append(le.opcao3)
        lista_object.append({'opcao' : le.opcao3, 'n_opcao' : le.n_opcao3})
    if len(le.opcao4) > 1:
        lista.append(le.opcao4)
        lista_object.append({'opcao' : le.opcao4, 'n_opcao' : le.n_opcao4})
    if len(le.opcao5) > 1:
        lista.append(le.opcao5)
        lista_object.append({'opcao' : le.opcao5, 'n_opcao' : le.n_opcao5})
    if len(le.opcao6) > 1:
        lista.append(le.opcao6)
        lista_object.append({'opcao' : le.opcao6, 'n_opcao' : le.n_opcao6})

    if obj != 0:
        return lista_object

    return lista


@register.filter()
def permission_video(lv, user):

    if lv.count() > 0:
        lv    = lv[0]
        plano = lv.plano
        if not plano or plano.name == 'Free':
            return True
        elif plano.name == u'Quero começar':
            return False
        else:
            return False
    else:
        return False

    return True


@register.inclusion_tag('templatetags/faq.html')
def faq(video):

    p = {}

    p['list_faq']      = Faq.objects.filter( Q(rede = video.rede) & Q(visible=True) & Q(treinamento = video) ).order_by('order', 'pergunta')
    p['treinamento']   = video
    if video.rede.email:
        p['is_create'] = _is_valid_email(video.rede.email)

    return p


@register.filter()
def get_type_arquive(arq):

    p = {}

    list_img = ['pdf.png', 'ppt.png', 'pptx.png', 'xls.png', 'xlsx.png', 'doc.png', 'docx.png']

    if list_img.count( '%s.png' % arq.file.name.split('.')[-1].lower() ) > 0:
        return '%s.png' % arq.file.name.split('.')[-1].lower()

    return 'default.png'


@register.filter()
def length_title_desc(desc):

    return len( striptags( desc.replace('&nbsp;', '').strip() ) )


@register.filter()
def get_technical_id(id):

    try:
        return Category.objects.get( Q(parent = int(id)) & Q(visible=True) & Q(tipo = 1) ).id
    except:
        pass
    return 0


list_technical, list_technical_category, list_tec_full_ids = [], [], []
def _get_category(obj):

    if obj.parent:
        if list_tec_full_ids.count(obj.parent.id) == 0:
            list_technical.append({'label' : obj.parent.get_name(), 'id' : obj.parent.id, 'display' : 'block'})
        else:
            list_technical.append({'label' : obj.parent.get_name(), 'id' : obj.parent.id, 'display' : 'none'})
        list_tec_full_ids.append(obj.parent.id)
        return _get_category(obj.parent)

    lt = list(list_technical)
    del list_technical[:]

    return lt


@register.inclusion_tag('templatetags/technical.html', takes_context=True)
def technical(context, rede=None):

    context['list_technical'] = Category.objects.filter( Q(rede = rede) & Q(visible=True) & Q(tipo = 1) ).order_by('order', 'name')
    context['count_enquete']  = Enquete.objects.filter( Q(visible = True) & Q(rede = rede) ).count()
    context['rede']           = rede

    if 'qt' in context and len(context['qt']) > 0:
        context['list_technical'] = context['list_technical'].filter( Q(text__icontains = context['qt']) | Q(name__icontains = context['qt']) ).order_by('order', 'name')

    for lt in context['list_technical']:
        list_c = _get_category(lt)
        list_c.reverse()
        list_technical_category.append( list_c )

    context['list_technical_category'] = list(list_technical_category)

    del list_technical_category[:]
    del list_tec_full_ids[:]

    return context


@register.inclusion_tag('templatetags/get_msg.html', takes_context=True)
def get_msg(context, rede=None):

    context['img'] = rede.image

    return context


@register.filter()
def is_menu_certificate(rede):

    return Menu.objects.filter( Q(visible = True) & Q(rede = rede) & Q(url__icontains = 'certificado') & Q(tipo = 'B') ).count() > 0


@register.inclusion_tag('templatetags/get_aviso.html', takes_context=True)
def get_aviso(context, rede=None, user=None):

    context['aviso'] = Aviso.objects.filter( Q(rede = rede) & Q(visible = True) )
    context['rede']  = rede
    context['user']  = user

    if context['aviso'].filter( Q(is_not_view = user) ).count() > 0:
        context['aviso'] = None
        return context

    if context['aviso'].count() > 0:
        aviso = context['aviso'][0]
        if not aviso.is_full_user:
            context['aviso'] = context['aviso'].filter(is_user_view = user)
        if aviso.date_init:
            context['aviso'] = context['aviso'].filter( Q(date_init__lte = datetime.now()) )
        if aviso.date_end:
            context['aviso'] = context['aviso'].filter( Q(date_end__gte = datetime.now()) )
        if not aviso.is_persistent:
            aviso.is_not_view.add(user)
            aviso.save()

    return context


@register.filter()
def is_observation(list, id):

    for l in list:
        if l['id'] == id:
            return 'block'

    return 'none'


@register.filter()
def get_observation(list, id):

    for l in list:
        if l['id'] == id:
            return l['obs']

    return ''


@register.filter()
def video_relacionado(video, user=None):

    if video.required.filter(visible = True).count() == 0:
        return ''
    else:
        for v in video.required.filter(visible = True).order_by('category__order', 'order'):
            if v.relatorioacoes_set.filter( Q(user = user) & Q(complete = True) ).count() == 0:
                return 'disabled'
        return ''

    return 'disabled'


@register.filter()
def video_relacionado_name(video, user=None):

    if video.required.filter(visible = True).count() == 0:
        return ''
    else:
        for v in video.required.filter(visible = True).order_by('category__order', 'order'):
            if v.relatorioacoes_set.filter( Q(user = user) & Q(complete = True) ).count() == 0:
                return v.name
        return ''

    return ''


@register.filter()
def category_video_relacionado(category, user=None):

    result = []
    quant  = category.treinamento_set().filter(visible = True).count()

    if quant == 0:
        return ''

    for video in category.treinamento_set().filter(visible = True):
        if video.required.filter(visible = True).count() > 0:
            for v in video.required.filter(visible = True).order_by('category__order', 'order'):
                if v.relatorioacoes_set.filter( Q(user = user) & Q(complete = True) ).count() == 0:
                    result.append(v.id)

    result = list(set(result))

    return ['', 'disabled'][len(result) >= quant]


@register.filter()
def category_video_relacionado_name(category, user=None):

    result = []
    quant  = category.treinamento_set().filter(visible = True).count()

    for video in category.treinamento_set().filter(visible = True).order_by('category__order', 'order'):
        if video.required.filter(visible = True).count() > 0:
            for v in video.required.filter(visible = True).order_by('order'):
                if v.relatorioacoes_set.filter( Q(user = user) & Q(complete = True) ).count() == 0:
                    return v.name

    return ''


@register.filter()
def medidor_porcent(number, value):

    v = float(number) / 100

    return int( round(v * value) )



