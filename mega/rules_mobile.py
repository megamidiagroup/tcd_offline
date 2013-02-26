# -*- coding: utf-8 -*-
#!/usr/bin/env python

def get_style_template(t):

    s = ''
    
    if t.tipo.name != 'mega':
        return s
    
    s += '#header #menu .search-button {'
    if (t.image4 and len(t.cor20) > 0) or (t.image4 and not len(t.cor20) > 0):
        s += 'background: '
        s += 'url("%s") no-repeat center ' % t.image4.url
    if not t.image4 and len(t.cor20) > 0:
        s += 'background-color: '
        s += '#%s ' % t.cor20
    if not t.image4 and not len(t.cor20) > 0:
        s += 'background: '
        s += 'none'
    s += ';'
    s += '}'

    s += '#header #menu .menu-button {'
    if len(t.cor16) > 0:
        s += 'color: #%s;' % t.cor16
    if len(t.cor3) > 0:
        s += 'background-color: #%s;' % t.cor3
    s += '}'

    s += '#header #menu .user-button {'
    if (t.image7 and len(t.cor20) > 0) or (t.image7 and not len(t.cor20) > 0):
        s += 'background: '
        s += 'url("%s") no-repeat center ' % t.image7.url
    if not t.image7 and len(t.cor20) > 0:
        s += 'background-color: '
        s += '#%s ' % t.cor20
    if not t.image7 and not len(t.cor20) > 0:
        s += 'background: '
        s += 'none'
    s += ';'
    s += '}'
    
    s += '#header #search button {'
    if len(t.cor27) > 0:
        s += 'background-color: #%s;' % t.cor27
    if len(t.cor28) > 0:
        s += 'color: #%s;' % t.cor28
    s += '}'

    s += '#header #menu ul li a {'
    if len(t.cor16) > 0:
        s += 'color: #%s;' % t.cor16
    if len(t.cor3) > 0 and not len(t.cor33) > 0:
        s += 'background: #%s;' % t.cor3
    if len(t.cor33) > 0 and len(t.cor3) > 0:
        s += 'filter: progid:DXImageTransform.Microsoft.gradient(startColorstr="#%s", endColorstr="#%s");' % (t.cor3, t.cor33)
        s += 'background: -webkit-gradient(linear, left top, left bottom, from(#%s), to(#%s));' % (t.cor3, t.cor33)
        s += 'background: -moz-linear-gradient(top,  #%s,  #%s);float:none; display:block;-webkit-border-radius: 0;' % (t.cor3, t.cor33)
    s += '}'

    return s