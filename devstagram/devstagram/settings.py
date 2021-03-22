from os.path import join
from pathlib import Path
from django.urls import reverse_lazy


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'f)xm7uoqw6fht^l%6q761trf)9tna(92hu%*7&bu-lg*8omgdv'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'fontawesome-free',
    'crispy_forms',
    'channels',

    'devstagram.registration',
    'devstagram.mainsite',
    'devstagram.chat',
    'devstagram.async_chat',

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

ROOT_URLCONF = 'devstagram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'devstagram.mainsite.custom_context.get_notifications',
                'devstagram.mainsite.custom_context.get_chats',
            ],
        },
    },
]

WSGI_APPLICATION = 'devstagram.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'devstagram',
        'USER': 'postgres',
        'PASSWORD': 'georgi',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ASGI_APPLICATION = 'devstagram.routing.application'


STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = (
    join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = reverse_lazy('index')
LOGOUT_REDIRECT_URL = reverse_lazy('landing page')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'georgipavlov910@gmail.com'
EMAIL_HOST_USER = 'georgipavlov910@gmail.com'
EMAIL_HOST_PASSWORD = 'Georgi0808'

# CHANNEL_LAYERS = {
#     'default': {
#         'BACKEND': 'channels.layers.InMemoryChannelLayer'
#     }
# }
CHANNEL_LAYERS = {
    "default": {
        "CONFIG": {
            "hosts": [('localhost','6379')],
        },
        "BACKEND": "channels_redis.core.RedisChannelLayer",
    },
}