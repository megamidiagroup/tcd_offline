from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
#admin.autodiscover()
import os

prefix = settings.MEGAVIDEO_CONF.get('channel_prefix', 'channel')
tvname = settings.MEGAVIDEO_CONF.get('tv_name', 'portallabel')

urlpatterns = patterns('',
        url(r'^$'               , include('megavideo.portal.urls')),
        url(r'^portal/'         , include('megavideo.portal.urls')),
        url(r'^embed/'          , 'megavideo.video.views.embed'),

        url(r'^api/'            , include('megavideo.api.urls')),
        url(r'^gateway/$'       , 'megavideo.amf_services.services.VflowGateway'),
        url(r'^video/'          , include('megavideo.video.urls')),

        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT }),

        url(r'^storage/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root' : '/home/' + tvname + '/storage/'}),

        url(r'^stat/'           , include('megavideo.statistics.urls')),
        url(r'^stats/'          , include('megavideo.statistics.urls')),
        url(r'^player/'         , 'megavideo.video.views.index'),
        url(r'^captcha/'        , include('captcha.urls')),
        url(r'^'                , include('megavideo.portal.urls')),
)