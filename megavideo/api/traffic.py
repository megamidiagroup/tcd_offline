	#! /usr/bin/python
# encoding:utf-8
import urllib, urllib2
import simplejson
import datetime
from django.conf import settings

def last_day_of_month(year, month):
        """ Work out the last day of the month """
        last_days = [31, 30, 29, 28, 27]
        for i in last_days:
                try:
                        end = datetime.datetime(year, month, i)
                except ValueError:
                        continue
                else:
                        return end.day
        return None



def get_traffic(**kwargs):
    #URL_TRAFIC = 'http://treinandoequipes.com.br/traffic/by_customer/in_json/'
    #URL_USAGE = 'http://treinandoequipes.com.br/traffic/diskusage/by_customer/in_json/'
    today = datetime.datetime.now()

    #default values
    kwargs['project'] = kwargs.get('project', 'portallabel')
    kwargs['year'] = kwargs.get('year', today.year)
    kwargs['month'] = kwargs.get('month', today.month)
    kwargs['plan'] = kwargs.get('plan', 'basico')
    kwargs['server'] = kwargs.get('server', 'v4.vflow.com.br')

    #url = URL_TRAFIC + '%s/%s/%s/' % (kwargs['project'], kwargs['year'], kwargs['month'])

    #last_day = last_day_of_month(kwargs['year'], kwargs['month'])
    #url_usage = URL_USAGE + '%s/%s/%s/%s/' % (kwargs['project'], kwargs['year'], kwargs['month'], today.day)

    #auth_handler = urllib2.HTTPPasswordMgrWithDefaultRealm()
    #top_level_url = "http://treinandoequipes.com.br/traffic/"
    #auth_handler.add_password(None, top_level_url, 'vflow', 'vflow_pass')

    #handler = urllib2.HTTPBasicAuthHandler(auth_handler)

    #opener = urllib2.build_opener(handler)

    #print 'URL ' , url
    #result = simplejson.load(opener.open(url))

    #print 'URL_USAGE ' , url_usage
    #usage = simplejson.load(opener.open(url_usage))

    #if result:

    #    plan = settings.VFLOW_PLAN.get(kwargs['plan'])

    #    dados_byte = int(plan['data'].replace('GB', '')) * 1024 ** 3
    #    tranferencia_byte = int(plan['transfer'].replace('GB', '')) * 1024 ** 3

        #FIXME - errado o valor total aqui é o de transferencia não o do total do servidor
        #result[0]['free_space'] = (dados_byte - result[0]['total']['bytes'])
    #    if usage:
    #        print 'USAGE ' , 0
    #        print 'dados_byte ' , dados_byte
    #        result[0]['usage_space'] = (usage[0][1])
    #        result[0]['free_space'] = (dados_byte - usage[0][1])

    #        if result[0]['free_space'] < 0:
    #            result[0]['free_space'] = 0
    #            result[0]['extra'] = (usage[0][1] - dados_byte)

    #    else:
    #        print 'USAGE ' , 0
    #        print 'dados_byte ' , dados_byte
    #        result[0]['usage_space'] = (0)
    #        result[0]['free_space'] = (dados_byte - 0)

    #    result[0]['free_trans'] = (tranferencia_byte - result[0]['total']['bytes'])
    #    if result[0]['free_trans'] < 0:
    #        result[0]['free_trans'] = 0
    #        result[0]['extra_tans'] = (result[0]['total']['bytes'] - tranferencia_byte)

    #    return result[0]
    #else:
    return []
