import os
import Image
from django.template import Library
from django.conf import settings
from megavideo.common.create_url import get_thumb_path

register = Library()

def aspect_ratio(original, final, border = False):
    ar = float(original[0]) / original[1]
    arf = float(final[0]) / final[1]

    if ((ar > arf) and border == False) or ((ar < arf) and border == True):
        heigth = final[1]
        width = final[1] * ar
        offset = (int((final[0] - width) / 2), 0)
    else:
        heigth = final[0] / ar
        width = final[0]
        offset = (0, int((final[1] - heigth) / 2))

    return offset, (int(width), int(heigth))


def thumbnail(video, size = '200x200'):
    # defining the size
    x, y = [int(x) for x in size.split('x')]

    try:
        t = video.get_thumb()
    except:
        return '/megavideo/static/manager/images/processando.gif'

    base_path = os.path.join(settings.MEGAVIDEO_CONF['video_storage'], video.dir)
    base_name = 'thumb_' + t.name
    basename, format = base_name.rsplit('.', 1)
    miniature = basename + '_' + size + '.' + format
    miniature_filename = os.path.join(base_path, miniature)
    sminiature_url = os.path.join(settings.STORAGE_URL + 'videos/' + str(video.dir) + '/', basename + '_' + size + '.' + format)

    if not os.path.exists(miniature_filename):
        filename = os.path.join(base_path, base_name)

        try:
            image = Image.open(filename)

        except:
            return '/megavideo/static/manager/images/processando.gif'

        output = Image.new('RGB', [x, y])
        offset, size = aspect_ratio(image.size, output.size)

        image = image.resize(size, Image.ANTIALIAS) # generate a 200x200 thumbnail
        output.paste(image, offset)
        output.save(miniature_filename, image.format)
    return sminiature_url



register.filter(thumbnail)
