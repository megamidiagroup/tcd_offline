from global_settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default']['USER'] = 'root'
DATABASES['default']['PASSWORD'] = '<password>'
if 'password' in DATABASES['default']['PASSWORD']:
    DATABASES['default']['PASSWORD'] = '12345678'

DATABASES['megavideo']['USER'] = 'root'
DATABASES['megavideo']['PASSWORD'] = '<password>'
if 'password' in DATABASES['megavideo']['PASSWORD']:
    DATABASES['megavideo']['PASSWORD'] = '12345678'