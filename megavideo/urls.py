from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
#admin.autodiscover()
import os

prefix = settings.MEGAVIDEO_CONF.get('channel_prefix', 'channel')
tvname = settings.MEGAVIDEO_CONF.get('tv_name', 'portallabel')

urlpatterns = patterns('',

        url(r'^teste/$'         , 'megavideo.portal.views.teste'),

        url(r'^$'               , include('megavideo.portal.urls')),
        url(r'^portal/'         , include('megavideo.portal.urls')),
        
        url(r'^get_media/(?P<user>\w+)/(?P<key>\w+)/' , 'megavideo.manager.views.get_media'),

        #app report
        url(r'^report/'         , include('megavideo.report.urls')),

        url(r'^embed/'          , 'megavideo.video.views.embed'),

        url(r'^api/'            , include('megavideo.api.urls')),
        url(r'^gateway/$'       , 'megavideo.amf_services.services.VflowGateway'),

        url(r'^iphone/'         , include('megavideo.iphone.urls')),

        url(r'^manager/'        , include('megavideo.manager.urls')),

        url(r'^video/'          , include('megavideo.video.urls')),

        url(r'^geoprocess/'     , 'megavideo.statistics.views.geoprocess'),

        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT }),

        url(r'^webtv/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/' + tvname + '/www/webtv_test/'}),

        url(r'^storage/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root' : '/home/' + tvname + '/storage/'}),

        url(r'^webtv/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/home/igdev/www/webtv/'}),

        url(r'^stat/'           , include('megavideo.statistics.urls')),
        url(r'^stats/'          , include('megavideo.statistics.urls')),
        url(r'^player/'         , 'megavideo.video.views.index'),

        url(r'^captcha/'        , include('captcha.urls')),

        url(r'^link/$'          , 'megavideo.link.views.index'),
        url(r'^link/add/$'      , 'megavideo.link.views.add_link'),
        url(r'^l/(?P<linkid>.+)', 'megavideo.link.views.access_link'),

        url(r'^link/$'          , 'megavideo.link.views.index'),
        url(r'^link/add/$'      , 'megavideo.link.views.add_link'),
        url(r'^l/(?P<linkid>.+)', 'megavideo.link.views.access_link'),

        url(r'^v/(?P<video_id>\d+)/' , 'megavideo.video.views.redirect'),
        url(r'^'                     , include('megavideo.portal.urls')),
)