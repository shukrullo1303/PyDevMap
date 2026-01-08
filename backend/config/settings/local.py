from config.settings.base import *

import os

BASE_DIR = BASE_DIR.parent

EXTERNAL_APPS = [
    'corsheaders',
    'rest_framework', 
    'drf_yasg',
    "debug_toolbar",
    'nested_admin',
    'django_filters',
    
]

LOCAL_APPS = ["src.core",
                "seed",
]

INSTALLED_APPS += EXTERNAL_APPS + LOCAL_APPS

SECRET_KEY = "secret-key-for-local-development"

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # bo‘lmasa ham bo‘lishi mumkin
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # MUHIM
                'django.contrib.auth.context_processors.auth',  # MAJBURIY
                'django.contrib.messages.context_processors.messages',  # MAJBURIY
            ],
        },
    },
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    }


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

CORS_ALLOW_ALL_ORIGINS = True


ALLOWED_HOSTS = ["*"]