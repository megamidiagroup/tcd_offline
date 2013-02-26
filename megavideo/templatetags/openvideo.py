from django import template
from django.conf import settings
register = template.Library()

def openvideo_url(video):
    ov = video.videotranscode_set.filter(transcode__name = 'OpenVideo')[0]
    return settings.MEDIA_URL + '/videos/' + video.dir + '/transcoded_' + ov.name

register.filter('openvideo_url', openvideo_url)


