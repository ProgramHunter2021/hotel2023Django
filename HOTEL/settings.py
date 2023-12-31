"""
Django settings for HOTEL project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
LINE_CHANNEL_ACCESS_TOKEN = 'WSIpKQI3MkKwdndQITzftukdNPE3vK3cEi8ovJqibU4URoEvc0AdlYtePE3hOKbHTSc3JIqIS+f+VtDHsz9giBFkrzPCFoTMZN5mSOeo+rEbKphmDPk5RvSP+sAy3U1ByDR1FSafOr/RIVo8oygfkAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'c296bfe109d90b2729e95bf69973369e'

PAY_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/request'   #測試
CONFIRM_API_URL = 'https://sandbox-api-pay.line.me/v2/payments/{}/confirm'    #測試

LINE_PAY_ID = '1657362199'   #((改))
LINE_PAY_SECRET = '171192f29cdc223d91da297cb60c87bc'   #((改))
STORE_IMAGE_URL = 'https://i.imgur.com/fN6dgex.jpg'   #((改))


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6)k8qbqbsl+!2t$0_$cdpcty0!(*58x(9#p9qu09%lbmhj5(7i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'booking.apps.BookingConfig',
    'activity.apps.ActivityConfig',
    'hotelbot.apps.HotelbotConfig',
    'hailAndChartered.apps.HailandcharteredConfig',
    'reservation.apps.ReservationConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'HOTEL.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates')],
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

WSGI_APPLICATION = 'HOTEL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',  #PostgreSQL
#         'NAME': 'hoteldb',  #資料庫名稱
#         'USER': 'postgres',  #資料庫帳號
#         'PASSWORD': 'admin',  #資料庫密碼
#         'HOST': 'localhost',  #Server(伺服器)位址
#         'PORT': '5432'  #PostgreSQL Port號
#     }
# }

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': dj_database_url.config(
#         # Feel free to alter this value to suit your needs.
#         default='postgresql://hoteldb_ds8f_user:0Dib1T5WnhwkIx0KNttiNquYMmca2vbu@dpg-ckh43ksldqrs73fv3jrg-a.singapore-postgres.render.com/hoteldb_ds8f',
#         conn_max_age=600
#     )
# }

DATABASES = {
    "default": dj_database_url.config(
        # Feel free to alter this value to suit your needs.
        default='postgres://hoteldb_ds8f_user:0Dib1T5WnhwkIx0KNttiNquYMmca2vbu@dpg-ckh43ksldqrs73fv3jrg-a.singapore-postgres.render.com/hoteldb_ds8f',
        
    )
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hant'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATICFILES_DIRS = [
        os.path.join(BASE_DIR,  'static'),
    ]
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


