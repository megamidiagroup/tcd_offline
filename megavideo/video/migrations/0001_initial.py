# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'TypeVideoFeatured'
        db.create_table('video_typevideofeatured', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
        ))
        db.send_create_signal('video', ['TypeVideoFeatured'])

        # Adding model 'VideoFeatured'
        db.create_table('video_videofeatured', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Category'], null=True, blank=True)),
            ('typevideofeatured', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.TypeVideoFeatured'], null=True, blank=True)),
            ('theme', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='themefeature_set', null=True, to=orm['video.Category'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Channel'], null=True, blank=True)),
        ))
        db.send_create_signal('video', ['VideoFeatured'])

        # Adding model 'Publicity'
        db.create_table('video_publicity', (
            ('scale', self.gf('django.db.models.fields.FloatField')(default=1)),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('posy', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('posx', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('timeout', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('time', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('link', self.gf('django.db.models.fields.TextField')()),
            ('rotation', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published', self.gf('django.db.models.fields.IntegerField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('video', ['Publicity'])

        # Adding model 'Question'
        db.create_table('video_question', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('question_text', self.gf('django.db.models.fields.TextField')()),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('published', self.gf('django.db.models.fields.IntegerField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('video', ['Question'])

        # Adding M2M table for field response on 'Question'
        db.create_table('video_question_response', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('question', models.ForeignKey(orm['video.question'], null=False)),
            ('responseintoquestion', models.ForeignKey(orm['video.responseintoquestion'], null=False))
        ))

        # Adding model 'ResponseIntoQuestion'
        db.create_table('video_responseintoquestion', (
            ('response_text', self.gf('django.db.models.fields.TextField')()),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('correct', self.gf('django.db.models.fields.IntegerField')(default=False, null=True, blank=True)),
        ))
        db.send_create_signal('video', ['ResponseIntoQuestion'])

        # Adding model 'VideoRoll'
        db.create_table('video_videoroll', (
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(related_name='rolls', to=orm['video.Video'])),
            ('published', self.gf('django.db.models.fields.IntegerField')(default=False, null=True, blank=True)),
            ('position', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('roll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='videos_roll_from', to=orm['video.Video'])),
        ))
        db.send_create_signal('video', ['VideoRoll'])

        # Adding model 'Category'
        db.create_table('video_category', (
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Category'], null=True, blank=True)),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.IntegerField')(default=False, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Channel'])),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('video', ['Category'])

        # Adding model 'UserProfile'
        db.create_table('video_userprofile', (
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal('video', ['UserProfile'])

        # Adding model 'UserChannel'
        db.create_table('video_userchannel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Channel'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('video', ['UserChannel'])

        # Adding model 'Tv'
        db.create_table('video_tv', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('video', ['Tv'])

        # Adding model 'Channel'
        db.create_table('video_channel', (
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('tv', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['video.Tv'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=1000, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('video', ['Channel'])

        # Adding M2M table for field video on 'Channel'
        db.create_table('video_channel_video', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('channel', models.ForeignKey(orm['video.channel'], null=False)),
            ('video', models.ForeignKey(orm['video.video'], null=False))
        ))

        # Adding model 'Metaclass'
        db.create_table('video_metaclass', (
            ('validate', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('video', ['Metaclass'])

        # Adding model 'Transcode'
        db.create_table('video_transcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('video', ['Transcode'])

        # Adding model 'VideoTag'
        db.create_table('video_videotag', (
            ('endtime', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('initime', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal('video', ['VideoTag'])

        # Adding model 'ContentFile'
        db.create_table('video_contentfile', (
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('original_name', self.gf('django.db.models.fields.TextField')()),
            ('server', self.gf('django.db.models.fields.CharField')(default='localhost', max_length=256)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dir', self.gf('django.db.models.fields.TextField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('video', ['ContentFile'])

        # Adding model 'ContentPart'
        db.create_table('video_contentpart', (
            ('content_file', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.ContentFile'])),
            ('part', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('offset', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('video', ['ContentPart'])

        # Adding model 'Video'
        db.create_table('video_video', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=24)),
            ('displayname', self.gf('django.db.models.fields.TextField')()),
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('total_size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('views', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('duration', self.gf('django.db.models.fields.FloatField')()),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User'], null=True, blank=True)),
            ('ratesum', self.gf('django.db.models.fields.IntegerField')()),
            ('published', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ratenum', self.gf('django.db.models.fields.IntegerField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('videoclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Videoclass'])),
            ('dir', self.gf('django.db.models.fields.TextField')()),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('video', ['Video'])

        # Adding model 'Videocategory'
        db.create_table('video_videocategory', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Category'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sequence', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('video', ['Videocategory'])

        # Adding model 'Videoclass'
        db.create_table('video_videoclass', (
            ('metatitle', self.gf('django.db.models.fields.TextField')()),
            ('displayname', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('video', ['Videoclass'])

        # Adding model 'Videocomment'
        db.create_table('video_videocomment', (
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('published', self.gf('django.db.models.fields.IntegerField')(default=True, null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('email', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('video', ['Videocomment'])

        # Adding model 'Videometa'
        db.create_table('video_videometa', (
            ('metaclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Metaclass'])),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('video', ['Videometa'])

        # Adding model 'Videometaclass'
        db.create_table('video_videometaclass', (
            ('displayname', self.gf('django.db.models.fields.TextField')()),
            ('sequence', self.gf('django.db.models.fields.IntegerField')()),
            ('metaclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Metaclass'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('videoclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Videoclass'])),
        ))
        db.send_create_signal('video', ['Videometaclass'])

        # Adding model 'Videothumb'
        db.create_table('video_videothumb', (
            ('name', self.gf('django.db.models.fields.TextField')()),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('position', self.gf('django.db.models.fields.FloatField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('size', self.gf('django.db.models.fields.CharField')(default='M', max_length=3)),
        ))
        db.send_create_signal('video', ['Videothumb'])

        # Adding model 'Videotranscode'
        db.create_table('video_videotranscode', (
            ('transcode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Transcode'])),
            ('size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('video', ['Videotranscode'])

        # Adding model 'Job'
        db.create_table('video_job', (
            ('status', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('original_name', self.gf('django.db.models.fields.CharField')(default='no_name', max_length=256)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pid', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'], null=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Channel'], null=True)),
        ))
        db.send_create_signal('video', ['Job'])

        # Adding model 'JobLog'
        db.create_table('video_joblog', (
            ('vars', self.gf('django.db.models.fields.TextField')(default='')),
            ('level', self.gf('django.db.models.fields.CharField')(default='D', max_length=3)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Job'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('video', ['JobLog'])

        # Adding model 'VideoVote'
        db.create_table('video_videovote', (
            ('vote', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('agent', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('video', ['VideoVote'])

        # Adding model 'DocumentClass'
        db.create_table('video_documentclass', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('video', ['DocumentClass'])

        # Adding model 'Document'
        db.create_table('video_document', (
            ('video', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Video'])),
            ('documentclass', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.DocumentClass'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.files.FileField')(max_length=1000, null=True, blank=True)),
        ))
        db.send_create_signal('video', ['Document'])

        # Adding model 'JobDispatch'
        db.create_table('video_jobdispatch', (
            ('commands_serialized', self.gf('django.db.models.fields.TextField')(default='')),
            ('dispatch_path', self.gf('django.db.models.fields.TextField')(default='')),
            ('start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Job'])),
            ('user', self.gf('django.db.models.fields.TextField')(default='www-data')),
            ('tvname', self.gf('django.db.models.fields.TextField')(default='')),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('video', ['JobDispatch'])

        # Adding model 'SearchRate'
        db.create_table('video_searchrate', (
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('rate', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('channel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['video.Channel'], null=True, blank=True)),
        ))
        db.send_create_signal('video', ['SearchRate'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'TypeVideoFeatured'
        db.delete_table('video_typevideofeatured')

        # Deleting model 'VideoFeatured'
        db.delete_table('video_videofeatured')

        # Deleting model 'Publicity'
        db.delete_table('video_publicity')

        # Deleting model 'Question'
        db.delete_table('video_question')

        # Removing M2M table for field response on 'Question'
        db.delete_table('video_question_response')

        # Deleting model 'ResponseIntoQuestion'
        db.delete_table('video_responseintoquestion')

        # Deleting model 'VideoRoll'
        db.delete_table('video_videoroll')

        # Deleting model 'Category'
        db.delete_table('video_category')

        # Deleting model 'UserProfile'
        db.delete_table('video_userprofile')

        # Deleting model 'UserChannel'
        db.delete_table('video_userchannel')

        # Deleting model 'Tv'
        db.delete_table('video_tv')

        # Deleting model 'Channel'
        db.delete_table('video_channel')

        # Removing M2M table for field video on 'Channel'
        db.delete_table('video_channel_video')

        # Deleting model 'Metaclass'
        db.delete_table('video_metaclass')

        # Deleting model 'Transcode'
        db.delete_table('video_transcode')

        # Deleting model 'VideoTag'
        db.delete_table('video_videotag')

        # Deleting model 'ContentFile'
        db.delete_table('video_contentfile')

        # Deleting model 'ContentPart'
        db.delete_table('video_contentpart')

        # Deleting model 'Video'
        db.delete_table('video_video')

        # Deleting model 'Videocategory'
        db.delete_table('video_videocategory')

        # Deleting model 'Videoclass'
        db.delete_table('video_videoclass')

        # Deleting model 'Videocomment'
        db.delete_table('video_videocomment')

        # Deleting model 'Videometa'
        db.delete_table('video_videometa')

        # Deleting model 'Videometaclass'
        db.delete_table('video_videometaclass')

        # Deleting model 'Videothumb'
        db.delete_table('video_videothumb')

        # Deleting model 'Videotranscode'
        db.delete_table('video_videotranscode')

        # Deleting model 'Job'
        db.delete_table('video_job')

        # Deleting model 'JobLog'
        db.delete_table('video_joblog')

        # Deleting model 'VideoVote'
        db.delete_table('video_videovote')

        # Deleting model 'DocumentClass'
        db.delete_table('video_documentclass')

        # Deleting model 'Document'
        db.delete_table('video_document')

        # Deleting model 'JobDispatch'
        db.delete_table('video_jobdispatch')

        # Deleting model 'SearchRate'
        db.delete_table('video_searchrate')
    
    
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
        'video.category': {
            'Meta': {'object_name': 'Category'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Channel']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Category']", 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.IntegerField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'video.channel': {
            'Meta': {'object_name': 'Channel'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'tv': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['video.Tv']"}),
            'video': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['video.Video']", 'symmetrical': 'False'})
        },
        'video.contentfile': {
            'Meta': {'object_name': 'ContentFile'},
            'dir': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'original_name': ('django.db.models.fields.TextField', [], {}),
            'server': ('django.db.models.fields.CharField', [], {'default': "'localhost'", 'max_length': '256'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'video.contentpart': {
            'Meta': {'object_name': 'ContentPart'},
            'content_file': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.ContentFile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offset': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'part': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.document': {
            'Meta': {'object_name': 'Document'},
            'documentclass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.DocumentClass']"}),
            'filename': ('django.db.models.fields.files.FileField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.documentclass': {
            'Meta': {'object_name': 'DocumentClass'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'video.job': {
            'Meta': {'object_name': 'Job'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Channel']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'original_name': ('django.db.models.fields.CharField', [], {'default': "'no_name'", 'max_length': '256'}),
            'pid': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']", 'null': 'True'})
        },
        'video.jobdispatch': {
            'Meta': {'object_name': 'JobDispatch'},
            'commands_serialized': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'dispatch_path': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Job']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tvname': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'user': ('django.db.models.fields.TextField', [], {'default': "'www-data'"})
        },
        'video.joblog': {
            'Meta': {'object_name': 'JobLog'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Job']"}),
            'level': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '3'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'vars': ('django.db.models.fields.TextField', [], {'default': "''"})
        },
        'video.metaclass': {
            'Meta': {'object_name': 'Metaclass'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'validate': ('django.db.models.fields.TextField', [], {})
        },
        'video.publicity': {
            'Meta': {'object_name': 'Publicity'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'posx': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'posy': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'published': ('django.db.models.fields.IntegerField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'rotation': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'scale': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'time': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'timeout': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.question': {
            'Meta': {'object_name': 'Question'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.IntegerField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'question_text': ('django.db.models.fields.TextField', [], {}),
            'response': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['video.ResponseIntoQuestion']", 'symmetrical': 'False'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.responseintoquestion': {
            'Meta': {'object_name': 'ResponseIntoQuestion'},
            'correct': ('django.db.models.fields.IntegerField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'response_text': ('django.db.models.fields.TextField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.searchrate': {
            'Meta': {'object_name': 'SearchRate'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Channel']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        },
        'video.transcode': {
            'Meta': {'object_name': 'Transcode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'video.tv': {
            'Meta': {'object_name': 'Tv'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'video.typevideofeatured': {
            'Meta': {'object_name': 'TypeVideoFeatured'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'video.userchannel': {
            'Meta': {'object_name': 'UserChannel'},
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Channel']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'video.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'video.video': {
            'Meta': {'object_name': 'Video'},
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['video.Category']", 'through': "orm['video.Videocategory']", 'symmetrical': 'False'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dir': ('django.db.models.fields.TextField', [], {}),
            'displayname': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.FloatField', [], {}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.IntegerField', [], {}),
            'ratenum': ('django.db.models.fields.IntegerField', [], {}),
            'ratesum': ('django.db.models.fields.IntegerField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'total_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'videoclass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Videoclass']"}),
            'views': ('django.db.models.fields.IntegerField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'video.videocategory': {
            'Meta': {'object_name': 'Videocategory'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Category']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sequence': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.videoclass': {
            'Meta': {'object_name': 'Videoclass'},
            'displayname': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metatitle': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.TextField', [], {})
        },
        'video.videocomment': {
            'Meta': {'object_name': 'Videocomment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'published': ('django.db.models.fields.IntegerField', [], {'default': 'True', 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.videofeatured': {
            'Meta': {'object_name': 'VideoFeatured'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Category']", 'null': 'True', 'blank': 'True'}),
            'channel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Channel']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'theme': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'themefeature_set'", 'null': 'True', 'to': "orm['video.Category']"}),
            'typevideofeatured': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.TypeVideoFeatured']", 'null': 'True', 'blank': 'True'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']", 'null': 'True', 'blank': 'True'})
        },
        'video.videometa': {
            'Meta': {'object_name': 'Videometa'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metaclass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Metaclass']"}),
            'value': ('django.db.models.fields.TextField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.videometaclass': {
            'Meta': {'object_name': 'Videometaclass'},
            'displayname': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metaclass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Metaclass']"}),
            'sequence': ('django.db.models.fields.IntegerField', [], {}),
            'videoclass': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Videoclass']"})
        },
        'video.videoroll': {
            'Meta': {'object_name': 'VideoRoll'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'published': ('django.db.models.fields.IntegerField', [], {'default': 'False', 'null': 'True', 'blank': 'True'}),
            'roll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos_roll_from'", 'to': "orm['video.Video']"}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rolls'", 'to': "orm['video.Video']"})
        },
        'video.videotag': {
            'Meta': {'object_name': 'VideoTag'},
            'endtime': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initime': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.videothumb': {
            'Meta': {'object_name': 'Videothumb'},
            'height': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'position': ('django.db.models.fields.FloatField', [], {}),
            'size': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '3'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        'video.videotranscode': {
            'Meta': {'object_name': 'Videotranscode'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'transcode': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Transcode']"}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"})
        },
        'video.videovote': {
            'Meta': {'object_name': 'VideoVote'},
            'agent': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['video.Video']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['video']
