import subprocess
import base64, pickle
from megavideo.common.dlog import LOGGER
from django.conf import settings
from megavideo.video.models import JobDispatch, Job
import os

class TaskManager():
    def __init__(self, channel_id):
        self.channel_id = channel_id

    def check_jobs(self):
        for i in Job.objects.using('megavideo').filter(channel__id = self.channel_id, status = 'A'):
            if i.pid != -1:
                try:
                    #se o processo existe, essa pasta existe
                    os.stat('/proc/' + str(i.pid))
                except:
                    i.status = 'E'
                    i.save(using='megavideo')

    def check_dispatch(self):
        if self.is_waiting_job_in_channel() and not self.is_active_job_in_channel():
            j = self.get_first_waiting_job()
            jd = j.jobdispatch_set.all()[0]
            try:
                self.run_dispatch(jd)
            except StandardError, e:
                LOGGER.debug('Erro no dispatch ' + str(e))

    def get_first_waiting_job(self):
        waiting_jobs = Job.objects.using('megavideo').filter(channel__id = self.channel_id, status = 'Q').order_by('date')
        return waiting_jobs[0]

    def run_dispatch(self, jobdispatch):
        jobdispatch.run()

    def is_active_job_in_channel(self):
        if Job.objects.using('megavideo').filter(status = 'A', channel__id = self.channel_id).count() > 0:
            return True
        else:
            return False

    def is_waiting_job_in_channel(self):
        if Job.objects.using('megavideo').filter(status = 'Q', channel__id = self.channel_id).count() > 0:
            return True
        else:
            return False

class AsyncCall():
    def __init__(self, dispatcher, tvname, channel_id = 1):
        self.tm = TaskManager(channel_id)
        self.dispatcher = dispatcher
        self.tvname = tvname
        self.reset()
        self.job = None
        self.channel_id = channel_id

    def reset(self):
        self.args = {'commands' : ()}

    def set_job(self, job):
        self.job = job

    def set_insert(self, filename, **kwargs):
        if 'chan_id' in kwargs:
            chan_id = kwargs['chan_id']
        else:
            chan_id = -1

        if 'keep_video' in kwargs:
            commands = (('insert_video', (filename, kwargs['keep_video'], chan_id)),)
        else:
            commands = (('insert_video', (filename, True, chan_id)),)

        commands += (('extract_infos', ()),)
        self.set_commands(commands, **kwargs)


    def set_commands(self, commands = (), **kwargs):

        if 'position' in kwargs:
            commands += (('create_thumb', (kwargs['position'],)),)
        else:
            commands += (('create_thumb', ()),)

        if 'select_video' in kwargs:
            commands += (('select_video', (kwargs['select_video'],)),)

        if 'source_metadatas' in kwargs:
            commands += (('set_flv_metadatas', (kwargs['source_metadatas'],)),)

        if 'publish_before' in kwargs:
            commands += (('set_publish', (kwargs['publish_before'],)),)

        if 'transcode' in kwargs and kwargs['transcode']:
            commands += (('create_all_transcodes', ()),)

        if '3gp' in kwargs and kwargs['3gp']:
            commands += (('create_3gp', ()),)

        if 'publish' in kwargs:
            commands += (('set_publish', (kwargs['publish'],)),)

        if 'cat_id' in kwargs:
            commands += (('add_category', (kwargs['cat_id'],)),)

        if 'user_id' in kwargs:
            commands += (('add_user', (kwargs['user_id'],)),)
            
        if 'metas' in kwargs and kwargs['metas']:
            commands += (('set_metas', (kwargs['metas'],)),)

        if 'post_insert_mail' in kwargs:
            commands += (('post_insert_mail', (kwargs['post_insert_mail'],)),)

        self.args['commands'] += commands


    def serialize(self):
        r = base64.b64encode(pickle.dumps(self.args))
        print r
        return r


    def call(self):
        cmd = self.args['commands']

        self.args['commands'] = (('set_job', (self.job.id,)),) + cmd

        self.job.status = 'Q'
        self.job.save(using='megavideo')

        jd = JobDispatch()
        jd.job = self.job
        jd.dispatch_path = self.dispatcher
        jd.tvname = self.tvname
        jd.commands_serialized = self.serialize()
        jd.save(using='megavideo')

        #limpa as tarefas rodando
        self.tm.check_jobs()
        #vamos ver se tiver algo esperando
        self.tm.check_dispatch()

        if self.tm.is_active_job_in_channel():
            #temos algo em processamento, vamos esperar
            self.job.status = 'Q'
            self.job.save(using='megavideo')
        else:
            #nao tem nada esperando, vamos la
            self.tm.run_dispatch(jd)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print 'usage :' + sys.argv[0] + ' tv file'
    ac = AsyncCall(settings.MEGAVIDEO_CONF.get('dispatch', ''), sys.argv[1])
    ac.set_insert(sys.argv[2], transcode = True)
    ac.call()
