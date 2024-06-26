"""
Django settings for Project project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""


from pathlib import Path
import os
import dj_database_url
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-!neg76s++03)b-6z^ynjyhy*tp@xe2%84ros0inlv^5e2b6jnm'
SECRET_KEY = os.environ.get('SECRET_KEY', default='t]jW]%1?n!"tjOnz9_t>62Trgl/?Vz_E')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False
# DEBUG = 'RENDER' not in os.environ


ALLOWED_HOSTS = []

RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Management',
    'bootstrap5',
]

LOGOUT_REDIRECT_URL = 'index'

# Configuración personalizada de Bootstrap5
BOOTSTRAP5 = {
    'primary_color': '#ff7c38', 
}

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

MIDDLEWARE = [
    #'django.middleware.locale.LocaleMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.cache.CacheMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]

# CACHE_MIDDLEWARE_SECONDS = 0

ROOT_URLCONF = 'Project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'Management/templates/base'),
            os.path.join(BASE_DIR, 'Management/templates/recepcionist'),
            os.path.join(BASE_DIR, 'Management/templates/customers'),
            os.path.join(BASE_DIR, 'Management/templatestags')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries':{
                'filters':'Management.templatetags.filters',
            }
        },
    },
]

WSGI_APPLICATION = 'Project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# if 'DABATASE_URL' in os.environ:

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3'
        # default='postgresql://postgres:postgres@localhost/postgres'
    )
}
# DATABASES = {
#     'default':{
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'dbproyectoautomotriz',
#         'USER': 'root',
#         'PORT': '3306',
#         'PASSWORD': ''
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_GROUP_MODEL_CUSTOMER = 'Management.Customer'
AUTH_GROUP_MODEL_RECEPCIONIST = 'Management.Recepcionist'
# Para desarrollo, puede ser True en producción
# SESSION_COOKIE_SECURE = False  
SESSION_COOKIE_SECURE = True  
SESSION_COOKIE_NAME = 'sessionid'  





# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# import locale
# locale._getdefaultlocale = (lambda *args: ['es_ES', 'utf8'])
LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [BASE_DIR / "static",]


# URL base para los archivos multimedia
MEDIA_URL = '/media/'
# Ruta al directorio donde se guardarán los archivos multimedia
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# if not DEBUG:
# Tell Django to copy statics to the `staticfiles` directory
# in your application directory on Render.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Turn on WhiteNoise storage backend that takes care of compressing static files
# and creating unique names for each version so they can safely be cached forever.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# EDMUNDS_API_KEY = '&api_key=ar355ajjgkz5pxxv5g3dfakx'
