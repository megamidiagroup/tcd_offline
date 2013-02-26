# -*- coding: utf-8 -*-
#!/usr/bin/env python

def get_style_template(t):

    s = ''
    
    if t.tipo.name != 'mega':
        if len(t.custom) > 0:
            s += '\n\n'
            s += '%s' % t.custom
        return s
    
    namefont = None

    ## aplicar fontes
    if t.font1 or t.font2 or t.font3 or t.font4:
        s += '@font-face {'
        try:
            array = t.font1.name.split('/')
            array.reverse()
            namefont = array[0].split('.')[0].upper()
        except:
            namefont = 'FONT-CUSTOM'
        s+= 'font-family:"%s";' % namefont
        if t.font2:
            s += 'src:url("%s");' % t.font2.url
            s += 'src:url("%s?#iefix") format("embedded-opentype")' % t.font2.url
        if t.font3:
            s += ','
            s += 'url("%s") format("woff")' % t.font3.url
        if t.font1:
            s += ','
            s += 'url("%s") format("truetype")' % t.font1.url
        if t.font4:
            s += ','
            s += 'url("%s#%s") format("svg")' % (t.font4.url, namefont)
        s += ';'
        s += '}'
    elif len(t.font_gle) > 0:
        s += '@import url(http://fonts.googleapis.com/css?family=%s);' % t.font_gle
        namefont = t.font_gle.replace('+', ' ')

    s += 'body {'
    if namefont:
        s += 'font-family:"%s",Helvetica,Arial,Verdana,sans-serif;' % namefont
    s += 'background: '
    if t.image1:
        s += 'url("%s") ' % t.image1.url
    if len(t.cor1) > 0:
        s += '#%s ' % t.cor1
    if len(t.advance1) > 0:
        s += '%s' % t.advance1
    if not t.image1 and not len(t.cor1) > 0:
        s += 'none'
    s += ';'
    s += '}'
    
    s += '#header {'
    s += 'background: '
    if t.image2:
        s += 'url("%s") repeat-x ' % t.image2.url
    if len(t.cor2) > 0:
        s += '#%s ' % t.cor2
    if not t.image2 and not len(t.cor2) > 0:
        s += 'none'
    s += ';'
    if t.larg4 > 0:
        s += 'border-bottom: %dpx solid #%s;' % (t.larg4, t.cor15)
    else:
        s += 'border-bottom: none;'
    s += '}'

    s += '#highlights {'
    s += 'background: '
    if t.image5:
        s += 'url("%s") ' % t.image5.url
    if len(t.cor22) > 0:
        s += '#%s ' % t.cor22
    if not t.image5 and not len(t.cor22) > 0:
        s += 'none'
    s += ';'
    if t.larg7 > 0:
        s += 'border-top: %dpx solid #%s;' % (t.larg7, t.cor23)
    else:
        s += 'border-top: none;'
    if t.larg8 > 0:
        s += 'border-bottom: %dpx solid #%s;' % (t.larg8, t.cor24)
    else:
        s += 'border-bottom: none;'
    s += '}'

    s += '#header #search button {'
    if (t.image4 and len(t.cor20) > 0) or (t.image4 and not len(t.cor20) > 0):
        s += 'background: '
        s += 'url("%s") no-repeat center ' % t.image4.url
    if t.image4 and len(t.cor20) > 0:
        s += '#%s' % t.cor20
    if not t.image4 and len(t.cor20) > 0:
        s += 'background-color: '
        s += '#%s ' % t.cor20
    if not t.image4 and not len(t.cor20) > 0:
        s += 'background: '
        s += 'none'
    s += ';'
    s += '}'
    
    s += '#header #search input {'
    if t.larg11 > 0:
        s += 'border: %dpx solid #%s;' % (t.larg11, t.cor39)
    else:
        s += 'border: 0 none;'
    s += '}'
    
    s += '#header .sub_pesquisa {'
    if len(t.cor40) > 0:
        s += 'color: #%s;' % t.cor40
    s += '}'

    s += '#header #menu {'
    if len(t.cor3) > 0:
        s += 'background-color: #%s;' % t.cor3
    if t.larg5 > 0:
        s += 'border: %dpx solid #%s;' % (t.larg5, t.cor17)
    else:
        s += 'border: none;'
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

    s += '#content {'
    if t.larg9 > 0:
        s += 'border-top: %dpx solid #%s;' % (t.larg9, t.cor25)
    else:
        s += 'border-top: none;'
    if t.larg10 > 0:
        s += 'border-bottom: %dpx solid #%s;' % (t.larg10, t.cor26)
    else:
        s += 'border-bottom: none;'
    s += '}'

    s += '#footer {'
    if len(t.cor5) > 0:
        s += 'color: #%s;' % t.cor5
    s += 'background: '
    if len(t.cor4) > 0:
        s += '#%s ' % t.cor4
    if t.image3:
        s += 'url("%s") ' % t.image3.url
    if not t.image3 and not len(t.cor4) > 0:
        s += 'none'
    s += ';'
    if t.larg6 > 0:
        s += 'border-top: %dpx solid #%s;' % (t.larg6, t.cor21)
    else:
        s += 'border-top: none;'
    s += '}'

    s += '#content .bar, '
    s += '.path .back {'
    if len(t.cor7) > 0:
        s += 'color: #%s;' % t.cor7
    if len(t.cor6) > 0:
        s += 'background-color: #%s;' % t.cor6
    s += '}'
    
    s += '#content .barra_parceiros {'
    if len(t.cor38) > 0:
        s += 'color: #%s;' % t.cor38
    elif len(t.cor7) > 0:
        s += 'color: #%s;' % t.cor7
    if len(t.cor37) > 0:
        s += 'background-color: #%s;' % t.cor37
    elif len(t.cor6) > 0:
        s += 'background-color: #%s;' % t.cor6
    s += '}'

    s += '#content ul.category li a {'
    if len(t.cor32) > 0:
        s += 'background-color: #%s;' % t.cor32
    else:
        s += 'background: none;'
    s += '}'

    s += '#content ul.category li a:hover {'
    if len(t.cor31) > 0:
        s += 'background-color: #%s;' % t.cor31
    else:
        s += 'background: none;'
    s += '}'

    s += '#content ul.category li div {'
    if t.larg1 > 0:
        s += 'border: %dpx solid #%s;' % (t.larg1, t.cor12)
    else:
        s += 'border: none;padding: 0;'
    s += '}'

    s += '#content ul.category li h2 {'
    if t.larg2 > 0:
        s += 'font-size: %dpx;' % t.larg2
    if len(t.cor13) > 0:
        s += 'color: #%s;' % t.cor13
    s += '}'

    s += '#login form label {'
    if len(t.cor13) > 0:
        s += 'color: #%s;' % t.cor13
    s += '}'

    s += '.buttom {'
    if len(t.cor27) > 0:
        s += 'background-color: #%s;' % t.cor27
    if len(t.cor28) > 0:
        s += 'color: #%s;' % t.cor28
    s += '}'

    s += '.buttom:hover {'
    if len(t.cor29) > 0:
        s += 'background-color: #%s;' % t.cor29
    if len(t.cor30) > 0:
        s += 'color: #%s;' % t.cor30
    s += '}'

    s += 'h3, .box-title {'
    if len(t.cor13) > 0:
        s += 'color: #%s;' % t.cor13
    s += '}'

    s += '.flex-control-nav li a {'
    if len(t.cor34) > 0:
        s += 'color: #%s;' % t.cor34
    s += '}'

    s += '.flex-control-nav li a.active {'
    if len(t.cor35) > 0:
        s += 'color: #%s;' % t.cor35
    s += '}'

    s += '.flex-control-nav li a:hover {'
    if len(t.cor36) > 0:
        s += 'color: #%s;' % t.cor36
    s += '}'

    s += '.path a, .path {'
    if len(t.cor6) > 0:
        s += 'color: #%s;' % t.cor6
    s += '}'

    if len(t.custom) > 0:
        s += '\n\n'
        s += '%s' % t.custom

    return s