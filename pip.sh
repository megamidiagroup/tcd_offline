#!/bin/bash

export WORKON_HOME=/var/www/tcd_offline/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv tcd

workon tcd

pip install yolk Django==1.3.2 django-simple-captcha django_mobile south state MySQL-python \
				django-ckeditor django-crequest BeautifulSoup flup django-flash django-tagging \
					PIL reportlab simplejson lxml pyamf django-grappelli

cd /tmp
git clone https://github.com/guillaumeesquevin/django-colors.git
cd django-colors
python setup.py install

cd /tmp
git clone https://github.com/coxmediagroup/django-admin-tools.git
cd django-admin-tools
python setup.py install