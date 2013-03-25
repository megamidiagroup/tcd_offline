# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import connections
from django.conf import settings

import os
import re
import base64

import simplejson as json

OFFLINE = getattr(settings, 'OFFLINE', False)
    
def set_sql(*args):

    if OFFLINE:

        query = connections['default'].queries
    
        count = 0
        
        for i in query:
            if check_not_tables(i['sql']) and i['sql'].count('INSERT') > 0 or i['sql'].count('UPDATE') > 0 or i['sql'].count('DELETE') > 0:
                sql = i['sql']
                # captura a data para normalizar
                
                for obj in args:  
                    for o in dir(obj):
                        try:
                            field = getattr(obj, o, '')
                        except:
                            field = ''
                        if field != '' and not str(field).isdigit() and ('unicode' in type(field).__name__ or 'str' in type(field).__name__) and sql.count(o) > 0:
                            sql   = sql.replace(field, '"%s"' % field.replace('"', '\\"').replace("'", "&#39;"))
                            
                if sql.count("= ,") > 0:
                    sql = sql.replace('= ,', '= "",').replace('= WHERE', '= "" WHERE').replace('= ;', '= "";')
                
                date = re.search('([0-9]{2,4})-([0][0-9]|1[0-2])-([0-2][0-9]|3[0-1]) (?:([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]))?', sql).group()
                # replace na data para tornar e string
                sql  = re.sub('([0-9]{2,4})-([0][0-9]|1[0-2])-([0-2][0-9]|3[0-1]) (?:([0-1][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9]))?', '"%s"' % date, sql)
                os.system("echo '%s;' >> /var/www/tcd_offline/tcd.config" % sql)
                count += 1

        return count
    
    return 0

def check_not_tables(sql):
    
    for i in ['django_session']:
        if sql.count(i) > 0:
            return False
    
    return True


def set_mail(to='', subject='', text=''):

    mail = base64.b64encode( json.JSONEncoder().encode({'to' : to, 'subject' : subject, 'text' : text}) )
        
    os.system("echo '%s;' >> /var/www/tcd_offline/mail.config" % mail)    
        