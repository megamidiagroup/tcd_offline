#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('states.views',
    url(r'^states/json-combo/$', 'states_json_combo', name='states_json_combo'),

)
