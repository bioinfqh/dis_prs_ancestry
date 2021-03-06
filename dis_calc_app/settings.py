"""
Django settings for testproject project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#BASE_DIR = os.path.dirname(__file__)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = os.getenv("SECRET_KEY",'9z5(_w$5&=_)eve^u(--xcg%ge3dxi38m^d$yqol5#*atybvt6') 
#SECRET_KEY = os.getenv("SECRET_KEY") 
SECRET_KEY = '4qu1-phs@%#hp_$de(+g!z0%_o+@@s3z7=4mfm((-s__0&n6)9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# allowed host must list every adress that is used for accessing the web server in the browser. In the docker container, it runs (for example) on 172.18.0.6:8000; when run outside a docker container, you can access the website on localhost:8000.
#ALLOWED_HOSTS = ['0.0.0.0','172.18.0.6','localhost']
#ALLOWED_HOSTS = ['*']

# get list of allowed hosts from environment variable
#ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", ['*'])
#ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS") 
ALLOWED_HOSTS = ['*']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dis_calc.apps.PollsConfig',
    #'polls.apps.PollsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

#ROOT_URLCONF = 'testproject.urls'
ROOT_URLCONF = 'dis_calc_app.urls'
# celery configuration. this line tells celery where it can access rabbitMQ.
#CELERY_BROKER_URL = 'amqp://localhost'
#CELERY_BROKER_URL = 'amqp://admin:mypass@rabbit:5672'
#CELERY_BROKER_URL = 'amqp://localhost'
# the serializer is used for passing results from celery to python functions. pickle is the only serializer that is suitable for all different data formats.

CACHES = {
   'default': {
      'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
      'LOCATION': 'my_cache_table',
      'TIMEOUT': 10000,
   }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
# tells the server where to find the HTML pages to display for the user.
#TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'polls/templates')]
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'dis_calc/templates')]

#WSGI_APPLICATION = 'testproject.wsgi.application'
WSGI_APPLICATION = 'dis_calc_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
#}
# here the database is referenced
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'database.sqlite3'),
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '',
#    }
#}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'mydatabase',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# tells the server where to look for static files. Static files are all non-html files used for display on the web pages, such as heatmaps or loading gifs.
#STATIC_URL = '/static/'
STATIC_URL = '/dis_calc/static/'
#STATIC_URL = '/'
#STATIC_ROOT = os.path.join(BASE_DIR, '../code/polls/static')
#STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'dis_calc/static')
# staticfile_dirs tells Django where to take additional static files from. It is possible to add further directories with static files there.
# In this case here, the shared volume is referenced where celery, livereload and django have access.
STATICFILES_DIRS = ['/dis_calc/static/']
#STATIC_ROOT = os.path.join(BASE_DIR, 'polls/static')
#STATICFILES_DIRS = ['/code/polls/static/']

