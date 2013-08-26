# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import transaction
from django.db.models import Q, Count, Sum
from django.contrib import admin
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminPasswordChangeForm
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext, ugettext_lazy as _
from django.conf.urls.defaults import include, patterns, url
from django.contrib.admin.widgets import FilteredSelectMultiple
from models import Rede, Filial, Category, Treinamento, Certificado, Question, Response, Parceiro, Banner, \
                        Faq, InfoUser, Menu, RelatorioAcoes, RelatorioAvalicao, RelatorioTentativa, \
                            TipoTemplate, Template, WebChat, Live, Anexo, Quiz, FreeResponse, \
                                Plano, Transation, Enquete, Url, ContatoComercial, Aviso

from crequest.middleware import CrequestMiddleware

from django.conf import settings

from mail import _send_email_user, _is_valid_email
from cpf import CPF as _cpf

from views import _get_rec, _quiz, _quiz_delete

csrf_protect_m = method_decorator(csrf_protect)


class RedeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(RedeForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsu = User.objects.all()

        if rede:
            qsu = qsu.filter( infouser__rede = rede )

        self.fields['user'].widget   = FilteredSelectMultiple(_(u'usuários'), False)
        self.fields['user'].queryset = qsu.order_by('username')

    class Meta:
        model = Rede


class RedeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'link', 'visible', 'is_faq', 'imagem_mensagem')
    list_filter   = ('visible',)
    search_fields = ['name']

    fieldsets = (
        (None, {
            'fields': ('name', 'link', 'logo', 'logo_log', 'visible', 'user', 'is_faq', 'is_login',)
        }),
        ('Imagem de fundo da mensagem de "Esta categoria não tem conteúdo cadastrado. "', {
            'fields' : ('image',)
        }),
        ('Agendamento de envio de Sugestões ou Dúvidas', {
            'fields' : ('email', 'date_send', 'resend',)
        }),
    )

    filter_horizontal = ('user',)

    form = RedeForm

    ## para limitar a lista por nivel de usuário
    def queryset(self, request, *args, **kwargs):
        qs = super(RedeAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(id = request.rede.id)
            return qs.all()
        return qs.filter(user = request.user)

admin.site.register(Rede, RedeAdmin)


class FilialAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'rede', 'visible',)
    list_filter  = ('visible',)

    def queryset(self, request):
        qs = super(FilialAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['name', 'visible', 'code']
        else:
            self.fields = ['rede', 'name', 'visible', 'code']
        return super(FilialAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()

admin.site.register(Filial, FilialAdmin)


class CategoryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsc = Category.objects.all()
        qsf = Filial.objects.all()

        if rede:
            qsc = qsc.filter( rede = rede )
            qsf = qsf.filter( rede = rede )

        self.fields['parent'].queryset = qsc.order_by('name')
        self.fields['filial'].queryset = qsf.order_by('name')

    class Meta:
        model = Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'tipo_categoria', 'categoria', 'rede', 'Filiais', 'visible', 'access', 'order', 'is_desc_g', 'is_text', 'is_email', 'is_groupc', 'is_groupv')
    list_filter  = ('visible', 'tipo', 'access', 'is_desc_g', 'is_text', 'is_email', 'is_groupc', 'is_groupv')

    filter_horizontal = ('filial',)

    def queryset(self, request):
        qs = super(CategoryAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fieldsets = (
                    (None, {
                        'fields': ('tipo', 'parent', 'name', 'is_name', 'home', 'visible',)
                    }),
                    ('Agrupamento de informação', {
                        'fields' : ('is_groupc', 'is_groupv',)
                    }),
                    (None, {
                        'fields' : ('order', 'image', 'desc', 'is_desc_g', 'is_text', 'text', 'desc_g', 'is_image', 'is_email', 'email', 'access', 'filial',)
                    }),
                )
        else:
            self.fieldsets = (
                    (None, {
                        'fields': ('rede', 'tipo', 'parent', 'name', 'is_name', 'home', 'visible',)
                    }),
                    ('Agrupamento de informação', {
                        'fields' : ('is_groupc', 'is_groupv',)
                    }),
                    (None, {
                        'fields' : ('order', 'image', 'desc', 'is_desc_g', 'desc_g', 'is_text', 'text', 'is_image', 'is_email', 'email', 'access', 'filial',)
                    }),
                )
        self.form       = CategoryForm
        return super(CategoryAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass

        if not obj.is_desc_g:
            obj.desc_g = ''

        if not obj.is_email:
            obj.email  = ''

        obj.save()

    class Media:
            js = ('mega/js/category_admin.js',)


admin.site.register(Category, CategoryAdmin)


class TreinamentoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TreinamentoForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsc = Category.objects.all()
        qst = Treinamento.objects.all()

        if rede:
            qsc = qsc.filter( rede = rede )
            qst = qst.filter( rede = rede )
            if 'instance' in kwargs and getattr(kwargs['instance'], 'id', False):
                qst = qst.exclude(id = kwargs['instance'].id)

        self.fields['category'].queryset    = qsc.order_by('name')
        self.fields['treinamento'].queryset = qst.order_by('name')

        self.fields['required'].widget   = FilteredSelectMultiple(_(u'Treinamentos'), False)
        self.fields['required'].queryset = qst.order_by('name')

    class Meta:
        model = Treinamento


class TreinamentoAdmin(admin.ModelAdmin):
    list_display  = ('name', 'tipo_t', 'categoria', 'treinamento', 'tipo', 'rede', 'visible', 'destaq', 'numero_sugestao', 'quant_faqs',)
    list_filter   = ('visible', 'tipo_t', 'destaq',)
    search_fields = ['name', 'category__name']

    filter_horizontal = ('required',)

    def queryset(self, request):
        qs = super(TreinamentoAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['tipo_t', 'category', 'treinamento', 'name', 'visible', 'destaq', 'tipo', 'code', 'image', 'image1', 'image2', 'image3', 'image4', 'file', 'agendado', 'time', 'author', 'order', 'desc', 'desc_l', 'required', 'idproduto', 'preco', 'datavalida']
        else:
            self.fields = ['rede', 'tipo_t', 'category', 'treinamento', 'name', 'visible', 'destaq', 'tipo', 'code', 'image', 'image1', 'image2', 'image3', 'image4', 'file', 'agendado', 'time', 'author', 'order', 'desc', 'desc_l', 'required', 'idproduto', 'preco', 'datavalida']
        self.form       = TreinamentoForm
        return super(TreinamentoAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()

    class Media:
        js = ('ckeditor/ckeditor/ckeditor.js', 'mega/js/combo_admin.js',)


admin.site.register(Treinamento, TreinamentoAdmin)


class CertificadoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CertificadoForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qst = Treinamento.objects.all()

        if rede:
            qst = qst.filter( rede = rede )

        self.fields['treinamento'].widget   = FilteredSelectMultiple(_(u'treinamentos'), False)
        self.fields['treinamento'].queryset = qst.order_by('name')

    class Meta:
        model = Certificado


class CertificadoAdmin(admin.ModelAdmin):
    list_display = ('name', 'rede', 'visible')
    list_filter  = ('visible',)

    filter_horizontal = ('treinamento',)

    def queryset(self, request):
        qs = super(CertificadoAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields  = ['name', 'treinamento', 'image', 'visible']
        else:
            self.fields  = ['rede', 'name', 'treinamento', 'image', 'visible']
        self.form        = CertificadoForm
        return super(CertificadoAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


admin.site.register(Certificado, CertificadoAdmin)


class QuestionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qst = Treinamento.objects.all()

        if rede:
            qst = qst.filter( rede = rede )

        self.fields['treinamento'].queryset = qst.order_by('name')

    class Meta:
        model = Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'treinamento', 'rede', 'pontos', 'visible')
    list_filter  = ('visible',)

    def queryset(self, request):
        qs = super(QuestionAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['treinamento', 'text', 'pontos', 'visible']
        else:
            self.fields = ['rede', 'treinamento', 'text', 'pontos', 'visible']
        self.form       = QuestionForm
        return super(QuestionAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


#admin.site.register(Question, QuestionAdmin)


class ResponseForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ResponseForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsq = Question.objects.all()

        if rede:
            qsq = qsq.filter( rede = rede )

        self.fields['question'].queryset = qsq.order_by('text')

    class Meta:
        model = Response


class ResponseAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'rede', 'correta')
    list_filter  = ('correta',)

    def queryset(self, request):
        qs = super(ResponseAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['question', 'text', 'correta']
        else:
            self.fields = ['rede', 'question', 'text', 'correta']
        self.form       = ResponseForm
        return super(ResponseAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


#admin.site.register(Response, ResponseAdmin)


class ParceiroForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ParceiroForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsc = Category.objects.all()

        if rede:
            qsc = qsc.filter( rede = rede )

        self.fields['category'].widget   = FilteredSelectMultiple(_(u'categorias'), False)
        self.fields['category'].queryset = qsc.order_by('name')

    class Meta:
        model = Parceiro


class ParceiroAdmin(admin.ModelAdmin):
    list_display = ('name', 'rede', 'Categorias', 'visible', 'home')
    list_filter  = ('visible',)

    filter_horizontal = ('category',)

    def queryset(self, request):
        qs = super(ParceiroAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['name', 'is_name', 'category', 'image', 'home', 'link', 'order', 'visible']
        else:
            self.fields = ['rede', 'name', 'is_name', 'category', 'image', 'home', 'link', 'order', 'visible']
        self.form       = ParceiroForm
        return super(ParceiroAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


admin.site.register(Parceiro, ParceiroAdmin)


class BannerForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(BannerForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsc = Category.objects.all()

        if rede:
            qsc = qsc.filter( rede = rede )

        self.fields['category'].widget   = FilteredSelectMultiple(_(u'categorias'), False)
        self.fields['category'].queryset = qsc.order_by('name')

    class Meta:
        model = Banner


class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'rede', 'Categorias', 'visible', 'home', 'order')
    list_filter  = ('visible',)

    filter_horizontal = ('category',)

    def queryset(self, request):
        qs = super(BannerAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['name', 'category', 'image', 'visible', 'legend', 'home', 'order', 'url', 'blank']
        else:
            self.fields = ['rede', 'name', 'category', 'image', 'visible', 'legend', 'home', 'order', 'url', 'blank']
        self.form       = BannerForm
        return super(BannerAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


admin.site.register(Banner, BannerAdmin)


class FaqForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(FaqForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsf = Filial.objects.all()
        qst = Treinamento.objects.all()

        if rede:
            qsf = qsf.filter( rede = rede )
            qst = qst.filter( rede = rede )

        self.fields['filial'].widget        = FilteredSelectMultiple(_(u'filiais'), False)
        self.fields['filial'].queryset      = qsf.order_by('name')
        self.fields['treinamento'].widget   = FilteredSelectMultiple(_(u'treinamentos'), False)
        self.fields['treinamento'].queryset = qst.order_by('name')

    class Meta:
        model = Faq


class FaqAdmin(admin.ModelAdmin):
    list_display = ('pergunta', 'rede', 'Filiais', 'order', 'visible', 'menu_all', 'quant_treinamentos',)
    list_filter  = ('visible', 'menu_all',)

    filter_horizontal = ('filial', 'treinamento',)

    def queryset(self, request):
        qs = super(FaqAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['pergunta', 'resposta', 'filial', 'visible', 'order', 'access', 'menu_all', 'treinamento']
        else:
            self.fields = ['rede', 'pergunta', 'resposta', 'filial', 'visible', 'order', 'access', 'menu_all', 'treinamento']
        self.form       = FaqForm
        return super(FaqAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


admin.site.register(Faq, FaqAdmin)


class InfoUserAdminForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(InfoUserAdminForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsf = Filial.objects.all()

        if rede:
            qsf = qsf.filter( rede = rede )

        self.fields['filial'].queryset = qsf.order_by('name')

    class Meta:
        model = InfoUser


class InfoUserForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(InfoUserForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.user.rede_set.filter(visible = True)
        except:
            rede = []

        qsf = Filial.objects.filter( Q(visible=True), Q(rede__in = rede) )

        if rede:
            qsf = qsf.filter( rede = rede )

        self.fields['filial'].queryset = qsf.order_by('name')

    class Meta:
        model = InfoUser


class InfoUserAdmin(admin.ModelAdmin):
    list_display  = ('nome', 'user', 'rede', 'filial', 'visible', 'pontos', 'offline', 'access',)
    list_filter   = ('visible', 'offline', 'access',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name',)

    ## para limitar a lista por nivel de usuário
    def queryset(self, request, *args, **kwargs):
        qs   = super(InfoUserAdmin, self).queryset(request)

        rede = request.user.rede_set.filter( Q(visible=True) )

        if request.user.is_superuser and request.rede:
            self.list_display = ('nome', 'user', 'filial', 'visible', 'pontos', 'offline')

        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()

        ca = qs.filter( Q(user__is_superuser = False) & Q(rede__in = rede) )
        if request.user.infouser.filial:
            self.list_display = ('nome', 'user', 'visible', 'pontos', 'offline')
            ca = ca.filter(filial = request.user.infouser.filial)

        return ca

    ### end custom

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            if request.rede:
                self.fields = ['filial', 'visible', 'nasc', 'sexo', 'rg', 'cpf', 'endereco', \
                                    'numero', 'complem', 'bairro', 'cep', 'estado', 'cidade', 'cargo', 'admissao', 'fone_com', \
                                            'fone_res', 'fone_cel', 'access', 'offline']
            else:
                self.fields = ['rede', 'filial', 'visible', 'nasc', 'sexo', 'rg', 'cpf', 'endereco', \
                                    'numero', 'complem', 'bairro', 'cep', 'estado', 'cidade', 'cargo', 'admissao', 'fone_com', \
                                            'fone_res', 'fone_cel', 'access', 'offline']
            self.form   = InfoUserAdminForm
        else:
            self.fields = ['filial', 'visible', 'nasc', 'sexo', 'rg', 'cpf', 'endereco', \
                                    'numero', 'complem', 'bairro', 'cep', 'estado', 'cidade', 'cargo', 'admissao', 'fone_com', \
                                            'fone_res', 'fone_cel', 'access', 'offline']
            self.form   = InfoUserForm
        return super(InfoUserAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()

    class Media:
        js = ('mega/js/state_admin.js',)


admin.site.register(InfoUser, InfoUserAdmin)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'Redes', 'tipo', 'order', 'visible')
    list_filter  = ('visible',)

    filter_horizontal = ('rede',)

    def queryset(self, request):
        qs = super(MenuAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['name', 'visible', 'url', 'tipo', 'order']
        else:
            self.fields = ['rede', 'name', 'visible', 'url', 'tipo', 'order']
        return super(MenuAdmin, self).get_form(request, obj=None, **kwargs)

    class Media:
        js = (
                'ckeditor/ckeditor/ckeditor.js',
                'ckeditor/ckeditor/config.js?t=B8DJ5M3',
                'ckeditor/ckeditor/skins/django/skin.js?t=B8DJ5M3',
                'ckeditor/ckeditor/lang/pt-br.js?t=B8DJ5M3',
                'ckeditor/ckeditor/plugins/styles/styles/default.js?t=B8DJ5M3',
                'mega/js/combo_admin.js',
             )


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'rede', 'visible', 'tipo', )
    list_filter  = ('visible',)

    fieldsets = (
        (None, {
            'fields': ('name', 'rede', 'tipo', 'visible',)
        }),
        ('Fundo do site', {
            'fields': ('font1', 'font2', 'font3', 'font4', 'font_gle', 'cor1', 'image1', 'advance1',)
        }),
        ('Cabeçario', {
            'fields': ('cor2', 'image2', 'cor15', 'larg4',)
        }),
        ('Menu principal', {
            'fields': ('cor3', 'cor16', 'cor18', 'cor19', 'cor17', 'cor33', 'larg5',)
        }),
        ('Campo Busca', {
            'fields': ('cor20', 'image4', 'image7', 'cor39', 'larg11', 'cor40',)
        }),
        ('Rodapé', {
            'fields': ('cor4', 'image3', 'cor5', 'cor21', 'larg6',)
        }),
        ('Banner Rotativo', {
            'fields': ('cor22', 'image5', 'cor23', 'larg7', 'cor24', 'larg8', 'cor34', 'cor35', 'cor36',)
        }),
        ('Conteúdo do site', {
            'fields': ('cor25', 'larg9', 'cor26', 'larg10',)
        }),
        ('Barra de Titulo', {
            'fields': ('title_d', 'title_ds', 'title_pd', 'cor6', 'cor7', 'cor37', 'cor38', )
        }),
        ('Categorias e Treinamentos', {
            'fields': ('larg2', 'cor13', 'larg3', 'cor14', 'cor12', 'larg1', 'cor32', 'cor31',)
        }),
        ('Demais Botões', {
            'fields': ('cor27', 'cor28', 'cor29', 'cor30',)
        }),
        ('Imagem Favicon', {
            'fields': ('image6',)
        }),
        ('CSS', {
            'fields': ('custom',)
        }),
    )

    def queryset(self, request):
        qs = super(TemplateAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                tmp = list(self.fieldsets[0][1]['fields'])
                if tmp.count('rede') > 0:
                    tmp.remove('rede')
                    self.fieldsets[0][1]['fields'] = tuple(tmp)
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            tmp = list(self.fieldsets[0][1]['fields'])
            if tmp.count('rede') > 0:
                tmp.remove('rede')
                self.fieldsets[0][1]['fields'] = tuple(tmp)
        return super(TemplateAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()

    class Media:
        js = ('mega/js/combo_admin.js',)


admin.site.register(Menu, MenuAdmin)

#admin.site.register(RelatorioAcoes)
#admin.site.register(RelatorioAvalicao)
#admin.site.register(RelatorioTentativa)
#admin.site.register(TipoTemplate)
admin.site.register(Template, TemplateAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Site)


class UserAdminCustom(admin.ModelAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    ## para limitar os combo usuários
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Groups'), {'fields': ('groups',)}),
        )

    add_fieldsets = (
                        (None, {
                            'classes': ('wide',),
                            'fields': ('username', 'password1', 'password2')}
                            ),
                    )

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    filter_horizontal = ('user_permissions',)

    def __call__(self, request, url):
        # this should not be here, but must be due to the way __call__ routes
        # in ModelAdmin.
        if url is None:
            return self.changelist_view(request)
        if url.endswith('password'):
            return self.user_change_password(request, url.split('/')[0])
        return super(UserAdminCustom, self).__call__(request, url)

    ### init custom
    def save_model(self, request, obj, form, change):

        obj.save()

        try:
            iu   = obj.infouser
            rede = iu.rede
        except:
            if request.rede:
                rede    = request.rede
            else:
                rede    = request.user.rede_set.filter( Q(visible=True) )[0]
            iu          = InfoUser()
            iu.user_id  = obj.id
            iu.rede     = rede
            iu.sexo     = u'M'
            iu.cpf      = '999.999.999-99'
            iu.matricul = 'XXXYYYZZZ'
            iu.save()

        #username = obj.username.replace('_', '')

        #if not _cpf(username).isValid() and not _is_valid_email(username) and username.isdigit():
        #    obj.username = username
        #    obj.save()

        if change and obj.email:

            p = {}

            p['to_mail']    = obj.email
            p['name']       = obj.get_full_name()
            p['rede']       = obj.infouser.rede

            p['link']       = '%slogin/?user=%s&action=%s&key=%s' % (settings.LIST_VARS.get('base_url', ''), obj.username, '/conta/edit/', obj.password)
            p['this_user']  = obj

            p['STATIC_URL'] = getattr(settings, 'STATIC_URL', '')

            r = _send_email_user(p, request)


    ## para limitar a lista por nivel de usuário
    def queryset(self, request, *args, **kwargs):
        qs   = super(UserAdminCustom, self).queryset(request)
        rede = request.user.rede_set.filter( Q(visible=True) )
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(infouser__rede = request.rede)
            return qs.all()
        ca = qs.filter( (Q(is_superuser = False) & Q(username = request.user.username)) | (Q(is_superuser = False) & Q(infouser__rede__in = rede)) )

        if request.user.infouser.filial:
            ca = ca.filter(infouser__filial = request.user.infouser.filial)
        return ca
    ### end custom

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdminCustom, self).get_fieldsets(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        """
        Use special form during user creation
        """

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
            if rede:
                self.add_fieldsets = (
                    (None, {
                        'classes': ('wide',),
                        'fields': ('username', 'password1', 'password2')}
                        ),
                )
                self.add_form_template = 'admin/auth/user/add_form.html'
            else:
                self.add_fieldsets = ()
                self.add_form_template = 'mega/admin/mensagem_user.html'

        except:
            rede = None
            self.add_fieldsets = ()
            self.add_form_template = 'mega/admin/mensagem_user.html'

        defaults = {}
        if obj is None:
            defaults.update({
                'form': self.add_form,
                'fields': admin.util.flatten_fieldsets(self.add_fieldsets),
                })
        defaults.update(kwargs)

        ## para limitar a lista por nivel de usuário
        if not request.user.is_superuser:
            self.fieldsets = (
                (None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': ('is_active', 'is_staff')}),
                (_('Groups'), {'fields': ('groups',)}),
            )
        ### end custom

        return super(UserAdminCustom, self).get_form(request, obj, **defaults)

    def get_urls(self):
        from django.conf.urls.defaults import patterns
        return patterns('',
            (r'^(\d+)/password/$', self.admin_site.admin_view(self.user_change_password)),
        ) + super(UserAdminCustom, self).get_urls()

    @csrf_protect_m
    @transaction.commit_on_success
    def add_view(self, request, form_url='', extra_context=None):
        # It's an error for a user to have add permission but NOT change
        # permission for users. If we allowed such users to add users, they
        # could create superusers, which would mean they would essentially have
        # the permission to change users. To avoid the problem entirely, we
        # disallow users from adding users if they don't have change
        # permission.
        if not self.has_change_permission(request):
            if self.has_add_permission(request) and settings.DEBUG:
                # Raise Http404 in debug mode so that the user gets a helpful
                # error message.
                raise Http404('Your user does not have the "Change user" permission. In order to add users, Django requires that your user account have both the "Add user" and "Change user" permissions set.')
            raise PermissionDenied
        if extra_context is None:
            extra_context = {}
        defaults = {
            'auto_populated_fields': (),
            'username_help_text': self.model._meta.get_field('username').help_text,
            }
        extra_context.update(defaults)
        return super(UserAdminCustom, self).add_view(request, form_url, extra_context)

    def user_change_password(self, request, id):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = get_object_or_404(self.model, pk=id)
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                new_user = form.save()
                msg = ugettext('Password changed successfully.')
                messages.success(request, msg)
                return HttpResponseRedirect('..')
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': form.base_fields.keys()})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        return render_to_response(self.change_user_password_template or 'admin/auth/user/change_password.html', {
            'title': _('Change password: %s') % escape(user.username),
            'adminForm': adminForm,
            'form': form,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
            'root_path': self.admin_site.root_path,
            }, context_instance=RequestContext(request))

    def response_add(self, request, obj, post_url_continue='../%s/'):
        """
        Determines the HttpResponse for the add_view stage. It mostly defers to
        its superclass implementation but is customized because the User model
        has a slightly different workflow.
        """
        # We should allow further modification of the user just added i.e. the
        # 'Save' button should behave like the 'Save and continue editing'
        # button except in two scenarios:
        # * The user has pressed the 'Save and add another' button
        # * We are adding a user in a popup
        if '_addanother' not in request.POST and '_popup' not in request.POST:
            request.POST['_continue'] = 1
        return super(UserAdminCustom, self).response_add(request, obj, post_url_continue)


admin.site.register(User, UserAdminCustom)

#admin.site.register(WebChat)

class LiveAdmin(admin.ModelAdmin):

    list_display = ('rede', 'live', 'Data_de_agendamento',)

    exclude = ['rede', 'live', 'user_not_chat', 'user_not_video', 'user_not_audio', 'user_not_all']

    def queryset(self, request):
        qs = super(LiveAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)


    def get_form(self, request, obj=None, **kwargs):

        return super(LiveAdmin, self).get_form(request, obj=None, **kwargs)

    def get_urls(self):
        urls = super(LiveAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^(?P<live_id>\d+)/$', admin.site.admin_view(_get_rec))
        )
        return my_urls + urls


#admin.site.register(Live, LiveAdmin)


class AnexoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AnexoForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qst = Treinamento.objects.all()
        qsc = Category.objects.all()

        if rede:
            qst = qst.filter( rede = rede )
            qsc = qsc.filter( rede = rede )

        self.fields['treinamento'].queryset = qst.order_by('name')
        self.fields['category'].queryset    = qsc.order_by('name')

    class Meta:
        model = Anexo


class AnexoAdmin(admin.ModelAdmin):

    list_display = ('name', 'rede', 'treinamento', 'category', 'visible',)

    def queryset(self, request):
        qs = super(AnexoAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['category', 'treinamento', 'name', 'visible', 'file', 'desc']
        else:
            self.fields = ['rede', 'category', 'treinamento', 'name', 'visible', 'file', 'desc']
        self.form = AnexoForm
        return super(AnexoAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


admin.site.register(Anexo, AnexoAdmin)


class QuizAdmin(admin.ModelAdmin):

    list_display  = ('primeira_pergunta', 'rede', 'treinamento', 'porcentagem_acerto', 'email_responsavel', 'quant_perguntas',)
    search_fields = ['treinamento']

    def get_urls(self):
        urls = super(QuizAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^add/'                     , admin.site.admin_view(_quiz)),
            (r'^(?P<quiz_id>\d+)/delete/' , admin.site.admin_view(_quiz_delete)),
            (r'^(?P<quiz_id>\d+)/'        , admin.site.admin_view(_quiz)),
        )
        return my_urls + urls

    def queryset(self, request):
        qs = super(QuizAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

admin.site.register(Quiz, QuizAdmin)


class PlanoAdmin(admin.ModelAdmin):

    list_display = ('name', 'rede', 'valor', 'visible', 'duracao',)

    def queryset(self, request):
        qs = super(PlanoAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['name', 'valor', 'desc', 'visible', 'duration', 'q_videos', 'q_badges', 'quiz', 'tutor']
        else:
            self.fields = ['rede', 'name', 'valor', 'desc', 'visible', 'duration', 'q_videos', 'q_badges', 'quiz', 'tutor']
        return super(PlanoAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


#admin.site.register(Plano, PlanoAdmin)

#admin.site.register(Transation)


class EnqueteAdmin(admin.ModelAdmin):

    list_display = ('title', 'rede', 'visible', 'quant_votos',)

    def queryset(self, request):
        qs = super(EnqueteAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['title', 'visible', 'opcao1', 'opcao2', 'opcao3', 'opcao4', 'opcao5', 'opcao6']
        else:
            self.fields = ['rede', 'title', 'visible', 'opcao1', 'opcao2', 'opcao3', 'opcao4', 'opcao5', 'opcao6']
        return super(EnqueteAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


admin.site.register(Enquete, EnqueteAdmin)


class UrlAdmin(admin.ModelAdmin):

    list_display = ('rede', 'type', 'active', 'key', 'date_v',)

    def queryset(self, request):
        qs = super(UrlAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['type', 'key', 'link', 'mto', 'mfrom', 'active', 'date_v']
        else:
            self.fields = ['rede', 'type', 'key', 'link', 'mto', 'mfrom', 'active', 'date_v']
        return super(UrlAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


#admin.site.register(Url, UrlAdmin)


class ContatoComercialForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContatoComercialForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsc = Category.objects.all()

        if rede:
            qsc = qsc.filter( rede = rede )

        self.fields['category'].queryset = qsc.order_by('name')

    class Meta:
        model = ContatoComercial


class ContatoComercialAdmin(admin.ModelAdmin):

    list_display  = ('nome', 'regiao', 'rede', 'category', 'visible', 'fone1')
    search_fields = ['nome', 'regiao']
    list_filter   = ('visible',)

    def queryset(self, request):
        qs = super(ContatoComercialAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['category', 'nome', 'visible', 'email', 'regiao', 'fone1', 'fone2']
        else:
            self.fields = ['rede', 'category', 'nome', 'visible', 'email', 'regiao', 'fone1', 'fone2']
        self.form = ContatoComercialForm
        return super(ContatoComercialAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()


admin.site.register(ContatoComercial, ContatoComercialAdmin)


class AvisoForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AvisoForm, self).__init__(*args, **kwargs)

        cm = CrequestMiddleware.get_request()

        try:
            rede = cm.rede
        except:
            rede = None

        qsu = User.objects.all()

        if rede:
            qsu = qsu.filter( infouser__rede = rede )

        self.fields['is_user_view'].widget   = FilteredSelectMultiple(_(u'usuários'), False)
        self.fields['is_user_view'].queryset = qsu.order_by('username')

    class Meta:
        model = Aviso


class AvisoAdmin(admin.ModelAdmin):

    list_display = ('rede', 'name', 'visible', 'is_video', 'is_persistent', 'is_full_user', 'Data_inicia', 'Data_termina',)

    def queryset(self, request):
        qs = super(AvisoAdmin, self).queryset(request)
        if request.user.is_superuser:
            if request.rede:
                return qs.filter(rede = request.rede)
            return qs.all()
        return qs.filter(rede__user = request.user)

    ## para limitar os combo das redes
    def get_form(self, request, obj=None, **kwargs):
        if request.rede:
            self.fields = ['name', 'image', 'is_video', 'link', 'code', 'is_persistent', 'is_full_user', 'is_user_view', 'visible', 'date_init', 'date_end']
        else:
            self.fields = ['rede', 'name', 'image', 'is_video', 'link', 'code', 'is_persistent', 'is_full_user', 'is_user_view', 'visible', 'date_init', 'date_end']
        self.form = AvisoForm
        return super(AvisoAdmin, self).get_form(request, obj=None, **kwargs)

    ## para salvar automaticamente a rede que está na session
    def save_model(self, request, obj, form, change):
        try:
            rede     = request.rede
            obj.rede = rede
        except:
            pass
        obj.save()

    class Media:
        js = ('mega/js/aviso_admin.js',)


admin.site.register(Aviso, AvisoAdmin)