# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string

from megavideo.video.models import *
from megavideo.api.video import video_search

per_page = 12


@login_required
def add_home(request, page=1, search=False , typevideofeatured=''):
    """ Mostra lista de itens para adicionar na home como destaque """
    p = menu_top(request)
    search = request.REQUEST.get('search', search)
    p['typevideofeatured'] = typevideofeatured


    if typevideofeatured == 'v':

        content_list = video_search(value=search, channel=request.channel_name)

        p['filter_title'] = 'Adicionar vídeo de destaque'
        p['digg_url'] = request.channel_url + 'manager/featured/add/video/page/'
        p['form_action'] = request.channel_url + 'manager/featured/add/video/'

    else:

        if search:
            content_list = Category.objects.using('megavideo').filter(name__icontains=search, published=True, channel__name=request.channel_name).distinct().order_by('-id')
        else:
            content_list = Category.objects.using('megavideo').filter(published=True, channel__name=request.channel_name)

        p['filter_title'] = 'Adicionar categoria de destaque'

        if search:
            p['flash_search'] = search
            p['digg_url'] = request.channel_url + 'manager/featured/add/category/search/s%/page/' % search
            p['form_action'] = request.channel_url + '/manager/featured/add/category/search/s%/' % search
        else:
            p['digg_url'] = request.channel_url + 'manager/featured/add/category/page/'
            p['form_action'] = request.channel_url + 'manager/featured/add/category/'

        p['theme'] = False

    paginator = DiggPaginator(content_list, per_page, body=5, padding=1 , margin=1, tail=1)

    try:
        p['content_list'] = paginator.page(page)
    except:
        p['content_list'] = paginator.page(paginator.num_pages)

    p['redirect'] = request.session.get('redirect', '')

    return render_to_response('manager/featured/form.html', p, context_instance=RequestContext(request))


@login_required
def list_home(request):
    """ Mostra a listagem dos destaques para categorias e videos """
    p = menu_top(request)

    request.breadcrumbs('Configurações', "javascript:void(0)")
    request.breadcrumbs(u'Destaque', request.channel_url + 'manager/featured/')

    p['category_id'] = 0
    redirect = request.channel_url + 'manager/featured/'

    request.session['redirect'] = redirect

    VF = VideoFeatured.objects.using('megavideo').filter(channel__name=request.channel_name)
    C = Category.objects.using('megavideo').filter(parent__isnull=True, channel__name=request.channel_name)

    category = VF.filter(typevideofeatured__name='c')
    video = VF.filter(typevideofeatured__name='v')

    try:
        p['video_list'] = Video.objects.using('megavideo').filter(id=video[0].video_id)
        p['video_id'] = video[0].id
    except:
        p['video_list'] = []

    try:
        p['destaque_category'] = category[0].category_id
        p['category_id'] = category[0].id
    except:
        pass

    p['category_list'] = C.all().order_by('-name')
    p['list_category'] = render_to_string('manager/featured/list_category.html', p)

    try:
        delete(request.session['search_flash'])
    except:
        pass

    return render_to_response('manager/featured/list.html', p, context_instance=RequestContext(request))


def ajax_del_home(request):
    """ para remove novo item na home """
    p = {}
    p['status'] = False
    id = int(request.REQUEST.get('id', 0))

    try:
        vf = VideoFeatured.objects.using('megavideo').get(id=id)
        vf.delete()
        p['status'] = True
    except:
        pass

    return HttpResponse(json.dumps(p), mimetype='application/json')


def ajax_add_home(request):
    """ para adicionar novo item na home """

    p = {}
    p['status'] = False

    id = request.REQUEST.get('itens[]', False)
    typevideofeatured = request.REQUEST.get('typevideofeatured', False)
    channel = Channel.objects.using('megavideo').get(name=request.channel_name)

    try:
        id = int(id)
    except:
        return HttpResponse(json.dumps(p), mimetype='application/json')

    try:
        vf = VideoFeatured.objects.using('megavideo').filter(channel__name=channel, typevideofeatured__name=typevideofeatured)
        vf.delete()
    except:
        pass

    if typevideofeatured:
        try:

            _type = TypeVideoFeatured.objects.using('megavideo').get(name=typevideofeatured)

            vf = VideoFeatured()
            if typevideofeatured == 'v':
                vf.video_id = id
            if typevideofeatured == 'c':
                vf.category_id = id
            vf.channel = channel
            vf.typevideofeatured = _type
            vf.save(using='megavideo')

            p['status'] = True

        except:
            pass

    return HttpResponse(json.dumps(p), mimetype='application/json')


@login_required
def add_videos(request, search=False, page=1):
    """ lista de videos para serem selecionados """

    #monta os menus
    p = menu_top(request)
    search = request.REQUEST.get('search', search)

    try:
        menu_action = request.POST.get('menu_action')
        for i in request.POST.getlist(u'list_checkbox[]'):
             set_publish_prograns(i , menu_action)
    except:
        pass

    content_list = video_search(channel=request.channel_name)

    if search:
        content_list = content_list.filter(videometa__value__icontains='test')
        p['digg_url'] = request.channel_url + 'manager/featured/addvideos/search/%s/page/' % search
        p['search'] = search
    else:
        p['digg_url'] = request.channel_url + 'manager/featured/addvideos/page/'

    paginator = DiggPaginator(content_list, 28 , body=5, padding=1 , margin=1, tail=1)

    try:
        p['content_list'] = paginator.page(page)
    except (EmptyPage, InvalidPage):
        p['content_list'] = paginator.page(paginator.num_pages)

    p['form_action'] = 'manager/featured/addvideos/'
    p['list_category'] = Category.objects.using('megavideo').filter(parent__isnull=True).filter(channel__name=request.channel_name).order_by('-id')

    return render_to_response('manager/featured/list_video.html', p, context_instance=RequestContext(request))


def ajax_list_category_featured(request):
    """ para obter a lista das categorias """

    p = {}
    p = menu_top(request)

    channel = request.channel_name

    VF = VideoFeatured.objects.using('megavideo').filter(channel__name=channel)
    C = Category.objects.using('megavideo').filter(parent__isnull=True, channel__name=channel)

    category = VF.filter(typevideofeatured__name='c')

    try:
        p['destaque_category'] = category[0].category_id
        p['category_id'] = category[0].id
    except:
        pass

    p['category_list'] = C.all().order_by('-name')

    return render_to_response('manager/featured/list_category.html', p, context_instance=RequestContext(request))
