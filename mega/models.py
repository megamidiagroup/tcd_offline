# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models
from django.core.files.base import ContentFile, File
from StringIO import StringIO
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.encoding import force_unicode
from django.utils.text import truncate_words
from django.db.models import Q, Count
from django.contrib.auth.models import User as UserAdmin
from django.template.defaultfilters import join as default_join, date as default_date, slugify
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from state.models import City, State
from mail import _is_valid_email

from BeautifulSoup import BeautifulSoup
from PIL import Image
from zipfile import ZipFile

from reference import reference

from ckeditor.fields import RichTextField, CKEditorWidget
from colors.fields import ColorField
from crequest.middleware import CrequestMiddleware

from rules import get_style_template
from rules_mobile import get_style_template as get_style_template_mobile
from rules_tablet import get_style_template as get_style_template_tablet
from command import Sh

import datetime
import os
import HTMLParser
import base64
import shutil

# Create your models here.

CHOICE_SEXO         = (('M', u'Masculino'), ('F', u'Feminino'),)
CHOICE_TIPO         = (('B', u'Botão'), ('S', u'Busca'), ('D', u'Destaque'),)
CHOICE_SERVER       = (('M', u'MegaVideo'), ('B', u'brightcove.com'), ('K', u'kaltura.org'),) ## ('L', u'Live'),)
CHOICE_RESEND       = (('I', u'Imediato'), ('U', u'Uma vez'), ('D', u'Diário'), ('S', u'Semanal'), ('M', u'Mensal'), ('A', u'Anual'),)
CHOICE_CATEGORY     = ((0, u'Padrão'), (1, u'Pasta Técnica'),)
CHOICE_TREINAMENTO  = ((0, u'Vídeo'), (1, u'Página Genérica'), (2, u'Vitrine Virtual'),)

default_mes         = {1:u'Janeiro', 2:u'Fevereiro', 3:u'Março', 4:u'Abril', 5:u'Maio', 6:u'Junho', 7:u'Julho', 8:u'Agosto',
                        9:u'Setembro', 10:u'Outubro', 11:u'Novembro', 12:u'Dezembro'}


def upload_file(self, filename):
    """ função para delegar o local onde vai estar as imagens e o slug do nome """
    name, ext, local = (filename.split('.')[0], filename.split('.')[1], slugify(self._meta.verbose_name),)
    return '%suploads/%s/%s/%s/%s.%s' % (settings.UPLOAD_STORAGE_DIR, local, datetime.datetime.now().year, datetime.datetime.now().month, slugify(name), ext,)


### Tabela para as Redes
class Rede(models.Model):
    user       = models.ManyToManyField(UserAdmin, verbose_name='Cliente Responsável', help_text='Usuários que poderão visualizar a sua rede. Segure CTRL e clique para selecionar mais de uma opção.', blank = True)
    name       = models.CharField(max_length = 255, verbose_name='Nome')
    link       = models.CharField(max_length = 255, verbose_name='URL')
    logo       = models.ImageField(upload_to = upload_file, max_length=255, help_text='A imagem deverá ser gerada em png com tamanho máximo de 370x100px ', verbose_name='Logo')
    logo_log   = models.ImageField(upload_to = upload_file, max_length=255, null = True, blank = True, help_text='Caso queira que a logo do login seja diferente, tamanho máximo de 370x100px ', verbose_name='Logo do Login')
    visible    = models.BooleanField(default = True, verbose_name='Habilitado')
    is_faq     = models.BooleanField(default = False, blank = True, verbose_name='Faq treinamento', help_text='Habilita Faq dos treinamentos, tanto para envio quanto para visualização')
    is_hit_cat = models.BooleanField(default = False, blank = True, verbose_name='Hit Categorias', help_text='Habilita hit das categorias, com o mouse encima da lista de categorias, mostra a descrição')
    is_hit_tre = models.BooleanField(default = False, blank = True, verbose_name='Hit Treinamentos', help_text='Habilita hit dos treinamentos, com o mouse encima da lista de vídeos, mostra a descrição')
    is_login   = models.BooleanField(default = True, verbose_name='Área de login', help_text='Habilita área de login da rede')
    image      = models.ImageField(upload_to = upload_file, max_length=255, null = True, blank = True, help_text='A imagem deverá ser gerada em png com cantos arredondados com tamanho de 540x198px, caso contrário, deixe o campo vazio.', verbose_name='Imagem de fundo')
    email      = models.CharField(max_length = 255, verbose_name='E-mail responsável', null = True, blank = True, help_text='Somente adicione o e-mail caso o cliente deseje receber as sugestões ou dúvidas, caso deseje mais de um e-mail, favor adicionar os e-mails separados por vírgula.')
    text_log   = RichTextField(null = True, blank = True, verbose_name='Texto do ícone', help_text='Texto que se aplica no icone de ajuda do login, caso não queira, deixe esse campo vazio.') 
    date_send  = models.DateField(verbose_name='Apartir da data', null = True, blank = True, help_text='Caso for diário, semanal, mensal ou anual, favor inserir a data para inicio do processo.')
    resend     = models.CharField(max_length = 1, choices = CHOICE_RESEND, null = True, blank = True, verbose_name='Envio acontece', help_text='O envio acontece todos os dias à meia-noite, caso for imediato, a sugestão ou dúvida é registrada e enviada imediatamente para o cliente, caso contrário, é enviado a opção selecionada.')
    date       = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.name

    def filter_not_filial(self, redes):
        r = [i.rede.id for i in Filial.objects.filter(rede__in = redes)]
        return Rede.objects.filter().exclude(id__in = r)

    def filter_in_filial(self, id):
        r = [i.rede.id for i in Filial.objects.filter(id = id)]
        return Rede.objects.filter(id__in = r)

    def imagem_mensagem(self):

        if not self.image:
            return u'Não'

        if len(self.image.path) > 0:
            return u'Sim'
        return u'Não'

    def get_rede(self):
        cm = CrequestMiddleware.get_request()
        try:
            user = cm.user
        except:
            user = None
        if user and user.infouser.filial:
            return '%s - %s' % (self.name, user.infouser.filial.name)
        return self.name

    def is_suggestion(self):
        if self.resend and len(self.email) > 0:
            if self.email.count(',') > 0:
                for e in self.email.replace(' ', '').split(','):
                    if not _is_valid_email(e):
                        return False
                return True
            elif _is_valid_email(self.email):
                return True
        return False

    class Meta:
        verbose_name = u'Rede'
        ordering     = ['name']


### Tabela para as Filiais
class Filial(models.Model):
    rede    = models.ForeignKey(Rede, related_name='+', verbose_name='Rede')
    name    = models.CharField(max_length = 255, verbose_name='Nome')
    visible = models.BooleanField(default = True, verbose_name='Habilitado')
    code    = models.CharField(max_length = 255, verbose_name='Código', help_text='Código de identificação da filial na rede')
    date    = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name        = u'Filial'
        verbose_name_plural = u'Filiais'
        ordering            = ['name']


### Tabela para as Categorias de Redes
class Category(models.Model):
    rede      = models.ForeignKey(Rede, related_name='+', verbose_name='Rede')
    tipo      = models.IntegerField(max_length=1, default=0, choices=CHOICE_CATEGORY, verbose_name='Tipo de categoria')
    filial    = models.ManyToManyField(Filial, blank=True, null=True, related_name='+', help_text='Filial que aparecerá a categoria. Segure CTRL e clique para selecionar mais de uma opção.')
    parent    = models.ForeignKey('self', null=True, blank=True, verbose_name='Categoria')
    link      = models.CharField(max_length = 255, null=True, blank=True, verbose_name='Link', help_text='Não usar caminho absoluto. Ex: (Não usar) https://www.treinandoequipes.com.br... Usar, Ex: /burgerking/docs/')
    name      = models.CharField(max_length = 255, verbose_name='Nome')
    is_name   = models.BooleanField(default = True, verbose_name='Mostrar Título', help_text='Mostra o título abaixo da categoria')
    visible   = models.BooleanField(default = True, verbose_name='Habilitado')
    is_groupc = models.BooleanField(default = False, verbose_name='Agrupar Anexos', help_text='Caso a categoria possuir anexos, pode ser agrupados em uma página em particular.')
    is_groupv = models.BooleanField(default = False, verbose_name='Agrupar Vídeos', help_text='Caso a categoria possuir vídeos, pode ser agrupados em uma página em particular.')
    home      = models.BooleanField(default = True, verbose_name='Visível na Home', help_text='Selecione para mostrar a categoria na home caso tenha selecionado que não seja um parceiro')
    order     = models.IntegerField(default = 0, verbose_name='Posição', help_text='posição do campo no menu ex: 4. Se todos os campos estiverem com valor "0" será ordena pelo nome')
    image     = models.ImageField(upload_to = upload_file, blank=True, max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site, tamanho padrão é de: 276 x 153 pixels', verbose_name='Imagem')
    desc      = RichTextField(verbose_name='Descrição', null=True, blank=True)
    is_desc_g = models.BooleanField(default = False, verbose_name='Habilitado descrição Geral')
    desc_g    = RichTextField(verbose_name='Descrição Geral', null=True, blank=True)
    is_text   = models.BooleanField(default = False, verbose_name='Habilitado conteúdo de texto')
    text      = RichTextField(verbose_name='Conteúdo texto', null=True, blank=True)
    is_image  = models.BooleanField(default = True, verbose_name='Habilitado imagem', help_text='Habilitar caso queira que a imagem apareça do lado da descrição geral')
    is_email  = models.BooleanField(default = False, verbose_name='Habilitado envio de mensagem (e-mail) pela categoria')
    email     = models.CharField(max_length = 255, verbose_name='E-mail de destino', null=True, blank=True, help_text='Somente adicione o e-mail caso o comercial deseje receber as mensagens realizadas no site, caso deseje mais de um e-mail, favor adicionar os e-mails separados por vírgula.')
    access    = models.BooleanField(default = False, verbose_name='Acesso Restrito', help_text='Bloqueia o acesso aos usuários que não possuem permissão para acessar as categorias restritas.')
    date      = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def categoria(self):
        array = []
        array.append(self.name)

        while self.parent:
            array.append(self.parent.name)
            self = self.parent
            
        array.append(self.rede.name)
        
        array.reverse()
        
        return '[' + self.rede.name + '] - ' + ' -> '.join(array[1:])
    
    def __unicode__(self):
        return self.categoria()

    def get_name(self):
        return self.name

    def Redes(self):
        return default_join(self.rede.filter(visible = True), ', ') or u'(Nenhum)'

    def Filiais(self):
        return default_join(self.filial.filter(visible = True), ', ') or u'(Nenhum)'

    def tipo_categoria(self):
        cc = dict((indice, value) for indice, value in CHOICE_CATEGORY)
        return cc[int(self.tipo)]

    def treinamento_set(self):
        return Treinamento.objects.filter(category = self)

    class Meta:
        verbose_name        = u'Categoria'
        ordering            = ['order', 'name']


### Tabela para os planos
class Plano(models.Model):
    rede     = models.ForeignKey(Rede, related_name='+', verbose_name='Rede')
    name     = models.CharField(max_length = 255, verbose_name='Nome')
    valor    = models.CharField(max_length = 50, verbose_name='Valor R$', help_text='Colocar o valor somente em numeros e virgula para separar os centavos.')
    desc     = models.TextField(verbose_name='Descrição', null = True, blank = True)
    visible  = models.BooleanField(default = True, verbose_name='Habilitado')
    duration = models.IntegerField(default = 0, verbose_name='Duração', help_text='Tempo de duração do plano, em dias, campo somente numérico. Ex: 365 dias para um ano.')
    q_videos = models.IntegerField(default = 0, verbose_name='Quantidade de vídeos', help_text='Quantidade limite de vídeos para assistir. 0 é infinito')
    q_badges = models.IntegerField(default = 0, verbose_name='Quantidade de badges', help_text='Quantidade limite de certificados ou badges para receber. 0 é infinito.')
    quiz     = models.BooleanField(default = False, verbose_name='Habilita quiz')
    tutor    = models.BooleanField(default = False, verbose_name='Habilita dúvidas com o tutor')
    date     = models.DateTimeField(auto_now_add = True, verbose_name='Data')

    def __unicode__(self):
        return self.name

    def duracao(self):
        if self.duration == 0:
            return u'Indeterminado'
        return self.duration

    class Meta:
        verbose_name = u'Plano'
        ordering     = ['name']


### Tabela para os Treinamentos
class Treinamento(models.Model):
    tipo_t      = models.IntegerField(max_length=1, default=0, choices=CHOICE_TREINAMENTO, verbose_name='Tipo de treinamento')
    rede        = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar os treinamentos.')
    category    = models.ForeignKey(Category, null = True, blank = True, related_name='+', verbose_name='Categoria')
    treinamento = models.ForeignKey('self', null = True, blank = True, verbose_name='Treinamento', related_name='Treinamento')
    name        = models.CharField(max_length = 255, verbose_name='Título')
    author      = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Autor')
    visible     = models.BooleanField(default = True, verbose_name='Habilitado')
    destaq      = models.BooleanField(default = False, verbose_name='Destaque', help_text='Sim, se marcado poderá aparecer em "Novos Vídeos"')
    tipo        = models.CharField(max_length=1, default='M', choices=CHOICE_SERVER, verbose_name='Servidor de vídeo')
    code        = models.CharField(max_length = 255, blank = True, verbose_name='Código do Vídeo', help_text='Ex.: 1638442624001')
    image       = models.ImageField(upload_to = upload_file, blank=True, max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site, tamanho padrão é de: 184 x 175 pixels', verbose_name='Imagem do Vídeo')
    time        = models.CharField(max_length = 255, blank = True, null = True, verbose_name='Duração', help_text='Ex.: 4:48 min')
    order       = models.IntegerField(default = 0, verbose_name='Posição', help_text='posição do campo no menu ex: 4. Se todos os campos estiverem com valor "0" será ordena pelo nome')
    desc        = RichTextField(verbose_name='Descrição')
    desc_l      = RichTextField(default = '', blank = True, verbose_name='Resumo da Descrição', help_text='Caso queira um resumo da descrição quando é listado, preencher esse campo, caso contrário, deixe em branco para mostrar a descrição padrão.')
    agendado    = models.DateTimeField(null = True, blank = True, verbose_name='Data de agendamento', help_text='Data de agendamento do live (AO VIVO), caso não seja, favor não preencher.')
    required    = models.ManyToManyField('self', symmetrical = False, blank=True, null=True, verbose_name='Treinamento obrigátorio', related_name='+', help_text='Selecione o(s) treinamento(s) que serão obrigatório(s) para assistir (introdução). Segure CTRL e clique para selecionar mais de uma opção.')
    ## elearning
    file        = models.FileField(upload_to = upload_file, max_length=255, blank=True, null=True, help_text='Enviar um arquivo zipado (.zip) contendo o index.html e demais swf\'s', verbose_name='Arquivo zip')
    dir         = models.CharField(max_length = 20, blank=True, null=True, editable=False, verbose_name='Diretório')
    ## vitrine virtual
    idproduto   = models.CharField(max_length = 20, blank=True, null=True, verbose_name='ID Produto', help_text='ID do produto do cliente, caso exista.')
    preco       = models.CharField(max_length = 20, blank=True, null=True, verbose_name='Preço', help_text='Exemplo: R$ 3.150,00.')
    datavalida  = models.DateField(null = True, blank = True, verbose_name='Oferta válida até', help_text='Caso exista validade na oferta, caso contrário, deixe em branco.')
    image1      = models.ImageField(upload_to = upload_file, blank=True, null = True, max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site, tamanho padrão é de: w x h pixels', verbose_name='Imagem 1')
    image2      = models.ImageField(upload_to = upload_file, blank=True, null = True, max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site, tamanho padrão é de: w x h pixels', verbose_name='Imagem 2')
    image3      = models.ImageField(upload_to = upload_file, blank=True, null = True, max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site, tamanho padrão é de: w x h pixels', verbose_name='Imagem 3')
    image4      = models.ImageField(upload_to = upload_file, blank=True, null = True, max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site, tamanho padrão é de: w x h pixels', verbose_name='Imagem 4')
    date        = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return '%s : %s' % (self.rede.name, self.name)

    def get_name(self):
        return self.name
    
    def get_desc(self):
        if len( strip_tags(self.desc_l) ) > 1:
            return self.desc_l
        return self.desc

    def categoria(self):
        return self.category.categoria()

    def get_list_suggestion(self, enviado=None):
        if enviado is None:
            return self.suggestion_set.all().order_by('date')
        return self.suggestion_set.filter(enviado = enviado).order_by('date')

    def numero_sugestao(self):
        return self.suggestion_set.filter(enviado = False).count()

    def quant_faqs(self):
        return Faq.objects.filter(treinamento = self).count()

    def save(self, *args, **kwargs):
        
        if self.file:

            super(Treinamento, self).save(*args, **kwargs)
    
            diretorio = settings.MEDIA_ROOT + settings.UPLOAD_STORAGE_DIR + 'uploads/elearning/'
    
            b64 = base64.b64encode( str(self.id) )
    
            self.dir = b64.lower()
    
            paste = diretorio + b64.lower()
    
            if os.path.isdir(paste):
                shutil.rmtree(paste)
    
            os.mkdir(paste)
    
            zip = ZipFile(self.file)
    
            zip.extractall(paste)

        super(Treinamento, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):

        if self.dir:
            diretorio = settings.UPLOAD_STORAGE_DIR + 'uploads/elearning/'
            paste     = diretorio + self.dir
    
            if os.path.isdir(paste):
                shutil.rmtree(paste)
            if self.file and self.file.path and os.path.exists(self.file.path):
                os.remove(self.file.path)

        super(Treinamento, self).delete(*args, **kwargs)


    class Meta:
        verbose_name = u'Treinamento'
        ordering     = ['category']


### Tabela para os Certificados
class Certificado(models.Model):
    rede        = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar os certificados.')
    name        = models.CharField(max_length = 255, verbose_name='Nome')
    treinamento = models.ManyToManyField(Treinamento, help_text='Treinamento(s) para obter o certificado. Segure CTRL e clique para selecionar mais de uma opção.')
    image       = models.ImageField(upload_to = upload_file, max_length=255, blank=True, null=True, help_text='O certificado deverá ter 1241px de largura por 1754 px de altura, qualidade em 72 DPI.', verbose_name='Imagem certificado')
    visible     = models.BooleanField(default = True, verbose_name='Habilitado')
    date        = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.name

    def get_list_treinamento(self):

        return [i.get_name() for i in self.treinamento.filter(visible=True)]


    class Meta:
        verbose_name = u'Certificado'
        ordering     = ['rede']


### Tabela para as transações
class Transation(models.Model):
    rede    = models.ForeignKey(Rede, related_name='+', verbose_name='Rede')
    user    = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário adquiriu o plano.')
    code    = models.CharField(max_length = 255, verbose_name='Código', null = True, blank = True)
    plano   = models.ForeignKey(Plano, related_name='+', verbose_name='Plano')
    visible = models.BooleanField(default = True, verbose_name='Habilitado')
    videos  = models.ManyToManyField(Treinamento, null = True, blank = True, verbose_name='Treinamentos assistidos.')
    badges  = models.ManyToManyField(Certificado, null = True, blank = True, verbose_name='Badges ou Certificados recebidos.')
    date    = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.code

    class Meta:
        verbose_name        = u'Transação'
        verbose_name_plural = u'Transações'
        ordering            = ['-date']


### Tabela para os Questões ou Perguntas
class Question(models.Model):
    rede        = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar as questões.')
    treinamento = models.ForeignKey(Treinamento, related_name='+', verbose_name='treinamento')
    text        = RichTextField(verbose_name='Pergunta')
    pontos      = models.IntegerField(default = 20, verbose_name='Pontos', help_text='o valor padrão é de 20 pontos, pode ser modificado pelo nivel da questão.')
    visible     = models.BooleanField(default = True, verbose_name='Habilitado')
    date        = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        h = HTMLParser.HTMLParser()
        return truncate_words(  h.unescape( strip_tags(self.text) ), 15  )

    def get_name(self):
        return self.name

    def get_list_response(self):
        return Response.objects.filter( Q(question = self), Q(rede = self.rede) ).order_by('?')

    def get_list_response_order(self):
        return Response.objects.filter( Q(question = self), Q(rede = self.rede) ).order_by('id')

    def get_free_response(self, user=None):

        if not user:
            cm = CrequestMiddleware.get_request()

            try:
                user = cm.user
            except:
                user = None

        return FreeResponse.objects.filter( Q(rede = self.rede) & Q(question = self) & Q(user = user) )

    class Meta:
        verbose_name = u'Pergunta'


### Tabela para as respostas
class Response(models.Model):
    rede     = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar as respostas.')
    question = models.ForeignKey(Question, related_name='+', verbose_name='Pergunta')
    text     = models.TextField(verbose_name='Resposta')
    correta  = models.BooleanField(default = False, verbose_name='Resposta Correta')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = u'Resposta'
        ordering     = ['question']


### Tabela para os Parceiros
class Parceiro(models.Model):
    rede     = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar os parceiros.')
    category = models.ManyToManyField(Category, blank = True, null = True, verbose_name='Categoria')
    name     = models.CharField(max_length = 255, verbose_name='Nome')
    is_name  = models.BooleanField(default = False, verbose_name='Mostrar Título', help_text='Mostra o título abaixo do parceiro')
    image    = models.ImageField(upload_to = upload_file, max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site, tamanho padrão é de: 184 x 175 pixels', verbose_name='Logo do parceiro')
    home     = models.BooleanField(default = True, verbose_name='Visível na Home', help_text='Selecione para mostrar o parceiro na home caso tenha selecionado uma ou mais categorias')
    order    = models.IntegerField(default = 0, verbose_name='Posição', help_text='posição do campo no menu ex: 4. Se todos os campos estiverem com valor "0" será ordena pelo nome')
    link     = models.CharField(max_length = 255, verbose_name='Link', blank = True, null = True)
    visible  = models.BooleanField(default = True, verbose_name='Habilitado')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.name

    def Categorias(self):
        return default_join(self.category.filter(visible = True), ', ') or u'(Nenhum)'

    class Meta:
        verbose_name = u'Parceiro'
        ordering     = ['name']


### Tabela para os Banners
class Banner(models.Model):
    rede     = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar os banner.')
    category = models.ManyToManyField(Category, null = True, blank = True, verbose_name='Categoria')
    name     = models.CharField(max_length = 255, verbose_name='Nome')
    image    = models.ImageField(upload_to = upload_file, max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site, tamanho padrão é de: 636 x 283 pixels', verbose_name='Imagem')
    visible  = models.BooleanField(default = True, verbose_name='Habilitado')
    legend   = models.BooleanField(default = True, verbose_name='Mostrar legenda')
    home     = models.BooleanField(default = True, verbose_name='Visível na Home', help_text='Selecione para mostrar o banner na home caso tenha selecionado uma ou mais categorias')
    order    = models.IntegerField(default = 0, verbose_name='Posição', help_text='posição do campo no menu ex: 4. Se todos os campos estiverem com valor "0" será ordena pelo nome')
    url      = models.CharField(max_length = 255, blank = True, null = True, verbose_name='URL')
    blank    = models.BooleanField(default = False, verbose_name='Abrir em uma nova janela')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.name

    def Categorias(self):
        return default_join(self.category.filter(visible = True), ', ') or u'(Nenhum)'

    class Meta:
        verbose_name = u'Banner'
        ordering     = ['order', 'name']


### Tabela para as perguntas e respostas
class Faq(models.Model):
    rede        = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar o FAQ.')
    filial      = models.ManyToManyField(Filial, blank=True, null=True, help_text='Filial que aparecerá o FAQ. Segure CTRL e clique para selecionar mais de uma opção.')
    pergunta    = models.TextField(verbose_name='Pergunta')
    resposta    = models.TextField(verbose_name='Resposta')
    visible     = models.BooleanField(default = True, verbose_name='Habilitado')
    order       = models.IntegerField(default = 0, verbose_name='Posição', help_text='posição do campo no menu ex: 4. Se todos os campos estiverem com valor "0" será ordena pelo nome')
    access      = models.BooleanField(default = False, verbose_name='Acesso Restrito', help_text='Bloqueia o acesso aos usuários que não possuem permissão para acessar os faqs restritos.')
    treinamento = models.ManyToManyField(Treinamento, blank=True, null=True, verbose_name='Treinamento', help_text='FAQ que aparecerá o Treinamento. Segure CTRL e clique para selecionar mais de uma opção.')
    menu_all    = models.BooleanField(default = True, verbose_name='Habilitado no Menu', help_text='Habilitar essa opção caso queira que apareça no menu principal, caso contrário, marque o treinamento.')
    date        = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.pergunta

    def Filiais(self):
        return default_join(self.filial.filter(visible = True), ', ') or u'(Nenhum)'

    def quant_treinamentos(self):
        return self.treinamento.filter(visible = True).count()

    class Meta:
        verbose_name = u'Faq'
        ordering     = ['order']



### Tabela para as informações dos usuários
class InfoUser(models.Model):
    user     = models.OneToOneField(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    rede     = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar o Usuário.')
    filial   = models.ForeignKey(Filial, blank=True, null=True, help_text='Filial do Usuário..', verbose_name='Filial')
    visible  = models.BooleanField(default = True, verbose_name='Habilitado')
    nasc     = models.DateField(verbose_name='Data de nascimento', blank = True, null = True, help_text='exemplo: 10/12/1980')
    sexo     = models.CharField(max_length=1, choices=CHOICE_SEXO, verbose_name='Sexo')
    rg       = models.CharField(blank = True, null = True, max_length=12, verbose_name='RG')
    cpf      = models.CharField(blank = True, null = True, max_length=15, verbose_name='CPF')
    cnpj     = models.CharField(blank = True, null = True, max_length=20, verbose_name='CNPJ')
    endereco = models.CharField(blank = True, null = True, max_length=255, verbose_name='Endereço')
    numero   = models.IntegerField(blank = True, null = True, verbose_name='Numero', help_text='Somente números')
    complem  = models.CharField(blank = True, null = True, max_length=255, verbose_name='Complemento')
    bairro   = models.CharField(blank = True, null = True, max_length=255, verbose_name='Bairro')
    cep      = models.CharField(blank = True, null = True, max_length=10, verbose_name='CEP')
    estado   = models.ForeignKey(State, blank = True, null = True, verbose_name='Estado')
    cidade   = models.ForeignKey(City, blank = True, null = True, verbose_name='Cidade')
    cargo    = models.CharField(max_length=255, blank = True, null = True, verbose_name='Cargo')
    admissao = models.DateField(verbose_name='Data de admissão', blank = True, null = True, help_text='exemplo: 10/12/2011')
    fone_com = models.CharField(max_length=50, blank=True, null=True, verbose_name='Telefone Comercial')
    fone_res = models.CharField(max_length=50, blank=True, null=True, verbose_name='Telefone Residencial')
    fone_cel = models.CharField(max_length=50, blank=True, null=True, verbose_name='Telefone Celular')
    receber  = models.BooleanField(default = True, verbose_name='Aceita receber mensagens')
    access   = models.BooleanField(default = False, verbose_name='Acesso Restrito', help_text='Liberá o acesso do usuario as categorias restritas.')
    envia    = models.BooleanField(default = False, verbose_name='Envia e-mail', help_text='Se marcado e o status for igual a ativo envia o email de confirmação para o usuário.')
    offline  = models.BooleanField(default = False, verbose_name='OffLine', help_text='Se marcado o usuário só pode acessar offline.')
    pontos   = models.IntegerField(editable=False, default=0, verbose_name='Pontos', help_text='Somente números')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.user.username

    def nome(self):
        if len(self.user.first_name) > 1:
            return '%s %s' % (self.user.first_name, self.user.last_name)
        else:
            return self.user.username

    def humanize_nasc(self):
        return default_date(self.nasc, 'd/m/Y')

    def humanize_sexo(self):
        return ['Feminino', 'Masculino'][self.sexo == 'M']

    class Meta:
        verbose_name        = u'Informação de Usuário'
        verbose_name_plural = u'Informações de Usuários'
        ordering            = ['user']


### Tabela para os menus
class Menu(models.Model):
    rede    = models.ManyToManyField(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Menu.')
    visible = models.BooleanField(default = True, verbose_name='Habilitado')
    name    = models.TextField(max_length = 255, verbose_name='Nome')
    url     = models.CharField(max_length = 255, verbose_name='URL')
    tipo    = models.CharField(max_length=1, default='B', choices=CHOICE_TIPO, verbose_name='Tipo')
    order   = models.IntegerField(default = 0, verbose_name='Posição', help_text='posição do campo no menu ex: 4. Se todos os campos estiverem com valor "0" será ordena pelo nome')
    date    = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return strip_tags(self.name)

    def get_name(self):
        if self.tipo == 'D':
            return u'Destaque: %s' % strip_tags(self.name)
        return self.name

    def Redes(self):
        return default_join(self.rede.filter(visible = True), ', ') or u'(Nenhum)'

    class Meta:
        verbose_name        = u'Menu'
        verbose_name_plural = u'Menu'
        ordering            = ['order']


### Tabela para os relatorio de play e complete
class RelatorioAcoes(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    video    = models.ForeignKey(Treinamento, verbose_name='Treinamento')
    play     = models.BooleanField(default = False, verbose_name='Play')
    complete = models.BooleanField(default = False, verbose_name='Assistido até o fim')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.video.name

    class Meta:
        verbose_name        = u'Relatório de Acão'
        verbose_name_plural = u'Relatório de Acões'
        ordering            = ['-date']


### Tabela para os relatorio de tentativas resgatando o tempo
class RelatorioTentativa(models.Model):
    rede        = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user        = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    treinamento = models.ForeignKey(Treinamento, verbose_name='Treinamento')
    date_init   = models.DateTimeField(blank = True, null = True, verbose_name='Data e hora inicio')
    date_end    = models.DateTimeField(blank = True, null = True, verbose_name='Data e hora fim')
    aprovado    = models.BooleanField(default = False, verbose_name='Aprovado')
    date        = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name        = u'Relatório de Tentativa de Acerto'
        verbose_name_plural = u'Relatório de Tentativas de Acerto'
        ordering            = ['-date']


### Tabela para os tipos de templates
class TipoTemplate(models.Model):
    name = models.CharField(max_length = 255, verbose_name='Nome')

    def __unicode__(self):

        return self.name

    class Meta:
        verbose_name = u'Tipo de Template'
        ordering     = ['name']


### Tabela para os templates
class Template(models.Model):
    rede     = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar o Template.')
    tipo     = models.ForeignKey(TipoTemplate, related_name='+', verbose_name='Tipo de Template', help_text='Selecione o tipo de template para filtrar o tema.')
    visible  = models.BooleanField(default = True, verbose_name='Habilitado')
    name     = models.CharField(max_length = 255, verbose_name='Nome')
    ## Fundo do site
    cor1     = ColorField(max_length = 30, verbose_name='Cor de fundo', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    image1   = models.ImageField(blank=True, null=True, upload_to = upload_file, verbose_name='Imagem', max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site.')
    advance1 = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Opções avançadas', help_text='Neste campo poderá usar opções avançadas como center, top, left, bottom, right, scroll, fixed.')
    ## Fonte geral do site
    font1    = models.FileField(blank=True, null=True, upload_to = upload_file, verbose_name='WebFont.ttf', max_length=255, help_text='Para gerar as font\'s, acesse o site http://www.fontsquirrel.com/fontface/generator. Caso contrário, deixe em branco.')
    font2    = models.FileField(blank=True, null=True, upload_to = upload_file, verbose_name='WebFont.eot', max_length=255, help_text='Para gerar as font\'s, acesse o site http://www.fontsquirrel.com/fontface/generator. Caso contrário, deixe em branco.')
    font3    = models.FileField(blank=True, null=True, upload_to = upload_file, verbose_name='WebFont.woff', max_length=255, help_text='Para gerar as font\'s, acesse o site http://www.fontsquirrel.com/fontface/generator. Caso contrário, deixe em branco.')
    font4    = models.FileField(blank=True, null=True, upload_to = upload_file, verbose_name='WebFont.svg', max_length=255, help_text='Para gerar as font\'s, acesse o site http://www.fontsquirrel.com/fontface/generator. Caso contrário, deixe em branco.')
    font_gle = models.CharField(blank=True, null=True, max_length = 255, verbose_name='GoogleFont', help_text='Caso não tenha os arquivos acima, acesse o site http://http://www.google.com/webfonts e localize sua fonte e copie e cole a family. Caso contrário, deixe em branco.')
    ## Cabeçario
    cor2     = ColorField(max_length = 30, verbose_name='Cor de fundo', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    image2   = models.ImageField(blank=True, null=True, upload_to = upload_file, verbose_name='Imagem de fundo', max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site.')
    cor15    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor da borda inferior')
    larg4    = models.IntegerField(default=0, verbose_name='Largura da borda inferior', help_text='valor numérico em pixels.')
    ## Menu principal
    cor3     = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor de fundo')
    cor16    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor de texto')
    cor18    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do botão ativo')
    cor19    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto do botão ativo')
    cor17    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor da borda')
    cor33    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor de fundo para degradê mobile')
    larg5    = models.IntegerField(default=0, verbose_name='Largura da borda', help_text='valor numérico em pixels.')
    ## Campo Busca
    image4   = models.ImageField(blank=True, null=True, upload_to = upload_file, verbose_name='Imagem icon busca', max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site.')
    image7   = models.ImageField(blank=True, null=True, upload_to = upload_file, verbose_name='Imagem icon usuário', max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site.')
    cor20    = ColorField(max_length = 30, verbose_name='Cor de fundo', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    cor39    = ColorField(max_length = 30, verbose_name='Cor da borda do campo', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    larg11   = models.IntegerField(default=0, blank = True, verbose_name='Largura da borda do campo', help_text='valor numérico em pixels.')
    cor40    = ColorField(max_length = 30, verbose_name='Cor do texto inferior da busca', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    ## Rodapé
    cor4     = ColorField(max_length = 30, verbose_name='Cor de fundo', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    cor5     = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor de texto')
    image3   = models.ImageField(blank=True, null=True, upload_to = upload_file, verbose_name='Imagem de fundo', max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site.')
    cor21    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor da borda superior')
    larg6    = models.IntegerField(default=0, blank = True, verbose_name='Largura da borda superior', help_text='valor numérico em pixels.')
    ## Banner Rotativo
    image5   = models.ImageField(blank=True, null=True, upload_to = upload_file, verbose_name='Imagem de fundo', max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site.')
    cor22    = ColorField(max_length = 30, verbose_name='Cor de fundo', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    cor23    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor da borda superior')
    larg7    = models.IntegerField(default=0, verbose_name='Largura da borda superior', help_text='valor numérico em pixels.')
    cor24    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor da borda inferior')
    larg8    = models.IntegerField(default=0, verbose_name='Largura da borda inferior', help_text='valor numérico em pixels.')
    cor34    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto do indicador numérico')
    cor35    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto do indicador numérico ativo')
    cor36    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto do indicador numérico mouse acima')
    ## Conteúdo do site
    cor25    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor da borda superior')
    larg9    = models.IntegerField(default=0, verbose_name='Largura da borda superior', help_text='valor numérico em pixels.')
    cor26    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor da borda inferior')
    larg10   = models.IntegerField(default=0, verbose_name='Largura da borda inferior', help_text='valor numérico em pixels.')
    ## Barra de Titulo
    title_d  = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Título default das categorias no plural', help_text='O padrão é SELECIONE UMA DAS %s CATEGORIAS ABAIXO')
    title_ds = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Título default da categoria no singular', help_text='O padrão é SELECIONE A CATEGORIA ABAIXO')
    title_pd = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Título default dos parceiros', help_text='O padrão é PARCEIROS')
    cor6     = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do fundo')
    cor7     = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto')
    cor37    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do fundo parceiros')
    cor38    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto parceiros')
    ## Categorias e Treinamentos
    cor12    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor da borda')
    larg1    = models.IntegerField(default=0, verbose_name='Largura da borda', help_text='valor numérico em pixels.')
    larg2    = models.IntegerField(default=12, verbose_name='Tamanho do titulo', help_text='valor numérico em pixels.')
    cor13    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do titulo')
    larg3    = models.IntegerField(default=12, verbose_name='Tamanho do texto', help_text='valor numérico em pixels.')
    cor14    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto')
    cor31    = ColorField(max_length = 30, blank = True, null = True, verbose_name='Cor do fundo ativo', help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    cor32    = ColorField(max_length = 30, blank = True, null = True, verbose_name='Cor do fundo', help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    ## Demais Botões
    cor27    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do fundo')
    cor28    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto')
    cor29    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do fundo ativo')
    cor30    = ColorField(max_length = 30, blank = True, default='ffffff', verbose_name='Cor do texto ativo')
    ## Mensagem dica login
    image8   = models.ImageField(blank=True, null=True, upload_to = upload_file, verbose_name='Imagem botão dica login', max_length=255, help_text='As imagens seram ajustadas para melhor visualização no site. Fundo transparente. PNG ou GIF.')
    cor41    = ColorField(max_length = 30, verbose_name='Cor do texto', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    cor42    = ColorField(max_length = 30, verbose_name='Cor da borda', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    cor43    = ColorField(max_length = 30, verbose_name='Cor de fundo', null = True, blank = True, help_text='Selecione a cor desejada, caso não queira deixe em branco.')
    ## Favicon
    image6   = models.ImageField(blank=True, null=True, upload_to = upload_file, verbose_name='Imagem ico', max_length=255, help_text='Imagem deve ser .ico e ter proporções 48x48 pixels.')
    ## custom css
    custom   = models.TextField(blank=True, null=True, verbose_name='CSS Customizado', help_text='Se precisar inserir linhas de css no código, caso contrário, deixe em branco.')

    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):

        return self.name

    def save(self, *args, **kwargs):

        f = open('%s/mega/media/%s/css/template/%s.css' % (settings.MODPATH, self.tipo.name, self.rede.link), 'w+')

        f.write('/* template do %s */\n\n' % self.rede.link)

        f.write(get_style_template(self))

        f.close()

        fm = open('%s/mega/media/%s/css/template/%s-mobile.css' % (settings.MODPATH, self.tipo.name, self.rede.link), 'w+')

        fm.write('/* template do %s mobile */\n\n' % self.rede.link)

        fm.write(get_style_template_mobile(self))

        fm.close()

        ft = open('%s/mega/media/%s/css/template/%s-tablet.css' % (settings.MODPATH, self.tipo.name, self.rede.link), 'w+')

        ft.write('/* template do %s tablet */\n\n' % self.rede.link)

        ft.write(get_style_template_tablet(self))

        ft.close()

        super(Template, self).save(*args, **kwargs)


    class Meta:
        verbose_name = u'Template'
        ordering     = ['rede']


## chat

### Tabela para as listas de mensagens no chat
class WebChat(models.Model):
    rede      = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Chat.')
    user      = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    live      = models.ForeignKey(Treinamento, verbose_name='Live')
    text      = models.TextField(verbose_name='Mensagem')
    user_lido = models.ManyToManyField(UserAdmin, related_name='Usuários que já leram', verbose_name='Usuários que já leram', help_text='Segure CTRL e clique para selecionar mais de uma opção.', blank = True)
    date      = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name        = u'Mensagem Web Chat'
        verbose_name_plural = u'Mensagens Web Chat'
        ordering            = ['-date']


### Tabela para as lista de videoconfere do cliente administrador
class Live(models.Model):
    rede           = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Ao Vivo.')
    live           = models.ForeignKey(Treinamento, verbose_name='Treinamento Ao Vivo')
    user_not_chat  = models.ManyToManyField(UserAdmin, related_name='Desabilitar Chat', verbose_name='Desabilitar Chat', help_text='Segure CTRL e clique para selecionar mais de uma opção.', blank = True)
    user_not_video = models.ManyToManyField(UserAdmin, related_name='Desabilitar Vídeo', verbose_name='Desabilitar Vídeo', help_text='Segure CTRL e clique para selecionar mais de uma opção.', blank = True)
    user_not_audio = models.ManyToManyField(UserAdmin, related_name='Desabilitar Áudio', verbose_name='Desabilitar Áudio', help_text='Segure CTRL e clique para selecionar mais de uma opção.', blank = True)
    user_not_all   = models.ManyToManyField(UserAdmin, related_name='Desabilitar Todos os recursos', verbose_name='Desabilitar Todos os recursos', help_text='Segure CTRL e clique para selecionar mais de uma opção.', blank = True)
    date           = models.DateTimeField(auto_now_add = True, verbose_name='Data')

    def __unicode__(self):
        return self.live.name

    def Data_de_agendamento(self):
        return default_date(self.live.agendado, 'd/m/Y á\s G:i')

    class Meta:
        verbose_name        = u'Ao Vivo'
        verbose_name_plural = u'Ao Vivo'
        ordering            = ['-date']


### Tabela para as lista de as sugestões, criticas e opniões sobre os treinamentos
class Suggestion(models.Model):
    rede        = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar as sugestões.')
    treinamento = models.ForeignKey(Treinamento, verbose_name='Treinamento')
    user        = models.ForeignKey(UserAdmin, verbose_name='Usuário')
    mensagem    = models.TextField(verbose_name='Mensagem')
    enviado     = models.BooleanField(default = False, verbose_name='Enviado')
    date_send   = models.DateTimeField(blank = True, null = True, verbose_name='Data do envio')
    command     = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Comando função')
    date        = models.DateTimeField(auto_now_add = True, verbose_name='Data')

    def __unicode__(self):
        return self.rede.name

    def Data_de_envio(self):
        return default_date(self.data_send, 'd/m/Y á\s G:i')

    class Meta:
        verbose_name        = u'Sugestão'
        verbose_name_plural = u'Sugestões'
        ordering            = ['-date']


### Tabela para as lista de Anexos para downloads
class Anexo(models.Model):
    rede        = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar os anexos.')
    category    = models.ForeignKey(Category, blank = True, null = True, verbose_name='Categoria')
    treinamento = models.ForeignKey(Treinamento, blank = True, null = True, verbose_name='Treinamento')
    name        = models.CharField(max_length = 255, verbose_name='Nome do arquivo')
    visible     = models.BooleanField(default = True, verbose_name='Habilitado')
    desc        = models.TextField(null = True, blank = True, verbose_name='Descrição')
    file        = models.FileField(upload_to = upload_file, verbose_name='Arquivo', max_length=255, help_text='Pode enviar qualquer tipo de arquivo, contanto que tenha extensão e se for vários arquivos, tente diminuir o conteudo usando compressão zip. Evite arquivos com extensão .exe ou .bin.')
    date        = models.DateTimeField(auto_now_add = True, verbose_name='Data')

    def save(self, *args, **kwargs):
        
        super(Anexo, self).save(*args, **kwargs)
        
        if '.pdf' in self.file.path.lower():
            sh  = Sh()
            if settings.DEBUG:
                sh.python( '%sbin/pdf_to_images.py %s --quiet' % (getattr(settings, 'MEGA_LIB', ''), self.id) )
            else:
                sh.pythonvirtualenv( '%s %sbin/pdf_to_images.py %s --quiet' % ('tcd', getattr(settings, 'MEGA_LIB', ''), self.id) )
                
                
    @staticmethod    
    def filter_custom(category):
   
        array = []

        for lia in ListImageAnexo.objects.filter( Q(anexo__category = category) ):
            if not array.count(lia.anexo) > 0:
                array.append(lia.anexo)

        return array
    

    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = u'Anexo'
        ordering     = ['-date']
        

### Tabela para as ListImageAnexo
class ListImageAnexo(models.Model):
    rede     = models.ForeignKey(Rede, related_name='+', verbose_name='Rede')
    image    = models.ImageField(upload_to = upload_file, max_length=255, verbose_name='Imagem')
    anexo    = models.ForeignKey(Anexo, related_name='+', verbose_name='Anexo')

    def __unicode__(self):
        return self.image.name

    class Meta:
        verbose_name = u'Lista de Imagens Anexo'
        ordering     = ['image']


### Tabela para as lista de Perguntas e Respostas com nível de aprovação
class Quiz(models.Model):
    rede          = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar os quiz.')
    treinamento   = models.ForeignKey(Treinamento, verbose_name='Treinamento')
    instrucao     = models.TextField(null = True, blank = True, verbose_name='Instruções')
    list_question = models.ManyToManyField(Question, related_name='Lista de Perguntas', verbose_name='Lista de Perguntas', help_text='Segure CTRL e clique para selecionar mais de uma opção.')
    list_response = models.ManyToManyField(Response, related_name='Lista de Respostas', verbose_name='Lista de Respostas', help_text='Segure CTRL e clique para selecionar mais de uma opção.')
    porcent       = models.IntegerField(default = 100, verbose_name='Porcentagem de acerto para aprovação', help_text='Valor númerico sem a %')
    responsavel   = models.ManyToManyField(UserAdmin, verbose_name='Responsável', help_text='Responsável por aprovar um usuário. Segure CTRL e clique para selecionar mais de uma opção.', blank = True, null = True)
    email_respon  = models.CharField(max_length = 255, verbose_name='E-mail responsável', null = True, blank = True, help_text='Somente adicione o email caso o responsável não estiver na lista.')
    date          = models.DateTimeField(auto_now_add = True, verbose_name='Data')

    def __unicode__(self):
        return self.treinamento.name

    def primeira_pergunta(self):
        list = self.list_question.filter(visible=True).order_by('id')
        if list.count() > 0:
            return list[0].text
        return u'(Nenhuma pergunta habilitada)'

    def porcentagem_acerto(self):
        return str(self.porcent) + '%'

    def email_responsavel(self):
        try:
            return self.responsavel.all()[0].email
        except:
            pass
        return self.email_respon

    def quant_perguntas(self):
        return len(self.list_question.filter(visible=True))

    class Meta:
        verbose_name        = u'Quiz'
        verbose_name_plural = u'Quiz'
        ordering            = ['-date']

## regras para deletar as perguntas e respostas
@receiver(pre_delete, sender=Quiz)
def _quiz_delete(sender, instance, **kwargs):
    ## limpa questões
    Question.objects.filter( treinamento = instance.treinamento ).delete()


### Tabela para os relatorio de pontos e avaliações
class RelatorioAvalicao(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar o Relatório.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário', help_text='Usuário para acesso do sistema.')
    quiz     = models.ForeignKey(Quiz, null = True, blank = True, verbose_name='Quiz', help_text='Quiz de perguntas e respostas.')
    pontos   = models.IntegerField(default=0, verbose_name='Pontos', help_text='Somente números')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name        = u'Relatório de Avaliação'
        verbose_name_plural = u'Relatório de Avaliações'
        ordering            = ['-date']


### Tabela para as livres respostas das questões
class FreeResponse(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar as respostas livres.')
    user     = models.ForeignKey(UserAdmin, verbose_name='Usuário')
    question = models.ForeignKey(Question, verbose_name='Pergunta')
    text     = models.TextField(verbose_name='Resposta')
    porcent  = models.IntegerField(default = 100, verbose_name='Porcentagem de acerto', help_text='Valor númerico sem a %')
    aprovado = models.BooleanField(default = False, verbose_name='Aprovado')
    date     = models.DateTimeField(auto_now_add = True, verbose_name='Data')

    def __unicode__(self):
        return self.question.text

    class Meta:
        verbose_name        = u'Resposta Livre'
        verbose_name_plural = u'Respostas Livre'
        ordering            = ['-date']


### Tabela para as Enquetes
class Enquete(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar as enquetes.')
    title    = models.CharField(max_length = 255, verbose_name='Título')
    visible  = models.BooleanField(default = True, verbose_name='Habilitado')
    opcao1   = models.CharField(max_length = 255, verbose_name='Opção 1')
    n_opcao1 = models.IntegerField(default = 0, verbose_name='Votos 1')
    opcao2   = models.CharField(max_length = 255, verbose_name='Opção 2')
    n_opcao2 = models.IntegerField(default = 0, verbose_name='Votos 2')
    opcao3   = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Opção 3')
    n_opcao3 = models.IntegerField(default = 0, verbose_name='Votos 3')
    opcao4   = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Opção 4')
    n_opcao4 = models.IntegerField(default = 0, verbose_name='Votos 4')
    opcao5   = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Opção 5')
    n_opcao5 = models.IntegerField(default = 0, verbose_name='Votos 5')
    opcao6   = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Opção 6')
    n_opcao6 = models.IntegerField(default = 0, verbose_name='Votos 6')
    users    = models.ManyToManyField(UserAdmin, null = True, blank = True, verbose_name='Usuários que votaram')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.title

    def quant_votos(self):
        return self.users.all().count()

    class Meta:
        verbose_name = u'Enquete'
        ordering     = ['-date']


### Tabela para url's por e-mail
class Url(models.Model):
    rede   = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar as url\'s.')
    type   = models.CharField(max_length = 255, verbose_name='Tipo')
    key    = models.TextField(verbose_name='Chave')
    link   = models.TextField(verbose_name='Link')
    mto    = models.CharField(max_length = 255, verbose_name='Quem enviou')
    mfrom  = models.CharField(max_length = 255, verbose_name='Quem recebeu')
    active = models.BooleanField(default = True, verbose_name='Ativo')
    date_v = models.DateTimeField(blank = True, null = True, verbose_name='Data e hora visualização')
    date   = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.type

    class Meta:
        verbose_name        = u'Url'
        verbose_name_plural = u'Url\'s'
        ordering            = ['-date']


### Tabela para os Contatos comerciais
class ContatoComercial(models.Model):
    rede     = models.ForeignKey(Rede, verbose_name='Rede', help_text='Selecione a rede para filtrar os contatos comerciais.')
    category = models.ForeignKey(Category, verbose_name='Categoria')
    nome     = models.CharField(max_length = 255, verbose_name='Nome')
    email    = models.EmailField(max_length = 255, verbose_name='E-mail')
    regiao   = models.CharField(max_length = 100, blank = True, null = True, verbose_name='Região', help_text="Região geográfica de atendimento (ou nome da empresa)")
    fone1    = models.CharField(max_length = 50, verbose_name='Fone 1')
    fone2    = models.CharField(max_length = 50, blank = True, null = True, verbose_name='Fone 2')
    visible  = models.BooleanField(default = True, verbose_name='Habilitado')
    date     = models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name        = u'Contato Comercial'
        verbose_name_plural = u'Contatos Comerciais'
        ordering            = ['nome']


### Tabela para os Avisos e notificações
class Aviso(models.Model):
    rede          = models.ForeignKey(Rede, related_name='+', verbose_name='Rede', help_text='Selecione a rede para filtrar os avisos.')
    name          = models.CharField(max_length = 255, verbose_name='Título')
    image         = models.ImageField(upload_to = upload_file, max_length=255, help_text='A imagem para ser mostrada poderá ser de qualquer tamanho, respeitando sempre a largura máxima para mobile.', verbose_name='Imagem')
    is_video      = models.BooleanField(default = False, verbose_name='Vídeo?')
    link          = models.CharField(max_length = 255, null = True, blank = True, verbose_name='Link')
    code          = models.CharField(max_length = 50, null = True, blank = True, verbose_name='Código MegaVideo')
    is_not_view   = models.ManyToManyField(UserAdmin, related_name='Usuários não quer mais visualizar', blank = True, help_text='Usuários que não desejam mais ver a mensagem.')
    is_persistent = models.BooleanField(default = True, verbose_name='Persistente?')
    is_full_user  = models.BooleanField(default = True, verbose_name='Todos os usuários vão ver?')
    is_user_view  = models.ManyToManyField(UserAdmin, related_name='Usuários que vão visualizar', verbose_name='Usuários que vão visualizar', blank = True, help_text='Somente os usuários que vão ver a mensagem.')
    visible       = models.BooleanField(default = True, verbose_name='Habilitado')
    date          = models.DateTimeField(auto_now_add=True, verbose_name='Data')
    date_init     = models.DateTimeField(null = True, blank = True, verbose_name='Data inicia demonstração')
    date_end      = models.DateTimeField(null = True, blank = True, verbose_name='Data termina demonstração')

    def __unicode__(self):
        return self.name

    def Data_inicia(self):
        if not self.date_init:
            return u'Imediato'
        return default_date(self.date_init, 'd/m/Y á\s G:i')

    def Data_termina(self):
        if not self.date_end:
            return u'Indefinido'
        return default_date(self.date_end, 'd/m/Y á\s G:i')

    class Meta:
        verbose_name = u'Aviso'
        ordering     = ['rede']


class Host(models.Model):
    rede    = models.ForeignKey(Rede, verbose_name='Rede')
    visible = models.BooleanField(default = True, verbose_name='Habilitado')
    ip      = models.CharField(max_length=128, verbose_name='IP')
    date    = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.ip

    class Meta:
        ordering = ['ip']
                
        
class Router(models.Model):
    rede    = models.ForeignKey(Rede, verbose_name='Rede')
    host    = models.ForeignKey(Host, verbose_name='Host')
    visible = models.BooleanField(default = True, verbose_name='Habilitado')
    ip      = models.CharField(max_length=128, verbose_name='IP', help_text='Use o IP do usuário, ou IP rotas, tipo 10.0.1, não use ponto no final.')

    def __unicode__(self):
        return self.ip

    class Meta:
        ordering = ['ip'] 
        
        
class ScreenSaver(models.Model):
    rede       = models.ForeignKey(Rede, verbose_name='Rede')
    is_offline = models.BooleanField(default = True, verbose_name='Ambiente OffLine')
    is_online  = models.BooleanField(default = False, verbose_name='Ambiente OnLine')
    list_video = models.CharField(max_length=255, verbose_name='Código Vídeo(s)', help_text='Caso mais que um código do MegaVideo, separar com ponto-e-vírgula. Ex: _XLXL456; _KFKF523')
    time_login = models.IntegerField(default = 60, verbose_name='Tempo do login', help_text='Em segundos, o tempo ocioso da área do login.')
    time_full  = models.IntegerField(default = (60*15), verbose_name='Tempo demais páginas', help_text='Em segundos, o tempo ocioso das demais páginas internas.')
    visible    = models.BooleanField(default = True, verbose_name='Habilitado')
    date       = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.rede.name
    
    def get_videos(self):
        
        lista = []
        for lv in self.list_video.split(';'):
            lista.append(lv.strip())
            
        return lista
        
    class Meta:
        verbose_name        = u'Protetor de tela'
        verbose_name_plural = u'Protetores de tela'
        ordering            = ['visible']
               

