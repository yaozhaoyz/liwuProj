"""
Django settings for liwu project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y7w*-a^63tjcsogf2jg0&ua&+sgw_z5l1(k7h2_=&_khyexs3n'
URL_PREFIX = 'http://115.28.9.133:8088'
BASE_DIR = os.path.dirname(__file__)
MEDIA_URL = "http://115.28.9.133:8088/"
QINIU_URL = "http://celebritymedia.qiniudn.com/media/"
QINIU_XHURL = "http://celebritymedia.qiniudn.com/"
MEDIA_ROOT = BASE_DIR + "/media/"
ROOT_URLCONF = 'liwu.urls'

ACCESS_KEY = "eA-tOav_Umkcqhj2mxrb61y6uItnNPTm2p_8NDmx"
SECRET_KEY = "4tPYpEkL0YAn0NtN1nPIf-AoY29F3e2VSJr0nmwM"
BUCKET_NAME = "celebritymedia"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
    '/disk1/liwuDjango/liwu/liwu/template' ,
    )

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'liwu.kgapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
 #   'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'liwu.urls'

WSGI_APPLICATION = 'liwu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DBNAME = 'liwuDB'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
UEDITOR_SETTINGS = {
    'toolbars':{"testa":[['fullscreen', 'source', '|', 'undo', 'redo', '|','bold', 'italic', 'underline']],
        "testb":[[ 'source', '|','bold', 'italic', 'underline']]
    },
    'images_upload':{
        'max_size':0,
        'path':"asd"
    },
    'scrawl_upload':{
        'path':'scrawlabc'
    }
}
