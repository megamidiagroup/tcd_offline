from megavideo.badwords.models import *
from django.template import Library

register = Library()


@register.filter("replace_bad_words")  
def replace_bad_words(value):  
     """ Replaces profanities in strings with safe words 
     For instance, "shit" becomes "s--t" 
     """  
     words_seen = [w for w in [i.word.lower() for i in Profanities.objects.using('megavideo').all()] if w in value.lower()]  
     if words_seen:  
         for word in words_seen:  
             value = value.replace(word, "%s%s%s" % (word[0], '-'*(len(word)-2), word[-1]))  
     return value 
