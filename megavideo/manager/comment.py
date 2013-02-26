# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from django.shortcuts import render_to_response
from django.template import RequestContext


from megavideo.video.models import *

per_page = 12

@login_required
def del_comments(request):
    """ clean delcategory """

    comment_id = request.POST.get('id', False)
    vc = VideoComment.objects.using('megavideo').get(id=comment_id)
    p = {}

    try:
       vc.delete()
       p['status'] = True
    except:
       p['status'] = False

    return HttpResponse(json.dumps(p), mimetype='application/json')


def ajax_pub_comments(request):
    """ clean pubcat """
    comment_id = request.POST['id']
    c = VideoComment.objects.using('megavideo').get(pk=comment_id)
    c.published = not c.published
    c.save(using='megavideo')

    p = {}
    p['status'] = int(c.published)

    return HttpResponse(json.dumps(p), mimetype='application/json')


@login_required
def update_comments(request, program_id):

    c = VideoComment.objects.using('megavideo').get(id=program_id)

    if 'upComment' in request.POST:
        c.content = request.POST['content']
        c.name = request.POST['name']
        c.email = request.POST['email']
        c.content = request.POST['content']
        c.save(using='megavideo');

    p['info'] = c

    return render_to_response('manager/comment/form.html', p, context_instance=RequestContext(request))


@login_required
def add_comments(request , comment_id=0):
    #monta os menus
    p = menu_top(request);
    p['form_action'] = request.get_full_path()[1:]

    request.breadcrumbs(u'Acervo', "javascript:void(0)")
    request.breadcrumbs(u'Comentários ', request.channel_url + 'manager/comment/')

    if comment_id == 0: #para cadastrar
        c = VideoComment()
        c.content = ''
        c.name = ''
        c.email = ''
        c.content = ''
        request.breadcrumbs(u'Cadastro', "javascript:void(0)")
    else: #para alterar o valor
        c = VideoComment.objects.using('megavideo').get(pk=comment_id)
        request.breadcrumbs(u'Alteração', "javascript:void(0)")

    if  'addValue' in request.POST:
        c.content = request.POST['content']
        c.name = request.POST['name']
        c.email = request.POST['email']

        p['form_error'] = []


        if c.content == '':
            p['form_error'] += [{'msg':'O comentário é um campo obrigatório'}]

        if c.name == '':
            p['form_error'] += [{'msg':'O nome é um campo obrigatório'}]

        if c.email == '':
            p['form_error'] += [{'msg':'O e-mail é um campo obrigatório'}]


        if len(p['form_error']) == 0:
             c.save(using='megavideo')
             return HttpResponseRedirect(request.channel_url + 'manager/comment/')

    p['metas'] = [
                  { 'name':'Nome*'       , 'validate': 'text'       , 'metaname' : 'name'      , 'value' : unicode(c.name) },
                  { 'name':'Email*'      , 'validate': 'text'       , 'metaname' : 'email'     , 'value' : unicode(c.email) },
                  { 'name':'Comentário*' , 'validate': 'longtext'   , 'metaname' : 'content'   , 'value' : unicode(c.content) },
                  ]

    p['video'] = c.video
    p['category_list'] = Category.objects.using('megavideo').filter(channel__name=request.channel_name)

    return render_to_response('manager/comment/form.html', p, context_instance=RequestContext(request))


@login_required
def list_comments(request, filtro='', program_id=0, page=1):
     #monta os menus
     p = menu_top(request);

     request.breadcrumbs('Acervo', "javascript:void(0)")
     request.breadcrumbs(u'Comentários ', request.channel_url + 'manager/comment/')
     per_page = 5

     print 'PROGRAM ID ' , program_id

     if program_id:
        video = Video.objects.using('megavideo').filter(id=program_id, channel__name=request.channel_name, videocomment__isnull=False).distinct().order_by('-date')
        p['video'] = video = video[0]
        p['digg_url'] = request.channel_url + 'manager/comment/%s/page/' % video.id
        per_page = 8
        content_list = video.videocomment_set.all()
     else:
        content_list = Video.objects.using('megavideo').filter(channel__name=request.channel_name, videocomment__isnull=False).distinct().order_by('-date')
        p['digg_url'] = request.channel_url + 'manager/comment/page/'

     paginator = DiggPaginator(content_list, per_page, body=5, padding=1 , margin=1, tail=1)

     try:
         p['content_list'] = paginator.page(page)
     except (EmptyPage, InvalidPage):
         p['content_list'] = paginator.page(paginator.num_pages)


     return render_to_response('manager/comment/list.html', p, context_instance=RequestContext(request))


def set_publish_comments(key, action):

    if action == 'active':

           c = VideoComment.objects.using('megavideo').get(pk=int(key))
           c.published = True
           c.save(using='megavideo')


    elif action == 'desactive':

           c = VideoComment.objects.using('megavideo').get(pk=int(key))
           c.published = False
           c.save(using='megavideo')

