# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import subprocess

from subprocess import Popen, PIPE

MODPATH = os.path.abspath(os.path.dirname(__file__))

try:
    user     = sys.argv[1]
except:
    sys.exit("Parametro 1: digite o usuario da maquina")

try:
    project  = sys.argv[2]
except:
    project  = 'tcd_offline'

try:
    password = sys.argv[3]
except:
    password = '12345678'
    
try:
    install  = sys.argv[4]
except:
    install  = ''
    
try:
    upgrade  = sys.argv[5]
except:
    upgrade  = ''
    

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
    
    list_program = ['mysql-client', 'mysql-server', 'nginx', 'vim', 'python-virtualenv', \
                    'python-setuptools', 'python-pip', 'expect']

    os.system('apt-get install %s' % ' '.join(list_program))
    
    os.system('apt-get build-dep python-mysqldb')

    if upgrade and upgrade == '--upgrade' and os.path.isdir('/var/www/tcd_offline'):
        sh.rm('-r /var/www/tcd_offline')
    
    if not os.path.isdir('/var/www/'):        
        sh.mkdir('/var/www/')
        if not os.path.isdir('/var/www/tcd_offline'):        
            sh.mkdir('/var/www/tcd_offline')
        sh.cp(' -r %s /var/www/tcd_offline' % MODPATH)
        os.system('easy_install -U virtualenv south')
        if not os.path.exists('/usr/local/bin/virtualenvwrapper.sh'):
            os.system('cd /tmp/; git clone https://github.com/bernardofire/virtualenvwrapper.git; cd virtualenvwrapper; python setup.py install')
            
        os.system('./pip.sh')
        os.system('chmod 775 /home/%s/.virtualenvs/hook.log' % user)
        os.system('chown root:%s /home/%s/.virtualenvs/hook.log' % (user, user))
        
    sh.find('/etc/nginx/nginx.conf -type f -exec sed -i "s/www-data/root/g" {} \;')
    
    sh.cp('%s/tcd_offline /etc/nginx/sites-enabled/tcd_offline' % MODPATH)
    
    if os.path.islink('/etc/nginx/sites-enabled/default'):
        os.system('rm /etc/nginx/sites-enabled/default')
        
    os.system('echo "CREATE DATABASE IF NOT EXISTS %s;" | mysql -u root -p%s' % (project, password))
    
    os.system('echo "CREATE DATABASE IF NOT EXISTS megavideo_%s;" | mysql -u root -p%s' % (project.split('_')[1], password))
        
    sh.cp('%s/tcd /etc/init.d/tcd' % MODPATH)
    
    if not os.path.isdir('/var/log/megavideo'):        
        sh.mkdir('/var/log/megavideo')
        
    if not os.path.isdir('/var/log/tcd'):
        sh.mkdir('/var/log/tcd')
    
    os.system('/etc/init.d/tcd')
    
    os.system('/etc/init.d/nginx restart')
    
    sys.exit('Terminou com sucesso! Abra o navegador e digite http://localhost ou IP da maquina.')


if not os.path.islink('/var/www/media/tcd/mega'):
    os.symlink('/var/www/tcd_offline/mega/media/mega', '/var/www/media/tcd/mega')
    
if not os.path.islink('/var/www/media/tcd/mega'):
    os.symlink('/var/www/tcd_offline/mega/media/ckeditor', '/var/www/media/tcd/ckeditor')
    
if not os.path.islink('/var/www/media/tcd/mega'):
    os.symlink('/var/www/tcd_offline/mega/media/admin_tools', '/var/www/media/tcd/admin_tools')

os.system('mysql -u root -p%s %s < /var/www/tcd.sql' % (password, project))

print 'sync db tcd.sql'

os.system('mysql -u root -p%s megavideo_%s < /var/www/megavideo.sql' % (password, project.split('_')[1]))

print 'sync db megavideo.sql'