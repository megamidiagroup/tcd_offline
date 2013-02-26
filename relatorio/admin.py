# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.contrib import admin
from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse

from models import AlunoCadastrado, AlunoCertificado, TreinamentoConcluido, PontuacaoAluno, \
                        TreinamentoCadastrado, RelatorioGrafico

from views import alunocadastrado, alunocertificado, treinamentoconcluido, pontuacaoaluno, \
                        treinamentocadastrado, relatoriografico


class AlunoCadastradoAdmin(admin.ModelAdmin):
    list_display  = ('rede', 'user',)
    list_filter   = ('rede',)
    search_fields = ['rede']

    exclude = ['rede', 'user', 'count', 'acesso']

    def get_urls(self):
        urls = super(AlunoCadastradoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', admin.site.admin_view(alunocadastrado))
        )
        return my_urls + urls

admin.site.register(AlunoCadastrado, AlunoCadastradoAdmin)


class AlunoCertificadoAdmin(admin.ModelAdmin):
    list_display  = ('rede', 'user',)
    list_filter   = ('rede',)
    search_fields = ['rede']

    exclude = ['rede', 'user', 'count', 'acesso']

    def get_urls(self):
        urls = super(AlunoCertificadoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', admin.site.admin_view(alunocertificado))
        )
        return my_urls + urls

admin.site.register(AlunoCertificado, AlunoCertificadoAdmin)


class TreinamentoConcluidoAdmin(admin.ModelAdmin):
    list_display  = ('rede', 'user',)
    list_filter   = ('rede',)
    search_fields = ['rede']

    exclude = ['rede', 'user', 'count', 'acesso']

    def get_urls(self):
        urls = super(TreinamentoConcluidoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', admin.site.admin_view(treinamentoconcluido))
        )
        return my_urls + urls

admin.site.register(TreinamentoConcluido, TreinamentoConcluidoAdmin)


class PontuacaoAlunoAdmin(admin.ModelAdmin):
    list_display  = ('rede', 'user',)
    list_filter   = ('rede',)
    search_fields = ['rede']

    exclude = ['rede', 'user', 'count', 'acesso']

    def get_urls(self):
        urls = super(PontuacaoAlunoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', admin.site.admin_view(pontuacaoaluno))
        )
        return my_urls + urls

admin.site.register(PontuacaoAluno, PontuacaoAlunoAdmin)


class TreinamentoCadastradoAdmin(admin.ModelAdmin):
    list_display  = ('rede', 'user',)
    list_filter   = ('rede',)
    search_fields = ['rede']

    exclude = ['rede', 'user', 'count', 'acesso']

    def get_urls(self):
        urls = super(TreinamentoCadastradoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', admin.site.admin_view(treinamentocadastrado))
        )
        return my_urls + urls

admin.site.register(TreinamentoCadastrado, TreinamentoCadastradoAdmin)


class RelatorioGraficoAdmin(admin.ModelAdmin):
    list_display  = ('rede', 'user',)
    list_filter   = ('rede',)
    search_fields = ['rede']

    exclude = ['rede', 'user', 'count', 'acesso']

    def get_urls(self):
        urls = super(RelatorioGraficoAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', admin.site.admin_view(relatoriografico))
        )
        return my_urls + urls

admin.site.register(RelatorioGrafico, RelatorioGraficoAdmin)