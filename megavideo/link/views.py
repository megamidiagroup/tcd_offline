from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from models import *
from megavideo.common import link_reduction

def index(request):
    return render_to_response('link/index.html')

def add_link(request):
    base = settings.MEGAVIDEO_CONF['base_url']
    
    original_url = request.REQUEST.get('original_url', '')

    if not original_url.startswith('http://'):
        original_url = 'http://' + original_url

    r = LinkReduced.objects.using('megavideo').filter(original_url = original_url)

    if r.count() == 0:
        lr = LinkReduced()
        lr.original_url = original_url
        lr.submitting_ip = request.META['REMOTE_ADDR']
        lr.comment = request.REQUEST.get('comment', '')
        lr.save(using='megavideo')
    else:
        lr = r[0]

    link = lr.link()
    return render_to_response('link/saved.html', {'link' : link})

def access_link(request, linkid):
    linkid = link_reduction.decode(str(linkid))[0]
    lr = LinkReduced.objects.using('megavideo').get(id = linkid)

    #put http in front of old urls
    if not lr.original_url.startswith('http://'):
        lr.original_url = 'http://' + lr.original_url 
        lr.save(using='megavideo')

    lc = LinkClicked()
    lc.link = lr
    lc.clicking_ip = request.META['REMOTE_ADDR']
    lc.save(using='megavideo')

    return HttpResponseRedirect(lr.original_url)
