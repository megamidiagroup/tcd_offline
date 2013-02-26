# -*- coding: utf-8 -*-

from django.conf import settings

from PIL import Image
from command import Sh

sh = Sh()
    
def reference(key, obj, delay=1595, recuo=0):
    
    obj.bg_height = obj.bg_height - ( ( obj.bg_height - (2200 - delay) ) % 50 )
    
    height = '400'
    
    if obj.cat_banner.croppedimage_set.all().exclude(image = '')[0].size.height == 200:
        height = '200'
            
    image_center = 'bg_center.jpg'
    image_left   = 'bg_left_%s_%s.jpg' % (key, height)
    image_middle = 'bg_%s_%s.jpg' % (key, height)
    image_right  = 'bg_right_%s_%s.jpg' % (key, height)
    reference    = '%sreference/' % settings.APP_DIR
    path         = '%smedia/country/storage/background/' % settings.APP_DIR
    
    ## imagem center 100%
    image = Image.open(reference + image_center)
    new   = Image.new('RGB', (962, obj.bg_height + delay))
    
    size_top = 0, 0, 962, (image.size[1] / 2) - recuo
    size_middle = 0, (image.size[1] / 2) - recuo, 962, (image.size[1] / 2) - recuo + 50
    size_bottom = 0, (image.size[1] / 2) - recuo, 962, image.size[1]
    
    crop_top = image.crop(size_top)
    crop_middle = image.crop(size_middle)
    crop_bottom = image.crop(size_bottom)
    
    new.paste(crop_top   , size_top)
    cont = 0
    if (obj.bg_height + delay) > image.size[1]:
        ran = ((obj.bg_height + delay) - image.size[1]) / 50
        for i in range(0, ran):
            new.paste(crop_middle, (0, (image.size[1] / 2) - recuo + cont, 962, (image.size[1] / 2) - recuo + 50 + cont))
            cont += 50
    new.paste(crop_bottom, (0, (image.size[1] / 2) - recuo + cont, 962, image.size[1] + cont))
    
    new.save('%sbg_center_%s.jpg' % (path, key), 'JPEG')
    
    sh.chmod('755 %sbg_center_%s.jpg' % (path, key))
    ###
    
    ## imagem left 100%
    image = Image.open(reference + image_left)
    new   = Image.new('RGB', (798, obj.bg_height + delay))
    
    size_top = 0, 0, 798, (image.size[1] / 2) - recuo
    size_middle = 0, (image.size[1] / 2) - recuo, 798, (image.size[1] / 2) - recuo + 50
    size_bottom = 0, (image.size[1] / 2) - recuo, 798, image.size[1]
    
    crop_top = image.crop(size_top)
    crop_middle = image.crop(size_middle)
    crop_bottom = image.crop(size_bottom)
    
    new.paste(crop_top   , size_top)
    cont = 0
    if (obj.bg_height + delay) > image.size[1]:
        ran = ((obj.bg_height + delay) - image.size[1]) / 50
        for i in range(0, ran):
            new.paste(crop_middle, (0, (image.size[1] / 2) - recuo + cont, 798, (image.size[1] / 2) - recuo + 50 + cont))
            cont += 50
    new.paste(crop_bottom, (0, (image.size[1] / 2) - recuo + cont, 798, image.size[1] + cont))
    
    new.save('%sbg_left_%s.jpg' % (path, key), 'JPEG')
    
    sh.chmod('755 %sbg_left_%s.jpg' % (path, key))
    ###
    
    ## imagem middle 100%
    image = Image.open(reference + image_middle)
    new   = Image.new('RGB', (962, obj.bg_height))
    
    size_top = 0, 0, 962, (image.size[1] / 2)
    size_middle = 0, (image.size[1] / 2), 962, (image.size[1] / 2) + 50
    size_bottom = 0, (image.size[1] / 2), 962, image.size[1]
    
    crop_top = image.crop(size_top)
    crop_middle = image.crop(size_middle)
    crop_bottom = image.crop(size_bottom)
    
    new.paste(crop_top   , size_top)
    cont = 0
    if obj.bg_height > image.size[1]:
        ran = (obj.bg_height - image.size[1]) / 50
        for i in range(0, ran):
            new.paste(crop_middle, (0, (image.size[1] / 2) + cont, 962, (image.size[1] / 2) + 50 + cont))
            cont += 50
    new.paste(crop_bottom, (0, (image.size[1] / 2) + cont, 962, image.size[1] + cont))
    
    new.save('%sbg_%s.jpg' % (path, key), 'JPEG')
    
    sh.chmod('755 %sbg_%s.jpg' % (path, key))
    ###
    
    ## imagem right 100%
    image = Image.open(reference + image_right)
    new   = Image.new('RGB', (10, obj.bg_height + delay))
    
    size_top = 0, 0, 10, (image.size[1] / 2)
    size_middle = 0, (image.size[1] / 2) - recuo, 10, (image.size[1] / 2) - recuo + 50
    size_bottom = 0, (image.size[1] / 2) - recuo, 10, image.size[1]
    
    crop_top = image.crop(size_top)
    crop_middle = image.crop(size_middle)
    crop_bottom = image.crop(size_bottom)
    
    new.paste(crop_top   , size_top)
    cont = 0
    if (obj.bg_height + delay) > image.size[1]:
        ran = ((obj.bg_height + delay) - image.size[1]) / 50
        for i in range(0, ran):
            new.paste(crop_middle, (0, (image.size[1] / 2) - recuo + cont, 10, (image.size[1] / 2) - recuo + 50 + cont))
            cont += 50
    new.paste(crop_bottom, (0, (image.size[1] / 2) - recuo + cont, 10, image.size[1] + cont))
    
    new.save('%sbg_right_%s.jpg' % (path, key), 'JPEG')
    
    sh.chmod('755 %sbg_right_%s.jpg' % (path, key))
    
    return key