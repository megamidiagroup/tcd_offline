#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf import settings

import os
import re
import base64

import simplejson as json

OFFLINE = getattr(settings, 'OFFLINE', False)


def check_is_tables(sql):
    
    for i in ['`auth_', '`captcha_', '`django_', '`mega_']:
        if sql.count(i) > 0:
            return True
    return False

    
def set_sql(*args):

    if OFFLINE:

        count = 0
        
        o = open('/var/log/mysql/mysql.log', 'r').read()
        for i in o.split('\n'):
            if check_is_tables(i) and (i.count('INSERT') > 0 or i.count('UPDATE') > 0 or i.count('DELETE') > 0) and not i.count('`django_session`') > 0:
                sql = i.replace("\\'", '&#39;')
                sql = sql.replace("'", '"')
                if sql.count('INSERT') > 0:
                    sql = 'INSERT %s' % ''.join(sql.split('INSERT')[1:])
                elif sql.count('UPDATE') > 0:
                    sql = 'UPDATE %s' % ''.join(sql.split('UPDATE')[1:])
                elif sql.count('DELETE') > 0:
                    sql = 'DELETE %s' % ''.join(sql.split('DELETE')[1:])
                os.system("echo '%s;' >> /var/www/tcd.config" % sql)
                count += 1
        os.system('echo "" > /var/log/mysql/mysql.log')

        return count
    
    return False


def set_mail(to='', subject='', text=''):

    mail = base64.b64encode( json.JSONEncoder().encode({'to' : to, 'subject' : subject, 'text' : text}) )
        
    os.system("echo '%s;' >> /var/www/mail.config" % mail)    
        