# -*- coding: utf-8 -*-
#from django.contrib.auth.decorators import login_required
from menu import *
from megavideo.common.DiggPaginator import *
from megavideo.common.login import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from megavideo.video.models import *

per_page = 12

@login_required
def jobs (request, highlight = 0):
    p = menu_top(request)
    for i in Job.objects.using('megavideo').filter(status = 'A'):
        try:
            os.stat('/proc/%d/' % (p.pid))
        except:
            jl = JobLog(job = i)
            jl.message = 'Process died'
            jl.save(using='megavideo')
            i.status = 'E'
            i.save(using='megavideo')

    p['running_jobs'] = Job.objects.using('megavideo').filter(status = 'A')
    #check running jobs
    p['last_jobs'] = Job.objects.using('megavideo').exclude(status = 'A')
    p['highlight'] = highlight

    return render_to_response('manager/jobs.html', p)


@login_required
def status_jobs(request):
    """ methodo com retorno em string para andamento de jobs """

    p = {}

    list_job = Job.objects.using('megavideo').all()

    p['job'] = list_job.exclude(status = 'F').filter(channel__name = request.channel_name)
    p['job_end'] = list_job.filter(channel__name = request.channel_name, status = 'F').order_by('-date')[0:5]

    return render_to_response('manager/import/list_job.html', p, context_instance = RequestContext(request))


def ajax_del_job(request):
    """ methodo para deletar um job """
    idjob = request.REQUEST.get('idjob', 0)
    p = {}
    p['status'] = False
    if id:
        try:
            job = Job.objects.using('megavideo').get(id = int(idjob))
            job.delete()
            p['status'] = True
        except:
            pass

    return HttpResponse(json.dumps(p), mimetype = 'application/json')
