# -*- coding: utf-8 -*-
#!/usr/bin/env python

import httplib
import urllib2
import sys
import os
import urllib

try:
    rede = sys.argv[1]
except:
    sys.exit("Parametro 1: digite a rede")
    
url  = 'http://10.0.1.95'
file = '/var/www/tcd.config'

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

