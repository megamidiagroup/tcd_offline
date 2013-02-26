# -*- coding: utf8 -*-
from django.db import models
from megavideo.video.models import *

class VisitorAction(models.Model):
#    +----+--------+
#    | id | name   |
#    +----+--------+
#    |  1 | play   | 
#    |  2 | pause  | 
#    |  3 | seek   | 
#    |  4 | end    | 
#    |  5 | rewind | 
#    |  6 | select | 
#    |  7 | click  | 
#    +----+--------+
    CHOICES = (
        ('play', 'play'),
        ('pause', 'pause'),
        ('seek', 'seek'),
        ('end', 'end'),
        ('rewind', 'rewind'),
        ('select', 'select'),
        ('click', 'click'),
    )

    name = models.CharField(max_length=10, choices=CHOICES)

    def __unicode__(self):
        return self.name


class VisitorDomain(models.Model):
    domain = models.CharField(max_length=255, null=True, blank=True)
    url = models.CharField(max_length=255 , null=True, blank=True)

    def __unicode__(self):
        return   self.domain


class VisitorDownload(models.Model):
    video = models.ForeignKey(Video)
    transcode = models.ForeignKey(Transcode, blank=True, null=True)
    channel = models.ForeignKey(Channel)
    size = models.IntegerField(default=0)
    start_time = models.FloatField(default=0)
    total_time = models.FloatField(default=0)
    visitor = models.ForeignKey('Visitor', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)


class VisitorLog(models.Model):
    visitor = models.ForeignKey("Visitor")
    action = models.ForeignKey(VisitorAction)
    video = models.ForeignKey(Video)
    seek_video = models.FloatField(null=True, blank=True, default=0)
    event_time = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(VisitorDomain, null=True)
    channel = models.ForeignKey(Channel, default=1)
    domain_url = models.CharField(max_length=128, default='') #migrate value

    def __unicode__(self):
        return   "Visitor: " + str(self.visitor.pk)


class LocationCountry(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=128, default='Não localizada')

    def __unicode__(self):
        return self.name


class LocationCity(models.Model):
    name = models.CharField(max_length=256, default='Não localizada')

    def __unicode__(self):
        return self.name


class Location(models.Model):
    county = models.ForeignKey(LocationCountry, null=True)
    city = models.ForeignKey(LocationCity, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    counter = models.IntegerField(default=1)
    nb = models.IntegerField(default=1) #migrate
    country_code = models.CharField(max_length=4) #migrate
    country_name = models.CharField(max_length=128, default='Não localizada') #migrate
    city_name = models.CharField(max_length=256, default='Não localizada') #migrate


class VisitorAgent(models.Model):
    agent = models.CharField(max_length=255)

    def __unicode__(self):
        return self.agent


class VisitorIp(models.Model):
    ip = models.CharField(max_length=128)

    def __unicode__(self):
        return self.ip


class Visitor(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, null=True)
    agents = models.ForeignKey(VisitorAgent, null=True)
    ips = models.ForeignKey(VisitorIp, null=True)
    ip = models.CharField(max_length=128) #migrate
    agent = models.CharField(max_length=255) #migrate

    def __unicode__(self):
        return " Visitor:" + str(self.location)
