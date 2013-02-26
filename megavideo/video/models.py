# -*- coding: utf8 -*-

from django.conf import settings
from django.db import connection, backend, models

#from megavideo.common.create_url import get_thumb_url
from django.template.defaultfilters import slugify
#from megavideo.common.channel import get_url_prefix
import datetime, pickle, base64

from tagging.fields import TagField
from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

from django.db.models import Sum

from django.contrib.auth.models import User , Group
from django.db.models.signals import post_save
import django.dispatch
from megavideo.templatetags.miniature import thumbnail
from megavideo.templatetags.embeds import video_embed
import os
import time
from django.template.loader import render_to_string

from megavideo.templatetags.humanize_megas import humanize_bytes
from django.utils.html import strip_tags
import re


def percent_calc(total, value):

    per = '%.2f' % (float((float(total)) / float(value)) * 100)

    return per


def convert_GB_to_Bytes(value):
    value = value.replace('GB', '')
    return (int(value) * (1024 ** 3))


#split space and trim
import shlex
import math
import unicodedata


def usercreation(sender, instance, **kwargs):

    try:
        instance.get_profile()
    except:
        up = UserProfile()
        up.user = instance
        # ver up.save(using='megavideo')

post_save.connect(usercreation, sender=User)

#Migration 003
class TypeVideoFeatured(models.Model):
   _option = (('v', 'video destaque') , ('c', 'categoria destaque'))
   name = models.CharField(max_length=25, choices=_option)

   def __unicode__(self):
       return self.name

   class Meta:
       ordering = ['name']


#Migration 003
class VideoFeatured(models.Model):
   video = models.ForeignKey('Video', null=True, blank=True)
   category = models.ForeignKey('Category', null=True , blank=True)
   theme = models.ForeignKey('Category', null=True , blank=True, related_name="themefeature_set")
   channel = models.ForeignKey('Channel', null=True , blank=True)
   date = models.DateTimeField(auto_now_add=True)
   #new field
   typevideofeatured = models.ForeignKey('TypeVideoFeatured', null=True, blank=True)

   class Meta:
       ordering = ['-id']


#Publicity Model
class Publicity(models.Model):
    name = models.TextField()#nome randomico da imagem com extensao
    title = models.TextField()#titulo somente para manager
    video = models.ForeignKey('Video')#referencia a tabela de video
    date = models.DateTimeField(auto_now_add=True)#data
    time = models.FloatField(default=0)#tempo de entrada do banner
    timeout = models.FloatField(default=0)#tempo de banner presente na tela
    posx = models.FloatField(default=0)#posicao x do banner
    posy = models.FloatField(default=0)#posicao y do banner
    rotation = models.FloatField(default=0)#rotacao do banner em graus
    scale = models.FloatField(default=1)#escala para zoom
    link = models.TextField()#link que quando clicar abrir uma pagina _blanck
    published = models.IntegerField(null=True, blank=True, default=False)#referencia de publicacao

    class Meta:
        ordering = ['-date']


#Question Model
class Question(models.Model):
    question_text = models.TextField()# pergunta
    response = models.ManyToManyField('ResponseIntoQuestion')
    video = models.ForeignKey('Video')# referencia a tabela de video
    date = models.DateTimeField(auto_now_add=True)# data
    published = models.IntegerField(null=True, blank=True, default=False)# referencia de publicacao

    def set_response(self, text, video_id=0, correct=False):
        q = self
        q.save(using='megavideo')
        riq = ResponseIntoQuestion()
        riq.video_id = video_id
        riq.correct = correct
        riq.response_text = text
        riq.save(using='megavideo')
        q.response.add(riq)

    class Meta:
        ordering = ['-date']


#ResponseIntoQuestion Model
class ResponseIntoQuestion(models.Model):
    response_text = models.TextField()# resposta
    correct = models.IntegerField(null=True, blank=True, default=False)# correta a resposta?
    video = models.ForeignKey("Video")

    class Meta:
        ordering = ['response_text']


class VideoRoll(models.Model):
    title = models.TextField()#titulo somente para manager
    video = models.ForeignKey("Video", related_name='rolls')
    roll = models.ForeignKey("Video", related_name='videos_roll_from')
    position = models.FloatField(default=0)
    published = models.IntegerField(null=True, blank=True, default=False)#referencia de publicacao


class Category(models.Model):
    channel = models.ForeignKey('Channel')
    parent = models.ForeignKey('self', null=True, blank=True)
    sequence = models.IntegerField(null=True, blank=True, default=0)
    name = models.TextField()
    published = models.IntegerField(null=True, blank=True, default=False)
    description = models.TextField(default='')
    image = models.ImageField(upload_to='category', max_length=1000, blank=True, null=True)
    #document = models.FileField(upload_to= 'upload_to', max_length=1000, blank = True, null = True)
    date = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.name

    def is_parent(self):
        if not self.parent:
            return True
        return False

    def count_video_published(self):
        return self.video_set.filter(published=True).count()

    def get_subcategory(self):
        return self.category_set.filter(published=True)

    def get_video(self):
        return self.video_set.filter(published=True)

    class Meta:
        ordering = ['sequence']


#class new tabel
class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    image = models.ImageField(upload_to='upload_images', max_length=1000, blank=True, null=True)

User.profile = property(lambda u: UserProfile.objects.using('megavideo').get_or_create(user=u)[0])


#FIXME new table
class UserChannel(models.Model):
    user = models.ForeignKey(User)
    channel = models.ForeignKey('Channel')


#class ChannelType(models.Model):
#    name = models.CharField(max_length = 255 , blank = True , null = True)
#    description = models.TextField()
#
#    def __unicode__(self):
#        return self.name

class Tv(models.Model):
    name = models.TextField()
    description = models.TextField()

class Channel(models.Model):
    name = models.TextField()
    description = models.TextField()
    video = models.ManyToManyField('Video')
    tv = models.ForeignKey('Tv', default=1)

    #FIXME
    image = models.ImageField(upload_to='upload_images', max_length=1000, blank=True, null=True) #new field

    #channeltype = models.ForeignKey('ChannelType')
    title = models.CharField(max_length=255, blank=True, null=True)

    if hasattr(settings, 'VFLOW_PLAN'):
        download_limit = convert_GB_to_Bytes(settings.VFLOW_PLAN['basico']['data'])
        bandwidth_limit = convert_GB_to_Bytes(settings.VFLOW_PLAN['basico']['transfer'])


    def __unicode__(self):
        return self.name


    def count_video(self):
        return self.video.all().count()


    def count_video_published(self):
        return self.video.filter(published=True).count()


    def get_download_limit(self):
        return self.download_limit


    def get_bandwidth_limit(self):
        return self.bandwidth_limit


    def get_bandwidth_month(self, month=datetime.datetime.now().month , year=datetime.datetime.now().year):
        from megavideo.statistics.models import VisitorDownload
        soma = sum(i.size for i in VisitorDownload.objects.using('megavideo').filter(video__channel__id=self.id, time__gte='%s-%s-01' % (year, month)).distinct())
        return soma


    def get_bandwidth_total(self):
        soma = sum([i.size + sum(j.size for j in i.videotranscode_set.all()) for i in Video.objects.using('megavideo').filter(channel=self)])
        return soma


    def get_download_total_percent(self):
        total = self.get_bandwidth_total()
        try:
            limit = self.download_limit
        except:
            return 0

        print 'get_download_total_percent '
        print 'total ', total
        print 'limit ', limit
        print 'percent ' , percent_calc(total, limit)

        return percent_calc(total, limit)


    def get_bandwidth_month_percent(self, month=datetime.datetime.now().month):
        total = self.get_bandwidth_month(month)
        try:
            limit = self.bandwidth_limit
        except:
            return 0

        print 'get_bandwidth_month_percent '
        print 'total ', total
        print 'limit ', limit
        print 'percent ' , percent_calc(total, limit)

        return percent_calc(total, limit)


class Metaclass(models.Model):
    name = models.TextField()
    validate = models.TextField()


#class Statistic(models.Model):
#    name = models.TextField()
#    description = models.TextField()

class Transcode(models.Model):
    name = models.TextField()

#class Tv(models.Model):
#    name = models.TextField()
#    description = models.TextField()

class VideoTag(models.Model):
    video = models.ForeignKey('Video')
    tags = TagField(blank=True)
    initime = models.FloatField(default=0)
    endtime = models.FloatField(default=0)

    def get_tags(self):
        return Tag.objects.using('megavideo').get_for_object(self)

    def get_cloud(self, max_size=6):
        return Tag.objects.using('megavideo').cloud_for_model(self, max_size)

    def set_tags(self, tag_list):
        Tag.objects.using('megavideo').update_tags(self, tag_list)

    class Meta:
        ordering = ['initime']


class ContentFile(models.Model):
    server = models.CharField(max_length=256, default='localhost')
    name = models.TextField()
    dir = models.TextField()
    original_name = models.TextField()
    size = models.IntegerField(default=0)


class ContentPart(models.Model):
    video = models.ForeignKey('Video')
    content_file = models.ForeignKey(ContentFile)
    part = models.IntegerField(default=1)
    offset = models.IntegerField(default=0)


def get_image_path(instance, filename):
    #filename = "_%s_%s" % (instance.id, slugify(str(time.time())))
    dirname = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = '_' + slugify(str(time.time()))
    print 'WHITE FILE -----------------------------------'
    print 'id ' , instance.id
    print 'dirname ' , dirname
    print 'filename ' , filename
    print '----------------------------------- WHITE FILE'
    return os.path.join(settings.MEGAVIDEO_CONF['video_storage'], dirname , filename)


class Video(models.Model):
    name = models.TextField()
    dir = models.TextField()
    videoclass = models.ForeignKey('Videoclass')
    status = models.CharField(max_length=24)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField()
    width = models.IntegerField()
    height = models.IntegerField()
    displayname = models.TextField()
    published = models.IntegerField()
    views = models.IntegerField()
    ratesum = models.IntegerField()
    ratenum = models.IntegerField()
    category = models.ManyToManyField(Category, through='Videocategory')
    size = models.IntegerField(default=0)
    total_size = models.IntegerField(default=0) #sum with vtranscodes
    #migration
    description = models.TextField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    #User
    user = models.ForeignKey(User, null=True, blank=True, default=1)

    #new filename
    #filename = models.FileField(upload_to = get_image_path)

    def serialize(self, id=0):
        if id == 0:
            id = self.id
    	key = base64.b64encode( str(id) )
    	return '_%s%s' % ( key[0:2], key )

    def deserialize(self, key=''):
    	if key[0] == '_':
    	    return int( base64.b64decode( key[3:] ) )
    	return int( base64.b64decode( key[2:] ) )

    def get_original_file(self):
        dirname = self.dir
        filename = os.path.join(settings.MEGAVIDEO_CONF['video_storage'] , dirname , '_' + self.name)

        try:
            original_name = self.job_set.all()[0].original_name
        except:
            original_name = 'undefined'

        self.realpath = filename
        self.original_name = original_name
        self.dirname = settings.MEGAVIDEO_CONF['video_storage'] + dirname

        return self


    def get_thumbnail(self, size="100x100"):
        return thumbnail(self, size)

    def get_last_five_comment(self):
        return self.videocomment_set.all().order_by('-id')[0:5]

    def get_channel(self):
        r = ''
        for i in self.channel_set.all():
            r += i.name + ', '
        r = r[0:-2]

        return r

    def get_channel_title(self):
        r = ''
        for i in self.channel_set.all():
            r += i.title + ', '
        r = r[0:-2]
        return r

    def get_contentpart(self):
        content = self.contentpart_set.get().content_file.contentpart_set.all().order_by('part')
        if content.count() > 1:
            return content
        return []

    def set_tag(self, value, initime=0, endtime=0):
        v = VideoTag()
        v.video = self
        v.tags = value
        v.initime = initime
        v.endtime = endtime
        v.save(using='megavideo')

    def get_tag_list(self):
        try:
            return [Tag.objects.using('megavideo').get_for_object(i) for i in self.videotag_set.all()]
        except:
            return []


    def b64id(self):
        import base64
        return base64.b64encode(str(self.id))

    def get_meta_keys (self):
        vc = self.videoclass
        return [i.metaclass.name for i in vc.videometaclass_set.all()]

    def set_meta(self, name, value):
        try:
            vm = self.videometa_set.filter(metaclass__name=name)[0]
        except:
            try:
                mc = Metaclass.objects.using('megavideo').filter(videometaclass__videoclass__video=self, name=name)[0]
                vm = VideoMeta()
                vm.metaclass = mc
                vm.value = value
                vm.video = self
                vm.save(using='megavideo')
            except:
                pass

        if name == 'title':
            if hasattr(self, 'title'):
                self.title = value
                self.save(using='megavideo')

        elif name == 'description':
            if hasattr(self, 'description'):
                self.description = value
                self.save(using='megavideo')


    def find_meta(self, metaname):
        try:
            return self.videometa_set.select_related().filter(metaclass__name=metaname)[0].value
        except:
            return 'No Data'

    def get_meta(self, metaname):
        if metaname == 'name':
           if hasattr(self, 'title'):
               if not self.title:
                   try:
                       self.title = self.find_meta(metaname)
                       self.save(using='megavideo')
                   except:
                       pass
               else:
                   return self.title

        if metaname == 'description':
            if hasattr(self, 'description'):
                if not self.description:
                    try:
                        self.description = self.find_meta(metaname)
                        self.save(using='megavideo')
                    except:
                        pass
                else:
                    return self.description

        return self.find_meta(metaname)

    def __unicode__(self):
        return self.get_meta('name')

    def get_category(self):
        if self.category.all().count():
                return self.category.all()[0].id
        return False

    def get_category_name(self):
        if self.category.all().count():
                return self.category.all()[0].name
        return False

    def get_document(self):
        try:
            return self.document_set.all()[0].filename
        except:
            return False

    def get_num_comment(self):
        return self.videocomment_set.filter(published=True).count()

    def get_transcode(self):
        return [i.transcode.name for i in self.videotranscode_set.all()]

    def get_vote(self):
        if self.ratenum == 0:
            return 0
        else:
            return self.ratesum / self.ratenum

    def get_thumb(self):
        return self.videothumb_set.all()[0]

    def get_all_thumb(self):
        return self.videothumb_set.all()

    def get_thumb_url(self):
        try:
            th = self.videothumb_set.all()[0]
        except:
            return settings.MEDIA_STATIC + 'megavideo/static/manager/images/processando.jpg'
        return get_thumb_url(th)

    def get_name(self):
        if not self.title or self.title == '' or slugify( self.title ) == u'no-data' or self.title == None:
    	    try:
    	        return slugify( self.job_set.all()[0].original_name )
    	    except:
                pass
        return self.title

    def get_title(self):
        if not self.title or self.title == '' or slugify( self.title ) == u'no-data' or self.title == None:
            try:
                return slugify( self.job_set.all()[0].original_name )
            except:
                pass
        return self.title

    def get_author(self):
        name = self.get_meta('author')
        return name

    def get_description(self):
        description = self.description
        return description

    def is_wide(self):
        if not self.height :
            return False
        if ((self.width + 0.0) / (self.height + 0.0)) > 1.4:
            return ((self.width + 0.0) / (self.height + 0.0))
        else:
            return False

    def get_embed(self, width=640, height=360):
        return '<script type="text/javascript" src="%sapi/video/embed.js?idContent=%s&width=%s&height=%s"></script>' % (settings.MEGAVIDEO_CONF['base_url'], self.serialize(self.id), width, height) 

    def tv_url(self):
        return settings.MEGAVIDEO_CONF['base_url'] + 'api/video/embed.js?idContent=' + self.serialize(self.id) + '&render_to_html=true'

    def last_videos(self):
        videos = self.objects.using('megavideo').filter(published=True).filter(category__isnull=False).filter(date__lte=datetime.datetime.now()).order_by('-date')[:15]
        return videos

    def get_video_url(self, urlvideo='video'):
        path = os.path.join('/', self.dir, self.name)
        path = settings.MEGAVIDEO_CONF['base_url'] + 'video/' + path
        return path

    #Statistics
    def get_log_play(self):
        return self.visitorlog_set.all().filter(action__name='play').count()

    def get_log_pause(self):
        return self.visitorlog_set.all().filter(action__name='pause').count()

    def get_log_stop(self):
        return self.visitorlog_set.all().filter(action__name='stop').count()

    def get_log_embed(self, base_url=''):
        return self.visitorlog_set.all().exclude(domain__contains=base_url , domain='null').count()

    def get_log_comment(self):
        return self.videocomment_set.filter(published=True).count()

    class Meta:
        ordering = ['-date']


class Videocategory(models.Model):
    video = models.ForeignKey(Video)
    category = models.ForeignKey(Category)
    sequence = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['sequence']

    def __unicode__(self):
        return "%s - %s - %s" % (self.video.name, self.category.name, self.sequence)

VideoCategory = Videocategory

class Videoclass(models.Model):
    name = models.TextField()
    displayname = models.TextField()
    metatitle = models.TextField()

VideoClass = Videoclass

class Videocomment(models.Model):
    video = models.ForeignKey(Video)
    name = models.TextField()
    email = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    published = models.IntegerField(null=True, blank=True, default=True)

VideoComment = Videocomment

class Videometa(models.Model):
    video = models.ForeignKey(Video)
    metaclass = models.ForeignKey(Metaclass)
    value = models.TextField()

VideoMeta = Videometa

class Videometaclass(models.Model):
    videoclass = models.ForeignKey(Videoclass)
    metaclass = models.ForeignKey(Metaclass)
    displayname = models.TextField()
    sequence = models.IntegerField()

VideoMetaclass = Videometaclass

Videothumb_sizes = (('XS', 'ExtraSmall'),
        ('XSW', 'ExtraSmallWide'),
        ('SW', 'SmallWide'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('MW', 'MediumWide'),
        ('L', 'Large'),
        ('LW', 'LargeWide'),
        ('XL', 'ExtraLarge'),
        ('XLW', 'ExtraLargeWide'))

class Videothumb(models.Model):
    video = models.ForeignKey(Video)
    name = models.TextField()
    size = models.CharField(choices=Videothumb_sizes, default='M', max_length=3)
    position = models.FloatField()
    height = models.IntegerField()
    width = models.IntegerField()

VideoThumb = Videothumb

class Videotranscode(models.Model):
    video = models.ForeignKey(Video)
    transcode = models.ForeignKey(Transcode)
    name = models.TextField()
    size = models.IntegerField(default=0)

VideoTranscode = Videotranscode

job_choices = (('A', 'Active'),
        ('C', 'Canceled'),
        ('E', 'Error'),
        ('F', 'Finished'))

class Job(models.Model):
    video = models.ForeignKey(Video, null=True)
    channel = models.ForeignKey(Channel, null=True)
    status = models.CharField(max_length=4, choices=job_choices)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    ip = models.CharField(max_length=128)
    pid = models.IntegerField(default= -1)
    original_name = models.CharField(max_length=256, default='no_name')

    class Meta:
        ordering = ['-date']

job_log_choices = (
        ('D', 'Debug'),
        ('W', 'Warning'),
        ('E', 'Error'),
        )

class JobLog(models.Model):
    job = models.ForeignKey(Job)
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    vars = models.TextField(default='')
    level = models.CharField(max_length=3, choices=job_log_choices, default='D')

    def show_arguments(self):
        largs = self.vars
        try:
            largs = pickle.loads(base64.b64decode(largs))
        except StandardError, e:
            pass
        return str(largs)

    class Meta:
        ordering = ['-id']


class VideoVote(models.Model):
    video = models.ForeignKey(Video)
    ip = models.CharField(max_length=128)
    agent = models.CharField(max_length=128)
    vote = models.IntegerField(default=0)
    #FIXME
    #date = models.DateTimeField(default = datetime.datetime.now) #new field

class DocumentClass(models.Model):
      name = models.CharField(max_length=32)


class Document(models.Model):
     documentclass = models.ForeignKey(DocumentClass)
     video = models.ForeignKey(Video)
     filename = models.FileField(upload_to='upload_to', max_length=1000, blank=True, null=True)


class JobDispatch(models.Model):
    job = models.ForeignKey(Job)
    tvname = models.TextField(default='')
    start = models.DateTimeField(auto_now_add=True)
    dispatch_path = models.TextField(default='')
    commands_serialized = models.TextField(default='')
    user = models.TextField(default='www-data')

    def run(self):
        import subprocess
        import pwd
        import os

        args = [self.dispatch_path, self.tvname, self.commands_serialized, '--no-change-user']

        #activate job
        job = self.job

        if self.job.status != 'Q':
            LOGGER.debug('JD %d : Not in queue, abandon running' % self.id)
            return False

        job.status = 'A'
        job.save(using='megavideo')

        p = subprocess.Popen(args, cwd='/tmp/', close_fds=True)

        fd = open('/tmp/last_insert_' + settings.MEGAVIDEO_CONF['tv_name'], 'w')
        for i in args:
            fd.write(str(i) + ' ')
        fd.close()

        p.wait()
        return True


class SearchRate(models.Model):
    channel = models.ForeignKey(Channel, null=True, blank=True)
    value = models.CharField(max_length=255, default='')
    rate = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def add(self, search, channel_id=0):
        se = search.replace(',', ' ')
        se = unicodedata.normalize('NFKD', se).encode('ascii', 'ignore').lower()
        se = shlex.split(se)

        for i in se:
            if not SearchRate.objects.using('megavideo').filter(value__iexact=i):
                self = SearchRate()
                self.value = i
                print 'add - ' , unicode(i)
            else:
                self = SearchRate.objects.using('megavideo').filter(value__iexact=i)[0]
                print 'rate - ' , unicode(i)

            self.rate += 1

            if int(channel_id):
                self.channel_id = channel_id

            self.save(using='megavideo')


    def get_cloud(self, channel_name=0 , steps=4, limit=10):

        if channel_name:
            tags = SearchRate.objects.using('megavideo').filter(channel__name=channel_name).order_by('-rate')[0:limit]
        else:
            tags = SearchRate.objects.using('megavideo').all().order_by('-rate')[0:limit]

        if tags.count():
            counts = [i.rate for i in tags]
            min_weight = float(min(counts))
            max_weight = float(max(counts))
            thresholds = _calculate_thresholds(min_weight, max_weight, steps)
            for tag in tags:
                font_set = False
                tag_weight = _calculate_tag_weight(tag.rate, max_weight, LOGARITHMIC)
                for i in range(steps):
                    if not font_set and tag_weight <= thresholds[i]:
                        tag.font_size = i + 1
                        font_set = True

        return tags


    def __unicode__(self):
        return self.value


#get tags
LOGARITHMIC, LINEAR = 1, 2

def _calculate_thresholds(min_weight, max_weight, steps):
    delta = (max_weight - min_weight) / float(steps)
    return [min_weight + i * delta for i in range(1, steps + 1)]


def _calculate_tag_weight(weight, max_weight, distribution=LOGARITHMIC):
    """
    Logarithmic tag weight calculation is based on code from the
    `Tag Cloud`_ plugin for Mephisto, by Sven Fuchs.

    .. _`Tag Cloud`: http://www.artweb-design.de/projects/mephisto-plugin-tag-cloud
    """
    if distribution == LINEAR or max_weight == 1:
        return weight
    elif distribution == LOGARITHMIC:
        return math.log(weight) * max_weight / math.log(max_weight)
    raise ValueError(_('Invalid distribution algorithm specified: %s.') % distribution)
