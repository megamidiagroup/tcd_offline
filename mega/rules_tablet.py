# -*- coding: utf-8 -*-
#!/usr/bin/env python

def get_style_template(t):

    s = ''
    
    if t.tipo.name != 'mega':
        return s

    s += '#header #menu {'
    if len(t.cor3) > 0:
        s += 'background-color: #%s;' % t.cor3
    if t.larg5 > 0:
        s += 'border: %dpx solid #%s;' % (t.larg5, t.cor17)
    s += '}'

    s += '#header #menu ul li a {'
    if len(t.cor16) > 0:
        s += 'color: #%s;' % t.cor16
    if len(t.cor3) > 0:
        s += 'background-color: #%s;' % t.cor3
    s += '}'

    s += '#header #menu ul li a:hover {'
    if len(t.cor19) > 0:
        s += 'color: #%s;' % t.cor19
    if len(t.cor18) > 0:
        s += 'background-color: #%s;' % t.cor18
    s += '}'

    return s