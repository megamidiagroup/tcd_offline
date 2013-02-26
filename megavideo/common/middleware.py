from django.conf import settings
from django.template import defaultfilters
from megavideo.common.dlog import LOGGER
from megavideo.common.login import get_user
from megavideo.video.models import Channel
import re

prefix = settings.MEGAVIDEO_CONF.get('channel_prefix', 'home')
prefix_regex = re.compile('/' + prefix + '/(?P<channame>.[^/]+)/(?P<realurl>.*)')


def join_url(x, y):
    try:
        d = str('/'.join([x, y]))
    except:
        d = unicode('/'.join([x, y]))
    return d.replace('//', '/')


class VFlowMiddlewareDispatcher(object):
    def process_request(self, request):
        
        if 'megavideo' in request.path:
    
            match = prefix_regex.search(request.path)
            if match:
                d = match.groupdict()
                
                realurl = '/' + d['realurl']
    
                if realurl[-1] != '/':
                    realurl += '/'
    
                realurl = '/megavideo%s' % realurl
    
                c = d['channame']
    
                request.path = realurl
                request.path_info = realurl
                request.has_prefix = True
            else:
                channel_default = Channel.objects.using('megavideo').get_or_create(name=settings.MEGAVIDEO_CONF['default_channel'])
                c = settings.MEGAVIDEO_CONF['default_channel']
                request.has_prefix = False
            
            request.user         = get_user(request)     
            request.channel_name = c
            request.channel_url  = "%s%s/%s/" % (settings.MEGAVIDEO_CONF.get('base_url', ''), prefix , c)
            request.base_url     = join_url(request.channel_url, request.get_full_path())
