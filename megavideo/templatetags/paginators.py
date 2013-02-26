from django.template import Library

register = Library()

@register.inclusion_tag('templatetags/diggpaginator.html')
def digg_paginator(content, url):
    p = {'content_list' : content , 'url' : url}
    return p

@register.inclusion_tag('templatetags/searchpaginator.html')
def search_paginator(content, url, var_search):
    p = {'content_list' : content , 'url' : url, 'var_search' : var_search}
    return p


@register.inclusion_tag('templatetags/djangopaginator.html')
def django_paginator(content, url):
    p = {'content_list' : content , 'url' : url }
    return p

@register.inclusion_tag('templatetags/comment_list.html')
def comment_list(scrapbook_list, person_info):
    p = {'scrapbook_list' : scrapbook_list , 'person_info' : person_info }
    return p
