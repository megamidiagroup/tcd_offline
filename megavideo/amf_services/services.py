# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.mail import send_mail, EmailMessage
from django.db.models import Q
from django.template.loader import render_to_string
from django.core.cache import cache

try:
    from django.core.validators import email_re
except:
    from django.forms.fields import email_re

from megavideo.common.dlog import LOGGER
from megavideo.common.create_url import get_thumb_url
from megavideo.video.models import *
from mega.models import Router, Host
from megavideo.common.categories import *
from megavideo.common.channel import *

from pyamf.remoting.gateway.django import DjangoGateway
from hashlib import sha1 as sha

import inspect
import django
import simplejson
import time
import datetime
import urllib
import pyamf
import datetime
import hashlib

services = {}

def cache_amf(timing = 30):
    def wrapper(func): 
        def f(request, *args, **kwargs):
            key = hashlib.md5(str(args) + str(kwargs)).hexdigest()
            v = cache.get(key)
            if v == None:
                v = func(request, *args, **kwargs)
                cache.set(key, v)
            return v
             
        return f
    return wrapper
    


def on_air(qs):
    return qs.filter(Q(published = True) & Q(date__lte = datetime.datetime.now()))
    

def api_response(code = 0, result_list = [], total = 0, from_to = []):
    r = {}
    r['code'] = code
    r['result_list'] = result_list
    r['total_num'] = total

    if from_to == [] or from_to == [0, 0]:
        return r
    else:
        r['result_list'] = result_list[from_to[0]:from_to[1]]
    return r

def api_get_cat_tree(cat_id, l, list_selected):
    """ clean """
    childs = []

    if cat_id == None:
        cat_id = 0

    for i in l:
        if i.parent != None:
            idParent = i.parent.id
        else:
            idParent = 0

        if int(idParent) == int(cat_id):
            cdict = {'id' : i.id,
                    'id_parent' : idParent ,
                    'name' : i.name,
                    'description' : i.description,
                    'childs' : api_get_cat_tree(i.id, l, list_selected)}
            if i in list_selected:
                cdict['status'] = 1
            else:
                cdict['status'] = 0
            if i.image:
                cdict['image'] = i.image.url
            cdict['nb_contents'] = i.video_set.filter(published = True).count()
            childs.append(cdict)
            
            
    return childs

def prepare_content(content, t = 'A', ip='localhost'):
    """ prepara os programas para serem retornados """

    r         = {}
    r['id']   = content.id
    r['type'] = t
    r['url_relative'] = ip
    r['meta'] = {}
    for i in ['name', 'description', 'author']:
        r['meta'][i] = content.get_meta(i)
    r['meta']['autor']    = r['meta']['author']
    r['publication_date'] = content.date
    r['transcodes']       = {}

    # resgata todas as tags desse programa
    vt = VideoTag.objects.using('megavideo').filter(video__id = content.id).exclude(initime=0)
	
    arrayTags = []
	
    for w in vt:
        arrayTags.append( {'id':w.id, 'tag':w.tags[1:-1], 'initime':w.initime, 'endtime':w.endtime} )
    r['tags'] = arrayTags

    for i in content.videotranscode_set.all():
        path = os.path.join(content.dir, 'transcoded_' + i.name)
        t = {
                'url' :  settings.MEGAVIDEO_CONF['base_url'] + 'video/get/' + str(content.id) +'/' + i.transcode.name + '/',
                'url_relative' : settings.STORAGE_URL_RELATIVE + 'videos/' + path
            }
        r['transcodes'][i.transcode.name] = t
    
    r['views']       = content.views
    
    try:
        vt           = content.videothumb_set.all()[0]
        path         = os.path.join(content.dir, 'thumb_' + vt.name)
        thumb        = get_thumb_url(vt)
        url_relative = settings.STORAGE_URL_RELATIVE + 'videos/' + path
    except:
        thumb        = '/megavideo/static/manager/images/processando.gif'
        url_relative = thumb

    r['thumbs'] = [{'position': 0, 'url' : thumb, 'url_relative' : url_relative}]

    r['length'] = content.duration
    r['total_comments'] = content.videocomment_set.filter(published = True).count()

    if content.document_set.filter(documentclass__name = 'PDF').count() != 0:
        r['pdf'] = content.document_set.filter(documentclass__name = 'PDF')[0].filename.url
    else:
        r['pdf'] = ''
    r['categories'] = [i.category_id for i in Videocategory.objects.using('megavideo').filter(video = content)]

    if content.ratenum == 0:
        r['rate'] = 0
    else:
        r['rate'] = content.ratesum / float(content.ratenum)
    
    publicity = []
    
    try:
        pub = Publicity.objects.using('megavideo').filter(published = True, video__id = int(content.id))
        for i in pub:
            publ = {'time': i.time, 'timeOut': i.timeout, 'url': str(settings.MEGAVIDEO_CONF['base_url']) + "storage/publicity/" + str(i.video_id) + '/' + 'thumb_' + str(i.name), 'x': i.posx, 'y': i.posy, 'rotation': i.rotation, 'link': i.link, 'scale': i.scale, 'title': i.title}
            publicity.append(publ)
    except:
        pass
    
    r['publicity'] = publicity
    
    videoroll = []
    
    channel = content.channel_set.all()[0]
    
    for i in content.rolls.all():
        rolllines = {
                'title': i.roll.get_name(), 
                'position': i.position,
                'idContentRoll' : i.roll.id }
        videoroll.append(rolllines)

    r['videoroll'] = videoroll
    r['question']  = content.question_set.filter(published = True).count()
    
    return r
	

def selectChannels(request):
    vl = [dict((('name', i.name ), ('id', i.id))) for i in Channel.objects.using('megavideo').all()]
    return api_response(code = 0, result_list = vl, total = len(vl))


@cache_amf(60)
def selectCategories(request, idparent = 0, depth = 2):
    """Get a tree of categories with their id, name, 
    number of videos and list of childs """

    current_channel = get_current_channel(request)
    if idparent != 0:
        main_obj = Category.objects.using('megavideo').get(pk = int(idparent))
    else:
        main_obj = current_channel

    c     = main_obj.category_set.all().order_by('sequence')
    cats  = api_get_cat_tree(None , c, [])
    
    total = len(cats)

    return api_response(code = 0, result_list = cats, total = total)


@cache_amf(60)
def selectCategoriesByChannel(request, chan_id = 0):
    if chan_id != 0:
        chan = Channel.objects.using('megavideo').get(pk = int(chan_id))
    else:
        chan = get_current_channel(request)

    c = Category.objects.using('megavideo').filter(channel = chan).order_by('sequence')
    cats  = api_get_cat_tree(0, c, [])
    total = len(cats)

    return api_response(code = 0, result_list = cats, total = total)


@cache_amf(10)
def selectContentByCategory(request, category_id, from_to = [], filter = 1):
    """ traz todos os programas de uma categoria id """

    cat = Category.objects.using('megavideo').get(id = int(category_id))
    content_list = cat.video_set.filter(published = True).order_by('-videocategory__sequence')
    
    if filter == 1:
        content_list = on_air(content_list)
    
    rl = [prepare_content(i) for i in content_list]
  
    return api_response(0, rl, content_list.count(), from_to)


def selectContentBySearch(request, pattern, from_to = [] , filter=1 ):
    
    content_list = Video.objects.using('megavideo').filter(published = True , videometa__value__icontains = pattern).order_by('-date').distinct()
    
    if filter == 1:
        content_list = on_air(content_list)
        
    rl = [prepare_content(i) for i in content_list]
    return api_response(0, rl, content_list.count(), from_to)


def selectContentByMetaSearch(request, pattern, meta_name,  from_to = [], filter=1):
    
    content_list = Video.objects.using('megavideo').filter(published = True).filter(videometa__value__icontains = pattern, videometa__metaclass__name = meta_name).order_by('-date').distinct()
    
    if filter == 1:
        content_list = on_air(content_list)
    
    rl = [prepare_content(i) for i in content_list]
    return api_response(0, rl, content_list.count(), from_to)

def selectContentByTag(request, tag,  from_to = []):
    #FIXME: waiting for tags to be ready
    #v = VideoTag.objects.using('megavideo').get(id = id)
    #return api_response(0, [v], 1)
    #não implementado...
    pass

def getContent(request, key):

    video_id    = Video().deserialize( key )
    
    ip_redirect = 'localhost'
    ip          = ''

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        v = Video.objects.using('megavideo').get(id = int(video_id))
    except:
        return api_response(-1, [], 0)

    channel = v.channel_set.all()[0]

    r = Router.objects.using('default').filter( Q(rede__link = channel.name) & Q(visible = True) & Q(host__visible = True) )
    if r.count() > 0:
        if r.filter(ip__iexact = ip).count() == 1:
            ip_redirect  = r.filter(ip__iexact = ip)[0].host.ip
        elif r.filter(ip__iexact = '.'.join(ip.split('.')[0:-1])).count() == 1:
            ip_redirect  = r.filter(ip__iexact = '.'.join(ip.split('.')[0:-1]))[0].host.ip
        elif r.filter(ip__iexact = '.'.join(ip.split('.')[0:-2])).count() == 1:
            ip_redirect  = r.filter(ip__iexact = '.'.join(ip.split('.')[0:-2]))[0].host.ip
        elif r.filter(ip__iexact = '.'.join(ip.split('.')[0:-3])).count() == 1:
            ip_redirect  = r.filter(ip__iexact = '.'.join(ip.split('.')[0:-3]))[0].host.ip

    LOGGER.debug('IP: ' + str(ip))
    LOGGER.debug('Redirect: ' + str(ip_redirect))

    return api_response(0, [prepare_content(v, ip=ip_redirect)], 1)

def getCategory(request, category_id):
    c = Category.objects.using('megavideo').get(pk = int(category_id))
    return api_response(0, [c], 1)


def addComment(request, id, email, name, content):
    vc = Videocomment()
    vc.video_id = id
    vc.email = email
    vc.name = name
    vc.content = content
    vc.published = False
    vc.save(using='megavideo')
    return api_response()


def getComments(request, video_id, from_to = []):
    """ Returns the comments of the video """
    v = Video.objects.using('megavideo').get(id = int(video_id))

    rl = []
    for i in v.videocomment_set.filter(published = True).order_by('-date'):
        j = {}
        j['name'] = i.name
        j['content'] = i.content
        j['date'] = i.date
        j['id'] = i.id

        rl.append(j)
    return api_response(0, rl, len(rl), from_to)


def getQuestion(request, video_id):
    """ Returns question into responses """
    
    v = Video.objects.using('megavideo').get(id = int(video_id))
    
    rl = []
    for i in v.question_set.filter(published = True):
        j = {}
        j['question'] = i.question_text
        j['response'] = [({'response' : u.response_text, 'correct' : u.correct, 'video_id' : u.video_id}) for u in i.response.all().order_by('?')]
        
        rl.append(j)
    return api_response(0, rl, len(rl), [])


def setRate(request, idcontent, value):
    value = int(value)
    if value > 5:
        value = 5
    if value < 0:
        value = 0

    video = Video.objects.using('megavideo').get(pk = int(idcontent))

    if VideoVote:
        videovote = VideoVote()
        videovote.video = video
        videovote.value = value
        videovote.ip = request.META['REMOTE_ADDR']
        try:
            videovote.agent = request.META['HTTP_USER_AGENT']
        except:
            videovote.agent = ''
        videovote.save(using='megavideo')

    video.ratenum += 1
    video.ratesum += value
    video.save(using='megavideo')

    return api_response() 


def is_valid_email(email):
    """ Define a verificação do email """
    return True if email_re.match(email) else False  


def _check_send_mail(request, name_from, mail_to, name_to, p={}, id_video=0):
    
    try:
        v = Video.objects.using('megavideo').get(id = int(id_video))
    except:
        return -1
    
    if not is_valid_email(mail_to):
        return -2

    p['base_url']  = settings.MEGAVIDEO_CONF['base_url'][0:-1]
    p['name']      = name_from
    p['video']     = v  
    p['title']     = 'Vflow Web Vídeo'
        
    content = render_to_string('email/recommended.html', p)
        
    msg = EmailMessage('Você recebeu uma mensagem', content, str(settings.MEGAVIDEO_CONF['email']), [mail_to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    
    return 0
 
	
def sendEmail(request, video_id, name_from, mail_to, name_to, uf='SP'):
    """ Envio de email por flash """

    LOGGER.debug('send E-mail: ' + str(video_id))

    code = _check_send_mail(request, name_from, mail_to, name_to, {}, int(video_id))

    return {'code' : code}


services = { 
        'vflowService.selectChannels'            : selectChannels,
        'vflowService.selectCategories'          : selectCategories,
        'vflowService.selectCategoriesByChannel' : selectCategoriesByChannel,
        'vflowService.selectContentByCategory'   : selectContentByCategory,
        'vflowService.selectContentBySearch'     : selectContentBySearch,     
        'vflowService.selectContentByMetaSearch' : selectContentByMetaSearch,
        'vflowService.selectContentByTag'		 : selectContentByTag,
        'vflowService.getContent'				 : getContent,
        'vflowService.getCategory'				 : getCategory,
        'vflowService.getComments' 				 : getComments,
        'vflowService.getQuestion'               : getQuestion,
        'vflowService.addComment' 				 : addComment,
        'vflowService.setRate' 					 : setRate,
        'vflowService.sendEmail' 				 : sendEmail
}

VflowGateway = DjangoGateway(services)
