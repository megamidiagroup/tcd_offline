# -*- coding: utf-8 -*-
#from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from megavideo.common.dlog import LOGGER
from megavideo.common.login import login_required


from megavideo.video.models import *

per_page = 12


@login_required
def add_channel(request, channel_id=0): #addcategory
    #monta os menus
    p = menu_top(request);
    p['form_title']  = 'Cadastro de rede'
    p['form_action'] = request.get_full_path()[1:]

    request.breadcrumbs(u'Configurações', "javascript:void(0)")
    request.breadcrumbs(u'Redes', request.channel_url + 'manager/channel/')

    if channel_id == 0: #para cadastrar
        c = Channel()
        c.name = ''
        c.title = ''
        c.description = ''
        c.image = ''
        # c.channeltype = ChannelType.objects.using('megavideo').all()[0]
        request.breadcrumbs(u'Cadastro', "javascript:void(0);")
    else: #para alterar o valor
        c = Channel.objects.using('megavideo').get(pk=channel_id)
        request.breadcrumbs(u'Alteração', "javascript:void(0);")

    if c.image:
        p['thumb_image'] = '/storage/' + str(c.image)
    else:
        p['thumb_image'] = '/megavideo/static/images/manager/default.jpg'

    if  'addValue' in request.POST:
        #FIXME default TV ID = 1
        url_amigavel = request.POST.get('name', '') != '' and request.POST.get('name', '') or request.POST.get('title', 'portallabel1')
        c.name = defaultfilters.slugify(url_amigavel)
        c.title = request.POST.get('title', '')
        c.description = request.POST.get('desc', '')

        p['form_error'] = []

        if c.title == '':
            p['form_error'] += [{'msg':'O nome é um campo obrigatório'}]

        if 'Filedata' in request.FILES and not upload_channel_image(request, channel_id , c):
             p['form_error'] += [{'msg':'A imagem não pode ser enviado'}]

        if len(p['form_error']) == 0:
             c.save(using='megavideo')
             return HttpResponseRedirect(request.channel_url + 'manager/channel/')

    channelId = 0

    p['metas'] = [
                  { 'float':'left'  , 'name':'Titulo*'       , 'validate': 'text'    , 'metaname' : 'title'       , 'value' : unicode(c.title) },
                  { 'float':'right' , 'name':'URL amigável:' , 'validate': 'text'    , 'metaname' : 'name'        , 'value' : unicode(c.name) },
                  { 'float':'left'  , 'name':'Descrição'     , 'validate': 'longtext', 'metaname' : 'desc'        , 'value' : unicode(c.description) },
                ]

    p['chan'] = channel_id

    p['channel_list'] = Channel.objects.using('megavideo').order_by('name')

    return render_to_response('manager/channel/form.html', p, context_instance=RequestContext(request))


def ajax_list_channel(request):
    p = {}

    program_id = request.REQUEST.get('video_id', False)
    c = Video.objects.using('megavideo').get(id=int(program_id))

    p['video'] = c
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']

    p['select_channel'] = c.get_channel()
    p['video_id'] = program_id

    p['channel_list'] = Channel.objects.using('megavideo').all().order_by('name')

    return render_to_response('manager/list_channel.html', p, context_instance=RequestContext(request))


def ajax_add_channel(request):
    p = {}

    listchan = request.REQUEST.getlist(u'listchannel[]')
    video_id = request.REQUEST.get('video_id')

    p['status'] = 'True'

    try:
        v = Video.objects.using('megavideo').get(id=int(video_id))
        for i in v.channel_set.all():
            v.channel_set.remove(i)
    except:
        p['status'] = 'False'
        print str('nao deletou nada!')

    for i in listchan:
        v.channel_set.add(Channel.objects.using('megavideo').get(id=int(i)))

    try:
        v = Video.objects.using('megavideo').get(id=int(video_id))
        p['count'] = v.channel_set.all().count()
    except:
        print 'nao trouxe video'
        p['count'] = 0

    return HttpResponse(json.dumps(p), mimetype='application/json')


def ajax_del_channel(request):
    p = {}

    video_id = request.REQUEST.get('video_id', False)
    channel_id = request.REQUEST.get('channel_id', False)

    p['status'] = False

    if channel_id and video_id:
        c = Video.objects.using('megavideo').get(id=int(video_id))
        c.channel_set.remove(Channel.objects.using('megavideo').get(id=int(channel_id)))
        p['status'] = True
    else:
        pass

    return HttpResponse(json.dumps(p), mimetype='application/json')



@login_required
def list_channel(request , page=1):
     #monta os menus
     p = menu_top(request);

     request.breadcrumbs('Configurações', "javascript:void(0)")
     request.breadcrumbs(u'Redes', request.channel_url + 'manager/channel/')

     content_list = Channel.objects.using('megavideo').all().order_by('name')
     p['filter_title'] = 'Gerênciar Canal'

     paginator = DiggPaginator(content_list, per_page, body=5, padding=1 , margin=1, tail=1)

     try:
         p['content_list'] = paginator.page(page)
     except:
         p['content_list'] = paginator.page(paginator.num_pages)

     p['digg_url'] = request.channel_url + 'manager/channel/page/'

     return render_to_response('manager/channel/list.html', p, context_instance=RequestContext(request))


@login_required
def del_channel(request):
    """ clean delcategory """

    channel_id = request.REQUEST.get('id', 0)

    ch = Channel.objects.using('megavideo').get(id=int(channel_id))
    p = {}

    try:
        ch.delete()
        p['status'] = True
    except:
        p['status'] = False

    cont = Channel.objects.using('megavideo').all().count()

    p['total'] = cont

    return HttpResponse(json.dumps(p), mimetype='application/json')


@login_required
def upload_channel_image(request, channel_id, c , path_dir='channel/'):

    file_data = request.FILES['Filedata']

    try:
        #delete old file for update new file
        os.remove(settings.MEDIA_ROOT + str(c.image))
    except:
        pass


    file_name = path_dir + str(c.id)
    name, ext = os.path.splitext(os.path.basename(file_data.name))
    file_name += '_' + os.path.basename(slugify(name)) + ext

    try:
        ipath = c.image.storage.save(file_name, file_data)

        #redimensionar imagem
        im = Image.open(settings.MEDIA_ROOT + file_name)
        im.save(settings.MEDIA_ROOT + file_name)

    except StandardError, e:
        LOGGER.debug(str(e))
        #print " error "

    c.image = ipath

    LOGGER.debug(str(c))

    c.save(using='megavideo')

    try:
        return True
    except:
        return False
