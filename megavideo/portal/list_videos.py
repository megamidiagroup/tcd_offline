# -*- coding: utf-8 -*-
#!/usr/bin/env python

#python
import os
import logging
import datetime
import simplejson as json
import tempfile

from megavideo.common.channel import *
from megavideo.video.models import *
from django.shortcuts import render_to_response
from megavideo.record.views import _prepare_recorder, _encode_dict, _decode_dict

#DiggPaginator
from megavideo.common.DiggPaginator import *


def ajax_list_videos(request):
    """ lista itens no popular block """
    
    p = {}
    
    p['last_video'] = []
    
    target = request.REQUEST.get('target', False)
    cat_id = int(request.REQUEST.get('cat_id', 0))
    
    chan  = request.channel_name
    
    p['channel_url'] = request.channel_url

    if target:
        try:

            if target == 'destaque':
                # pega videos e categorias em destaque
                vf = VideoFeatured.objects.using('megavideo').filter(typevideofeatured__name='c', channel__name=chan).order_by('-id')
                p['last_video'] = Video.objects.using('megavideo').filter(published=True, channel__name=chan, category=vf[0].category).order_by('-id')[0:6]
            else:
                
                if cat_id > 0:
                    mList = Video.objects.using('megavideo').filter(published=True, channel__name=chan).filter(category__id=cat_id)
                else:
                    mList = Video.objects.using('megavideo').filter(published=True, channel__name=chan)
                
                if target == 'last':
                    p['last_video'] = mList.order_by('-date')[0:6]
                if target == 'vistos':
                    p['last_video'] = mList.exclude(views=0).distinct().order_by('-views')[0:6]
                elif target == 'comentados':
                    p['last_video'] = mList.exclude(videocomment__isnull=True).annotate(num_comment=Count('videocomment')).order_by('-num_comment')[0:6]
                elif target == 'votados':
                    p['last_video'] = mList.exclude(ratenum=0).distinct().order_by('-ratenum')[0:6]
                else:
                    pass
            
        except:
            pass
    
    return render_to_response('portal/ajaxlistvideos.html', p, context_instance=RequestContext(request))


def ajax_super_list_videos(request, page=1):
    
    p = {}
    
    idelement = request.REQUEST.get('idelement', '')
    
    chan = request.channel_name
    
    if idelement == 'featured':

        vf = VideoFeatured.objects.using('megavideo').filter(channel__name = chan, video__isnull=True)
        
        if vf.count() > 0:
            superlistvideos = vf[0].category.video_set.filter(published=True).order_by('-id')
        else:
            superlistvideos = Video.objects.using('megavideo').filter(published=True, channel__name=chan).order_by('-id')
            
    elif idelement == 'listvideos':
        
        superlistvideos = Video.objects.using('megavideo').filter(published=True, channel__name=chan).order_by('-date')

        
    paginator = DiggPaginator(superlistvideos, 4, body=5, padding=1 , margin=1, tail=1)

    try:
        superlistvideospage = paginator.page(page)
    except:
        superlistvideospage = paginator.page(paginator.num_pages)
            
    p['superlistvideos'] = {'list' : superlistvideospage}

    return render_to_response('portal/super_listvideos.html', p)