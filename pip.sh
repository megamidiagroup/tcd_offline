#!/bin/bash

export WORKON_HOME=/var/www/tcd_offline/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv tcd

workon tcd

pip install yolk
pip install Django==1.3.2
pip install django-simple-captcha
pip install django_mobile
pip install south
pip install state
pip install MySQL-python
pip install django-ckeditor
pip install django-crequest
pip install BeautifulSoup

cd /tmp
git clone https://github.com/guillaumeesquevin/django-colors.git
cd django-colors
python setup.py install

cd /tmp
git clone https://github.com/coxmediagroup/django-admin-tools.git
cd django-admin-tools
python setup.py install