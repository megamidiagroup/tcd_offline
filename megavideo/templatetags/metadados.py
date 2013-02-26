from django.template import Library
from django.conf import settings

register = Library()

@register.filter
def get_meta(video, name, limit = 0):
    value = video.get_meta(name)
    if limit != 0:
        value = value[0:limit]
    return value
