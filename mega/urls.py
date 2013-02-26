from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

urlpatterns = patterns('%smega.views' % settings.PROJECT_URL,
    url(r'^noie6/'                                           , 'noie6', name='noie6'),
    url(r'^home/'                                            , 'home', name='home'),

    url(r'^(?P<rede>\w+)/logout/$'                           , 'logout', name='logout'),
    url(r'^logout/$'                                         , 'logout', name='logout'),
    url(r'^(?P<rede>\w+)/login/$'                            , 'login', name='login'),
    url(r'^login/$'                                          , 'login', name='login'),

    url(r'^(?P<rede>\w+)/action/$'                           , 'action', name='action'),
    
    url(r'^cities/(?P<state_id>\d+)/$'                       , 'cities', name='cities'),
    url(r'^cities/$'                                         , 'cities', name='cities'),
    
    url(r'^favicon\.ico$'                                    , 'favicon', name='favicon'),

    url(r'^(?P<rede>\w+)/busca/$'                            , 'busca', name='busca'),
    url(r'^(?P<rede>\w+)/conta/edit/$'                       , 'conta_edit', name='conta_edit'),
    url(r'^(?P<rede>\w+)/conta/add/$'                        , 'conta_add', name='conta_add'),
    url(r'^(?P<rede>\w+)/conta/$'                            , 'conta', name='conta'),
    url(r'^(?P<rede>\w+)/certificado/(?P<tipo>\w+)/$'        , 'certificado', name='certificado'),
    url(r'^(?P<rede>\w+)/certificado/$'                      , 'certificado', name='certificado'),
    url(r'^(?P<rede>\w+)/faq/$'                              , 'faq', name='faq'),
    url(r'^(?P<rede>\w+)/avaliacao/(?P<key>[a-zA-Z=0-9]+)/$' , 'avaliacao', name='avaliacao'),
    url(r'^(?P<rede>\w+)/questionario/(?P<video_id>\d+)/$'   , 'questionario', name='questionario'),
    url(r'^(?P<rede>\w+)/suggestion/(?P<video_id>\d+)/$'     , 'suggestion', name='suggestion'),
    url(r'^(?P<rede>\w+)/elearning/(?P<video_id>\d+)/$'      , 'elearning', name='elearning'),
    url(r'^(?P<rede>\w+)/treinamento/(?P<video_id>\d+)/$'    , 'treinamento', name='treinamento'),
    url(r'^(?P<rede>\w+)/treinamento/send_faq/(?P<id>\d+)/$' , 'send_faq', name='send_faq'),
    url(r'^(?P<rede>\w+)/treinamento/faq_edit/(?P<id>\d+)/$' , 'faq_edit', name='faq_edit'),
    url(r'^(?P<rede>\w+)/live/(?P<video_id>\d+)/$'           , 'live', name='live'),
    url(r'^(?P<rede>\w+)/live/load/(?P<video_id>\d+)/$'      , 'live_load', name='live_load'),
    url(r'^(?P<rede>\w+)/category/(?P<cat_id>\d+)/$'         , 'category', name='category'),
    url(r'^(?P<rede>\w+)/downanexo/(?P<anexo_id>\d+)/$'      , 'download_anexo', name='download_anexo'),
    url(r'^(?P<rede>\w+)/planos/$'                           , 'planos', name='planos'),
    url(r'^(?P<rede>\w+)/static/(?P<page>\w+)/$'             , 'static', name='static'),
    url(r'^(?P<rede>\w+)/teaser/$'                           , 'teaser', name='teaser'),
    url(r'^(?P<rede>\w+)/badget/(?P<key>[a-zA-Z=0-9]+)/$'    , 'badget', name='badget'),
    url(r'^(?P<rede>\w+)/agendamento/$'                      , 'agendamento', name='agendamento'),
    url(r'^(?P<rede>\w+)/retornopagamento'                   , 'retornopagamento', name='retornopagamento'),
    
    url(r'^(?P<rede>\w+)/widget/video/(?P<video_id>\d+)/$'   , 'widget_video', name='widget_video'),
    url(r'^(?P<rede>\w+)/ajax_check_mail/$'                  , 'ajax_check_mail', name='ajax_check_mail'),
    
    url(r'^(?P<rede>\w+)/home/$'                             , 'home', name='home'),
    url(r'^(?P<rede>\w+)$'                                   , 'home', name='home'),
    url(r'^(?P<rede>\w+)/$'                                  , 'home', name='home'),

    url(r'^$'                                                , 'home', name='home'),
    url(r'^'                                                 , 'home', name='home'),
)