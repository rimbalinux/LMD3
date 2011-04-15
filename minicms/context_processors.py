from django.conf import settings
from translate.lang import tr

def cms(request):
    return {
        'site_name': tr(settings.SITE_NAME, request),
        'site_copyright': settings.SITE_COPYRIGHT,
        'google_analytics_id': getattr(settings, 'GOOGLE_ANALYTICS_ID', None),
        'google_custom_search_id': getattr(settings, 'GOOGLE_CUSTOM_SEARCH_ID',
                                           None),
    }
