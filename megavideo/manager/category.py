# -*- coding: utf-8 -*-
#from django.contrib.auth.decorators import login_required

from menu import *
from megavideo.common.DiggPaginator import *
from megavideo.common.login import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from megavideo.common.dlog import LOGGER
from PIL import Image


from megavideo.video.models import *

per_page = 12

#===============================================================================

def ajax_categorize(request):
    p = {}
    select_category = request.POST.getlist(u'select_category[]')
    select_video = request.POST.getlist(u'select_video[]')

    p['status'] = True

    #add for all videos all categories selected
    for i in select_video:

        c = VideoCategory.objects.using('megavideo').get(video__id=i)
        c.delete()

        for j in select_category:
            vc = VideoCategory()
            vc.video_id = i
            vc.category_id = j
            try:
                vc.save(using='megavideo')
            except:
                p['status'] = False
                break

    return HttpResponse(json.dumps(p), mimetype='application/json')


def ajax_list_category(request):

    p = menu_top(request);

    program_id = request.REQUEST.get('video_id', False)

    c = Video.objects.using('megavideo').get(id=int(program_id))
    p['video'] = c
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']

    p['select_category'] = c.get_category()
    p['video_id'] = program_id

    p['category_list'] = Category.objects.using('megavideo').filter(parent__isnull=True, channel__name=request.channel_name).order_by('name')

    return render_to_response('manager/list_category.html', p, context_instance=RequestContext(request))


def ajax_del_category(request):

    p = {}

    video_id = request.REQUEST.get('video_id', False)
    category_id = request.REQUEST.get('category_id', False)

    p['status'] = False

    if category_id and video_id:
        c = VideoCategory.objects.using('megavideo').filter(video__id=int(video_id), category__id=int(category_id))
        c.delete()
        p['status'] = True
    else:
        pass

    """
    try:
        v = Video.objects.using('megavideo').get(id = int(video_id))
        p['count'] = v.videocategory_set.all().count()
        if p['count'] == 0:
            print 'depublica video'
            v.published = False
            v.save(using='megavideo')
    except:
        print 'nao trouxe video'
        p['count'] = 0
    """

    return HttpResponse(json.dumps(p), mimetype='application/json')


def ajax_add_category(request):

    p = {}

    listcat  = request.REQUEST.getlist(u'listcategory[]')
    video_id = request.REQUEST.get('video_id')

    p['status'] = 'True'

    try:
        v = Video.objects.using('megavideo').get(id=int(video_id))
        c = v.videocategory_set.all()
        c.delete()
    except:
        p['status'] = 'False'

    for i in listcat:
        try:
            v.videocategory_set.create(category_id = int(i))
        except:
            pass

    try:
        v = Video.objects.using('megavideo').get(id=int(video_id))
        p['count'] = v.videocategory_set.all().count()
    except:
        p['count'] = 0

    return HttpResponse(json.dumps(p), mimetype='application/json')


def ajax_toggle_category(request):
    p = {}
    category_id = int(request.REQUEST.get('category_id', 0))
    video_id = int(request.REQUEST.get('video_id', 0))

    f = VideoCategory.objects.using('megavideo').filter(video__id=video_id, category__id=category_id)

    if f.count() > 0:
        f.delete()
        p['status'] = 'removed'
    else:
        vc = VideoCategory()
        vc.video_id = video_id
        vc.category_id = category_id
        vc.save(using='megavideo')
        p['status'] = 'cadastred'

    return HttpResponse(json.dumps(p), mimetype='application/json');


@login_required
def list_category(request , category_id=0 , filtro='', page=1):
     #monta os menus
     p = menu_top(request)

     request.breadcrumbs('Configurações', "javascript:void(0)")
     request.breadcrumbs(u'Categorias', request.channel_url + 'manager/category/')

     if category_id:
         request.breadcrumbs(Category.objects.using('megavideo').get(id=category_id).name, "javascript:void(0)")
         content_list = Category.objects.using('megavideo').filter(id=category_id, channel__name=request.channel_name).order_by('sequence', 'name', '-id')
     else:
         content_list = Category.objects.using('megavideo').filter(parent__isnull=True, channel__name=request.channel_name).order_by('sequence', 'name', '-id')

     p['filter_title'] = 'Gerênciar categorias'

     try:
         menu_action = request.POST.get('menu_action')
         for i in request.POST.getlist(u'list_checkbox[]'):
              set_publish_category(i , menu_action)
     except:
         pass

     if filtro == 'active':
         content_list = content_list.filter(published=True , channel__name=request.channel_name).order_by('sequence', 'name', '-id')
         p['filter_title'] = 'Gerênciar categorias ativas'

     elif filtro == 'desactive':
         content_list = Category.objects.using('megavideo').filter(published=False , channel__name=request.channel_name).order_by('sequence', 'name', '-id')
         p['filter_title'] = 'Gerênciar categorias desativas'


     #paginator    = Paginator(content_list, per_page) # mostra 15 contatos por página
     total_record = content_list.count() + 1
     paginator = DiggPaginator(content_list, total_record , body=5, padding=1 , margin=1, tail=1)

     try:
         p['content_list'] = paginator.page(page)
     except:
         p['content_list'] = paginator.page(paginator.num_pages)


     p['digg_url'] = request.channel_url + 'manager/category/page/'

     return render_to_response('manager/category/list.html', p, context_instance=RequestContext(request))

@login_required
def add_category(request, parent=0, category_id=0, parent_id=0): #addcategory
    #monta os menus
    p = menu_top(request)
    p['form_action'] = request.get_full_path()[1:]

    request.breadcrumbs(u'Configurações', "javascript:void(0)")

    if parent_id:
        try:
            p['parent'] = Category.objects.using('megavideo').get(id=parent_id)
            request.breadcrumbs(u'Subcategorias ', "javascript:void(0)")
        except:
            pass
    else:
        request.breadcrumbs(u'Categorias ', request.channel_url + 'manager/category/')

    current_channel = Channel.objects.using('megavideo').get(name=request.channel_name)

    if category_id == 0: #para cadastrar
        c = Category()
        c.name = ''
        #c.description   = ''
        c.image = ''
        p['tipo'] = 'Cadastrar categoria'
        request.breadcrumbs(u'Cadastro', "javascript:void(0)")

        if int(parent_id) != 0:
            c.parent = Category.objects.using('megavideo').get(pk=parent_id)
        else:
            c.parent = None

    else: #para alterar o valor
        c = Category.objects.using('megavideo').get(pk=category_id)
        p['tipo'] = 'Alterar categoria'
        request.breadcrumbs(u'Alteração', "javascript:void(0)")

    if c.image:
        p['thumb_image'] = '/storage/' + str(c.image)

    if  'addValue' in request.POST:
        c.name = request.POST['title']
        c.description = request.POST['desc']
        parent_id = int(request.POST.get('parent_id', 0))

        c.channel_id = current_channel.id

        p['form_error'] = []

        if c.name == '':
            p['form_error'] += [{'msg':'O nome é um campo obrigatório'}]

        if 'Filedata' in request.FILES and not upload_category_image(request, category_id , c):
             p['form_error'] += [{'msg':'A imagem não pode ser enviado'}]

        if 'DocFile' in request.FILES and not upload_category_document(request, category_id, c):
             p['form_error'] += [{'msg':'O arquivo não pode ser enviado'}]

        if len(p['form_error']) == 0:
             c.save(using='megavideo')
             category_id = c.id
             return HttpResponseRedirect(request.channel_url + 'manager/category/')

    p['metas'] = [
                  { 'name':'Titulo*'  , 'validate': 'text'       , 'metaname' : 'title'      , 'value' : unicode(c.name) },
                  { 'name':'Imagem'  , 'validate': 'file'       , 'metaname' : 'Filedata'   , 'value' : unicode(c.image) },
                  { 'name':'Descrição' , 'validate': 'longtext'   , 'metaname' : 'desc'       , 'value' : unicode(c.description) },
                  ]


    return render_to_response('manager/category/form.html', p, context_instance=RequestContext(request))


@login_required
def del_category(request):
    """ clean delcategory """

    category_id = request.POST.get('id', 0)

    c = Category.objects.using('megavideo').get(pk=int(category_id))
    p = {}

    try:
       c.delete()
       p['status'] = True
    except:
       p['status'] = False

    c = Category.objects.using('megavideo').all()

    p['total'] = c.count()
    p['total_active'] = c.filter(published=True).count()
    p['total_desactive'] = c.filter(published=False).count()

    return HttpResponse(json.dumps(p), mimetype='application/json')


@login_required
def pub_category(request):
    """ clean pubcat """
    category_id = request.POST.get('id', False)
    p = {}
    if category_id:
        c = Category.objects.using('megavideo').get(pk=category_id)

        #print 'category_id --------------------------------------------------'
        #print category_id

        if c.published != True:
            c.published = True
        else:
            c.published = False
            sub_c = Category.objects.using('megavideo').filter(parent__id=category_id)
            for i in sub_c:
                i.published = False
                i.save(using='megavideo')

        c.save(using='megavideo')


        p['status'] = c.published

    else:

        p['status'] = 'Não recebeu o id da categoria'


    return HttpResponse(json.dumps(p), mimetype='application/json')

def order_category_sort(request):
    p = {}
    order = request.REQUEST.get('order', '').split(',')
    order.remove('')
    print 'UPDATE'
    p['order'] = order
    p['status'] = False

    if len(order):
        to_change = Category.objects.using('megavideo').filter(id__in=order).order_by('sequence')
        count = 1
        for i in order:
            d = to_change.get(id=i)
            d.sequence = count
            d.save(using='megavideo')
            count += 1
            p['status'] = True

    return HttpResponse(json.dumps(p), mimetype='application/json')


@login_required
def order_category(request):
     #monta os menus
     p = menu_top(request)

     content_list = Category.objects.using('megavideo').filter(parent=None, channel__name=request.channel_name).order_by('sequence')

     #paginator =  Paginator(content_list, content_list.count()) # mostra 15 contatos por página
     paginator = DiggPaginator(content_list, per_page, body=5, padding=1 , margin=1, tail=1)

     p['total_active'] = content_list.filter(published=True).count()
     p['total_desactive'] = content_list.exclude(published=True).count()
     p['total_categorys'] = content_list.count()

     try:
         p['content_list'] = paginator.page(page)
     except:
         p['content_list'] = paginator.page(paginator.num_pages)

     return render_to_response('manager/order/list.html', p, context_instance=RequestContext(request))

def upload_category_image(request, category_id, c , path_dir='category/'):

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

def upload_category_document(request, category_id , c , path_dir='category/document/'):

    file_data = request.FILES['DocFile']

    try:
        #delete old file for update new file
        os.remove(settings.MEDIA_URL + slugify(c.image))
    except:
        pass

    file_name = path_dir + str(c.id)
    name, ext = os.path.splitext(os.path.basename(file_data.name))
    file_name += '_' + os.path.basename(slugify(name)) + ext

    try:
        ipath = c.document.storage.save(file_name, file_data)
    except StandardError, e:
        LOGGER.debug(str(e))
    c.document = ipath

    try:
        c.save(using='megavideo')
        return True
    except:
        return False
