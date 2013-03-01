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
pip install django-admin-tools