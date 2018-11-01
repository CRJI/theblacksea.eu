from django.conf import settings

def blacktail_settings(request):
    return {
        'PROD': settings.BLACKTAIL_PROD,
    }
