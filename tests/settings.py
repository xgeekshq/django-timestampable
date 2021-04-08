SECRET_KEY = '!fake'

DEBUG = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_extensions',
    'rest_framework',

    'timestamps',
    'tests'
]

ROOT_URLCONF = 'tests.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

ALLOW_PERMANENT_BULK_DELETE = True
BULK_ACTIONS_RETURNS_CONTENT = True
