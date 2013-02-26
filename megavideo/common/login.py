from django.conf import settings
from django.shortcuts import HttpResponseRedirect


def login_required(f):
    def wrap(request, *args, **kwargs):
        
        next    = request.path
        channel = ''
        
        try:
            channel = request.session.get('login_megavideo', None).userchannel_set.all()[0].channel.name
        except:
            pass
        
        if request.session.get('login_megavideo', None) is None or not request.session.get('login_megavideo', None).is_active or (channel and channel != request.channel_name):
            if len(next) > 2:
                return HttpResponseRedirect(settings.MEGAVIDEO_LOGIN_URL + '?next=%s' % next.replace('/megavideo/', '/'))
            return HttpResponseRedirect(settings.MEGAVIDEO_LOGIN_URL)
        
        return f(request, *args, **kwargs)

    wrap.__doc__   = f.__doc__
    wrap.__name__  = f.__name__
    
    return wrap


def set_login(request, user):
    
    request.session['login_megavideo'] = user
    
    return user


def get_user(request):
    
    try:
        return request.session.get('login_megavideo', request.user)
    except:
        pass
    
    return None


def del_login(request):
    
    try:
        del request.session['login_megavideo']
    except:
        pass

    return request