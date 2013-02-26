from django.http import HttpResponse
from megavideo.common.dlog import LOGGER
from django.conf import settings
from megavideo.video.models import Job
from megavideo.common.channel import get_current_channel

from megavideo.async.call import AsyncCall
import simplejson

import os.path
import tempfile

from auth import check_token

@check_token()
def upload(request):

    """ clean """
    LOGGER.debug('upload starts ' + str(request.FILES.keys()))
    LOGGER.debug('before')
    r = {}
    msg = {}

    if 'category' in request.REQUEST:
        category_id = request.REQUEST['category']
    else:
        category_id = 0

    r = {'name' : '', 'description' : ''}
    for i in ['name', 'description', 'author']:
        if i in request.POST:
            r[i] = request.POST[i]

    LOGGER.debug('receive post')

    if 'Filedata' in request.FILES:
        LOGGER.debug('insider')

        LOGGER.debug('aqui')

        file_uploaded = request.FILES['Filedata']

        if r['name'] == '':
            r['name'] = file_uploaded.name

#        r['author'] = 'Sebrae'

        conf = settings.MEGAVIDEO_CONF
        tmp = tempfile.mktemp('_' + conf['tv_name'])
        tmp = conf['tmp'] + os.path.basename(tmp)
        fd = open(tmp, 'wb')
        LOGGER.debug('opened')

        for chunk in file_uploaded.chunks():
            fd.write(chunk)
        fd.close()

        LOGGER.debug('insider3')

        job = Job()
        job.channel = get_current_channel(request)
        job.ip = request.META['REMOTE_ADDR']
        job.status = 'A'
        job.original_name = file_uploaded.name
        job.message = 'inserting upload/vflow interface'
        job.save(using='megavideo')

        LOGGER.debug('insider4')
        try:

            chan = get_current_channel(request)
            acall = AsyncCall(conf['dispatch'], conf['tv_name'], channel_id = chan.id)

            #print 'CHANNEL -----------------------------------------------------'
            #print chan

            kargs = {
                    'metadatas' :-1, #create metadatas from scratch
                    'transcode' : True,
                    'keep_video' : True,
                    'chan_id' : chan.id,
                    'metas': r
                    }

            if int(category_id) != 0:
                kargs['cat_id'] = category_id
            LOGGER.debug('insider5')

             # Add user on video if logged
            if request.user.is_authenticated():
                kargs['user_id'] = request.user.id
                LOGGER.debug('Add user:  %s' % kargs['user_id'])

            acall.set_job(job)
            acall.set_insert(tmp, **kargs)
            acall.call()

            LOGGER.debug('after calling')

        except StandardError, e:
            msg = {'code' :-1}
            LOGGER.debug(str(e))


        if 'redirect' in request.REQUEST:
            return HttpResponseRedirect('/' + p['url_channel'] + 'manager/jobs/%d/' % (job.id))

        msg = {'code' : 0, 'jobid' : job.id}
        return HttpResponse(simplejson.dumps(msg))

    msg = {'code' :-1}
    return HttpResponse(simplejson.dumps(msg))


def cancel(request):
    return HttpResponse('{}')

@check_token()
def check(request, jobid):
    """ def para trazer status do job em andamento """
    r = {}

    try:
        job = Job.objects.using('megavideo').get(pk = int(jobid))
    except:
        job = None

    if job:
        if job.video:
            r = {'code' : 0, 'state' : 'F', 'video_id' : job.video.id}

        if job.status == 'E':
            r = {'code' : 0, 'state' : 'E'}
        elif job.status == 'A':
            r = {'code' : 0, 'state' : 'A'}
        elif job.status == 'F':
            r = {'code' : 0, 'state' : 'F', 'video_id': job.video_id }
        elif job.status == 'Q':
            r = {'code' : 0, 'state' : 'Q'}
        else:
            if r == {}:
                r = {'code' :-1}

    if r == {}:
        r = {'code' :-2, 'state' : 'N'} # no job \;
    return HttpResponse(simplejson.dumps(r))

