#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseForbidden
from django.utils import simplejson as json
from states.models import State

def states_json_combo(request):
    if not request.is_ajax():
        return HttpResponseForbidden('access denied')
    
    state_pk = request.POST.get('state_pk', None)
    if not state_pk:
        return HttpResponseForbidden('required header not sent')
    
    try:
        state = State.objects.get(pk=int(state_pk))
    except ValueError:
        return HttpResponseForbidden('bad format')
    except State.DoesNotExist:
        return HttpResponseForbidden('bad value')
        
    
    data = [{'state_pk': city.state.pk, 'name': city.name, 'pk': city.pk} for city in state.city_set.all()]
    response = json.dumps(data)
    
    return HttpResponse(response)
