from django.conf.urls.defaults import include, patterns, url
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

admin.site.login = login_required(admin.site.login)

handler500 = '%smega.views.server_error_500' % settings.PROJECT_URL

urlpatterns = patterns('',
    url(r'^grappelli/'          , include('grappelli.urls')),
    url(r'^megavideo/'          , include('%smegavideo.urls' % settings.PROJECT_URL)),
    url(r'^admin/clear_cache/$' , '%smega.views.clear_cache' % settings.PROJECT_URL, name='clear_cache'),
    url(r'^admin/doc/'          , include('django.contrib.admindocs.urls')),
    url(r'^admin/'              , include(admin.site.urls)),
    url(r'^admin_tools/'        , include('admin_tools.urls')),
    url(r'^ckeditor/'           , include('ckeditor.urls')),

    url(r'^media/(?P<path>.*)$' , 'django.views.static.serve',
        {'document_root': settings.STATIC_DOC_ROOT}),

    url(r'^captcha/'            , include('captcha.urls')),

    url(r'^$'                   , include('%smega.urls' % settings.PROJECT_URL)),
    url(r'^'                    , include('%smega.urls' % settings.PROJECT_URL)),
)
