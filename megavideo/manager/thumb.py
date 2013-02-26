from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from django.conf import settings
import os
import os.path

#from megavideo.content.models import *

def get_generic_file(name, dir, prefix=''):
    return os.path.join(settings.MEGAVIDEO_CONF['video_storage'], dir, prefix + '_' + name)

def get_generic_file_publicity(name, dir, prefix=''):
    return os.path.join(settings.MEDIA_ROOT + "publicity/", dir, prefix + '_' + name)

def build_thumb_url(idcontent, name):
    url = '/vflow/thumb/' + str(idcontent) + '/' + name + '/'
    return url

def build_minithumb_url(idcontent):
    url = '/vflow/minithumb/' + str(idcontent)  + '/'
    return url

def mini_thumb (request, idcontent):
    t = request.db['contentThumb']
    s = select([t]).where(and_(t.c.idcontent == idcontent,
        t.c.height == minithumb_height,
        t.c.width == minithumb_width))
    r = s.execute()

    if r.rowcount < 1:
        r = select([request.db['content']]).where(request.db['content'].c.id == idcontent).execute()
        v = dict(zip(r.keys, r.fetchone()))

        print "creating minithumb "
        skt = SkThumbnail(skmc)
        skt.height = minithumb_height
        skt.width = minithumb_width
        th = skt.create(v, drop_on_error = False)
    else:
        th = dict(zip(r.keys, r.fetchone()))

    return thumb(request, idcontent, th['name'])

def thumb_player(request, idcontent):
    v = Content.objects.using('megavideo').get(pk = idcontent)

    #natura
    cats = [i.name for i in v.category.all()]

    if "Audio" in cats:
        HttpResponseRedirect('/megavideo/static/images/manager/default.jpg')
    elif "Text" in cats:
        HttpResponseRedirect('/megavideo/static/images/manager/default.jpg')

    try:
        t = v.get_thumb()
        path = get_generic_file(t['name'], v.dir, 'thumb');
        wrapper = FileWrapper(file(path))
    except:
        return HttpResponseRedirect('/megavideo/static/manager/images/processando.gif')
    response = HttpResponse(wrapper)
    response['Content-Type'] = 'image/jpeg'
    response['Content-Length'] = str(os.path.getsize(path))
    return response

#@cache_page(10)
def thumb(request, idcontent, name):
    v = Content.objects.using('megavideo').get(pk = idcontent)

    if v == None:
        raise Http404

    #natura
    cats = [i.name for i in v.category.all()]

    if "Audio" in cats:
        HttpResponseRedirect('/megavideo/static/images/thumb_audio.jpg')
    elif "Text" in cats:
        HttpResponseRedirect('/megavideo/static/images/thumb_texto.jpg')


    path = get_generic_file(name, v.dir, 'thumb');

    try:
        wrapper = FileWrapper(file(path))
    except:
        return HttpResponseRedirect('/megavideo/static/manager/images/processando.gif')

    response = HttpResponse(wrapper)
    response['Content-Type'] = 'image/jpeg'
    response['Content-Length'] = str(os.path.getsize(path))
    return response


def pub_comment(request, comment_id, act):
    c = ContentComment.objects.using('megavideo').get(pk = comment_id)
    if act == 'pub':
        c.moderated = 1
    elif act == 'depub':
        c.moderated = -1
    elif act == 'read':
        if c.moderated == None:
            c.moderated = -1

    c.save(using='megavideo')
    return HttpResponse('ok')

def del_comment(request, comment_id):
    c = ContentComment.objects.using('megavideo').get(pk = comment_id)
    c.delete()
    return HttpResponse('ok')

