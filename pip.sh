#!/bin/bash

export WORKON_HOME=/var/www/tcd_offline/.virtualenvs

source /usr/local/bin/virtualenvwrapper.sh

mkvirtualenv tcd

pip install yolk Django==1.3.2 django-simple-captcha