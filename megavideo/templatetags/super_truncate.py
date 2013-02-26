# -*- coding: utf-8 -*-

#Version: 1.0
#User: Rafael Feijo
#Email: rafael.exe@hotmail.com

from django.template import Library

register = Library()

@register.filter
def super_truncatewords(word, num):
    """ o super_truncatewords limita palavras como o truncatewords do django + limitador de caracter máximo """ 
    
    max_words = ''
    count = trunc = char = 0

    try:
        if num.count('-') > 0:
            trunc = int(num.split('-')[0])
            char  = int(num.split('-')[1])
        else:
            trunc = int(num)
    except:
        pass

    try:
        if word.count(' ') > 0:
            for i in word.split(' '):
                if count < trunc:
                    max_words += i + ' '
                    count += 1
                else:
                    break
        else:
            max_words = word        
    except:
        word = 'error'
	max_words = word 
            
            
    if char > 0 and len(max_words) > char:
        max_words = max_words[0:char] + ' ...'
    else:
        if len(word) > len(max_words):
            max_words += ' ...'

    return max_words

register.filter('super_truncate', super_truncatewords)
