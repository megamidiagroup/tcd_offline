# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.template import Library
from django.conf import settings

# import de todos os models da aplicação
from django.db.models import get_apps, get_models
for app in get_apps(): 
    for model in get_models(app): 
        locals()[model.__name__] = model

 
register = Library()

@register.filter()
def get_seo(category, type='title'):
    
    try:
        cat = category[0]
    except:
        cat = category
        
    s = cat.seo_set.all().order_by('date')
    
    if s.count() > 0:
        s = s[0]
    else:
        if cat.parent:
            cat = cat.parent
            s   = cat.seo_set.all().order_by('date')
            if s.count() > 0:
                s = s[0]
            else:
                # defaut
                s = Seo.objects.all().order_by('date')[0]
        else:
            # defaut
            s = Seo.objects.all().order_by('date')[0]
    
    if type == 'title':
        return s.title
    elif type == 'description':
        return s.description
    elif type == 'keywords':
        return s.keywords
    
    return ''