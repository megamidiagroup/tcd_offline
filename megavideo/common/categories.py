from megavideo.video.models import *
def get_cat_childs(cat_id, l, list_selected):
    """ clean"""
    childs = []

    if cat_id == None:
        cat_id = 0

    for i in l:
        if i.parent != None:
            idParent = i.parent.id
        else:
            idParent = 0

        if int(idParent) == int(cat_id):
            cdict = {'id' : i.id, 
                    'idParent' : idParent , 
                    'name' : i.name, 
                    'childs' : get_cat_childs(i.id, l, list_selected)}
            if i in list_selected:
                cdict['status'] = 1
            else:
                cdict['status'] = 0
            cdict['nbvideos'] = i.video_set.all().count()
            childs.append(cdict)
    return childs

