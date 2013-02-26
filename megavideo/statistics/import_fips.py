#!/usr/bin/python
# encoding: utf-8
filedata = open('./statistics/fips_include.txt', 'r')
data = filedata.readlines()

from statistics.models import *

for i in data:
    values = i.split(',')
    _code = values[0].replace('\"', '').replace('\n', '')
    _region = values[1].replace('\"', '').replace('\n', '')
    _state_name = values[2].replace('\"', '').replace('\n', '')
    print LocationRegion.objects.using('megavideo').get_or_create(code=_code, region=_region, state_name=_state_name)
