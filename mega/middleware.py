from django.conf import settings
from django.contrib import auth

from models import *

from datetime import datetime, timedelta

import re

class AutoLogout:
  def process_request(self, request):
    if not request.user.is_authenticated() :
      #Can't log out if not logged in
      return

    try:
      if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        auth.logout(request)
        del request.session['last_touch']
        return
    except KeyError:
      pass

    request.session['last_touch'] = datetime.now()

    
prefix = settings.LIST_VARS.get('rede_prefix', 'rede')
prefix_regex = re.compile('/' + prefix + '/(?P<rede>.[^/]+)/(?P<realurl>.*)')

class RedeMiddleware(object):
    def process_request(self, request):
        match = prefix_regex.search(request.path)
        
        if match and not 'add' in match.groupdict()['rede'] and not match.groupdict()['rede'].isdigit():
            d = match.groupdict()
            c = None

            realurl = '/' + d['realurl']
            if realurl[-1] != '/':
                realurl += '/'

            if not 'admin' in d['rede']:
                try:
                    c = Rede.objects.get(link = d['rede'])
                except:
                    pass

            request.session['rede'] = c
            request.path            = realurl
            request.path_info       = realurl
            request.rede            = c
            
        else:
            
            try:
                request.rede = request.session['rede']
            except:
                request.rede = None
