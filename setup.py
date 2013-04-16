# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys
import subprocess
import compileall
import random
import string
import httplib
import urllib

from subprocess import Popen, PIPE
from datetime import datetime as dt

MODPATH = os.path.abspath(os.path.dirname(__file__))

url = 'www.treinandoequipes.com.br'

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
    action   = sys.argv
except:
    action   = 'no-actions'
    

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
    
sh = Sh()

try:
    conn = httplib.HTTPSConnection(url)
    conn.request("GET", "/login/")
    r1   = conn.getresponse()
    if not r1.reason == 'OK' or not r1.status == 200:
        sys.exit('Sem conexao internet')
    conn.close()
except:
    sys.exit('Sem conexao internet')
    

if action.count('--install') == 1 or action.count('--upgrade') == 1:
    print 'preparando para instalar'
    
    os.system('apt-get update')
    
    list_program = ['mysql-client', 'mysql-server', 'nginx', 'vim', 'python-virtualenv', \
                    'python-setuptools', 'python-pip', 'expect', 'libxml2-dev', 'libxslt1-dev', \
                    'python-lxml', 'ssh', 'python-alsaaudio']

    os.system('apt-get install -y %s' % ' '.join(list_program))
    
    os.system('apt-get build-dep -y python-mysqldb')
    
    os.system('apt-get update')
    
    os.system('echo "CREATE DATABASE IF NOT EXISTS %s;" | mysql -u root -p%s' % (project, password))
    
    os.system('echo "CREATE DATABASE IF NOT EXISTS megavideo_%s;" | mysql -u root -p%s' % (project.split('_')[1], password))

    if action.count('--upgrade') == 1 and os.path.isdir('/var/www/tcd_offline'):
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
        compileall.compile_dir("/var/www/tcd_offline", force=1)
        os.system('rm -r /var/www/tcd_offline/urls.py /var/www/tcd_offline/settings.py /var/www/tcd_offline/Makefile /var/www/tcd_offline/__init__.py /var/www/tcd_offline/global_settings.py /var/www/tcd_offline/sql_offline.py /var/www/tcd_offline/context_processor.py')
        os.system('find /var/www/tcd_offline/mega/ -name \*\.py -exec rm {} \; -print')
        os.system('find /var/www/tcd_offline/megavideo/ -name \*\.py -exec rm {} \; -print')
        os.system('find /var/www/tcd_offline/monkey_patch/ -name \*\.py -exec rm {} \; -print')
        os.system('find /var/www/tcd_offline/relatorio/ -name \*\.py -exec rm {} \; -print')
        os.system('find /var/www/tcd_offline/state/ -name \*\.py -exec rm {} \; -print')

    sh.find('/etc/nginx/nginx.conf -type f -exec sed -i "s/www-data/root/g" {} \;')
    
    sh.cp('%s/tcd_offline /etc/nginx/sites-enabled/tcd_offline' % MODPATH)
    
    if os.path.islink('/etc/nginx/sites-enabled/default'):
        os.system('rm /etc/nginx/sites-enabled/default')
          
    sh.cp('%s/tcd /etc/init.d/tcd' % MODPATH)
    
    if not os.path.isdir('/var/log/megavideo'):        
        sh.mkdir('/var/log/megavideo')
        
    if not os.path.isdir('/var/log/tcd'):
        sh.mkdir('/var/log/tcd')
    
    os.system('/etc/init.d/tcd')
    
    os.system('/etc/init.d/nginx restart')
    
    sh.cp('%s/sync /var/www/tcd_offline/sync.sh' % MODPATH)
    sh.cp('%s/ftp /var/www/tcd_offline/ftp.sh' % MODPATH)
    
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<user>/%s/g" {} \;' % user)
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<project>/%s/g" {} \;' % project)
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<rede>/%s/g" {} \;' % rede)
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<password>/%s/g" {} \;' % password)

    if len(sh.grep('-ir "/var/www/tcd_offline/sync.sh" /etc/crontab')) == 0:
        os.system('echo "00 00 * * * root (cd / && /var/www/tcd_offline/sync.sh >> /var/log/tcd/sync.log 2>&1)" >> /etc/crontab')
        
    if len(sh.grep('-ir "(exec /etc/init.d/tcd)" /etc/rc.local')) == 0:
        sh.find('/etc/rc.local -type f -exec sed -i "s/exit 0//g" {} \;')
        os.system('echo "(exec /etc/init.d/tcd)" >> /etc/rc.local')
        os.system('echo "exit 0" >> /etc/rc.local')
    
    my   = open('/etc/mysql/my.cnf', 'r')
    read = my.read()
    if read.count('#general_log_file        = /var/log/mysql/mysql.log') > 0:
        my   = open('/etc/mysql/my.cnf', 'w')
        str = read.replace('#general_log_file        = /var/log/mysql/mysql.log', 'log = /var/log/mysql/mysql.log')
        my.write(str)
        my.close()
        os.system('/etc/init.d/mysql restart')
        
    os.system('sudo chmod 661 /var/www -R')

    if action.count('--block') == 0:
        sys.exit('Terminou com sucesso! Abra o navegador e digite http://localhost ou IP da maquina.')
    print 'Terminou com sucesso! Abra o navegador e digite http://localhost ou IP da maquina.'
 

if action.count('--pull') == 1:
    print 'atualizando scripts'
    
    sh.cp('-r /tmp/tcd_offline/* /var/www/tcd_offline/')
    sh.find('/var/www/tcd_offline/mega/views.py -type f -exec sed -i "s/rede=None/rede=\'%s\'/g" {} \;' % rede)
    compileall.compile_dir("/var/www/tcd_offline", force=1)
    os.system('rm -r /var/www/tcd_offline/urls.py /var/www/tcd_offline/settings.py /var/www/tcd_offline/Makefile /var/www/tcd_offline/__init__.py /var/www/tcd_offline/global_settings.py /var/www/tcd_offline/sql_offline.py /var/www/tcd_offline/context_processor.py')
    os.system('find /var/www/tcd_offline/mega/ -name \*\.py -exec rm {} \; -print')
    os.system('find /var/www/tcd_offline/megavideo/ -name \*\.py -exec rm {} \; -print')
    os.system('find /var/www/tcd_offline/monkey_patch/ -name \*\.py -exec rm {} \; -print')
    os.system('find /var/www/tcd_offline/relatorio/ -name \*\.py -exec rm {} \; -print')
    os.system('find /var/www/tcd_offline/state/ -name \*\.py -exec rm {} \; -print')
    
    sh.cp('%s/tcd_offline /etc/nginx/sites-enabled/tcd_offline' % MODPATH)
          
    sh.cp('%s/tcd /etc/init.d/tcd' % MODPATH)

    sh.cp('%s/sync /var/www/tcd_offline/sync.sh' % MODPATH)
    sh.cp('%s/ftp /var/www/tcd_offline/ftp.sh' % MODPATH)
    
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<user>/%s/g" {} \;' % user)
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<project>/%s/g" {} \;' % project)
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<rede>/%s/g" {} \;' % rede)
    sh.find('/var/www/tcd_offline/sync.sh -type f -exec sed -i "s/<password>/%s/g" {} \;' % password)
        
    os.system('sudo chmod 661 /var/www -R')
    
    os.system('/etc/init.d/nginx restart')
    
    os.system('/etc/init.d/tcd')
    
    sys.exit('Terminou com sucesso! O sistema foi atualizado com sucesso.')
 
    
if action.count('--block') == 1:
    print 'preparando para bloquear notebook'
    
    os.system('apt-get install -y xbindkeys flashplugin-installer')
    
    os.system('apt-get remove -y unity')
    
    os.system('mv /etc/init/tty* ~')
    os.system('mv ~/tty2.conf /etc/init/')
    
    os.system('mv /usr/share/xsessions/* ~/')
    
    sh.cp('/var/www/tcd_offline/kiosk.desktop', '/usr/share/xsessions/kiosk.desktop')
    os.system('chmod 644 /usr/share/xsessions/kiosk.desktop')
        
    if not os.path.isdir('/home/%s/.mozilla/firefox/kiosk.default' % user):    
        sh.cp('-r /var/www/tcd_offline/kiosk.default', '/home/%s/.mozilla/firefox/kiosk.default' % user)
        os.system('chmod 777 /home/%s/.mozilla/firefox/kiosk.default -R' % user)
        
    if not os.path.islink('/home/%s/.xbindkeysrc' % user):    
        os.symlink('/var/www/tcd_offline/.xbindkeysrc', '/home/%s/.xbindkeysrc' % user)
        
    os.system('sudo -i -u %s python -c "import alsaaudio; alsaaudio.Mixer().setvolume(100)"' % user)
    
    sys.exit('Terminou com sucesso! O computador está bloqueado. Reinicie o sistema.')


if not os.path.islink('/var/www/media/tcd/mega'):
    os.symlink('/var/www/tcd_offline/mega/media/mega', '/var/www/media/tcd/mega')
    
if os.path.exists('/var/www/media/tcd/icone_%s.png' % rede) and not os.path.islink('/var/www/media/tcd/mega/images/icone_%s.png' % rede):
    os.symlink('/var/www/media/tcd/icone_%s.png' % rede, '/var/www/media/tcd/mega/images/icone_%s.png' % rede)
    
if os.path.isdir('/var/www/media/tcd/mega/css/template'):
    os.system('rm -r /var/www/media/tcd/mega/css/template')
if os.path.isdir('/var/www/media/tcd/storage/template'):
    os.symlink('/var/www/media/tcd/storage/template', '/var/www/tcd_offline/mega/media/mega/css/template')

os.system('mysql -u root -p%s %s < /var/www/tcd.sql' % (password, project))

print 'sync db tcd.sql'

os.system('mysql -u root -p%s megavideo_%s < /var/www/megavideo.sql' % (password, project.split('_')[1]))

print 'sync db megavideo.sql'

os.system('chmod 661 /var/www -R')

if os.path.exists('/var/www/tcd.config'):
    sh.find('/var/www/tcd.config -type f -exec sed -i "s/&#39;/\'/g" {} \;')
    os.system("mysql -u root -p%s %s < %s" % (password, project, '/var/www/tcd.config'))
    os.system('echo "" > /var/log/mysql/mysql.log')
    hash = '%s_%s' % ( dt.strftime(dt.now(), '%Y%m%d_%H%M'), ''.join(random.sample((string.ascii_uppercase + string.digits)*8,8)) )
    mail = '0'
    arquivo_mail = ''
    if os.path.exists('/var/www/mail.config'):
        mail = '1'
        arquivo_mail = '%s_mail.config' % hash
    os.system('/var/www/tcd_offline/ftp.sh %s %s %s' % (rede, mail, hash))
    params  = urllib.urlencode({'sql_config': '%s_tcd.config' % hash, 'mail_config': arquivo_mail})
    r1      = urllib.urlopen("https://%s/%s/sync?%s" % (url, rede, params))
    if r1.read() == rede:
        os.system('rm /var/www/%s_tcd.config' % hash)
        os.system('echo "" > /var/www/tcd.config')
        if len(arquivo_mail) > 2:
            os.system('rm /var/www/%s_mail.config' % hash)
            os.system('echo "" > /var/www/mail.config')
    else:
        os.system('echo "CRITICAL: ERRO FATAL NO SINCRONISMO SYNC DO CLIENTE" >> /var/log/tcd/log.debug')
    conn.close()
        
if os.path.exists('/var/www/requirements.config'):
    arquivo = open('/var/www/requirements.config', 'r').read()
    lines   = arquivo.split('\n')
    for line in lines:
        os.system("%s" % line)

