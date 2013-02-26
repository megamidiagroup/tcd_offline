#!/usr/bin/env python
#-*- coding: utf-8 -*-

from django.conf.urls.defaults import include, patterns, url

urlpatterns = patterns('megavideo.video',
    url(r'^get/_(?P<key>[a-zA-Z=0-9]+)/(?P<tname>\w+)/'	, 'views.get_transcode'),
    url(r'^player/_(?P<key>[a-zA-Z=0-9]+)/'		, 'views.player'),
    url(r'^thumb/_(?P<key>[a-zA-Z=0-9]+)/(?P<tsize>\w+)/'	, 'views.get_thumb'),
)