from django.db import models
import datetime
from megavideo.common import link_reduction
from django.conf import settings

class LinkReduced(models.Model):
    original_url = models.TextField(default = '')
    submitting_ip = models.TextField(default = '')
    date = models.DateTimeField(default = datetime.datetime.now)
    comment = models.TextField(default = '')

    def link(self):
        base = settings.MEGAVIDEO_CONF['base_url']
        url = base + 'l/' + link_reduction.encode(self.id)
        return url

class LinkClicked(models.Model):
    link = models.ForeignKey(LinkReduced)
    clicking_ip = models.TextField(default = '')
    date = models.DateTimeField(default = datetime.datetime.now)
    referer = models.TextField(default = '')
