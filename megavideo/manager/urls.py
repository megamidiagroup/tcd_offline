from django.conf.urls.defaults import include, patterns, url
from django.conf.urls.defaults import *

urlpatterns = patterns('megavideo.manager',

     url(r'^$'                                                     , 'views.login_view'),

     url(r'^logout'                                                , 'views.logout_view'),

     url(r'^orderby/reload/'                                      , 'order.list_order_reload'),
     url(r'^orderby/ajax_category_sort/'                          , 'order.ajax_category_sort'),
     url(r'^orderby/ajax_video_sort/'                             , 'order.ajax_video_sort'),
     url(r'^orderby/'                                             , 'order.list_order'),

     url(r'^panel/'                                                , 'views.index'),
     url(r'^ajax_register_bug/'                                    , 'views.ajax_register_bug'),

     url(r'^featured/add/video/search/(?P<search>.[^/]*)/page/(?P<page>\d+)/' , 'featured.add_home', {'typevideofeatured' : 'v'}),
     url(r'^featured/add/video/page/(?P<page>\d+)/'                        , 'featured.add_home', {'typevideofeatured' : 'v'}),
     url(r'^featured/add/video/search/(?P<search>.[^/]*)/'                    , 'featured.add_home', {'typevideofeatured' : 'v'}),
     url(r'^featured/add/video/'                                           , 'featured.add_home', {'typevideofeatured' : 'v'}),

     url(r'^featured/add/category/search/(?P<search>.[^/]*)/page/(?P<page>\d+)/' , 'featured.add_home', {'typevideofeatured' : 'c'}),
     url(r'^featured/add/category/page/(?P<page>\d+)/'                     , 'featured.add_home', {'typevideofeatured' : 'c'}),
     url(r'^featured/add/category/search/(?P<search>.[^/]*)/'                 , 'featured.add_home', {'typevideofeatured' : 'c'}),
     url(r'^featured/add/category/'                                        , 'featured.add_home', {'typevideofeatured' : 'c'}),

     url(r'^featured/addvideos/search/(?P<search>.[^/]*)/page/(?P<page>\d+)/' , 'featured.add_videos'),
     url(r'^featured/addvideos/page/(?P<page>\d+)/'                        , 'featured.add_videos'),
     url(r'^featured/addvideos/search/(?P<search>.[^/]*)/'                    , 'featured.add_videos'),
     url(r'^featured/addvideos/'                                           , 'featured.add_videos'),

     url(r'^featured/ajaxadd/'                                             , 'featured.ajax_add_home'),
     url(r'^featured/ajaxdel/'                                             , 'featured.ajax_del_home'),
     url(r'^featured/ajaxlistcategory/'                                    , 'featured.ajax_list_category_featured'),
     url(r'^featured/'                                                     , 'featured.list_home'),

     url(r'^import/jobs/'                                          , 'jobs.status_jobs'),
     url(r'^import/ajaxdeljob/'                                    , 'jobs.ajax_del_job'),
     url(r'^import/'                                               , 'views.flashimport'),

     url(r'^category/addsub/(?P<parent_id>\d+)/'          , 'category.add_category'),
     url(r'^category/update/(?P<category_id>\d+)'                  , 'category.add_category'),
     url(r'^category/filter/(?P<filtro>\w+)/page/(?P<page>\d+)/'   , 'category.list_category'),
     url(r'^category/filter/(?P<filtro>\w+)/'                      , 'category.list_category'),
     url(r'^category/del/'                                         , 'category.del_category'),
     url(r'^category/publish/'                                     , 'category.pub_category'),
     url(r'^category/add/'                                         , 'category.add_category'),
     url(r'^category/addsub/(?P<parent>\d+)/'                      , 'category.add_category'),
     url(r'^category/order/sort/'                                  , 'category.order_category_sort'),
     url(r'^category/order/'                                       , 'category.order_category'),
     url(r'^category/(?P<category_id>\d+)/ordervideo/'             , 'video.order_video'),
     url(r'^category/(?P<category_id>\d+)/'                        , 'category.list_category'),
     url(r'^category/'                                             , 'category.list_category'),

     url(r'^user/add/'                                     , 'user.add_user'),
     url(r'^user/update/(?P<user_id>\d+)/'                 , 'user.add_user'),
     url(r'^user/del/'                                     , 'user.del_user'),
     url(r'^user/page/(?P<page>\d+)/'                      , 'user.list_user'),
     url(r'^user/'                                         , 'user.list_user'),


     url(r'^channel/add/'                                          , 'channel.add_channel'),
     url(r'^channel/update/(?P<channel_id>\d+)/'                    , 'channel.add_channel'),
     url(r'^channel/del/'                                          , 'channel.del_channel'),
     url(r'^channel/page/(?P<page>\d+)/'                           , 'channel.list_channel'),
     url(r'^channel/'                                              , 'channel.list_channel'),

     url(r'^program/order/sort/'                                   , 'video.order_video_sort'),
     url(r'^ftp/del/'                                              , 'ftp.del_file'),
     url(r'^ftp/'                                                  , 'ftp.list_ftp'),

     url(r'^program/download/(?P<video_id>\d+)/'                   , 'video.download_video'),
     url(r'^program/ajaxcategorize/'                               , 'category.ajax_categorize'),

     url(r'^program/search/(?P<search>.[^/]*)/category/(?P<category_id>\d+)/page/(?P<page>\d+)/'  , 'video.list_program'),
     url(r'^program/search/(?P<search>.[^/]*)/category/(?P<category_id>\d+)/'  , 'video.list_program'),

     url(r'^program/search/(?P<search>.[^/]*)/page/(?P<page>\d+)/'    , 'video.list_program'),
     url(r'^program/search/(?P<search>.[^/]*)/'                       , 'video.list_program'),


     url(r'^program/category/(?P<category_id>\d+)/page/(?P<page>\d+)/'  , 'video.list_program'),
     url(r'^program/category/(?P<category_id>\d+)/'                     , 'video.list_program'),

     url(r'^program/category/ajaxdel/'                                 , 'category.ajax_del_category'),
     url(r'^program/category/ajaxadd/'                                 , 'category.ajax_add_category'),
     url(r'^program/category/ajaxlistcategory/'                        , 'category.ajax_list_category'),

     url(r'^program/channel/ajaxdel/'                                 , 'channel.ajax_del_channel'),
     url(r'^program/channel/ajaxadd/'                                 , 'channel.ajax_add_channel'),
     url(r'^program/channel/ajaxlistchannel/'                         , 'channel.ajax_list_channel'),

     url(r'^set_thumb/_(?P<key>[a-zA-Z=0-9]+)/'                    , 'video.set_thumb'),

     url(r'^program/tag/(?P<video_id>\d+)/'                        , 'tag.list_tag'),
     url(r'^program/ajaxaddtag/'                                   , 'tag.add_tag'),
     url(r'^program/ajaxedittag/'                                  , 'tag.edit_tag'),
     url(r'^program/ajaxlisttags/'                                 , 'tag.ajax_list_tag'),
     url(r'^program/ajaxdeltag/'                                   , 'tag.ajax_del_tag'),
     url(r'^program/ajaxgettag/'                                   , 'tag.ajax_get_tag'),

     url(r'^program/publicity/(?P<video_id>\d+)/'                  , 'publicity.list_publicity'),
     url(r'^program/publicity/ajaxdel/'                            , 'publicity.ajax_del_publicity'),
     url(r'^program/publicity/ajaxlist/'                           , 'publicity.ajax_list_publicity'),
     url(r'^program/publicity/ajaxpublished'                       , 'publicity.ajax_published_publicity'),

     url(r'^program/filter/(?P<filtro>\w+)/page/(?P<page>\d+)/'    , 'video.list_program'),
     url(r'^program/filter/(?P<filtro>\w+)/'                       , 'video.list_program'),
     url(r'^program/page/(?P<page>\d+)/'                           , 'video.list_program'),
     url(r'^program/deldoc/'                                       , 'video.deldoc_program'),
     url(r'^program/publish/'                                      , 'video.pub_program'),
     url(r'^program/ajaxtogglecategory/'                           , 'category.ajax_toggle_category'),
     url(r'^program/update/(?P<program_id>\d+)/'                   , 'video.add_program'),
     url(r'^program/ajaxupdateprogram/'                            , 'video.ajax_update_program'),
     url(r'^program/del/'                                          , 'video.del_program'),
     url(r'^program/add/'                                          , 'video.add_program'),

     #url(r'^program/category/(?P<category_id>\d+)/page/(?P<page>\d+)/', 'views.list_program'),
     #url(r'^program/category/(?P<category_id>\d+)/'                   , 'views.list_program'),

     url(r'^program/'                                              , 'video.list_program'),

     url(r'^upload/'                                                , 'video.upload'),
     url(r'^uploadpublicity/(?P<video_id>\d+)/(?P<idpublicity>\d+)' , 'views.upload_publicity'),
     url(r'^uploadpublicity/(?P<video_id>\d+)'                      , 'views.upload_publicity'),
     url(r'^savepublicity/(?P<idpublicity>\d+)'                     , 'views.save_values_publicity'),

     url(r'^comment/(?P<program_id>\d+)/page/(?P<page>\d+)/'       , 'comment.list_comments'),
     url(r'^comment/(?P<program_id>\d+)/'                          , 'comment.list_comments'),
     url(r'^comment/update/(?P<comment_id>\d+)'                    , 'comment.add_comments'),
     url(r'^comment/filter/(?P<filtro>\w+)/page/(?P<page>\d+)/'    , 'comment.list_comments'),
     url(r'^comment/filter/(?P<filtro>\w+)/'                       , 'comment.list_comments'),
     url(r'^comment/page/(?P<page>\d+)/'                           , 'comment.list_comments'),
     url(r'^comment/del/'                                          , 'comment.del_comments'),
     url(r'^comment/ajax_publish/'                                 , 'comment.ajax_pub_comments'),
     url(r'^comment/add/'                                          , 'comment.add_comments'),
     url(r'^comment/'                                              , 'comment.list_comments'),
     url(r'^list_embed/page/(?P<page>\d+)/'                        , 'video.list_embed'),
     url(r'^list_embed/'                                           , 'video.list_embed'),

     url(r'^live/'                                                 , 'live.index'),

#     url(r'^statistic/list/page/(?P<page>\d+)'                     , 'statistic.list'),
#     url(r'^statistic/list/(?P<busca>\w+)/'                        , 'statistic.list'),
#     url(r'^statistic/list/'                                       , 'statistic.list'),
     url(r'^statistic/info/(?P<video_id>\d+)'                      , 'statistic.index'),
     url(r'^statistics/ajax_table/'                                , 'statistic.refresh_maps'),
     url(r'^statistics/ajax_table_domain/'                         , 'statistic.refresh_maps_domain'),
     url(r'^statistic/'                                            , 'statistic.index'),

     url(r'^jobs/'                                                 , 'jobs.jobs'),
     url(r'^jobs/(?P<highlight>\d+)/'                              , 'jobs.jobs'),
     url(r'^embed/(?P<item>\w+)/'                                  , 'views.embed'),
#     url(r'^stat/sumary/(?P<category>.*),(?P<domain>.*),(?P<d_from>.*),(?P<d_to>.*),' , 'statistic.sumary'),

     url(r'^preroll/(?P<video_id>\d+)/', 'preroll.prerolldemo'),
)
