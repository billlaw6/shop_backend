"""

Django settings for shop_backend project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd1ln%!y6c9439k8nt2i899!evk#l3f+ao)km-5iknqi&8zuq)g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['123.56.115.20', 'carryon.top', 'localhost']



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'django.contrib.sites',
    # django-rest-framework-social-oauth2
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    # django-rest-auth
    'rest_auth',
    'rest_auth.registration',
    'allauth',
    'allauth.account',
    # My apps
    'weixin.apps.WeixinConfig',
    'dict_manage.apps.DictManageConfig',
    'user_manage.apps.UserManageConfig',
    'verify_utils.apps.VerifyUtilsConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shop_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['shop_frontend/dist'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # django-rest-framework-social-oauth2
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'shop_backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

# 静态文件由nginx提供了，并且在HTML文件中写链接，不用django模板，所以此处不用配置
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'shop_frontend/dist/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'shop_frontend/dist/static/')
]

# REST_FRAMEWORK settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        # django-rest-framework-social-oauth2
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        # Use Django's standard `django.contrib.auth` permissions,
        # or allow read-only access for unauthenticated users.
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        # 'rest_framework.permissions.IsAdminUser',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

AUTH_USER_MODEL = 'user_manage.ShopUser'
# LOGIN_REDIRECT_URL Default: '/accounts/profile/'
LOGIN_REDIRECT_URL = '/'
AUTHENTICATION_BACKENDS = [
    'user_manage.backends.EmailModelBackend',
    'user_manage.backends.CellPhoneModelBackend',

    # Social OAuth2 backends
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.weixin.WeixinOAuth2',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
]

CORS_ORIGIN_WHITELIST = (
    'localhost:8080',
    'localhost:8000',
    '127.0.0.1:8080',
    '127.0.0.1:8000',
    '123.56.115.20:8080',
)

# django-rest-auth
# http://django-rest-auth.readthedocs.io/en/latest/installation.html
SITE_ID = 1

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.163.com'
EMAIL_HOST_USER = 'carryontop@163.com'
EMAIL_HOST_PASSWORD = 'woaini2006'
EMAIL_SUBJECT_PREFIX = u'carryon.top'
EMAIL_USE_TLS = True
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

OAUTH2_PROVIDER = {
    # this is the list of availabel scopes
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}
}

# https://github.com/PhilipGarnero/django-rest-framework-social-oauth2
# Will not be updated in the pipeline process
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['username']
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/logged_out'

SOCIAL_AUTH_GITHUB_KEY = 'b19f4ff7146560185f3b'
SOCIAL_AUTH_GITHUB_SECRET = '39b78edc6726ce2bd19540452511ceb307ac4cd3'
SOCIAL_AUTH_WEIBO_KEY = '3814205163'
SOCIAL_AUTH_WEIBO_SECRET = 'bd5c4a1e1e8f09f1c9f4caa3c515b203'
SOCIAL_AUTH_WEIXIN_KEY = 'wx4a32725dfd171687'
SOCIAL_AUTH_WEIXIN_SECRET = '14123aca2110ec62e097ab8c1cb2734d'

SOCIAL_AUTH_GITHUB_SCOPE = ['email']
SOCIAL_AUTH_GITHUB_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}
SOCIAL_AUTH_WEIBO_SCOPE = ['email']
SOCIAL_AUTH_WEIXIN_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}

# Default scope: snsapi_login
SOCIAL_AUTH_WEIXIN_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_WEIXIN_SCOPE = ['snsapi_userinfo']
# SOCIAL_AUTH_WEIXIN_SCOPE = ['snsapi_base']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#         },
#         'simple': {
#             'format': '%(levelname)s %(message)s'
#         },
#     },
#     'filters': {
#         # 'special': {
#         #     '()': 'project.logging.SpecialFilter',
#         #     'foo': 'bar',
#         # },
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'INFO',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['require_debug_true']
#             # 'filters': ['special']
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['mail_admins'],
#             'level': 'ERROR',
#             'propagate': False,
#         },
#         'myproject.custom': {
#             'handlers': ['console', 'mail_admins'],
#             'level': 'INFO',
#             'filters': ['require_debug_true']
#             # 'filters': ['special']
#         }
#     }
# }

WEIXIN_APPID = 'wx4a32725dfd171687'
WEIXIN_APPSECRET = '14123aca2110ec62e097ab8c1cb2734d'
