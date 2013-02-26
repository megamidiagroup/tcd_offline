#-*- coding: utf-8 -*-
from django.conf.urls.defaults import include, patterns, url

urlpatterns = patterns('megavideo.report',
        url(r'^email?/?$' , 'views.send_test'),
        url(r'^$' , 'views.index'),
)