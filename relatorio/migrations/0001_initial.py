# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AlunoCadastrado'
        db.create_table('relatorio_alunocadastrado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Rede'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('acesso', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('relatorio', ['AlunoCadastrado'])

        # Adding model 'AlunoCertificado'
        db.create_table('relatorio_alunocertificado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Rede'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('acesso', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('relatorio', ['AlunoCertificado'])

        # Adding model 'TreinamentoConcluido'
        db.create_table('relatorio_treinamentoconcluido', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Rede'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('acesso', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('relatorio', ['TreinamentoConcluido'])

        # Adding model 'PontuacaoAluno'
        db.create_table('relatorio_pontuacaoaluno', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Rede'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('acesso', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('relatorio', ['PontuacaoAluno'])

        # Adding model 'TreinamentoCadastrado'
        db.create_table('relatorio_treinamentocadastrado', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rede', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mega.Rede'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('acesso', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('relatorio', ['TreinamentoCadastrado'])


    def backwards(self, orm):
        # Deleting model 'AlunoCadastrado'
        db.delete_table('relatorio_alunocadastrado')

        # Deleting model 'AlunoCertificado'
        db.delete_table('relatorio_alunocertificado')

        # Deleting model 'TreinamentoConcluido'
        db.delete_table('relatorio_treinamentoconcluido')

        # Deleting model 'PontuacaoAluno'
        db.delete_table('relatorio_pontuacaoaluno')

        # Deleting model 'TreinamentoCadastrado'
        db.delete_table('relatorio_treinamentocadastrado')


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
        'relatorio.alunocadastrado': {
            'Meta': {'ordering': "['-date']", 'object_name': 'AlunoCadastrado'},
            'acesso': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'relatorio.alunocertificado': {
            'Meta': {'ordering': "['-date']", 'object_name': 'AlunoCertificado'},
            'acesso': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'relatorio.pontuacaoaluno': {
            'Meta': {'ordering': "['-date']", 'object_name': 'PontuacaoAluno'},
            'acesso': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'relatorio.treinamentocadastrado': {
            'Meta': {'ordering': "['-date']", 'object_name': 'TreinamentoCadastrado'},
            'acesso': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'relatorio.treinamentoconcluido': {
            'Meta': {'ordering': "['-date']", 'object_name': 'TreinamentoConcluido'},
            'acesso': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['relatorio']