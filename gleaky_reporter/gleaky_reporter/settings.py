"""
Django settings for gleaky_reporter project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG =  int(os.environ.setdefault(GK_DEBUG, '1'))
DEV_MODE =  int(os.environ.setdefault(GK_DEV_MODE, '1'))
INSECURE_SECRET_KEY = 'django-insecure-zp+$9xu$)^67#dp@3=$@1uqsbp!id5mzs%95xq!3jbslg^zjat'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.setdefault('GK_SECRET_KEY', INSECURE_SECRET_KEY if DEBUG and DEV_MODE)
if not SECRET_KEY:
    print('Missing SECRET_KEY: Set GK_SECRET_KEY or turn GK_DEBUG and GK_DEV_MODE off')


TENANT_USERS_DOMAIN = os.environ.setdefault("GK_DOMAIN_NAME", "gleaky.com")
SESSION_COOKIE_DOMAIN = ".{}".format(TENANT_USERS_DOMAIN)
SYSTEM_EMAIL = os.environ.setdefault("GK_SYSTEM_EMAIL", "root@gleaky.com")
ADMIN_EMAIL = os.environ.setdefault("GK_ADMIN_EMAIL", "admin@gleaky.com")
ADMIN_PASSWORD = os.environ.setdefault("GK_ADMIN_PASSWORD", "password")
ALLOWED_HOSTS = ["127.0.0.*", "0.0.0.0"] + [TENANT_USERS_DOMAIN, SESSION_COOKIE_DOMAIN]

# Tenant=Country, TennatGroup=GeopoliticalOrganization
AUTO_CREATE_TEST_TENANT_GROUP = int(os.environ.setdefault("GK_CREATE_TEST_TENANT_GROUP", DEBUG and "1" or "0"))
AUTO_CREATE_TEST_TENANT = int(os.environ.setdefault("GK_CREATE_TEST_TENANT", DEBUG and "1" or "0"))
TEST_TENANT_GROUP_NAME = "test_corporation"
TEST_TENANT_HOST = "test"
TEST_TENANT_NAME = "Test Country"
GLEAKY_VERSION = os.environ.setdefault("GK_VERSION", "v0.0.1")
TENANT_MODEL = "world.Country"
AUTH_USER_MODEL = 'world.TenantUser'
TENANT_DOMAIN_MODEL = "world.Domain"
SESSION_COOKIE_DOMAIN = '.mydomain.com'

PUBLIC_SCHEMA_URLCONF = 'gleaky_reporter.urls_public'
ROOT_URLCONF = 'gleaky_reporter.urls_tenants'




# Application definition

SHARED_APPS = [
    'django_tenants',
    'tenant_users.permissions',
    'tenant_users.tenants',
    'world',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

TENANT_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'tenant_users.permissions',
)


 
 #PG_EXTRA_SEARCH_PATHS should be a list of schemas you want to make visible globally.
 #PG_EXTRA_SEARCH_PATHS = ['extensions']

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'tenant_users.permissions.backend.UserBackend',
)

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

WSGI_APPLICATION = 'gleaky_reporter.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': os.environ.get("GLEAKY_DB_NAME"),
        'USER': os.environ.get("GLEAKY_DB_USER"),
        'PASSWORD': os.environ.get("GLEAKY_DB_PWD"),
        'HOST': os.environ.get("GLEAKY_DB_HOST"),
        'PORT': os.environ.get("GLEAKY_DB_PORT"),
        # 'CONN_MAX_AGE': 500, #  see celery bug #4878
        'CONN_MAX_AGE': 0,
    }
}

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': [
            'redis://username:password@127.0.0.1:6379', # leader
            'redis://username:password@127.0.0.1:6378', # read-replica 1
            'redis://username:password@127.0.0.1:6377', # read-replica 2
        ],
        'KEY_FUNCTION': 'django_tenants.cache.make_key',
        'REVERSE_KEY_FUNCTION': 'django_tenants.cache.reverse_key',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'KEY_FUNCTION': 'django_tenants.cache.make_key',
        'TIMEOUT': 300,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Before using the database cache, you must create the cache table with this command:
# python manage.py createcachetable



# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
