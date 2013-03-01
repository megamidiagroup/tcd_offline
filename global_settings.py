# -*- coding: utf-8 -*-
# Django settings for tuto_app project.

import os

MODPATH = os.path.abspath(os.path.dirname(__file__))
abspath = lambda path: os.path.join(MODPATH, path)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Rafael', 'rafael.feijo@megamidia.com.br'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.mysql',
        'NAME'     : 'tcd_offline',             
        'USER'     : '',                   
        'PASSWORD' : '',                 
        'HOST'     : 'localhost',
        'PORT'     : '',                
    },
    'megavideo': {
        'ENGINE'   : 'django.db.backends.mysql',
        'NAME'     : 'megavideo_offline',             
        'USER'     : '',                   
        'PASSWORD' : '',                 
        'HOST'     : 'localhost',
        'PORT'     : '',                
    }          
}

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-br'
SITE_ID = 1
USE_I18N = True

MEDIA_ROOT = '/var/www/media/'
MEDIA_URL = 'http://localhost/media/'
MEDIA_STATIC = MEDIA_URL
ADMIN_MEDIA_PREFIX = MEDIA_URL + 'admin/'
STATIC_URL = MEDIA_URL + 'tcd/'
STATIC_DOC_ROOT = '../media/'
ADMIN_MEDIA_URL = ''

UPLOAD_STORAGE_DIR = '../media/tcd/storage/'

SECRET_KEY = 'z$(jn12v73nqz539xpr(-#8gjet7)3%_dc)4=j&h2t&@+i81_$tcd_dev'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
    'django.template.loaders.filesystem.Loader',
    'django_mobile.loader.Loader',
)

MIDDLEWARE_CLASSES = (
    'crequest.middleware.CrequestMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'mega.middleware.AutoLogout',
    'mega.middleware.RedeMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django_mobile.context_processors.flavour',
    'tcd_offline.context_processor.static_url',
)

ROOT_URLCONF = 'tcd_offline.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #'./templates',
)

INSTALLED_APPS = (
    'monkey_patch',
    'crequest',
    'ckeditor',
    'colors',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    #'gunicorn',
    'state',
    'tcd_offline.mega',
    'tcd_offline.relatorio',
    'south',
    'django_mobile',
    'captcha',
)

LIST_VARS = {
    'base_url'     : 'http://localhost/',
    'from_email'   : 'rafael.feijo@megamidia.com.br',
    'log'          : '/var/www/logging/tcd_dev.log',
    'log_start'    : True,
	'rede_prefix'  : 'rede',
	'rtmp'         : 'treinandoequipes.com.br:1935/live',
    'log_file'     : '/var/log/tcd/log.debug',
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Configurações
GRAPPELLI_ADMIN_TITLE = 'TCD - Gerenciador de Conteúdo'

PROJECT_URL = 'tcd_offline.'

APP_DIR = '/var/www/tcd_offline/'

LOGIN_URL = '/login/'

# MAIL
DEFAULT_FROM_EMAIL = 'silomegamidia@gmail.com'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'silomegamidia@gmail.com'
EMAIL_HOST_PASSWORD = 'pt36uzkt'
EMAIL_PORT = 587
EMAIL_SUBJECT_PREFIX = u'[TCD]'
EMAIL_USE_TLS = True

CKEDITOR_UPLOAD_PATH = '/var/www/tcd_offline/mega/media/storage/uploads'

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 200,
        'width': 700,
        },
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/www/django_cache',
        'TIMEOUT': 0, ##60 * 5,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

AUTO_LOGOUT_DELAY = 10000 # minutos inativo == logout

FACEBOOK_APP_ID = {
                    'sala4' : '198334286958308' ## teste do fulano de tal
}

PAGSEGURO_CONF = {
                    'email_cobranca'  : 'rafael.feijo@megamidia.com.br',
                    'token'           : 'C68D3949A86F4ABAA18AB44586C9CC17',
                    'StatusTransacao' : 'Completo'
}

STORAGE     = '/var/www/tcd_offline/mega/media/storage/'

### MEGAVIDEO CONFIGURACOES

MV_TVNAME   = 'megavideo'
MV_TVDOMAIN = 'localhost/megavideo'
TV_NAME     = 'Megavideo - TCD'

APPEND_SLASH = True
DEFAULT_CHARSET = 'utf-8'

INSTALLED_APPS += (
    'tcd_offline.megavideo',
)

MEGAVIDEO_CONF = {
    'tv_name' : MV_TVNAME,
    'channel_prefix' : 'home',
    'object_type': 'Video',
    'base_url' : 'http://' + MV_TVDOMAIN + '/',
    'domain' : MV_TVDOMAIN,
    'tmp' : '/tmp/',
    'default_tv' : 'TV',
    'default_channel' : 'tcd',
    'log_file' : '/var/log/megavideo/log.debug',
    'default_class' : 'default',
    'video_storage' : '/var/www/tcd_offline/megavideo/media/storage/videos',
    'dispatch' : '/var/www/mega-lib/bin/dispatch',
    'email': 'rafael.feijo@megamidia.com.br',
    'sec_link' : False,
    'urlencode_legacy' : True,
    'thumbnail' : {'width' : '640', 'height' : '360', 'maintain_ar' : True},
    'transcodes' : {
        'Mp4High' : {
            'vcodec': 'libx264',
            'br': '350k',
            'bt' : '400k',
            'width' : '1280',
            'height' : '720',
            'qmax' : '35',
            'maintain_ar' : True,
            'acodec': 'libfaac',
            'multipass' : False,
            'extension' : 'mp4',
            'threads' : '4',
            'ar' : '44100',
            'ab' : '48k'
        }, 
        'Mp4Medium' : {
            'vcodec': 'libx264',
            'br': '250k',
            'bt' : '300k',
            'width' : '640',
            'height' : '360',
            'qmax' : '37',
            'maintain_ar' : True,
            'acodec': 'libfaac',
            'multipass' :False,
            'extension' : 'mp4',
            'threads' : '4',
            'ar' : '44100',
            'ab' : '48k'
        },
        'Mp4Low' : {
            'vcodec': 'libx264',
            'br': '150k',
            'bt' : '200k', 
            'width' : '426',
            'height' : '240',
            'qmax' : '40',
            'maintain_ar' : True,
            'acodec': 'libfaac',
            'multipass' :False,
            'extension' : 'mp4',
            'threads' : '4',
            'ar' : '44100',
            'ab' : '48k'
        },
        'WebM' : {},
        'Ogv'  : {},
    },
}

TEMPLATE_DIRS += (
    '/var/www/tcd_offline/megavideo/templates/',
    '/var/www/tcd_offline/megavideo/portal/templates/',
    '/var/www/tcd_offline/megavideo/manager/templates/',
    '/var/www/tcd_offline/megavideo/api/templates/',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'megavideo.common.context.static',     
    'djangoflash.context_processors.flash',
    'megavideo.common.context.request',
    'megavideo.common.context.client_css',
    'megavideo.common.context.client_js',
)

FLASH_IGNORE_MEDIA = True
FLASH_STORAGE = 'session'

AUTH_PROFILE_MODULE = 'video.UserProfile'

MIDDLEWARE_CLASSES += (
    'django.middleware.doc.XViewMiddleware',
    'djangoflash.middleware.FlashMiddleware',
    'megavideo.common.middleware.VFlowMiddlewareDispatcher',
    'megavideo.breadcrumbs.middleware.BreadcrumbsMiddleware',
)

BREADCRUMBS = True
BREADCRUMBS_AUTO_HOME = False

#sorl.thumbnail
THUMBNAIL_PREFIX = 'thumb_'
THUMBNAIL_QUALITY = 85


THUMBNAIL_PROCESSORS = (
    # Default processors
    'sorl.thumbnail.processors.scale_and_crop',
    'sorl.thumbnail.processors.filters',
)

GEOIP_PATH = '/var/www/tcd_offline/geoip'

STATIC_ROOT = MEDIA_ROOT + 'megavideo/static/'

STORAGE_URL = '/media/megavideo/storage/'
STORAGE_URL_RELATIVE = STORAGE_URL

STORAGE2    = '/var/www/tcd_offline/megavideo/media/storage/'

AUTHENTICATION_BACKENDS = (
    'megavideo.common.nondefaultdb.NonDefaultModelBackend',
    #'django.contrib.auth.backends.ModelBackend',
)

MEGAVIDEO_LOGIN_URL = '/megavideo/manager/'
