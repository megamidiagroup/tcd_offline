# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys

from subprocess import Popen, PIPE

MODPATH = os.path.abspath(os.path.dirname(__file__))

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
    

class Cmd(object):
    def __init__(self, cmd):
        self.cmd = cmd
    def __call__(self, *args):
        command = '%s %s' % (self.cmd, ' '.join(args))
        result = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        return result.communicate()[0]


class Sh(object):
    def __getattr__(self, attribute):
        return Cmd(attribute)


if install and install == '--install':
    print 'preparando para instalar'
    
    sh = Sh()
    
    list_program = ['mysql-client', 'mysql-server', 'nginx', 'vim']

    os.system('sudo apt-get install %s' % ' '.join(list_program))
    
    if not os.path.isdir('/var/www/'):
        sh.mkdir('/var/www/')
        sh.cp(' -r %s /var/www/tcd_offline' % MODPATH)

    sh.find('/etc/nginx/nginx.conf -type f -exec sed -i "s/www-data/root/g" {} \;')
    
    sh.cp('%s/tcd_offline /etc/nginx/sites-enabled/tcd_offline' % MODPATH)
    
    if os.path.islink('/etc/nginx/sites-enabled/default'):
        os.system('sudo rm /etc/nginx/sites-enabled/default')
        
    sh.cp('%s/tcd /etc/init.d/tcd' % MODPATH)
    
    os.system('sudo /etc/init.d/tcd')
    
    os.system('sudo /etc/init.d/nginx restart')
    
    sys.exit('Terminou com sucesso! Abra o navegador e digite http://localhost ou IP da maquina.')


os.system('mysql -u root -p%s %s < /var/www/tcd.sql' % (password, project))

print 'sync db tcd.sql'

os.system('mysql -u root -p%s megavideo_%s < /var/www/megavideo.sql' % (password, project.split('_')[1]))

print 'sync db megavideo.sql'