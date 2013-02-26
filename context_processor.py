from django.conf import settings

def static_url(request):
    
    # The URL path to STATIC_ROOT
    URL      = getattr(settings, 'STATIC_URL', '')
    PREFIX   = getattr(settings, 'ADMIN_MEDIA_PREFIX', '')
    BASE_URL = settings.LIST_VARS.get('base_url', '')
    
    return {'STATIC_URL': URL, 'ADMIN_MEDIA_PREFIX': PREFIX, 'BASE_URL': BASE_URL, 'STATIC_URL_TCD': URL }