from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import Library, loader, Context
from django.utils import simplejson
from megavideo.api.video import video_search
import base64

def render_to_js(template, datas = {}):
    t = loader.get_template(template)
    r = t.render(Context(datas))
    a = ''
    for i in r.splitlines():
        a += 'document.write(' + simplejson.dumps(i.decode('utf-8') + '\n') + ');\n'
    r = HttpResponse(a, mimetype = "text/javascript")
    return r

def render_to_jsonp(template, datas , callback):
    t = loader.get_template(template)
    a = t.render(Context(datas))
    r = HttpResponse(callback + '(' + simplejson.dumps(a) + ')', mimetype = "text/javascript")
    return r

def index(request):
    return render_to_js('api/swidget.html', { 'server_base' : settings.BASE_URL })

def init(request):
    return render_to_response('api/js/swidget_init.js', { 'server_base' : settings.BASE_URL })

def search(request):
    if 'pattern' in request.GET:
        vl = video_search(value = request.REQUEST.get('value', 0), category = request.GET['pattern'])
    else:
        vl = video_search(value = request.REQUEST.get('value', 0))
    vl = vl[0:5]
    p = { 'videos' : vl }
    for i in p['videos']:
        i['idVideo'] = base64.b64encode(str(i['id']))
        i['thumb'] = settings.BASE_URL + i['thumb']

    return render_to_jsonp('api/swidget_search.html', p, request.GET['jsoncallback'])
