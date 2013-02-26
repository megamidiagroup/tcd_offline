# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.template import RequestContext
from megavideo.common.dlog import LOGGER

import os
import simplejson as json
import tempfile

### import dos defs ###
from megavideo.portal.tools import _prepare_page


def index(request):
    """ para captar os dados do usuario que envia o video """
    
    p = {}
    
    p['base_url'] = settings.MEGAVIDEO_CONF['base_url']
    p['record']   = True

    return render_to_response('portal/live.html', p, context_instance=RequestContext(request))