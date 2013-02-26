# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from megavideo.common.DiggPaginator import *
from megavideo.video.models import *
from megavideo.manager.menu import *

@login_required
def index(request):
    """ pagina para transmissão ao vivo de video """

    p = menu_top(request)

    return render_to_response('manager/live/index.html', p, context_instance=RequestContext(request))
