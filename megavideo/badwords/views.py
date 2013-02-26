# -*- coding: utf-8 -*-
from megavideo.badwords.models import *
  
def replace_bad_words(value):  
    """ Replaces profanities in strings with safe words 
    For instance, "shit" becomes "s--t" 
    """  
    words_seen = [w for w in Profanities.objects.using('megavideo').all() if w in value]  
    if words_seen:  
       for word in words_seen:  
           value = value.replace(word, "%s%s%s" % (word[0], '-'*(len(word)-2), word[-1]))  
    return value  


def safe_words(value):
        
    check_words     = []
    filter_words    = []
    safe_words      = []
    
    if ',' in value:
        check_words = str(value).lower().strip().split(',')

    elif ' ' in value:
        check_words = str(value).lower().strip().split(' ')
    
    else:
        check_words.append(value) 
        
    bad_words = [i.word.lower().strip() for i in Profanities.objects.using('megavideo').all()]
        
    for i in bad_words:
        for j in check_words:
            if i in j and j not in filter_words:
                filter_words.append(j)

    #auto save new bad words
    for i in filter_words:
        if i not in bad_words:
            b = Profanities()
            b.word = i
            b.save(using='megavideo')    
    
    
    for i in check_words:
        if i not in filter_words:
            if len(i) > 2:
                safe_words.append(i)
    
    
    return safe_words               