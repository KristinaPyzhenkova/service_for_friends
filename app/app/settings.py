from pathlib import Path
import dotenv
import os

dotenv.load_dotenv('../../.env')

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY", 'secret')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.getenv("DEBUG", 0))

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1 localhost db").split(" ")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'drf_yasg',
    'service_backend.apps.ServiceBackendConfig',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",

]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": os.getenv("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": os.getenv("SQL_DATABASE", os.path.join(BASE_DIR, "db.sqlite3")),
        "USER": os.getenv("SQL_USER", "user"),
        "PASSWORD": os.getenv("SQL_PASSWORD", "password"),
        "HOST": os.getenv("SQL_HOST", "localhost"),
        "PORT": os.getenv("SQL_PORT", "5432"),
        'ATOMIC_REQUESTS': True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = 'Europe/Istanbul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "service_backend.User"

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}

DJOSER = {
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'username',
    'PERMISSIONS': {
        'user_list': [
            'rest_framework.permissions.AllowAny'
        ],
        'user': [
            'rest_framework.permissions.AllowAny',
        ],
    }
}

