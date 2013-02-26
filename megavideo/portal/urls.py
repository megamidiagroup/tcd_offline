#-*- coding: utf-8 -*-

from django.conf.urls.defaults import include, patterns, url

urlpatterns = patterns('megavideo.portal',

        url(r'^video/(?P<video_id>\d+)/'                            , 'index.index'),
        url(r'^$'                                                   , 'index.index'),
        url(r'^category/(?P<cat_id>\d+)/subject/(?P<sub_id>\d+)'    , 'index.index'),
        url(r'^category/(?P<cat_id>\d+)/'                           , 'index.index'),
        
        url(r'^vast/(?P<video_id>\d+)/'                             , 'index.vast'),
        url(r'^vast/'                                               , 'index.vast'),

        #traduction
        url(r'^search/page/(?P<page>\d+)/tag/(?P<tag>\w+)/'         , 'search.search'),
        url(r'^search/page/(?P<page>\d+)/'                          , 'search.search'),
        url(r'^search/tag/(?P<tag>\w+)/'                            , 'search.search'),
        url(r'^search/'                                             , 'search.search'),

        #captcha
        url(r'^ajaxcaptcha/'                                        , 'views.ajax_captcha'),

        #ajax
        url(r'^ajaxsearch/'                                         , 'search.ajax_search'),
        url(r'^ajax_send_comment/'                                  , 'comments.ajax_send_comment'),
        url(r'^ajax_itens_comment/'                                 , 'comments.ajax_itens_comment'),
        url(r'^ajax_comment_list/'                                  , 'comments.ajax_comment_list'),
        url(r'^optionembed/'                                        , 'views.option_embed'),
        url(r'^live/'                                               , 'live.index'),
        
)