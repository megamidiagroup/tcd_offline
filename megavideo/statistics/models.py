# -*- coding: utf8 -*-
from django.db import models
from megavideo.video.models import *

if hasattr(settings, 'GEOIP_PATH'):
    from django.contrib.gis.utils import GeoIP
    geo = GeoIP()


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


class VisitorUrl(models.Model):
    url = models.CharField(max_length=255 , null=True, blank=True)

    def __unicode__(self):
        return self.url


class VisitorDomain(models.Model):
    domain = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.domain

    class Meta:
        ordering = ['-id']


class VisitorDownload(models.Model):
    video = models.ForeignKey(Video)
    transcode = models.ForeignKey(Transcode, blank=True, null=True)
    channel = models.ForeignKey(Channel)
    size = models.IntegerField(default=0)
    start_time = models.FloatField(default=0)
    total_time = models.FloatField(default=0)
    visitor = models.ForeignKey('Visitor', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']


class VisitorLog(models.Model):
    visitor = models.ForeignKey("Visitor")
    action = models.ForeignKey(VisitorAction)
    video = models.ForeignKey(Video)
    seek_video = models.FloatField(null=True, blank=True, default=0)
    event_time = models.DateTimeField(auto_now_add=True)
    domain = models.ForeignKey(VisitorDomain, null=True)
    channel = models.ForeignKey(Channel, default=1)
    url = models.ForeignKey(VisitorUrl, null=True)
#    domain_url = models.CharField(max_length=128, default='') #migrate value

    def __unicode__(self):
        return   "Visitor: " + str(self.visitor.pk)

    class Meta:
        ordering = ['-id']


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
    country = models.ForeignKey(LocationCountry, null=True)
    city = models.ForeignKey(LocationCity, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    counter = models.IntegerField(default=1)
#    nb = models.IntegerField(default=1) #migrate rename field
#    country_code = models.CharField(max_length=4) #migrate
#    country_name = models.CharField(max_length=128, default='Não localizada') #migrate
#    city_name = models.CharField(max_length=256, default='Não localizada') #migrate

    class Meta:
        ordering = ['-id']


class VisitorAgent(models.Model):
    agent = models.CharField(max_length=255)

    def __unicode__(self):
        return self.agent


class VisitorIp(models.Model):
    ip = models.CharField(max_length=255)

    def __unicode__(self):
        return self.ip



class LocationRegion(models.Model):
    code = models.CharField(max_length=10, null=True, blank=True)
    region = models.CharField(max_length=10, null=True, blank=True)
    state_name = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.state_name


class Visitor(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, null=True, blank=True)
    agent = models.ForeignKey(VisitorAgent, null=True, blank=True)
    ip = models.ForeignKey(VisitorIp, null=True, blank=True)
    region = models.ForeignKey(LocationRegion, null=True, blank=True)
#    ip_old = models.CharField(max_length=128) #migrate
#    agent_old = models.CharField(max_length=255) #migrate

    def __unicode__(self):
        return " Visitor:" + str(self.location)


    def geo_register(self):
        try:
            data = geo.city(self.ip.ip)
        except:
            data = None
        _code = ''
        _region = ''

        if data:
            if not self.region:

                if 'country_code' in data:
                    _code = data['country_code']

                if 'region' in data:
                    _region = data['region']

                _location = LocationRegion.objects.using('megavideo').filter(region=_region, code=_code)

                if _location:
                    print 'GEO REGISTRED '
                    self.region = _location[0]

                self.save(using='megavideo')
                return (self.id , self.region)

            else:

                return self.region
        else:
            print 'GEO ERROR - NO CITY OBJECT'


    class Meta:
        ordering = ['-id']



