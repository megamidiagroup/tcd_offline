# -*- coding: utf-8 -*-
#django
from django.template import Library
from django.conf import settings
from django.template import defaultfilters

register = Library()

@register.filter
def get_subcategory(cat, limit):
    return cat.category_set.all().order_by('-id')[0:limit]
