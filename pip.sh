#!/bin/bash

URL='10.0.1.133'
PASS='deploy'

cd /tmp
/usr/bin/expect <<EOD
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/virtualenvwrapper.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "continue connecting" {
        	send "yes\r"
            exp_continue
            exit 0
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

if [ $? == 1 ]; then
echo "erro, vamos tentar pela rede interna"
URL='200.195.168.7'
/usr/bin/expect <<EOD
	set timeout 120
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/virtualenvwrapper.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "continue connecting" {
        	send "yes\r"
            exp_continue
            exit 0
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD
fi

cd virtualenvwrapper
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import virtualenvwrapper'
echo "virtualenvwrapper >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install virtualenvwrapper


export WORKON_HOME=/var/www/tcd_offline/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv tcd

workon tcd


cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/yolk.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd yolk
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import yolk'
echo "yolk >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install yolk

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import django'
echo "django >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install Django==1.3.2

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-simple-captcha.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-simple-captcha
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import captcha'
echo "captcha >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install django-simple-captcha

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-mobile.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-mobile
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import django_mobile'
echo "django_mobile >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install django_mobile

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/south.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd south
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import south'
echo "south >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install south

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/mysql-python.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd mysql-python
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

echo "mysql-python >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install MySQL-python

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-ckeditor.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-ckeditor
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

echo "django-ckeditor >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install django-ckeditor

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-crequest.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-crequest
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import crequest'
echo "crequest >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install django-crequest

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/BeautifulSoup.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd BeautifulSoup
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import BeautifulSoup'
echo "BeautifulSoup >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install BeautifulSoup

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/flup.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd flup
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import flup'
echo "flup >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install flup

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-flash.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-flash
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import djangoflash'
echo "djangoflash >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install django-flash

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-tagging.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-tagging
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import tagging'
echo "tagging >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install django-tagging

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/PIL.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd PIL
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import PIL; import Image'
echo "PIL >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install PIL

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/ReportLab.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd ReportLab
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import reportlab'
echo "reportlab >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install reportlab

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/simplejson.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd simplejson
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import simplejson'
echo "simplejson >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install simplejson

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/cython.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd cython
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import cython'
echo "cython >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install "Cython>=0.17.3"

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/lxml.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd lxml
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import lxml'
echo "lxml >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install lxml

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/PyAMF.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd PyAMF
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import pyamf'
echo "pyamf >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install pyamf

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-grappelli.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-grappelli
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import grappelli'
echo "grappelli >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

### pip install django-grappelli

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-colors.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-colors
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import colors'
echo "colors >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

cd /tmp
/usr/bin/expect <<EOD
	set timeout 600
    spawn /bin/sh -c "git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-admin-tools.git"
    expect {
        timeout {
            exit 1
        }
        -re "lost" {
            exit 1
        }
        -re "No route to host" {
            exit 1
        }
        -re "deploy@$URL's password:" {
            send "$PASS\r"
            exp_continue
            exit 0
        }
    }
EOD

cd django-admin-tools
python setup.py install

echo ">>>>>>>>>>>>>>>>>>>>>>"

python -c 'import admin_tools'
echo "admin_tools >> ok"

echo "<<<<<<<<<<<<<<<<<<<<<<"

