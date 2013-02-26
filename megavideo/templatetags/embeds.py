from django.template import Library
from django.conf import settings

register = Library()

@register.inclusion_tag('templatetags/embed.html')
def video_embed(video, width = 640, height = 360, channel = settings.MEGAVIDEO_CONF['default_channel'], transcode = 'FlashWeb'):
    p = {}
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
    p['dimensao'] = { 'width': width, 'height': height }
    p['video_id'] = video.id
    return p
