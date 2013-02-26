# -*- coding: utf-8 -*-
#from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import connection, transaction
from django.template.defaultfilters import slugify, linebreaks
from megavideo.common.dlog import LOGGER
from django.contrib.auth.models import User
from django.conf import settings
from megavideo.video.models import *
from megavideo.common.login import login_required

per_page = 12

@login_required
def add_user(request , user_id = 0):
    p = menu_top(request);
    p['form_action'] = request.get_full_path()[1:]

    request.breadcrumbs(u'Configurações', "javascript:void(0)")
    request.breadcrumbs(u'Usuários ', request.channel_url + 'manager/user/')
    canal_list = 0

    if user_id == 0: #para cadastrar
        u = User()
        request.breadcrumbs(u'Cadastro', "javascript:void(0)")
    else: #para alterar o valor
        u = User.objects.using('megavideo').get(id = user_id)
        request.breadcrumbs(u'Alterar', "javascript:void(0)")

        try:
            canal_list = u.userchannel_set.all()[0].channel.id
        except:
            pass


    if  'addValue' in request.POST:
        u.username = request.POST.get('username'    , 0)

        passwordExit = request.POST.get('password'    , 0)

        if passwordExit != str(u.password)[0:5]:
            u.set_password(passwordExit)

        u.email = request.POST.get('email'      , 0)
        u.first_name = request.POST.get('firstname'  , 0)
        u.last_name = request.POST.get('lastname'   , 0)
        u.is_staff = request.POST.get('is_superuser', 0)
        u.is_active = request.POST.get('is_active'   , 0)
        u.is_superuser = request.POST.get('is_superuser', 0)
#        canal_list          = request.POST.getlist('check_list')
        canal_list = request.POST.get('channel', 0)

        p['form_error'] = []

        if u.username == '':
            p['form_error'] += [{'msg':'O nome é um campo obrigatório'}]


        if 'Filedata' in request.FILES and not upload_user_image(request, user_id , u):
             p['form_error'] += [{'msg':'A imagem não pode ser enviada.'}]


        if len(p['form_error']) == 0:
            u.save(using='megavideo')

            u.userchannel_set.all().delete()
            u.userchannel_set.create(channel_id = canal_list)

            return HttpResponseRedirect(request.channel_url + 'manager/user/')


    p['channel_list'] = Channel.objects.using('megavideo').order_by('name')
    p['user'] = u
    metas     = []

    p['metas'] = [
                  { 'name':'Senha'          , 'validate': 'password', 'metaname' : 'password'      , 'value'    : unicode(u.password) },
                  { 'name':'Primeiro nome'  , 'validate': 'text'    , 'metaname' : 'firstname'     , 'value'    : unicode(u.first_name) },
                  { 'name':'Sobre nome'     , 'validate': 'text'    , 'metaname' : 'lastname'      , 'value'    : unicode(u.last_name) },
                  { 'name':'E-mail'         , 'validate': 'text'    , 'metaname' : 'email'         , 'value'    : unicode(u.email) },
                ]

    if request.user.is_superuser:
        metas = [
                  { 'name':'Usuário*'       , 'validate': 'text'    , 'metaname' : 'username'      , 'value'    : unicode(u.username) },
		          { 'name':'É super usuário', 'validate': 'checkbox', 'metaname' : 'is_superuser'  , 'value'    : u.is_superuser },
                  { 'name':'Está ativo'     , 'validate': 'checkbox', 'metaname' : 'is_active'     , 'value'    : u.is_active },
                  { 'name':'Rede'           , 'validate': 'select'  , 'class'    :'select_channel' , 'metaname' : 'channel' , 'value' : int(canal_list) , 'list' : p['channel_list']  },
                ]
    else:
        metas = [
                  { 'name':'Usuário*' , 'validate': 'text'     , 'metaname' : 'username'  , 'value'    : unicode(u.username), 'disabled' : 'disabled'},
                  { 'name':''         , 'validate': 'checkbox' , 'metaname' : 'is_active' , 'value'    : u.is_active },
		          { 'name':''         , 'validate': 'text'     , 'metaname' : 'username'  , 'value'    : unicode(u.username) },
                ]

    tmp          = p['metas']
    p['metas']   = metas
    p['metas']  += tmp

    p['request'] = request

    return render_to_response('manager/user/form.html', p, context_instance = RequestContext(request))


@login_required
def del_user(request):
    """ clean deluser """

    user_id = request.REQUEST.get('id', 0)

    u = User.objects.using('megavideo').get(pk = int(user_id))
    p = {}
    
    p['status'] = False

    activeUser     = request.user
    totalStaffUser = User.objects.using('megavideo').filter(is_staff = 1, is_superuser = 1).exclude(id = u.id).count()

    if activeUser.is_superuser and activeUser.is_staff:
        if totalStaffUser >= 1 and activeUser.id != user_id:
            
            cursor = connection.cursor()
            
            try:
                #u.delete(using='megavideo')
                ## function definitiva para excluir user sem interferir nos objetos do tcd
                cursor.execute('DELETE FROM megavideo.auth_user WHERE id = %d' % int(user_id))
                p['status'] = True
            except:
                pass

    cont = User.objects.using('megavideo').all().count()

    p['total'] = cont

    return HttpResponse(json.dumps(p), mimetype = 'application/json')


@login_required
def list_user(request, page = 1):
     p = menu_top(request)

     request.breadcrumbs('Configurações', "javascript:void(0)")
     request.breadcrumbs(u'Usuários', request.channel_url + 'manager/user/')

     try:
         sUser = request.user
     except:
         sUser = 0

     content_list = User.objects.using('megavideo').all().order_by('username')

     p['current_user'] = sUser.id

     p['filter_title'] = 'Gerênciar usuários'

     paginator = DiggPaginator(content_list, per_page, body = 5, padding = 1 , margin = 1, tail = 1)

     if sUser:
         p['is_superuser'] = sUser.is_superuser

     p['content_list'] = paginator.page(page)

     p['digg_url'] = request.channel_url + 'manager/user/page/'

     return render_to_response('manager/user/list.html', p, context_instance = RequestContext(request))


def upload_user_image(request, user_id, u , path_dir = 'user/'):

    file_data = request.FILES['Filedata']

    try:
        #delete old file for update new file
        os.remove(settings.MEDIA_ROOT + str(u.get_profile().image))
    except:
        pass

    file_name = path_dir + str(u.id)
    name, ext = os.path.splitext(os.path.basename(file_data.name))
    file_name += '_' + os.path.basename(slugify(name)) + ext

    try:
        ipath = u.get_profile().image.storage.save(file_name, file_data)
    except StandardError, e:
        LOGGER.debug(str(e))
        #print " error "

    LOGGER.debug(str(u))
    u.get_profile().save(using='megavideo')

    try:
        return True
    except:
        return False
