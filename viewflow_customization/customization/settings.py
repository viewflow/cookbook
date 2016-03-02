import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '$mq=4(a5fj&#@q_*_+j5t-dqn0&km%8rcg8#n4w36+%b5jhc6a'

DEBUG = not os.path.exists(os.path.join(BASE_DIR, 'deploy'))
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'bootstrap3',
    'guardian',
    'viewflow',
    'customization.users',
    'customization.parcel',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'customization.urls'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'deploy/static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'deploy/media')

# Templates
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'customization.website.users',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# Auth
LOGIN_URL = '/login/'
AUTH_USER_MODEL = 'users.User'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1
GUARDIAN_GET_INIT_ANONYMOUS_USER = 'customization.users.models.get_anonymous_user_instance'
