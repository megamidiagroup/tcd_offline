# -*- coding: utf-8 -*-

#from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from megavideo.video.models import *
from menu import *
from megavideo.video.views   import get_absolute_url
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from megavideo.statistics.models import VisitorAction, VisitorLog, Visitor, Location, VisitorDownload
from django.db.models import Count, Sum
from megavideo.common.DiggPaginator import *

from megavideo.async.call import AsyncCall
from megavideo.common.dlog import LOGGER
from megavideo.common.channel import get_current_channel

from django.conf import settings
import os.path
import tempfile
import simplejson as json
from datetime import datetime, timedelta

from megavideo.video.models import *
from megavideo.api.video import video_search
from megavideo.common.login import login_required
from django.core.servers.basehttp import FileWrapper
from django.template.defaultfilters import slugify

per_page = 10

def build_video_url(video_id, name):
    """ clean """
    url = '/vflow/video/' + str(video_id) + '/' + name + '/'
    return url


def build_video_js_url (video_id, name):
    """ clean """
    url = 'javascript: loadPlayer("' + str(video_id) + '", "' + name + '")'
    return url


def get_video(video_id):
    """ clean """
    return Video.objects.using('megavideo').get(pk=video_id)


def get_video_meta_display(video_id):
    """ clean """
    v = Video.objects.using('megavideo').get(pk=video_id)
    res = []
    for i in get_video_meta_keys(video_id):
        vm = v.videometa_set.filter(metaclass__id=i[2])
        if len(vm) != 0:
            res.append({'name' : i[1], 'value' : vm[0].value, 'metaname' : i[0], 'validate' : i[3]})
        else:
            res.append({'name' : i[1], 'metaname' : i[0], 'validate' : i[3]})
    return res


def get_video_meta_keys(video_id):
    """ clean """
    v = Video.objects.using('megavideo').get(pk=video_id)
    vmc = v.videoclass.videometaclass_set.all()

    r = []
    for i in vmc:
        mc = i.metaclass
        r.append([mc.name, i.displayname, mc.id, mc.validate])

    return r


@csrf_exempt
def get_video_meta_values(video_id):
    """ clean """
    v = Video.objects.using('megavideo').get(pk=video_id)

    res = {}
    for i in get_video_meta_keys(video_id):
        vm = v.videometa_set.filter(metaclass__id=i[2])
        if len(vm) != 0:
            res[i[0]] = vm[0].value
        else:
            res[i[0]] = ''
    return res


def get_video_infos(video_id):
    baseurl = INI.get('SkMC', 'base_url')
    v = Video.objects.using('megavideo').get(pk=video_id)
    r = {'duration': v.duration, 'name': v.name, 'dir' : v.dir, 'id': v.id}
    if r['duration'] == 0:
        ski = SkInfo()
        f = INI.get_generic_file(r['name'], r['dir'])
        d = ski.infoFile(f)
        if d != None:
            try:
                r['duration'] = d['general']['duration']
                v.duration = r['duration']
                v.save(using='megavideo')
            except:
                pass
    if r['rateNum'] != 0:
        r['rate'] = r['rateSum'] / r['rateNum']
    else:
        r['rate'] = 0

    r['link'] = baseurl + "?idVideo=" + str(r['id'])
    return r


def set_video_meta_values(video_id, vdict):
    """ clean """
    v = Video.objects.using('megavideo').get(pk=video_id)

    safe_fields = ['name', 'description']

    for i in safe_fields:

        if i == 'name':
            v.title = vdict[i]

        if i == 'description':
            v.description = vdict[i]

    v.save(using='megavideo')

    return HttpResponse('ok')


@login_required
def order_video(request, category_id=1 , page=1):

    p = menu_top(request)
    category = Category.objects.using('megavideo').get(id=category_id)

    content_list = category.videocategory_set.all().order_by('sequence')

    p['total_active'] = 0
    p['total_desactive'] = 0
    p['total_categorys'] = content_list.count()

    paginator = DiggPaginator(content_list, per_page, body=5, padding=1 , margin=1, tail=1)

    p['content_list'] = paginator.page(page)
    p['selection'] = category.name

    return render_to_response('manager/order/list_video.html', p, context_instance=RequestContext(request))


def order_video_sort(request):
    p = {}
    order = request.REQUEST.get('order', '').split(',')
    order.remove('')
    p['order'] = order
    p['status'] = False

    if len(order):
        to_change = VideoCategory.objects.using('megavideo').filter(id__in=order).order_by('sequence')
        count = 1
        for i in order:
            d = to_change.get(id=i)
            d.sequence = count
            d.save(using='megavideo')
            count += 1
            p['status'] = True

    return HttpResponse(json.dumps(p), mimetype='application/json')



#===============================================================================
# Gerencia de Programas
#===============================================================================

def set_publish_program(key, action):
    if action == 'active':
           c = Video.objects.using('megavideo').get(pk=int(key))
           c.published = True
           c.save(using='megavideo')

    elif action == 'desactive':
           c = Video.objects.using('megavideo').get(pk=int(key))
           c.published = False
           c.save(using='megavideo')


@login_required
def list_program(request, category_id=0, page=1, filtro='', search=''):
     #monta os menus
     p = menu_top(request)
     p['form_action'] = 'manager/program/'

     search = request.REQUEST.get('search', search)
     category_id = request.REQUEST.get('category_id', category_id)

     request.breadcrumbs('Acervo', "javascript:void(0)")
     request.breadcrumbs(u'Vídeos', request.channel_url + 'manager/program/')

     if search:
        p['form_action'] += 'search/%s/' % search

     if category_id:
        p['category_id'] = int(category_id)
        p['form_action'] += 'category/%s/' % category_id


     content_list = video_search(category=category_id, value=search, channel=request.channel_name, orderby='-id')


     if filtro:
         p['form_action'] += 'filter/%s/' % filtro

     paginator = DiggPaginator(content_list, 16 , body=5, padding=1 , margin=1, tail=1)

     try:
         p['content_list'] = paginator.page(page)
     except (EmptyPage, InvalidPage):
         p['content_list'] = paginator.page(paginator.num_pages)

     p['list_category'] = Category.objects.using('megavideo').filter(parent__isnull=True, channel__name=request.channel_name).order_by('name').distinct()
     p['search'] = search
     p['digg_url'] = request.channel_url + p['form_action'] + 'page/'

     return render_to_response('manager/program/list.html', p, context_instance=RequestContext(request))


def upload_program_document(request, program_id , c , path_dir='program/document/'):

    file_data = request.FILES['DocFile']

    try:
        d = Document.objects.using('megavideo').filter(video=c)[0]
    except:
        d = Document()

    ##print "path old file " +  settings.MEDIA_ROOT + slugify(d.filename)

    try:
        #delete old file for update new file
        os.remove(settings.MEDIA_ROOT + d.filename)
    except:
        pass

    file_name = path_dir + str(c.id)
    name, ext = os.path.splitext(os.path.basename(file_data.name))
    file_name += '_' + os.path.basename(slugify(name)) + ext

    try:
        ipath = d.filename.storage.save(file_name, file_data)
    except StandardError, e:
        LOGGER.debug(str(e))

    dc = DocumentClass.objects.using('megavideo').get(name='PDF')

    d.documentclass = dc
    d.video = c
    d.filename = ipath
    d.save(using='megavideo')

    try:
        return True
    except:
        return False

def ajax_update_program(request):
    """ para salvar itens do formulario left das informações dos programas """

    p = {}
    filtered = {}
    cont = 0

    index = request.REQUEST.getlist(u"index[]")
    value = request.REQUEST.getlist(u"value[]")

    for i in index:
        filtered[i] = value[cont]
        cont += 1

    p['filter'] = filtered

    p['form_msg'] = []
    p['status'] = False

    if 'name' in filtered and not filtered['name']:
        p['form_msg'] += [{'msg':'O título é um campo obrigatório'}]

    if 'description' in filtered and not filtered['description']:
        p['form_msg'] += [{'msg':'A descrição é um campo obrigatório'}]

    if len(p['form_msg']) == 0 and len(filtered):
        #import manager/video_views.py
        set_video_meta_values(filtered['id'], filtered)
        p['status'] = True
        p['form_msg'] += [{'msg':'Dados cadastrados com sucesso'}]

    return HttpResponse(json.dumps(p), mimetype='application/json')


@login_required
def add_program(request, program_id=0): #addcategory
    #monta os menus
    p = menu_top(request)
    p['form_action'] = request.get_full_path()[1:]
    p['menu_session'] = 'update'

    request.breadcrumbs(u'Configurações', "javascript:void(0)")
    request.breadcrumbs(u'Vídeo ', request.channel_url + 'manager/program/')

    if program_id == 0:
        program_id = request.REQUEST.get('program_id', False)

    if not program_id: #para cadastrar
        c = Video()
        request.breadcrumbs(u'Cadastro', "javascript:void(0)")
    else: #para alterar o valor
        request.breadcrumbs(u'Alteração', "javascript:void(0)")
        c = Video.objects.using('megavideo').get(pk=program_id)
        p['video'] = c
        p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
        p['absolute_url'] = get_absolute_url(request, 'FlashWeb', program_id)
        p['dimensao'] = {'width': 640, 'height': 360}
        p['video_id'] = c.id
        p['flash'] = render_to_string('embed.html', p)
        soma = p['video'].ratesum / 5

        #{{ base_url }}portal/video/{{ update.id }}/{{ update.get_name|slugify }}
        p['url_prefix_video'] = unicode(request.channel_url + 'video/' + str(c.id) + '/' + defaultfilters.slugify(c.get_name()))

        if soma < 5:
            p['safe_voted'] = soma
        else:
            p['safe_voted'] = 5

        p['vote'] = [1, 2, 3, 4, 5]

        #statistics
        status = 1
        base_url = settings.MEGAVIDEO_CONF['base_url']

        list = {'data1':0, 'data2':0 }
        pick = pickle.dumps(list)
        p['pick64'] = pick64 = base64.b64encode(pick)

        p['total_published'] = c.videocomment_set.filter(published=True).count()
        p['total_despublished'] = c.videocomment_set.filter(published=False).count()

        p['select_category'] = c.get_category()
        p['video_id'] = program_id

    combo = [
               {'value' : 'Colorido'        , 'metaname' : 'colorido'} #c.get_meta('cor')
             , {'value' : 'Preto e branco'  , 'metaname' : 'preto e branco'}
    ]

    p['metas'] = [
              {'name' : 'Titulo'      , 'validate' : 'text'     , 'id' : 'form_name'         , 'metaname' : 'name'          , 'disabled' : 'false' , 'value' : c.get_meta('name')}
            , {'name' : 'Descrição'   , 'validate' : 'longtext' , 'id' : 'form_description'  , 'metaname' : 'description'   , 'disabled' : 'false' , 'value' : c.get_meta('description'), 'class' : 'resizable'}
            , {'name' : ''            , 'validate' : 'hidden'   , 'id' : 'form_hiddenid'     , 'metaname' : 'id'            , 'disabled' : 'false' , 'value' : program_id}
    ]
    
    p['list_channel']  = Channel.objects.using('megavideo').all().order_by('-name')
    p['list_category'] = Category.objects.using('megavideo').filter(parent__isnull=True, channel__name=request.channel_name).order_by('-name')
    
    p['category_id']   = None
    
    try:
        p['category_id'] = c.videocategory_set.all()[0].category.id
    except:
        pass
    
    try:
        for j in request.user.userchannel_set.all():
            tmp = j.channel.name
            p['list_channel'] = None
    except:
        pass

    p['extra_css'] = 'portal_background'

    p['no_del']    = True

    try:
        #está para estado de false para não fazer isso mais por enquanto
        if request.session['category_id'] > 0 and False:

            p['selection'] = Category.objects.using('megavideo').filter(id=request.session['category_id'])[0].name

            objectVideos = Video.objects.using('megavideo').filter(category__id=int(request.session['category_id']))

            total_active = objectVideos.filter(published=True).distinct().count()
            total_desactive = objectVideos.filter(published=False).distinct().count()
            total_videos = objectVideos.distinct().count()

            p['menu_nav'] = [
                  {'url' : request.channel_url + 'manager/program/filter/vote/page/1/'       , 'menu_item' : 'mais_vistos'   , 'class' : ''         , 'text' : 'Mais vistos' }
                , {'url' : request.channel_url + 'manager/program/'                          , 'menu_item' : 'todos_videos'  , 'class' : ''         , 'text' : 'Todos os vídeos (' + str(total_videos) + ')' }
                , {'url' : request.channel_url + 'manager/program/filter/active/page/1/'     , 'menu_item' : 'publicados'    , 'class' : 'public'   , 'text' : 'Públicados (<span id="total_active">' + str(total_active) + '</span>)' }
                , {'url' : request.channel_url + 'manager/program/filter/desactive/page/1/'  , 'menu_item' : 'despublicados' , 'class' : 'nopublic' , 'text' : 'Despúblicados (<span id="total_desactive">' + str(total_desactive) + '</span>)' }
            ]

        else:
            p['selection'] = c.videocategory_set.all()[0].category.name
            p['selection2'] = 'Editar Vídeo'
            p['selectionaction'] = request.channel_url + 'manager/program/' + str(c.videocategory_set.all()[0].category.id)
    except:
        pass
    
    p['code'] = c.serialize(c.id)

    return render_to_response('manager/program/form.html', p, context_instance=RequestContext(request))


def build_content_infos (idcontent):
    """ almost clean """
    v = Video.objects.using('megavideo').get(pk=idcontent)
    #t = v.videothumb_set.all()[0]
    href = build_content_url(idcontent, v.name)
    p = {'playerfile' : urllib.urlencode({'arquivo' : href})}
    p['video_href'] = href
    p['metas'] = get_content_meta_display(idcontent)
    p['comments'] = v.contentcomment_set.all().order_by('id')
    mv = get_content_meta_values(video_id)
    p['displayName'] = mv[v.contentclass.metatitle]
    p['numComments'] = len(p['comments'])
    p['views'] = v.views
    lcats = [i.type for i in v.contenttype.all()]
    if 'A' in lcats:
        p['thumb'] = '/megavideo/static/images/thumb_audio.jpg'
    elif 'T' in lcats:
        p['thumb'] = '/megavideo/static/images/thumb_texto.jpg'
    else:
        p['thumb'] = v.get_thumb_url()
    p['duration'] = str(v.duration) + ' segundos '
    if v.published:
        p['published'] = 1
    else:
        p['published'] = 0
    p['id'] = idcontent
    if v.ratenum > 0:
        p['rate'] = v.ratesum / v.ratenum
    else:
        p['rate'] = 0

    p['votes'] = v.ratenum
    p['video_idb64'] = base64.b64encode(str(v.id))
    p['date'] = v.date.strftime('%d/%m/%y, %H:%M:%S')
    p['transcodes'] = ['Original'] + [i.transcode.name for i in v.contanttranscode_set.all()]
    return p


@login_required
def del_program(request):
    """ clean delcategory """

    program_id = request.POST['id']
    c = Video.objects.using('megavideo').get(pk=program_id)
    p = {}

    try:
       c.delete()
       p['status'] = True

    except:
       p['status'] = False

    vc = Video.objects.using('megavideo').all()

    p['total'] = vc.count()
    p['total_active'] = vc.filter(published=True).count()
    p['total_desactive'] = vc.filter(published=False).count()

    return HttpResponse(json.dumps(p) , mimetype='application/json')


@login_required
def deldoc_program(request):
    """ clean delcategory """
    program_id = request.POST['id']
    c = Video.objects.using('megavideo').get(pk=program_id)
    p = {}

    try:
        #delete old file for update new file
        for j in c.document_set.all():
            os.remove(settings.MEDIA_ROOT + str(j.filename))
            j.delete()

        p['status'] = True

    except:

        for j in c.document_set.all():
            p['alvo'] = settings.MEDIA_ROOT + str(j.filename)

        p['status'] = False

    return HttpResponse(json.dumps(p) , mimetype='application/json')


def auto_maling_radio():
    print 'Enviar email para os radialistas'


@login_required
def pub_program(request):
    """ clean pubcat """
    program_id = request.POST['id']
    v = Video.objects.using('megavideo').get(pk=program_id)
    p = {}

    v.published = not v.published
    v.save(using='megavideo')

    p['alert'] = False
    p['status'] = v.published

    return HttpResponse(json.dumps(p), mimetype='application/json')

#===============================================================================    
@csrf_exempt
def upload(request):
    """ clean """
    LOGGER.debug('upload starts ' + str(request.FILES.keys()))
    LOGGER.debug('before')
    r = {}
    msg = {}

    print 'REQUEST.POST --------------------------------------------- >'
    print request.POST
    print 'REQUEST.POST --------------------------------------------- <'


    if 'category' in request.REQUEST:
        category_id = request.REQUEST['category']
    else:
        category_id = 0

    r = {'name' : '', 'description' : '', 'author': '', 'email': ''}
    for i in ['name', 'description', 'author', 'email']:
        if i in request.POST:
            r[i] = request.POST[i]


    LOGGER.debug('receive post ' + str(request.FILES))


    if 'Filedata' in request.FILES:
        LOGGER.debug('insider')

        file_uploaded = request.FILES['Filedata']

        if r['name'] == '':
            try:
                r['name'] = file_uploaded.name
            except:
                r['name'] = datetime.datetime.now()
                LOGGER.debug('Erro no nome do arquivo')

        LOGGER.debug('hook')

        try:
            conf = settings.MEGAVIDEO_CONF
            tmp  = tempfile.mktemp('_' + conf['tv_name'])
            tmp  = conf['tmp'] + os.path.basename(tmp)
            fd   = open(tmp, 'wb')
        except  StandardError, e:
           LOGGER.debug("Erro ao criar o arquivo: " + str(e))

        LOGGER.debug('opened')

        for chunk in file_uploaded.chunks():
            fd.write(chunk)
        fd.close()

        LOGGER.debug('insider3')

        job = Job()
        job.channel = Channel.objects.using('megavideo').get(name=request.channel_name)
        job.ip = request.META['REMOTE_ADDR']
        job.status = 'A'
        job.original_name = file_uploaded.name
        job.message = 'inserting upload/megavideo interface'
        job.save(using='megavideo')

        LOGGER.debug('insider4')
        try:
            acall = AsyncCall(conf['dispatch'], conf['tv_name'], channel_id=job.channel.id)
            #print 'CHANNEL -----------------------------------------------------'
            #print chan

            kargs = {
                    'transcode' : True,
                    'keep_video' : True,
                    'chan_id' : job.channel.id,
                    'metas': r
                    }

            if int(category_id) != 0:
                kargs['cat_id'] = category_id
            LOGGER.debug('insider5')

            # Add user on video if logged
            if request.user.is_authenticated():
                kargs['user_id'] = request.user.id
                LOGGER.debug('Add user - insider6')


        except StandardError, e:
             LOGGER.debug("create kwargs error " + str(e))

        try:
            acall.set_job(job)
            acall.set_insert(tmp, **kargs)
            acall.call()
            LOGGER.debug('after calling acall')
        except StandardError, e:
            LOGGER.debug("acall error " + str(e))


        if 'redirect' in request.REQUEST:
            return HttpResponseRedirect(request.channel_url + 'manager/jobs/%d/' % (job.id))
        msg = {'error' : 0, 'job' : job.id}
        return HttpResponse(json.dumps(msg), mimetype='application/json')

    msg = {'error' : 1, 'job' : 0}

    return HttpResponse(json.dumps(msg), mimetype='application/json')


@csrf_exempt
def set_thumb(request, key=''):
    """ clean """

    video_id = Video().deserialize( key )

    v = Video.objects.using('megavideo').get(pk=int(video_id))
    conf = settings.MEGAVIDEO_CONF
    seek = request.REQUEST['tempo']
    chan = get_current_channel(request)
    acall = AsyncCall(conf['dispatch'], conf['tv_name'], channel_id=chan.id)

    acall.args['commands'] = (('select_video', (v.id,)),
                            ('extract_infos', ()),
                            ('delete_thumbnails', ()),
                            ('create_thumb', (seek,)))


    job = Job()
    job.ip = request.META['REMOTE_ADDR']
    job.status = 'A'
    job.original_name = v.get_name()
    job.message = 'Recreate thumbnail'
    job.save(using='megavideo')

    acall.set_job(job)

    acall.call()

    r = {'error' : 0, 'job' : job.id}
    return HttpResponse(json.dumps(r))


def ajax_change_channel(request):
    video_id = request.REQUEST.get('video_id', 0)
    channel_id = request.REQUEST.get('channel_id', 0)

    try:
        video = Video.objects.using('megavideo').get(id=video_id)
        video_channel = video.channel_set.all()[0]
        video.remove(video_channel)
        video.add(Channel.objects.using('megavideo').get(id=channel_id))
        r = { 'status':1 }
    except:
        r = { 'status':0 }

    return HttpResponse(json.dumps(r))



def download_video(request, video_id=0):
    video = Video.objects.using('megavideo').filter(id=video_id)

    if video:
        video = video[0]

        #record download
        dw = VisitorDownload()
        dw.video = video
        dw.channel = video.channel_set.all()[0]
        dw.size = video.size
        dw.time = datetime.datetime.now()
        dw.save(using='megavideo')

        video.get_original_file()
        filename = video.realpath
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper)


        pointer = video.original_name.rfind('.')
        basename = video.original_name[0:pointer]
        ext = video.original_name[pointer:]

        response['Content-Disposition'] = 'attachment; filename=%s%s' % (slugify(basename), ext)

        return response


@login_required
def list_embed(request, page=1):
    
    p = menu_top(request)
    
    p['form_action'] = 'manager/list_embed/'
    
    content_list  = video_search(category=0, value='', channel=request.channel_name, orderby='-id')
    
    p['base_url'] = settings.MEGAVIDEO_CONF.get('base_url', 'https://www.treinandoequipes.com.br/megavideo/')
    
    paginator = DiggPaginator(content_list, 4, body=5, padding=1 , margin=1, tail=1)

    try:
        p['content_list'] = paginator.page(page)
    except:
        p['content_list'] = paginator.page(paginator.num_pages)

    p['digg_url'] = request.channel_url + p['form_action'] + 'page/'
    
    return render_to_response('manager/program/list_embed.html', p, context_instance=RequestContext(request))