# -*- coding: utf-8 -*-
#!/usr/bin/env python

#CaptchaField
from django import forms
from django.contrib.comments.forms import CommentForm
from captcha.fields import CaptchaField
from django.template.loader import render_to_string
from megavideo.video.models import *

try:
    from django.core.validators import email_re
except:
    from django.forms.fields import email_re

#DiggPaginator
from megavideo.common.DiggPaginator import *


class CaptchaTestForm(forms.Form):
    captcha = CaptchaField()

def is_valid_email(email):
    return True if email_re.match(email) else False

def _prepare_comment(p, video = 0, page = 1, limit = 3):

    comments = VideoComment.objects.using('megavideo').filter(published = True, video__id = int(video)).order_by('-date')

    arrComm = []

    for y in comments:
        arrComm.append({'id':y.id, 'name':y.name, 'content':y.content, 'date':y.date})

    p['comments_buttom'] = False

    if len(arrComm) > 5:
        p['comments_buttom'] = True

    paginator = DiggPaginator(arrComm, limit, body = 5, padding = 1 , margin = 1, tail = 1)
    p['comments_list'] = paginator.page(page)

    p['action'] = '/ajax_send_comment/'

    return p

def _menu(request, p):
    """ função para montar os valores do menu """

    c = Category.objects.using('megavideo').filter(published = True, channel__name = request.channel_name)
    category = c.filter(parent__isnull = True).order_by('sequence')

    list = []

    for i in category:
        list.append({'list' : i, 'childs' : [child for child in i.category_set.filter(published = True)]})

    p['category_menu'] = list

    return p


def _prepare_page(request, p, cat_id = 0, sub_id = 0, video_id = 0, lastvideos_id = ''):

    p = _menu(request, p)

    p['combocat'] = render_to_string('portal/combocat.html', p)

    p = _prepare_featured(request, p , page = 1, cat_id = cat_id, lastvideos_id = lastvideos_id)

    if int(cat_id):
        print 'other in sub_id'
        p['other_video'] = Video.objects.using('megavideo').filter(category__id = cat_id, published = True, channel__name = request.channel_name).order_by('?')[0:4]

    elif int(sub_id):
        print 'other in sub_id'
        p['other_video'] = Video.objects.using('megavideo').filter(category__id = sub_id, published = True, channel__name = request.channel_name).order_by('?')[0:4]

    elif video_id:
        catVideo = Video.objects.using('megavideo').filter(id = video_id)
        if catVideo:
            catVideo = catVideo[0].get_category
            if catVideo:
                print 'other in video'
                p['other_video'] = Video.objects.using('megavideo').filter(category__id = catVideo, published = True, channel__name = request.channel_name).order_by('?')[0:4]

    if 'other_video' in p:
        if not p['other_video']:
            p['other_video'] = Video.objects.using('megavideo').filter(published = True, channel__name = request.channel_name).order_by('?')[0:4]

    if not 'other_deo' in p:
        p['other_video'] = Video.objects.using('megavideo').filter(published = True, channel__name = request.channel_name).order_by('?')[0:4]

    p = _prepare_last_videos(request, p, page = 1)

    return p



def _prepare_featured(request, p , page = 1, cat_id = 0 , lastvideos_id = ''):
    """ traz os videos de destaque """
    
    vf = VideoFeatured.objects.using('megavideo').filter(channel__name = request.channel_name, video__isnull = True, typevideofeatured__name = 'c')
    
    if cat_id:
        superlistvideos = Video.objects.using('megavideo').filter(published = True, channel__name = request.channel_name, category__id = int(cat_id)).order_by('videocategory__sequence')
        try:
            subtitle = superlistvideos[0].category.all()[0].name
        except:
            subtitle = u'Sem vídeos'
        title = 'Categoria'
    else:
        if vf.count() > 0:
            superlistvideos = vf[0].category.video_set.filter(published = True).order_by('videocategory__sequence')
            subtitle = vf[0].category.name
            title = 'Destaques'
        else:
            subtitle = ''
            title = 'Últimos vídeos'
            superlistvideos = Video.objects.using('megavideo').filter(published = True, channel__name = request.channel_name).order_by('-date')

    paginator = DiggPaginator(superlistvideos, 4, body = 5, padding = 1 , margin = 1, tail = 1)

    try:
        superlistvideospage = paginator.page(1)
    except:
        superlistvideospage = paginator.page(paginator.num_pages)

    p['superlistvideos'] = {'list' : superlistvideospage, 'title' : title, 'subtitle' : subtitle, 'id' : 'featured', 'max' : paginator.num_pages}
    p['featured'] = render_to_string('portal/super_listvideos.html', p)

    return p


def _prepare_last_videos(request, p, page = 1, lastvideos_id = ''):

    last_videos = Video.objects.using('megavideo').filter(published = True, channel__name = request.channel_name).order_by('-ratesum')
    paginator = DiggPaginator(last_videos, 4, body = 5, padding = 1 , margin = 1, tail = 1)

    try:
        last_videos = paginator.page(1)
    except:
        last_videos = paginator.page(paginator.num_pages)

    #print 'lastvideos_id: ' , lastvideos_id

    p['superlistvideos'] = {'list' : last_videos, 'title' : 'Últimos vistos', 'id' : 'listvideos', 'max' : paginator.num_pages, 'class' : lastvideos_id}
    p['last_videos'] = render_to_string('portal/super_listvideos.html', p)

    return p
