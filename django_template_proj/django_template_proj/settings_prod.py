"""
Django settings for django_template_proj project.

Generated by 'django-admin startproject' using Django 3.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import django_heroku
import os

jj = os.path.join
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

# Application definition

INSTALLED_APPS = [
    # for template resolution priority with django.contrib.admin app
    'user.apps.UserConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'rest_framework.apps.RestFrameworkConfig',
    'rest_framework.authtoken',

    'user_api.apps.UserApiConfig',
    'social.apps.SocialConfig',
    'google_api.apps.GoogleApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # whitenoise package
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_template_proj.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'django_template_proj.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# CELERY Known Issues
# CONN_MAX_AGE other than zero is known to cause issues according to bug #4878.
# Until this is fixed, please set CONN_MAX_AGE to zero.

# DATABASES = {
#     "default": {
#         'ENGINE': os.environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
#         'NAME': os.environ.get("SQL_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
#         'USER': os.environ.get("SQL_USER", "user"),
#         'PASSWORD': os.environ.get("SQL_PASSWORD", "password"),
#         'HOST': os.environ.get("SQL_HOST", "localhost"),
#         'PORT': os.environ.get("SQL_PORT", "5432"),
#     }
# }

# django-db-geventpool
# for django 1.6 and newer version, CONN_MAX_AGE must be set to 0, or connections will never go back to the pool
DATABASES = {
    'default': {
        'ENGINE': 'django_db_geventpool.backends.postgresql_psycopg2',
        'NAME': os.environ.get("SQL_NAME", os.path.join(BASE_DIR, "db.sqlite3")),
        'USER': os.environ.get("SQL_USER", "user"),
        'PASSWORD': os.environ.get("SQL_PASSWORD", "password"),
        'HOST': os.environ.get("SQL_HOST", "localhost"),
        'PORT': os.environ.get("SQL_PORT", "5432"),
        'ATOMIC_REQUESTS': False,
        'CONN_MAX_AGE': 0,
        'OPTIONS': {
            'MAX_CONNS': 20
        }
    }
}

# import dj_database_url

# if "DATABASE_URL" in env:
#     DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = jj(BASE_DIR, 'static')
# will not if Debug=True
# Versioned files are cached forever, non-versioned files are cached for 60 seconds.
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# whitenoise settings
WHITENOISE_KEEP_ONLY_HASHED_FILES = True
# Versioned files age (hashed usually by md5 algorithm)
WHITENOISE_MAX_AGE = 3600

# Media files (user upload images etc...)
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# django.contrib.sites
SITE_ID = 1

# Custom user model
AUTH_USER_MODEL = 'user.EmailUser'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

# Email Backend
# Console Backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# File Backend
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = jj(BASE_DIR, 'emails')

# Email: Send Grid: SMTP server
# SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
#
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = SENDGRID_API_KEY
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# Email: Send Grid  Using Web API
# requires: pip install django-sendgrid-v5
# EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
# SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")

# There are also optional settings to deliver emails in debug mode or to send them to standard output:
# Toggle sandbox mode (when running in DEBUG mode)
# SENDGRID_SANDBOX_MODE_IN_DEBUG = True

# echo to stdout or any other file-like object that is passed to the backend via the stream kwarg.
# SENDGRID_ECHO_TO_STDOUT = True

# social google
GOOGLE_CLIENT_FILE_PATH = jj(jj(BASE_DIR, 'google_api'), 'client_secret.json')
GOOGLE_OPTIONS = {'prompt': 'consent'}

# celery::broker via rabbitmq
BROKER_USER = os.environ.get("BROKER_USER")
BROKER_PASSWORD = os.environ.get("BROKER_PASSWORD")
BROKER_HOST = os.environ.get("BROKER_HOST")
BROKER_PORT = os.environ.get("BROKER_PORT")
BROKER_VHOST = os.environ.get("BROKER_VHOST")

CELERY_BROKER_URL = f"amqp://{BROKER_USER}:{BROKER_PASSWORD}@{BROKER_HOST}:{BROKER_PORT}/{BROKER_VHOST}"
# CELERY_BROKER_URL = 'amqp://mahdi:mahdi@rabbitmq:5672/mahdi_vhost'

# celery::broker via redis
# CELERY_BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

# Celery Data Format
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tehran'

# CPU-bound tasks are best executed by a prefork execution pool.
# I/O bound tasks are best executed by a gevent/eventlet execution pool.
# both gevent/eventlet are base on greenlet (also known as green threads)
# CELERY_POOL = 'gevent'

# celery -A django_template_proj.celery worker -n worker2@%h --loglevel=info -Q mail -P gevent
# CELERY_TASK_QUEUES = {
#     'mail': {
#         'exchange': 'mail',
#         'routing_key': 'mail',
#     },
# }
# celery  routing and queues ,,,,django_template_proj.user.tasks.,,,
# CELERY_TASK_ROUTES  = {
#     'user.tasks.*': {
#         'queue': 'mail',
#         # 'routing_key': 'mail',
#         # 'exchange': 'mail',
#     }
# }

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

## Logging configuration
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file_DEBUG': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(os.path.join(BASE_DIR, 'django_template_proj'), 'debug.log'),
#         },
#         'file_INFO': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(os.path.join(BASE_DIR, 'django_template_proj'), 'info.log'),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file_DEBUG'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['file_INFO'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }
from django.utils.log import DEFAULT_LOGGING

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s %(levelname)s [%(name)s:%(lineno)s] %(module)s %(process)d %(thread)d %(message)s'
        },
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        # 'django.server': DEFAULT_LOGGING['formatters']['django.server'],

    },
    'handlers': {
        # 'gunicorn_file_debug': {
        #     'level': 'DEBUG',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'formatter': 'verbose',
        #     'filename': os.path.join(os.path.join(BASE_DIR, 'django_template_proj'), 'gunicorn.debug.log'),
        #     'maxBytes': 1024 * 1024 * 100,  # 100 mb
        # },
        'django': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(os.path.join(BASE_DIR, 'django_template_proj'), 'django.log'),
            # TimedRotatingFileHandler: Rotate log file daily, only keep 1 backup
            'when': 'd',
            'interval': 1,
            'backupCount': 1,
        },
        'django.request': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.join(BASE_DIR, 'django_template_proj'), 'django.request.log'),
        },
        'django.server': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(os.path.join(BASE_DIR, 'django_template_proj'), 'django.server.log'),
            'formatter': 'django.server',
        }
        # 'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # 'gunicorn.errors': {
        #     'level': 'DEBUG',
        #     'handlers': ['gunicorn_file_debug'],
        #     'propagate': True,
        # },
        'django': {
            'handlers': ['django'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['django.request'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # 'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
}

# Activate Django-Heroku.
# logging=False :: do not over write my logging in this setting
django_heroku.settings(locals(), logging=False)
