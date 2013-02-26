import os
import re
import sys
import locale
import urllib
import optparse
import itertools
import subprocess
from xml.etree import ElementTree

import gdata.media
import gdata.geo
import gdata.youtube
import gdata.youtube.service

import os
import os.path
#from _initlib import *
from django.conf import settings
from megavideo.common.dlog import LOGGER
VERSION = "0.1"

from megavideo.video.models import *
from megavideo.templatetags.super_truncate import super_truncatewords

if settings.GEOIP_PATH:
    from django.contrib.gis.utils import GeoIP

def get_encoding():
    return sys.stdout.encoding or locale.getpreferredencoding()


def debug(obj):
    """Write obj to standard error."""
    LOGGER.debug(str(obj))


def run(command, inputdata=None, **kwargs):
    """Run a command and return standard output/error"""
    debug("run: %s" % " ".join(command))
    popen = subprocess.Popen(command, **kwargs)
    outputdata, errdata = popen.communicate(inputdata)
    return outputdata, errdata

def ffmpeg(*args, **kwargs):
    """Run ffmpeg command and return standard error output."""
    kwargs2 = {}
    if "show_stderr" not in kwargs:
        kwargs2["stderr"] = subprocess.PIPE
    outputdata, errdata = run(["ffmpeg"] + list(args), **kwargs2)
    return errdata

def get_video_duration(video_path):
    """Return video duration in seconds."""
    errdata = ffmpeg("-i", video_path)
    match = re.search(r"Duration:\s*(.*?),", errdata)
    if not match:
        return
    strduration = match.group(1)
    return sum(factor * float(value) for (factor, value) in
               zip((60 * 60, 60, 1), strduration.split(":")))

def split_video(video_path, max_duration, max_size=None, time_rewind=0):
    """Split video in chunks and yield path of splitted videos."""
    if not os.path.isfile(video_path):
        raise ValueError, "Video path not found: %s" % video_path
    total_duration = get_video_duration(video_path)
    assert total_duration
    if total_duration <= max_duration and os.path.getsize(video_path) <= max_size:
        yield video_path
        return

    dirname = os.path.dirname(video_path)
    base, extension = os.path.splitext(os.path.basename(video_path))

    debug("split_video: %s, total_duration=%02.f" % (video_path, total_duration))
    offset = 0
    for index in itertools.count(1):
        debug("split_video: index=%d, offset=%d (total=%d)" %
            (index, offset, total_duration))
        output_path = "%s/%s-%d.%s" % (dirname, base, index, "mp4")
        temp_output_path = "%s/%s-%d.%s" % (dirname, base, index, "partial.mp4")
        if os.path.isfile(output_path) and get_video_duration(output_path):
            debug("skipping existing file: %s" % output_path)
        else:
            args = ["-y", "-i", video_path]
            if max_size:
                args += ["-fs", str(int(max_size))]
            args += ["-vcodec", "copy", "-acodec", "copy", "-ss", str(offset),
                     "-t", str(max_duration), temp_output_path]
            err = ffmpeg(*args, **dict(show_stderr=True))
            os.rename(temp_output_path, output_path)
        yield output_path
        size = os.path.getsize(output_path)
        assert size
        duration = get_video_duration(output_path)
        assert duration
        debug("chunk file size: %d (max: %d)" % (size, max_size))
        debug("chunk duration: %d (max: %d)" % (duration, max_duration))
        if size < max_size and duration < max_duration:
            debug("end of video reached: %d chunks created" % index)
            break
        offset += duration - time_rewind


def split_youtube_video(video_path):
    """Split video to match Youtube restrictions (<2Gb and <10minutes)."""
    return split_video(video_path, 60 * 10, max_size=int(2e9), time_rewind=5)


def set_video_youtube_meta_values(video_id, vdict):
    """ clean """
    v = Video.objects.using('megavideo').get(pk=video_id)

    for i in vdict.keys():
        if i in vdict:
            if i == 'name':
                v.title = vdict[i]
                v.save(using='megavideo')

            if i[0] == 'description':
                v.description = vdict[i]
                v.save(using='megavideo')

            vm = v.videometa_set.filter(metaclass__name=i)
            if len(vm) != 0:
                vm[0].value = vdict[i]
                vm[0].save(using='megavideo')
            else:
                vmc = v.videoclass.videometaclass_set.filter(metaclass__name=i)[0]
                vm = Videometa()
                vm.value = vdict[i]
                vm.video = v
                vm.metaclass = vmc.metaclass
                vm.save(using='megavideo')


def get_geo(video):
    latitude = 0.0
    longitude = 0.0
    g = GeoIP()
    if settings.GEOIP_PATH:
        try:
            data = g.city(video.job_set.all()[0].ip)
            if data:
                latitude = float(data['latitude'])
                longitude = float(data['longitude'])
        except StandardError, e:
            LOGGER.debug(str(e))
    return (latitude , longitude)


def keywords_to_string(video):
    cat = ''
    for i in video.category.all():
        cat += i.name + ','
    return cat


def tag_list(video):
    keywords = ', '.join([i[0].__str__() for i in video.get_tag_list()])
    if len(keywords) < 25:
        return keywords
    return 'tvt'

def register_youtube_videos(realpath, youtube_id , video , video_name):
    register = VideoYoutube()
    register.file = realpath
    register.youtube_id = youtube_id
    register.video = video
    register.name = video_name
    register.save(using='megavideo')


class Youtube:

    def __init__(self):
        developer_key = 'AI39si5cIJgjW17pmMdXNYJfLqMBvQASkdg77vRduoKtlf8q_2jYvqi-zVLDd9Ry9bp8Taeypvwg80eFgDuOKCRMphrA0nyzaw'

        yt_service = gdata.youtube.service.YouTubeService()
        yt_service.developer_key = developer_key
        yt_service.ssl = False
        yt_service.email = getattr(settings, 'YOUTUBE_USER', 'valder@vflow.com.br')
        yt_service.password = getattr(settings, 'YOUTUBE_PASS', 'valder_pass')
        yt_service.ProgrammaticLogin()
        self.yt_service = yt_service


    def update_youtube_video(self, video):
        youtube_id = video.get_youtube_id()
        if youtube_id:
            try:
                new_entry = self.yt_service.GetYouTubeVideoEntry(video_id=youtube_id)
                new_entry.title.text = video.get_name()
                new_entry.description.text = video.get_description()
                updated_entry = self.yt_service.UpdateVideoEntry(new_entry)
            except StandardError, e:
                LOGGER.debug(str(e))


    def delete_youtube_video(self, video):
        youtube_id = video.get_youtube_id()
        if youtube_id:
            new_entry = self.yt_service.GetYouTubeVideoEntry(video_id=youtube_id)
            response = self.yt_service.DeleteVideoEntry(new_entry)
            LOGGER.debug(str('DELETE YOUTUBE %s' % youtube_id))
            if response:
              print 'Video successfully deleted!'


    def send_youtube_video(self, video):

        video_name = super_truncatewords(video.get_name(), '20-150')

        media_group = gdata.media.Group(
            title=gdata.media.Title(text=video_name),
            description=gdata.media.Description(description_type='plain', text=super_truncatewords(video.get_description(), '20-150')),
            keywords=gdata.media.Keywords(text=tag_list(video)),
            category=[gdata.media.Category(text='Film', label='Film', scheme='http://gdata.youtube.com/schemas/2007/categories.cat')],
            private=None,
            player=None
        )

        # prepare a geo.where object to hold the geographical location
        # of where the video was recorded
        where = gdata.geo.Where()
        where.set_location(get_geo(video))

        # create the gdata.youtube.YouTubeVideoEntry to be uploaded
        video_entry = gdata.youtube.YouTubeVideoEntry(media=media_group, geo=where)

        # set the path for the video file binary
        storage_path = settings.MEGAVIDEO_CONF['video_storage']
        video_file_location = storage_path + '/' + video.dir + '/transcoded_' + str(video.videotranscode_set.filter(transcode__name='FlashWeb')[0].name)
        video_file_location = video_file_location.replace('//', '/')
        exist_file = os.path.exists(video_file_location)

        LOGGER.debug(str('FILE EXIST  %s %s' % (video_file_location, exist_file)))

        if exist_file:

            videos = list(split_youtube_video(video_file_location))
            index = 1

            for video_path in videos:

                if len(videos) > 1:
                    video_entry.media.title.text = '%s - Parte %s' % (video_name, index)

                new_entry = self.yt_service.InsertVideoEntry(video_entry, video_path)
                youtube_id = new_entry.id.text
                youtube_id = youtube_id[youtube_id.rfind('/') + 1:]
                meta = { 'youtube_id' : youtube_id }
                #add media youtube
                set_video_youtube_meta_values(video.id, meta)
                register_youtube_videos(video_path, new_entry.id.text , video , video_entry.media.title.text)
                index += 1

        return new_entry
