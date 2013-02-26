from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'megavideo.api.views.index'),
    url(r'^widget/', 'megavideo.api.views.widget'),
    url(r'^widget_moodle/', 'megavideo.api.views.widget_moodle'),

    url(r'^swidget/', 'megavideo.api.search_widget.index'),
    url(r'^swidget_init', 'megavideo.api.search_widget.init'),
    url(r'^swidget_search', 'megavideo.api.search_widget.search'),

    url(r'^sebrae/html', 'megavideo.api.views.sebrae', {'html': True}),
    url(r'^sebrae/(?P<catname>\w+)/', 'megavideo.api.views.sebrae'),
    url(r'^sebrae', 'megavideo.api.views.sebrae'),

    url(r'^video/(?P<video_id>\d+)/set_metas/', 'megavideo.api.video.set_metas'),
    url(r'^video/embed.js', 'megavideo.api.embed.embed_js'),
    url(r'^video/(?P<video_id>\d+)/thumb/', 'megavideo.api.video.thumb'),

    # widget 
    url(r'^embed/test/', 'megavideo.api.embed.test'),
    url(r'^embed.js', 'megavideo.api.embed.embed_js'),

    url(r'^comment/test/', 'megavideo.api.comment.test'),
    url(r'^comment/add/', 'megavideo.api.comment.add_comment'),
    url(r'^comment.js', 'megavideo.api.comment.index'),

    url(r'^record/test/', 'megavideo.api.record.test'),
    url(r'^record.js', 'megavideo.api.record.index'),

    url(r'^list/test/', 'megavideo.api.list.test'),
    url(r'^list.js', 'megavideo.api.list.index'),
)