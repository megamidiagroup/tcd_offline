"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

from django.conf import settings
from django.utils.functional import lazy
from megavideo.common.channel import get_current_channel
import os


def static(request):
    """
    Adds static-related context variables to the context.

    """
    return {'STATIC_URL': settings.STATIC_URL + '../%s' % settings.MV_TVNAME}


def request(request):
    """
    Adds request-related context variables to the context.
    """
    return {'request': request}


def client_css(request):
    """
    Adds request-related context variables to the context.

    """
    chan = get_current_channel(request)
    l = []
    try:
        for i in os.listdir(settings.STATIC_ROOT + '/portal/css/channels/'):
            if i.startswith(chan.name.lower())  and i.endswith('css'):
                l.append(i)

    except:
        pass
    return {'CLIENT_CSS' : l}

def client_js(request):
    """
    Adds request-related context variables to the context.

    """
    chan = get_current_channel(request)
    l = []
    try:
        for i in os.listdir(settings.STATIC_ROOT + '/portal/js/channels/'):
            if i.startswith(chan.name.lower())  and i.endswith('js'):
                l.append(i)
    except:
        pass

    return {'CLIENT_JS' : l}


