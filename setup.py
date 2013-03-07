# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import subprocess
import compileall

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
    rede     = sys.argv[3]
except:
    rede     = 'tcd'

try:
    password = sys.argv[4]
except:
    password = '12345678'
    
try:
    install  = sys.argv[5]
except:
    install  = ''
    
try:
    upgrade  = sys.argv[6]
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
    
    os.system('apt-get update')
    
    list_program = ['mysql-client', 'mysql-server', 'nginx', 'vim', 'python-virtualenv', \
                    'python-setuptools', 'python-pip', 'expect', 'libxml2-dev', 'libxslt1-dev', \
                    'python-lxml']

    os.system('apt-get install %s' % ' '.join(list_program))
    
    os.system('apt-get build-dep python-mysqldb')
    
    os.system('apt-get update')

    if upgrade and upgrade == '--upgrade' and os.path.isdir('/var/www/tcd_offline'):
        sh.rm('-r /var/www/tcd_offline')
    
    if not os.path.isdir('/var/www/'):        
        sh.mkdir('/var/www/')
    if not os.path.isdir('/var/www/tcd_offline'):        
        sh.mkdir('/var/www/tcd_offline')
        sh.cp(' -r %s /var/www/' % MODPATH)
        os.system('easy_install -U virtualenv south lxml pyamf')
        os.system('./pip.sh')
        os.system('chmod 775 /var/www/tcd_offline/.virtualenvs/hook.log')
        os.system('chown root:%s /var/www/tcd_offline/.virtualenvs/hook.log' % user)
        sh.find('/var/www/tcd_offline/mega/views.py -type f -exec sed -i "s/rede=None/rede=\'%s\'/g" {} \;' % rede)
        compileall.compile_dir("../tcd_offline", force=1)
        os.system('rm -r /var/www/tcd_offline/urls.py /var/www/tcd_offline/settings.py /var/www/tcd_offline/Makefile /var/www/tcd_offline/__init__.py /var/www/tcd_offline/global_settings.py /var/www/tcd_offline/context_processor.py')
        os.system('find /var/www/tcd_offline/mega/ -name \*\.py -exec rm {} \; -print')
        os.system('find /var/www/tcd_offline/megavideo/ -name \*\.py -exec rm {} \; -print')
        os.system('find /var/www/tcd_offline/monkey_patch/ -name \*\.py -exec rm {} \; -print')
        os.system('find /var/www/tcd_offline/relatorio/ -name \*\.py -exec rm {} \; -print')
        os.system('find /var/www/tcd_offline/state/ -name \*\.py -exec rm {} \; -print')

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
    
    sh.cp('%s/sync /var/www/tcd_offline/sync.sh' % MODPATH)
    
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<rede>/%s/g" {} \;' % rede)

    if len(sh.grep('-ir "/etc/init.d/tcd" /etc/rc.local')) == 0:
        sh.find('/etc/rc.local -type f -exec sed -i "s/exit\ 0//g" {} \;')
        os.system('echo "(exec /etc/init.d/tcd)" >> /etc/rc.local; echo "exit 0" >> /etc/rc.local')
    
    if len(sh.grep('-ir "/var/www/tcd_offline/sync.sh" /etc/crontab')) == 0:
        os.system('echo "00 00 * * * root (cd / && /var/www/tcd_offline/sync.sh >> /var/log/tcd/sync.log 2>&1)" >> /etc/crontab')

    sys.exit('Terminou com sucesso! Abra o navegador e digite http://localhost ou IP da maquina.')


if not os.path.islink('/var/www/media/tcd/mega'):
    os.symlink('/var/www/tcd_offline/mega/media/mega', '/var/www/media/tcd/mega')
    
if not os.path.islink('/var/www/media/tcd/ckeditor'):
    os.symlink('/var/www/tcd_offline/mega/media/ckeditor', '/var/www/media/tcd/ckeditor')
    
if not os.path.islink('/var/www/media/tcd/admin_tools'):
    os.symlink('/var/www/tcd_offline/mega/media/admin_tools', '/var/www/media/tcd/admin_tools')

os.system('mysql -u root -p%s %s < /var/www/tcd.sql' % (password, project))

print 'sync db tcd.sql'

os.system('mysql -u root -p%s megavideo_%s < /var/www/megavideo.sql' % (password, project.split('_')[1]))

print 'sync db megavideo.sql'

os.system('sudo chmod 660 /var/www -R')