# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from megavideo.video.models import *
from menu import *
from megavideo.video.views   import get_absolute_url
from django.template.loader import render_to_string
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q, Count, Sum
from megavideo.common.DiggPaginator import *

from megavideo.async.call import AsyncCall
from megavideo.common.dlog import LOGGER

from django.conf import settings
import os.path
import tempfile
import simplejson as json
from datetime import datetime, timedelta

from megavideo.video.models import *
from megavideo.api.video import video_search

import os
import os.path
import shutil
import commands
import stat
from unicodedata import normalize

MOVIE_EXTENSIONS = ['.avi', '.flv', '.mp4', '.ogg', '.wmv']

def recordVideo(filename):

    conf = settings.MEGAVIDEO_CONF
    tmp = tempfile.mktemp('_' + conf['tv_name'])
    tmp = conf['tmp'] + os.path.basename(tmp)

    meta_data = {'name' : os.path.basename(filename), 'description' : '', 'author': 'FTP', 'email': ''}

    try:
        default_channel = request.channel_name
    except:
        default_channel = conf['default_channel']

    shutil.move(filename, tmp)
    #move_action = os.popen('mv %s %s' % (filename, tmp))

    job = Job()
    job.channel = Channel.objects.using('megavideo').get(name=default_channel)

    try:
        job.ip = request.META['REMOTE_ADDR']
    except:
        job.ip = 0

    job.status = 'A'
    job.original_name = filename
    job.message = 'inserting upload/vflow ftp'
    job.save(using='megavideo')

    acall = AsyncCall(conf['dispatch'], conf['tv_name'], job.channel.id)

    kargs = {
            'metadatas' :-1, #create metadatas from scratch
            'transcode' : True,
            'keep_video' : True,
            'chan_id' : job.channel.id,
            'metas': meta_data
            }

    acall.set_job(job)
    acall.set_insert(tmp, **kargs)

    return acall.call()


def processDirectory (args, dirname, filenames):
    #print 'Directory',dirname
    for filename in filenames:
        base, ext = os.path.splitext(filename)
        realpath = os.path.realpath(filename)
        try:
            size = os.path.getsize(realpath)
        except:
            size = 0
        ext = ext.replace('.', '')
        if ext.lower() in MOVIE_EXTENSIONS:
            realpath = os.path.join(dirname, filename)
            recordVideo(realpath)
            #print ' File', filename
            #print ' Ext', ext
            #print ' Name', base
            #print ' Size', str(size)
            #print '-------------------------------------------------------------------'


def list_files(top_level_dir="/home/tvt/videos"):
    os.path.walk(top_level_dir, processDirectory, None)


def del_file(request):
    p = {}

    id = request.POST.get('id', '')
    realpath = request.REQUEST.get('realpath', '')

    try:
        os.unlink(realpath)
        p['status'] = True
    except:
        p['status'] = False

    return HttpResponse(json.dumps(p) , mimetype='application/json')



def merge_path(root, dirname, filename):
    value = ''
    if root:
        value += str(root)
    if dirname:
        value += str(dirname)
    if filename:
        value += str(filename)

    value = value.replace('//', '/')
    return value



@login_required
def list_ftp(request, page=1):

    p = menu_top(request)
    content_list = []
    dir_target = getattr('FTP_ROOT', 'settings' , '/home/tvt/videos/')

    if 'add_files' in request.POST:
        files = request.POST.getlist('file')
        for filename in files:
            print ' FILES' , filename
            recordVideo(filename)


    for root, dirname , filenames in os.walk(dir_target):
        for filename in filenames:
            oldname = os.path.join(root, filename)
            try:
                newname = normalize('NFKD', oldname.decode('utf-8')).encode('ASCII', 'ignore')
            except:
                newname = normalize('NFKD', oldname.decode('latin1')).encode('ASCII', 'ignore')

            os.rename(oldname, newname)


    for roots, dirname , filenames in os.walk(dir_target):
        #print ' dirname' , dirname
        for filename in filenames:
            realpath = merge_path(roots, dirname, filename)
            basename, ext = os.path.splitext(filename)

            if ext.lower() in MOVIE_EXTENSIONS:
                status = os.stat(realpath)
                file_date = datetime.datetime.fromtimestamp(status[stat.ST_CTIME])
                file_size = status[stat.ST_SIZE]

    #            if not os.path.isfile(thumbname):
    #                grabimage = "ffmpeg -y -i %s -vframes 1 -ss 00:00:02 -an -vcodec png -f rawvideo -s 56x42 %s " % (realpath, thumbname)
    #                grab = commands.getoutput(grabimage)
    #                print grab

                content_list.append({ 'realpath' : realpath , 'name': os.path.basename(realpath), 'thumb' : '', 'date' : file_date , 'size' : file_size})

    content_list = sorted(content_list, key=lambda x: x['date'], reverse=True)

    p['content_list'] = content_list

    return render_to_response('manager/ftp/list_ftp.html', p, context_instance=RequestContext(request))


if __name__ == '__main__':
    list_files()
