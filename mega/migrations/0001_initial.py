# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rede'
        db.create_table('mega_rede', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Rede'])

        # Adding M2M table for field user on 'Rede'
        db.create_table('mega_rede_user', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('rede', models.ForeignKey(orm['mega.rede'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('mega_rede_user', ['rede_id', 'user_id'])

        # Adding model 'Filial'
        db.create_table('mega_filial', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Filial'])

        # Adding model 'Category'
        db.create_table('mega_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Category'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('desc', self.gf('ckeditor.fields.RichTextField')(null=True, blank=True)),
            ('access', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Category'])

        # Adding M2M table for field filial on 'Category'
        db.create_table('mega_category_filial', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('category', models.ForeignKey(orm['mega.category'], null=False)),
            ('filial', models.ForeignKey(orm['mega.filial'], null=False))
        ))
        db.create_unique('mega_category_filial', ['category_id', 'filial_id'])

        # Adding model 'Treinamento'
        db.create_table('mega_treinamento', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('destaq', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='B', max_length=1)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Treinamento'])

        # Adding model 'Certificado'
        db.create_table('mega_certificado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Certificado'])

        # Adding M2M table for field treinamento on 'Certificado'
        db.create_table('mega_certificado_treinamento', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('certificado', models.ForeignKey(orm['mega.certificado'], null=False)),
            ('treinamento', models.ForeignKey(orm['mega.treinamento'], null=False))
        ))
        db.create_unique('mega_certificado_treinamento', ['certificado_id', 'treinamento_id'])

        # Adding model 'Question'
        db.create_table('mega_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('treinamento', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Treinamento'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('pontos', self.gf('django.db.models.fields.IntegerField')(default=20)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Question'])

        # Adding model 'Response'
        db.create_table('mega_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Question'])),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('correta', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Response'])

        # Adding model 'Parceiro'
        db.create_table('mega_parceiro', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['mega.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Parceiro'])

        # Adding model 'Banner'
        db.create_table('mega_banner', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['mega.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=255)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('legend', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('blank', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Banner'])

        # Adding model 'Faq'
        db.create_table('mega_faq', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('pergunta', self.gf('django.db.models.fields.TextField')()),
            ('resposta', self.gf('django.db.models.fields.TextField')()),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('access', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Faq'])

        # Adding M2M table for field filial on 'Faq'
        db.create_table('mega_faq_filial', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('faq', models.ForeignKey(orm['mega.faq'], null=False)),
            ('filial', models.ForeignKey(orm['mega.filial'], null=False))
        ))
        db.create_unique('mega_faq_filial', ['faq_id', 'filial_id'])

        # Adding model 'InfoUser'
        db.create_table('mega_infouser', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('filial', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Filial'], null=True, blank=True)),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('nasc', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('sexo', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('rg', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
            ('cpf', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('endereco', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('numero', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('complem', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('bairro', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cep', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('estado', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['state.State'], null=True, blank=True)),
            ('cidade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['state.City'], null=True, blank=True)),
            ('fone_com', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('fone_res', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('fone_cel', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('receber', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('access', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('envia', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('matricul', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('pontos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['InfoUser'])

        # Adding model 'Menu'
        db.create_table('mega_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.TextField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('tipo', self.gf('django.db.models.fields.CharField')(default='B', max_length=1)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Menu'])

        # Adding model 'RelatorioAcoes'
        db.create_table('mega_relatorioacoes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Rede'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Treinamento'])),
            ('play', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['RelatorioAcoes'])

        # Adding model 'RelatorioAvalicao'
        db.create_table('mega_relatorioavalicao', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Rede'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('pontos', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['RelatorioAvalicao'])

        # Adding M2M table for field question on 'RelatorioAvalicao'
        db.create_table('mega_relatorioavalicao_question', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('relatorioavalicao', models.ForeignKey(orm['mega.relatorioavalicao'], null=False)),
            ('question', models.ForeignKey(orm['mega.question'], null=False))
        ))
        db.create_unique('mega_relatorioavalicao_question', ['relatorioavalicao_id', 'question_id'])

        # Adding model 'RelatorioTentativa'
        db.create_table('mega_relatoriotentativa', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Rede'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('treinamento', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Treinamento'])),
            ('date_init', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('aprovado', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['RelatorioTentativa'])

        # Adding model 'TipoTemplate'
        db.create_table('mega_tipotemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mega', ['TipoTemplate'])

        # Adding model 'Template'
        db.create_table('mega_template', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.Rede'])),
            ('tipo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mega.TipoTemplate'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cor1', self.gf('colors.fields.ColorField')(max_length=7, null=True, blank=True)),
            ('image1', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('advance1', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cor2', self.gf('colors.fields.ColorField')(max_length=7, null=True, blank=True)),
            ('image2', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('cor15', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg4', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cor3', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor16', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor18', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor19', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor17', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor33', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg5', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image4', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('image7', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('cor20', self.gf('colors.fields.ColorField')(max_length=7, null=True, blank=True)),
            ('cor4', self.gf('colors.fields.ColorField')(max_length=7, null=True, blank=True)),
            ('cor5', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('image3', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('cor21', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg6', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('image5', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('cor22', self.gf('colors.fields.ColorField')(max_length=7, null=True, blank=True)),
            ('cor23', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg7', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cor24', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg8', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cor34', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor35', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor36', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor25', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg9', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cor26', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg10', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('cor6', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor7', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor12', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg1', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('larg2', self.gf('django.db.models.fields.IntegerField')(default=12)),
            ('cor13', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('larg3', self.gf('django.db.models.fields.IntegerField')(default=12)),
            ('cor14', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor31', self.gf('colors.fields.ColorField')(max_length=7, null=True, blank=True)),
            ('cor32', self.gf('colors.fields.ColorField')(max_length=7, null=True, blank=True)),
            ('cor27', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor28', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor29', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('cor30', self.gf('colors.fields.ColorField')(default='ffffff', max_length=7, blank=True)),
            ('image6', self.gf('django.db.models.fields.files.ImageField')(max_length=255, null=True, blank=True)),
            ('custom', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('mega', ['Template'])


    def backwards(self, orm):
        # Deleting model 'Rede'
        db.delete_table('mega_rede')

        # Removing M2M table for field user on 'Rede'
        db.delete_table('mega_rede_user')

        # Deleting model 'Filial'
        db.delete_table('mega_filial')

        # Deleting model 'Category'
        db.delete_table('mega_category')

        # Removing M2M table for field filial on 'Category'
        db.delete_table('mega_category_filial')

        # Deleting model 'Treinamento'
        db.delete_table('mega_treinamento')

        # Deleting model 'Certificado'
        db.delete_table('mega_certificado')

        # Removing M2M table for field treinamento on 'Certificado'
        db.delete_table('mega_certificado_treinamento')

        # Deleting model 'Question'
        db.delete_table('mega_question')

        # Deleting model 'Response'
        db.delete_table('mega_response')

        # Deleting model 'Parceiro'
        db.delete_table('mega_parceiro')

        # Deleting model 'Banner'
        db.delete_table('mega_banner')

        # Deleting model 'Faq'
        db.delete_table('mega_faq')

        # Removing M2M table for field filial on 'Faq'
        db.delete_table('mega_faq_filial')

        # Deleting model 'InfoUser'
        db.delete_table('mega_infouser')

        # Deleting model 'Menu'
        db.delete_table('mega_menu')

        # Deleting model 'RelatorioAcoes'
        db.delete_table('mega_relatorioacoes')

        # Deleting model 'RelatorioAvalicao'
        db.delete_table('mega_relatorioavalicao')

        # Removing M2M table for field question on 'RelatorioAvalicao'
        db.delete_table('mega_relatorioavalicao_question')

        # Deleting model 'RelatorioTentativa'
        db.delete_table('mega_relatoriotentativa')

        # Deleting model 'TipoTemplate'
        db.delete_table('mega_tipotemplate')

        # Deleting model 'Template'
        db.delete_table('mega_template')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mega.banner': {
            'Meta': {'ordering': "['order', 'name']", 'object_name': 'Banner'},
            'blank': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['mega.Category']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'legend': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.category': {
            'Meta': {'ordering': "['name']", 'object_name': 'Category'},
            'access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'filial': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['mega.Filial']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Category']", 'null': 'True', 'blank': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.certificado': {
            'Meta': {'ordering': "['rede']", 'object_name': 'Certificado'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'treinamento': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mega.Treinamento']", 'symmetrical': 'False'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.faq': {
            'Meta': {'ordering': "['order']", 'object_name': 'Faq'},
            'access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'filial': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mega.Filial']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pergunta': ('django.db.models.fields.TextField', [], {}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'resposta': ('django.db.models.fields.TextField', [], {}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.filial': {
            'Meta': {'ordering': "['name']", 'object_name': 'Filial'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.infouser': {
            'Meta': {'ordering': "['user']", 'object_name': 'InfoUser'},
            'access': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cep': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'cidade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['state.City']", 'null': 'True', 'blank': 'True'}),
            'complem': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cpf': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'envia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'estado': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['state.State']", 'null': 'True', 'blank': 'True'}),
            'filial': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Filial']", 'null': 'True', 'blank': 'True'}),
            'fone_cel': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'fone_com': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'fone_res': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'matricul': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'nasc': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'numero': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'receber': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'rg': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.menu': {
            'Meta': {'ordering': "['order']", 'object_name': 'Menu'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'B'", 'max_length': '1'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.parceiro': {
            'Meta': {'ordering': "['name']", 'object_name': 'Parceiro'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['mega.Category']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.question': {
            'Meta': {'object_name': 'Question'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'treinamento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Treinamento']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.rede': {
            'Meta': {'ordering': "['name']", 'object_name': 'Rede'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.relatorioacoes': {
            'Meta': {'ordering': "['-date']", 'object_name': 'RelatorioAcoes'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"})
        },
        'mega.relatorioavalicao': {
            'Meta': {'ordering': "['-date']", 'object_name': 'RelatorioAvalicao'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mega.Question']", 'symmetrical': 'False'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mega.relatoriotentativa': {
            'Meta': {'ordering': "['-date']", 'object_name': 'RelatorioTentativa'},
            'aprovado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_init': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'treinamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mega.response': {
            'Meta': {'ordering': "['question']", 'object_name': 'Response'},
            'correta': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Question']"}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'mega.template': {
            'Meta': {'ordering': "['rede']", 'object_name': 'Template'},
            'advance1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cor1': ('colors.fields.ColorField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'cor12': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor13': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor14': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor15': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor16': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor17': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor18': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor19': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor2': ('colors.fields.ColorField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'cor20': ('colors.fields.ColorField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'cor21': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor22': ('colors.fields.ColorField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'cor23': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor24': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor25': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor26': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor27': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor28': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor29': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor3': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor30': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor31': ('colors.fields.ColorField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'cor32': ('colors.fields.ColorField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'cor33': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor34': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor35': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor36': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor4': ('colors.fields.ColorField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'cor5': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor6': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor7': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'custom': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image2': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image3': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image4': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image5': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image6': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image7': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'larg1': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'larg10': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'larg2': ('django.db.models.fields.IntegerField', [], {'default': '12'}),
            'larg3': ('django.db.models.fields.IntegerField', [], {'default': '12'}),
            'larg4': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'larg5': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'larg6': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'larg7': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'larg8': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'larg9': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'tipo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.TipoTemplate']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'mega.tipotemplate': {
            'Meta': {'ordering': "['name']", 'object_name': 'TipoTemplate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mega.treinamento': {
            'Meta': {'ordering': "['category']", 'object_name': 'Treinamento'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'destaq': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'B'", 'max_length': '1'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'state.city': {
            'Meta': {'ordering': "['name']", 'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['state.State']"})
        },
        'state.state': {
            'Meta': {'ordering': "['name']", 'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uf': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['mega']