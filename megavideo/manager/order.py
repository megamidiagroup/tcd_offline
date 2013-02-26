# -*- coding: utf-8 -*-
#from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from megavideo.common.login import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext


from megavideo.video.models import *
from django.template.loader import render_to_string

per_page = 12


@login_required
def list_order(request):
     """ index para trazer a lista montada """
     
     p = menu_top(request)
     category = Category.objects.using('megavideo').filter(parent__isnull = True, channel__name = request.channel_name).order_by('sequence', '-id')

     request.breadcrumbs('Configurações', "javascript:void(0)")
     request.breadcrumbs(u'Ordenar', request.channel_url + 'manager/orderby/')

     try:
         selected = request.REQUEST.get('id', category[0].id)
     except:
         return render_to_response('manager/order/list_order.html', p, context_instance = RequestContext(request))

     p['selected']          = int(selected)
     p['category_list']     = category
     p['subcategory_list']  = category.get(id = selected).get_subcategory()
     
     try:
         p['video_list'] = p['subcategory_list'][0].video_set.all().order_by('videocategory__sequence')[0:20]
     except:
         p['video_list'] = category.get(id = selected).videocategory_set.all().order_by('sequence')[0:20]

     return render_to_response('manager/order/list_order.html', p, context_instance = RequestContext(request))


def list_order_reload(request):
    """ ordenação das categorias, subcategorias e programas """
    
    p = {}
    
    catid    = request.REQUEST.get('catid'      , 0)
    subcatid = request.REQUEST.get('subcatid'   , 0)
    parentid = request.REQUEST.get('parentid'   , 0)

    c = Category.objects.using('megavideo').filter(parent__isnull = True, channel__name = request.channel_name).order_by('sequence', '-id')

    if catid:
        p['subcategory_list'] = c.get(id = int(catid)).get_subcategory()
        t = {}
        t['parentid'] = int(catid)
        try:
            t['subcatid'] = p['subcategory_list'][0].id
        except:
            t['subcatid'] = int(catid)

        t['content'] = render_to_string('manager/order/list_order_subcategory.html', p, context_instance = RequestContext(request))

        return HttpResponse(json.dumps(t), mimetype = 'application/json')

    if subcatid:
        try:
            p['video_list'] = c[0].category_set.all()[0].video_set.all().order_by('videocategory__sequence')[0:20]
        except:
            p['video_list'] = c.get(id = int(parentid)).videocategory_set.all().order_by('sequence')[0:20]

        return render_to_response('manager/order/list_order_video.html', p, context_instance = RequestContext(request))

    p['video_list'] = 0
    
    return render_to_response('manager/order/list_order_video.html', p, context_instance = RequestContext(request))


def ajax_category_sort(request):
    p = {}
    order = request.REQUEST.getlist('order[]')
    p['order'] = order
    p['status'] = False

    if len(order):
        to_change = Category.objects.using('megavideo').filter(id__in = order).order_by('sequence')
        count = 1
        for i in order:
            d = to_change.get(id = i)
            d.sequence = count
            d.save(using='megavideo')
            count += 1
            p['status'] = True

    return HttpResponse(json.dumps(p), mimetype = 'application/json')


def ajax_video_sort(request):
    p = {}
    order = request.REQUEST.getlist('order[]')
    print 'UPDATE'
    p['order'] = order
    p['status'] = False

    if len(order):
        to_change = VideoCategory.objects.using('megavideo').filter(id__in = order).order_by('sequence')
        count = 1
        for i in order:
            d = to_change.get(id = i)
            d.sequence = count
            d.save(using='megavideo')
            count += 1
            p['status'] = True

    return HttpResponse(json.dumps(p), mimetype = 'application/json')
