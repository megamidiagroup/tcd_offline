from django.template import Library
from django.conf import settings

register = Library()

@register.inclusion_tag('templatetags/show_star.html')
def show_star(video):
    vote = int(video.get_vote())
    stars_voted = []

    for i in range(1, 6):
        if vote >= i:
            stars_voted.append(True)
        else:
            stars_voted.append(False)

    p = {
         'stars_voted' : stars_voted ,
         'STATIC_URL' : getattr(settings, 'STATIC_URL', '')
         }
    return p
