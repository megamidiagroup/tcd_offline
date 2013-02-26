from django.template import Library
from django.template import Context, Template

register = Library()

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    BeautifulSoup = None

VALID_TAGS = "b strong a div p li ul ol blockquote".split()
@register.filter
def soup(value):
    """ Strips text from the given html string, leaving only tags. """
    if BeautifulSoup is None:
        return value
    soup = BeautifulSoup(value)
    [ tag.extract() for tag in list(soup) if not (getattr(tag, 'name', None) in VALID_TAGS) ]
    return str(soup)