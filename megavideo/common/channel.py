from megavideo.video.models import *
from django.conf import settings
from django.template import defaultfilters

def get_url_prefix(request, channel): # FIXME: replace to request.channel_url
    if 'channel_prefix' in settings.MEGAVIDEO_CONF:
        prefix = settings.MEGAVIDEO_CONF['channel_prefix']
    else:
        prefix = 'channel'

    if channel:
        return prefix + '/' + channel.name + '/'
    else:
        return prefix + '/' + request.session['channel'].name + '/'

def get_video_url(request, video): # FIXME: replace to model video.get_video_url
    try:
        prefix = get_url_prefix(request, video.channel_set.all()[0])
    except:
        prefix = ''
    return settings.MEGAVIDEO_CONF['base_url'] + prefix + "video/" + str(video.id) + "/" + defaultfilters.slugify(video.get_name())

def get_current_channel(request): # FIXME: replace to request.channel_name
    try:
        return Channel.objects.using('megavideo').get(name=request.channel_name)
    except:
        try:
            return Channel.objects.using('megavideo').get(name=settings.MEGAVIDEO_CONF['default_channel'])
        except:
            chan = Channel.objects.using('megavideo').create(name=settings.MEGAVIDEO_CONF['default_channel'], description='Auto create default channel from settings')
            return chan
