# -*- coding: utf8 -*-
from django.db import models
from datetime import datetime
from megavideo.video.models import *

#Downloaded Item, Important for billing.
class VisitorDownload(models.Model):
    video = models.ForeignKey(Video)
    transcode = models.ForeignKey(Transcode, blank=True, null=True)
    channel = models.ForeignKey(Channel)
    size = models.IntegerField(default=0)
    start_time = models.FloatField(default=0)
    total_time = models.FloatField(default=0)
    visitor = models.ForeignKey('Visitor', blank=True, null=True)
    time = models.DateTimeField(default=datetime.datetime.now)


class VisitorAction(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class VisitorDomain(models.Model):
    domain = models.CharField(max_length=128)

    def __unicode__(self):
        return   self.domain


class VisitorLog(models.Model):
    visitor = models.ForeignKey("Visitor")
    video = models.ForeignKey(Video)
    action = models.ForeignKey(VisitorAction)
    seek_video = models.FloatField()
    event_time = models.DateTimeField(auto_now=True)
    domain = models.ForeignKey(VisitorDomain, null=True)
    channel = models.ForeignKey(Channel, default=1)
    domain_url = models.CharField(max_length=128, default='')
#   domain      = models.CharField(max_length = 128, default = '')

    def __unicode__(self):
        return   "Visitor: " + str(self.visitor.pk)


class Location(models.Model):
    country_code = models.CharField(max_length=4)
    country_name = models.CharField(max_length=128, default='Não localizada')
    city_name = models.CharField(max_length=256, default='Não localizada')
    latitude = models.FloatField()
    longitude = models.FloatField()
    nb = models.IntegerField(default=1)


class Visitor(models.Model):
#    videos = models.ManyToManyField(Video)
    cookie = models.CharField(max_length=256)
    ip = models.CharField(max_length=128)
    start_time = models.DateTimeField(auto_now=True) #new field 02/06/2009
    location = models.ForeignKey(Location, null=True)
    agent = models.CharField(max_length=255) #new field 02/06/2009


    def __unicode__(self):
        return " Visitor:" + str(self.location)

class StatisticForm(models.Model):
    # modelo para salvar campos na base do user
    value = models.TextField()
    visitor = models.ForeignKey("Visitor")
