# -*- coding: utf8 -*-
from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
admin.autodiscover()
import os

urlpatterns = patterns('',
	url(r'^click/', 'megavideo.statistics.views.click'),
	url(r'^/', 'megavideo.statistics.views.click'),
)