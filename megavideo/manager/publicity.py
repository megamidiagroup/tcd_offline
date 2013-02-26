# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from django.shortcuts import render_to_response
from django.template import RequestContext

from megavideo.video.models import *

per_page = 12

#===============================================================================
# Gerencia Publicity
#===============================================================================

@login_required
def list_publicity(request, video_id = 0):
    #monta os menus
    p = menu_top(request);
    request.breadcrumbs(u'Configurações', "javascript:void(0)")
    request.breadcrumbs(u'Vídeo ', request.channel_url + 'manager/program/')
    request.breadcrumbs(u'Publicity', "javascript:void(0)")

    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
    p['update'] = Publicity.objects.using('megavideo').filter(video__id = int(video_id))
    p['video'] = Video.objects.using('megavideo').get(id = int(video_id))
    p['video_id'] = video_id

    p['extra_css'] = 'portal_background'
    p['rota'] = '/manager/program/publicity/'

    return render_to_response('manager/publicity/list.html', p, context_instance = RequestContext(request))


def ajax_del_publicity(request):
    """ ação deletar propaganda """

    p = {}
    p['status'] = False
    idpublicity = request.REQUEST.get('id', False)

    if idpublicity:
        try:
            pub = Publicity.objects.using('megavideo').get(id = int(idpublicity))
            pub.delete()
            p['status'] = True
        except:
           pass

    return HttpResponse(json.dumps(p) , mimetype = 'application/json')


def ajax_list_publicity(request):
    """ ação para gerar a lista de propagandas """

    video_id = request.REQUEST.get('video_id', False)
    filtro = request.REQUEST.get('filtro', '')

    p = {}

    pub = Publicity.objects.using('megavideo').filter(video__id = int(video_id))
    if filtro == 'true':
        pub = pub.filter(published = True)
    elif filtro == 'false':
        pub = pub.filter(published = False)

    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
    p['update'] = pub
    p['video'] = Video.objects.using('megavideo').get(id = int(video_id))

    return render_to_response('manager/publicity/ajax_list.html', p, context_instance = RequestContext(request))


def ajax_published_publicity(request):
    """ ação para publicar e despublicar as propagandas """

    p = {}
    p['status'] = ""
    idpublicity = request.REQUEST.get('id', False)

    if idpublicity:
        try:
            pub = Publicity.objects.using('megavideo').get(id = int(idpublicity))
            pub.published = not pub.published
            pub.save(using='megavideo')
            p['status'] = pub.published
        except:
           pass

    return HttpResponse(json.dumps(p) , mimetype = 'application/json')

#======== end publicity ============#


def ajax_publish_video(request):

    p = {}

    p['error'] = 1

    video_id = request.POST.get('video_id', 0)

    if video_id:

        try:
            v = Video.objects.using('megavideo').get(id = int(video_id))
            v.published = not v.published
            v.save(using='megavideo')
            p['error'] = 0
            p['published'] = v.published
        except:
            pass

    return HttpResponse(json.dumps(p), mimetype = 'application/json')


def upload_publicity(request, video_id = 0, idpublicity = 0):
    """ def upload para propagandas do player publicity do manager """

    LOGGER.debug("iniciado o processo de upload publicity")

    values = {}

    try:
        p = Publicity.objects.using('megavideo').get(id = int(idpublicity))
    except:
        p = Publicity()

    if 'Filedata' in request.FILES and (video_id or idpublicity):

        file_data = request.FILES['Filedata']

        LOGGER.debug("nome da image: " + str(file_data))

        try:
            name_tmp = str(file_data)
            extent = name_tmp[-3:]

            if len(extent) == 3:
                extent = "." + str(extent)
            else:
                extent = ".jpg"
        except:
            extent = ".jpg"

        tmp = tempfile.mktemp('_' + settings.MEGAVIDEO_CONF['tv_name'])
        tmp = tmp + extent

        LOGGER.debug("tmp da image: " + str(tmp))

        fd = open(tmp, 'wb')

        LOGGER.debug("opened")

        fd.write(file_data.read())

        LOGGER.debug("read")

        fd.close()

        LOGGER.debug("close")

        LOGGER.debug("opened 2")

        if p.name != '':
            arquive = p.name
        else:
            arquive = md5.md5(str(random.random())).hexdigest()[0:12] + extent
            p.name = arquive
            p.video_id = video_id
            p.save(using='megavideo')

        dirname = settings.MEDIA_ROOT + 'publicity/' + str(video_id) + '/'
        if not os.path.isdir(dirname):
            try:
                os.mkdir(dirname)
            except:
                values = { 'url': '', 'status': "-2", 'list': 'Sem permissão para criar diretorio: ' + str(video_id)}
                return HttpResponse(json.dumps(values), mimetype = 'application/json')

        thumb_file = get_generic_file_publicity(str(arquive), str(video_id), 'thumb')

        LOGGER.debug("get_generic_file")

        LOGGER.debug("thumb_file " + str(thumb_file))

        LOGGER.debug("movendo a imagem para seu diretorio correto")

        LOGGER.debug(str(tmp) + " - into - " + str(thumb_file))

        shutil.move(tmp, thumb_file)

        LOGGER.debug("movido com sucesso")

        LOGGER.debug("tentar unlink no tmp: " + str(tmp))

        try:
            os.unlink(tmp)
            LOGGER.debug("o arquivo persistiu, mas aqui foi deletado!")
        except:
            LOGGER.debug("o arquivo não está mais aqui!")

        LOGGER.debug("unlink no tmp, efetuado com sucesso")

    else:

        try:
            if video_id and p.name:
                variables = {'title' : p.title, 'link': p.link, 'posx': p.posx, 'posy': p.posy,
                                'rotation': p.rotation, 'scale': p.scale, 'time': p.time, 'timeout': p.timeout, 'idpublicity': p.id}
                values = { 'url': "storage/publicity/" + str(video_id) + "/thumb_" + str(p.name), "status": "0", 'list': variables, 'length': p.video.duration }
            else:
                values = { 'url': '', 'status': "-1", 'list': '', 'length': 0}
        except:
            pass

        return HttpResponse(json.dumps(values), mimetype = 'application/json')

    try:
        values = { 'url': "storage/publicity/" + str(video_id) + "/thumb_" + str(arquive), "status": "0", 'list': {'idpublicity': p.id}, 'length': 0 }
    except:
        pass

    return HttpResponse(json.dumps(values), mimetype = 'application/json')


def save_values_publicity(request, idpublicity):
    """ para salvar as informações da propaganda """

    r = {}
    r['status'] = False

    title = request.REQUEST.get('title', False)
    link = request.REQUEST.get('link', False)
    time = request.REQUEST.get('time', False)
    timeout = request.REQUEST.get('timeout', False)
    posx = request.REQUEST.get('posx', False)
    posy = request.REQUEST.get('posy', False)
    rotation = request.REQUEST.get('rotation', False)
    scale = request.REQUEST.get('scale', False)

    try:
        p = Publicity.objects.using('megavideo').get(id = int(idpublicity))
    except:
        p = {}

    if p and title and link and time and timeout and posx and posy and rotation and scale:
        try:
            p.title = title
            p.link = link
            p.timeout = float(timeout)
            p.time = float(time)
            p.posx = float(posx)
            p.posy = float(posy)
            p.rotation = float(rotation)
            p.scale = float(scale)
            p.save(using='megavideo')
            r['status'] = True
        except:
            pass

    return HttpResponse(json.dumps(r), mimetype = 'application/json')
