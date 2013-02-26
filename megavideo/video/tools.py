# -*- coding: utf-8 -*-

from megavideo.video.models import *

######## etapas para metas #################

## 1º passo: ver os video classes, define para qual tv terá que usar, default id 1
def get_video_class_key_values():
    """ para trazer todos os videoclass """

    vc = Videoclass.objects.using('megavideo').all()

    for i in vc:
        print "id: " + str(i.id) + " | name: " + str(i.name) + " | displayname: " + str(i.displayname) + " | metatitle: " + str(i.metatitle)

    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"


def add_video_class_key_values(name, displayname, metatitle):
    """ para adicionar novo video class """

    vc = Videoclass()

    try:
        vc.name = str(name)
        vc.displayname = unicode(displayname)
        vc.metatitle = str(metatitle)
        vc.save(using='megavideo')
    except ValueError:
        print "erro!"

    print " out: " + str(vc.id)
    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"

    return vc


def del_video_class_key_values(id):
    """ para deletar um video class por id """

    try:
        vc = Videoclass.objects.using('megavideo').get(id = id)
        vc.delete()
    except ValueError:
        print "erro!"

    print " deletado com sucesso! "
    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"


## 2º passo: ver os meta classes, define o campo e que tipo será o campo
def get_meta_class_key_values():
    """ para trazer todos os metaclass """

    mc = Metaclass.objects.using('megavideo').all()

    for i in mc:
        print "id: " + str(i.id) + " | name: " + str(i.name) + " | validate: " + str(i.validate)

    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"


def add_meta_class_key_values(name, validate):
    """ para adicionar novo meta class """

    mc = Metaclass()

    try:
        mc.name = str(name)
        mc.validate = str(validate)
        mc.save(using='megavideo')
    except ValueError:
        print "erro!"

    print " out: " + str(mc.id)
    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"

    return mc


def del_meta_class_key_values(id):
    """ para deletar um meta class por id """

    try:
        mc = Metaclass.objects.using('megavideo').get(id = id)
        mc.delete()
    except ValueError:
        print "erro!"

    print " deletado com sucesso! "
    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"


## 3º passo (final): ver os video meta class, define exatemente que projeto vai ser usado que tipo de campo.
def get_video_meta_class_key_values():
    """ para trazer todos os videometaclass """

    vmc = Videometaclass.objects.using('megavideo').all()

    for i in vmc:
        print u"id: " + unicode(i.id) + u" | videoclass.name: " + unicode(i.videoclass.name) + u" | metaclass.name: " + unicode(i.metaclass.name + u" | displayname: " + unicode(i.displayname) + u" | sequence: " + unicode(i.sequence))

    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"


def add_video_meta_class_key_values(videoclass, metaclass, displayname, sequence=0):
    """ para adicionar novo meta class """

    vmc = Videometaclass()

    vc = Videoclass.objects.using('megavideo').filter(name = str(videoclass))
    if vc:
        mc = Metaclass.objects.using('megavideo').filter(name = str(metaclass))
        if mc:
            try:
                vmc.videoclass = vc[0]
                vmc.metaclass = mc[0]
                vmc.displayname = displayname.decode('utf-8')
                vmc.sequence = int(sequence)
                vmc.save(using='megavideo')
            except ValueError:
                print "erro!"
        else:
            print "não existe o metaclass.name!"
    else:
        print "não existe o videoclass.name!"

    print " out: " + str(vmc.id)
    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"

    return vmc


def del_video_meta_class_key_values(id):
    """ para deletar um video meta class por id """

    try:
        vmc = Videometaclass.objects.using('megavideo').get(id = id)
        vmc.delete()
    except ValueError:
        print "erro!"

    print " deletado com sucesso! "
    print ""
    print " >>>>>>>>>>>>> end <<<<<<<<<<<<<<"


## passo alternativo: incluir uma meta automaticamente, lista e deletar
def get_metas():
    """ para listar as metas existentes """
    get_video_meta_class_key_values()


def add_meta(tv, displayname_tv, metatitle_tv, meta_name, meta_name_type, descrition, sequence=0):
    """ """

    vc = Videoclass.objects.using('megavideo').filter(name = str(tv))
    mc = Metaclass.objects.using('megavideo').filter(name = str(meta_name))

    if vc:
        print 'ja existe o videoclass!'
    else:
        vc = add_video_class_key_values(tv, displayname_tv, metatitle_tv)
        print 'cadastrado o videoclass com sucesso!'

    if mc:
        print 'ja existe o metaclass!'
    else:
        mc = add_meta_class_key_values(meta_name, meta_name_type)
        print 'cadastrado o metaclass com sucesso!'

    if vc and mc:
        add_video_meta_class_key_values(vc[0].name, mc[0].name, descrition, sequence)
        print 'cadastrado o videometaclass com sucesso!'
    else:
        print 'impossivel cadastrar o video meta class!'


def del_meta(meta_name):
    """ """

    mc  = Metaclass.objects.using('megavideo').filter(name = str(meta_name))
    vmc = Videometaclass.objects.using('megavideo').filter(metaclass = mc)

    if vmc:
        vmc.delete()
        print 'deletado o videometaclass com sucesso!'
    else:
        print 'video meta class não existe!'

    if mc:
        mc.delete()
        print 'deletado o metaclass com sucesso!'
    else:
        print 'Não existe o metaclass!'