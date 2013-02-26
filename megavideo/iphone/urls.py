#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django.conf.urls.defaults import include, patterns, url

urlpatterns = patterns('megavideo.iphone',
        url(r'^$', 'views.index'),
        url(r'^app/', 'views.index_app'),
)