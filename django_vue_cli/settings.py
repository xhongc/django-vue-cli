from pathlib import Path
import sys
import os
import datetime

# lib文件夹中手动导入的第三方库
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(1, os.path.join(os.getcwd(), 'lib'))

# docker 中redis
BROKER_URL = "redis://redis:6379/3"

SECRET_KEY = 'django-insecure-u5_r=pekio0@zt!y(kgbufuosb9mddu8*qeejkzj@=7uyvb392'

DEBUG = False

ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_NAME = "django_vue_cli_csrftoken"
CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:8080"
]

# Application definition

INSTALLED_APPS = [
    "corsheaders",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "rest_framework",
    "applications.task",
    "applications.user",

]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    "component.drf.middleware.AppExceptionMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_vue_cli.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "static", "dist")],
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

WSGI_APPLICATION = 'django_vue_cli.wsgi.application'
TIME_ZONE = "Asia/Shanghai"
LANGUAGE_CODE = "zh-hans"
# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "dj-vue",  # noqa bomboo
        "USER": "root",
        "PASSWORD": "123456",  # xhongc
        "HOST": "127.0.0.1",  # todo docker config mysql
        "PORT": "3306",
        # 单元测试 DB 配置，建议不改动
        "TEST": {"NAME": "test_db", "CHARSET": "utf8", "COLLATION": "utf8_general_ci"},
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = 'static'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]  # noqa

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
IS_USE_CELERY = True

if IS_USE_CELERY:
    INSTALLED_APPS += ("django_celery_beat", "django_celery_results")
    CELERY_ENABLE_UTC = False
    CELERY_TASK_SERIALIZER = "pickle"
    CELERY_ACCEPT_CONTENT = ['pickle', ]
    CELERYBEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "component.drf.generics.exception_handler",
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "component.drf.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ),
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "NON_FIELD_ERRORS_KEY": "params_error",
}
DJORM_POOL_PESSIMISTIC = False
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/8",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
JWT_AUTH = {
    # 过期时间，生成的took七天之后不能使用
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 刷新时间 之后的token时间值
    # 'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=1),
    # 请求头携带的参数
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}
try:
    from local_settings import *  # noqa
except ImportError:
    pass
