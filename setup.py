# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys

try:
    project  = sys.argv[1]
except:
    project  = 'tcd_offline'

try:
    password = sys.argv[2]
except:
    password = '12345678'
    
try:
    install  = sys.argv[3]
except:
    install  = ''

if install and install == '--install':
    print 'preparando para instalar'
    
    os.system('')
    
    sys.exit('stop')


os.system('mysql -u root -p%s %s < /var/www/tcd.sql' % (password, project))

print 'sync db tcd.sql'

os.system('mysql -u root -p%s megavideo_%s < /var/www/megavideo.sql' % (password, project.split('_')[1]))

print 'sync db megavideo.sql'