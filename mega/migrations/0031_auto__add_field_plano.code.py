# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Plano.code'
        db.add_column('mega_plano', 'code', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True))
    
    
    def backwards(self, orm):
        
        # Deleting field 'Plano.code'
        db.delete_column('mega_plano', 'code')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mega.anexo': {
            'Meta': {'object_name': 'Anexo'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'treinamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.banner': {
            'Meta': {'object_name': 'Banner'},
            'blank': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mega.Category']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'home': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'legend': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.category': {
            'Meta': {'object_name': 'Category'},
            'access': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('ckeditor.fields.RichTextField', [], {'null': 'True', 'blank': 'True'}),
            'filial': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['mega.Filial']"}),
            'home': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'is_name': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Category']", 'null': 'True', 'blank': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.certificado': {
            'Meta': {'object_name': 'Certificado'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'treinamento': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mega.Treinamento']", 'symmetrical': 'False'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.elearning': {
            'Meta': {'object_name': 'Elearning'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dir': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'not_video': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'treinamento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Treinamento']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.faq': {
            'Meta': {'object_name': 'Faq'},
            'access': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'filial': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mega.Filial']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pergunta': ('django.db.models.fields.TextField', [], {}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'resposta': ('django.db.models.fields.TextField', [], {}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.filial': {
            'Meta': {'object_name': 'Filial'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.freeresponse': {
            'Meta': {'object_name': 'FreeResponse'},
            'aprovado': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'porcent': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Question']"}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mega.infouser': {
            'Meta': {'object_name': 'InfoUser'},
            'access': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'bairro': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cep': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'cidade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['state.City']", 'null': 'True', 'blank': 'True'}),
            'cnpj': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'complem': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cpf': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'endereco': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'envia': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
            'receber': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'rg': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'sexo': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.live': {
            'Meta': {'object_name': 'Live'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user_not_all': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'Desabilitar Todos os recursos'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'user_not_audio': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'Desabilitar \\xc3\\x81udio'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'user_not_chat': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'Desabilitar Chat'", 'blank': 'True', 'to': "orm['auth.User']"}),
            'user_not_video': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'Desabilitar V\\xc3\\xaddeo'", 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'mega.menu': {
            'Meta': {'object_name': 'Menu'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rede': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mega.Rede']", 'symmetrical': 'False'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'B'", 'max_length': '1'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.parceiro': {
            'Meta': {'object_name': 'Parceiro'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['mega.Category']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'home': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'is_name': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.plano': {
            'Meta': {'object_name': 'Plano'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'valor': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.question': {
            'Meta': {'object_name': 'Question'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'text': ('ckeditor.fields.RichTextField', [], {}),
            'treinamento': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Treinamento']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.quiz': {
            'Meta': {'object_name': 'Quiz'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email_respon': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_question': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Lista de Perguntas'", 'symmetrical': 'False', 'to': "orm['mega.Question']"}),
            'list_response': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'Lista de Respostas'", 'symmetrical': 'False', 'to': "orm['mega.Response']"}),
            'porcent': ('django.db.models.fields.IntegerField', [], {'default': '100'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'responsavel': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'treinamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"})
        },
        'mega.rede': {
            'Meta': {'object_name': 'Rede'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_send': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'resend': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.relatorioacoes': {
            'Meta': {'object_name': 'RelatorioAcoes'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'play': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"})
        },
        'mega.relatorioavalicao': {
            'Meta': {'object_name': 'RelatorioAvalicao'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pontos': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Quiz']", 'null': 'True', 'blank': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mega.relatoriotentativa': {
            'Meta': {'object_name': 'RelatorioTentativa'},
            'aprovado': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_init': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'treinamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mega.response': {
            'Meta': {'object_name': 'Response'},
            'correta': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Question']"}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'mega.suggestion': {
            'Meta': {'object_name': 'Suggestion'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_send': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'enviado': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mensagem': ('django.db.models.fields.TextField', [], {}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'treinamento': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'mega.template': {
            'Meta': {'object_name': 'Template'},
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
            'cor37': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor38': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor4': ('colors.fields.ColorField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'cor5': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor6': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'cor7': ('colors.fields.ColorField', [], {'default': "'ffffff'", 'max_length': '7', 'blank': 'True'}),
            'custom': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'font1': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'font2': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'font3': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'font4': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'font_gle': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'title_d': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_ds': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title_pd': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.tipotemplate': {
            'Meta': {'object_name': 'TipoTemplate'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mega.transation': {
            'Meta': {'object_name': 'Transation'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plano': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Plano']"}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.treinamento': {
            'Meta': {'object_name': 'Treinamento'},
            'agendado': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Category']"}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('ckeditor.fields.RichTextField', [], {}),
            'destaq': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'plano': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Plano']", 'null': 'True', 'blank': 'True'}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mega.Rede']"}),
            'required': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'required_rel_+'", 'null': 'True', 'to': "orm['mega.Treinamento']"}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tipo': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'})
        },
        'mega.webchat': {
            'Meta': {'object_name': 'WebChat'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Treinamento']"}),
            'rede': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mega.Rede']"}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_lido': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'Usu\\xc3\\xa1rios que j\\xc3\\xa1 leram'", 'blank': 'True', 'to': "orm['auth.User']"})
        },
        'state.city': {
            'Meta': {'object_name': 'City'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['state.State']"})
        },
        'state.state': {
            'Meta': {'object_name': 'State'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'uf': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }
    
    complete_apps = ['mega']
