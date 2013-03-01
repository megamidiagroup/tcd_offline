#-*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _


class State(models.Model):

    name = models.CharField(_('name'), max_length=30)
    uf = models.CharField(_('UF'), max_length=2)

    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')
        ordering = ['name']

    def __unicode__(self):
        return self.name


class City(models.Model):

    state = models.ForeignKey(State, verbose_name=_('state'))
    name = models.CharField(_('name'), max_length=255)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')
        ordering = ['name']

    def __unicode__(self):
        return self.name
