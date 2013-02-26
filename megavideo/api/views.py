#-*- coding: utf8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import Library, loader, Context
from django.core.mail import send_mail, EmailMessage
from django.template import RequestContext

import re
from megavideo.common.channel import *
from django.utils import simplejson
from megavideo.video.models import *

from django.views.decorators.cache import cache_page

import simplejson

def index(request):
    #video list
    l = _get_video_init(request.sa)
    p = {'video_list': []}

    for i in l:
        p['video_list'].append(_video_info(request.sa, i))

    p['infos'] = {}

    return HttpResponse(simplejson.JSONEncoder().encode(p))

def categories(request):
    p = {}
    render_to_response('api/categories.xml', p)

def search(request, pattern):
    pass

#--- test
def _get_video_from():
    v = DB['video']
    vc = DB['videoChannel']
    chan = DB['channel']
    vcc = DB['videoCategory']
    c = DB['category']

    fo = join(join(join(v, vc), vcc), c)

    return fo

def _get_video_init(sess):
    v = DB['video']
    chan = DB['channel']

    fo = _get_video_from()
    s = select([v], from_obj = [fo], order_by = [desc(v.c.id)])
    r = sess.execute(s.where(and_(v.c.published == True,
        chan.c.name == INI.cfg.get('SkMC', 'default_channel'))).limit(10))
    return r.fetchall()

def _get_video_random(sess, catname , limiter):
    v = DB['video']
    chan = DB['channel']

    fo = _get_video_from()

    s = select([v], from_obj = [fo], order_by = [func.rand()])
    r = sess.execute(s.where(and_(v.c.published == True,
        #c.c.name == catname,
        chan.c.name == INI.cfg.get('SkMC', 'default_channel'))).limit(limiter))
    return [dict(zip(r.keys, i)) for i in r.fetchall()]


def widget(request):
    t = loader.get_template('js/widget.js')
    vl = build_video_list(request, _get_video_random(request.sa, '', 4))
    for i in vl:
        i['tv_url'] = INI.cfg.get('SkMC', 'siteRootUrl') + 'home/?id=' + base64.b64encode(str(i['id']))

    p = {'videos' : vl, 'base_url' : settings.BASE_URL}
    c = Context(p)
    r = HttpResponse(t.render(c), mimetype = "text/javascript")
    return r

def test(request):
    t = loader.get_template('api/test.html')
    r = t.render(Context({}))
    a = ''
    for i in r.splitlines():
        a += "document.write('%s')\n" % simplejson.dumps(i)
    r = HttpResponse(a, mimetype = "text/javascript")
    return r

def indique(request):
    dest = request.POST['destinatario']
    email_re = re.compile(r'([0-9a-zA-Z]([-.w]*[0-9a-zA-Z])*@([0-9a-zA-Z][-w]*[0-9a-zA-Z].)+[a-zA-Z]{2,9})')
    dest = [i[0] for i in email_re.findall(dest)]
    con = request.POST['mensagem']
    nome = request.POST['nome']
    vid = request.POST['id']

    content = u"Olá\n"

    video = Video.objects.using('megavideo').get(pk = int(vid))
    content += settings.MEGAVIDEO_CONF['base_url'] + u'?id=' + vid + "\n"
    content += " ------ Mensagem ----- \n"
    content += con
    content += "\n --------------------- \n"

    msg = EmailMessage('Vflow TV', content, 'vflow@vflow.com.br', [dest])
    msg.send()
    return HttpResponse('ok')

def widget_moodle(request):
    p = {}

    p['channel'] = get_current_channel(request)
    chan = p['channel']

    if 'idcategory' in request.GET:
        p['videos'] = Video.objects.using('megavideo').filter(category__id = int(request.GET['idcategory']), published = True).order_by('-date')[0:6]
    else:
        p['videos'] = Video.objects.using('megavideo').filter(channel = chan, published = True).order_by('-date')[0:6]
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
    return render_to_response('api/js/widget_moodle.js', p)


def sebrae(request, catname = 0, html = False):
    vl = Video.objects.using('megavideo').filter(published = True)
    if catname != 0:
        cat = Category.objects.using('megavideo').get(name = catname)
        vl = vl.filter(videocategory__category = cat).order_by('videocategory__sequence')
    r = []
    for i in vl:
        a = {}
        a['id'] = i.id
        a['id64'] = base64.b64encode(str(i.id))
        a['title'] = i.get_meta('name')
        a['date'] = i.date
        a['description'] = i.get_meta('description')
        r.append(a)

    if html:
        return render_to_response('api/test.html', {'objects' : r})

    t = loader.get_template('api/test.html')
    en = t.render(Context({'objects' : r}))
    a = ''
    for i in en.splitlines():
        a += 'document.write(' + simplejson.dumps(i + '\n') + ');\n'

    t = loader.get_template('api/end_script.html')
    en = t.render(Context({'objects' : r}))

    r = HttpResponse(a + en, mimetype = "text/javascript")
    return r



def _out_js(text):
    """
       Saída em js das informações
    """
    a = u''
    for i in text.splitlines():
        if len(i) > 0:
            a += u'document.write(%s);' % simplejson.dumps(i)
    return a

@cache_page(60*2)
def embed_js(request):
    """ contexto para criar um js dinâmico """
    p = {}

    p['channel']   = get_current_channel(request)
    p['idContent'] = request.REQUEST.get('idContent', '')

    p['playAuto'] = request.REQUEST.get('playAuto'  , 'false')
    p['base_url'] = request.REQUEST.get('base_url'  , settings.MEGAVIDEO_CONF['base_url'])
    p['types']    = request.REQUEST.get('types'     , 'true')

    print p['idContent']

    video = Video.objects.using('megavideo').get(id = int(p['idContent']))

    p['values'] = ''

    player = 'megaplayer.swf'

    for i, j in p.items():
        p['values'] += str(i) + '=' + str(j) + '&'

    #configuração
    p['width']  = request.REQUEST.get('width'     , '640')
    p['height'] = request.REQUEST.get('height'    , '360')
    p['player'] = request.REQUEST.get('player'    , settings.MEGAVIDEO_CONF['base_url'] + 'static/portal/swf/' + player)

    text = render_to_string('api/embed.html', p, context_instance = RequestContext(request))

    text = _out_js(text)

    return HttpResponse(text)
