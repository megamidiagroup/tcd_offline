#!/bin/bash

export WORKON_HOME=/var/www/tcd_offline/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv tcd

workon tcd

URL='200.195.168.7'

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/yolk.git
if [ $? -ne 0 ]; then
    echo "erro, vamos tentar pela rede interna"
    URL='10.0.1.133'
    git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/yolk.git
fi
cd yolk
python setup.py install

### pip install yolk

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django.git
cd django
python setup.py install

### pip install Django==1.3.2

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-simple-captcha.git
cd django-simple-captcha
python setup.py install

### pip install django-simple-captcha

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-mobile.git
cd django-mobile
python setup.py install

### pip install django_mobile

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/south.git
cd south
python setup.py install

### pip install south

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/mysql-python.git
cd mysql-python
python setup.py install

### pip install MySQL-python

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-ckeditor.git
cd django-ckeditor
python setup.py install

### pip install django-ckeditor

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-crequest.git
cd django-crequest
python setup.py install

### pip install django-crequest

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/BeautifulSoup.git
cd BeautifulSoup
python setup.py install

### pip install BeautifulSoup

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/flup.git
cd flup
python setup.py install

### pip install flup

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-flash.git
cd django-flash
python setup.py install

### pip install django-flash

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-tagging.git
cd django-tagging
python setup.py install

### pip install django-tagging

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/PIL.git
cd PIL
python setup.py install

### pip install PIL

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/ReportLab.git
cd ReportLab
python setup.py install

### pip install reportlab

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/simplejson.git
cd simplejson
python setup.py install

### pip install simplejson

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/cython.git
cd cython
python setup.py install

### pip install "Cython>=0.17.3"

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/lxml.git
cd lxml
python setup.py install

### pip install lxml

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/pyamf.git
cd pyamf
python setup.py install

### pip install pyamf

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-grappelli.git
cd django-grappelli
python setup.py install

### pip install django-grappelli

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-colors.git
cd django-colors
python setup.py install

cd /tmp
git clone ssh://deploy@$URL/var/django/tcd_offline/dependences/django-admin-tools.git
cd django-admin-tools
python setup.py install

