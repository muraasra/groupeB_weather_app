# settings.py
import os

# Autres configurations...

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'weather/static'),
]
