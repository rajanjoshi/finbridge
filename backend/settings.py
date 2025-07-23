from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'fake-key'
DEBUG = True
ALLOWED_HOSTS = ['*']

LOGIN_URL = "/login/"

GCP_PROJECT_ID = "learn-gcp-465905"
GCP_REGION = os.getenv("GCP_REGION", "us-central1") 
VERTEX_RAG_CORPUS_ID = os.getenv("VERTEX_RAG_CORPUS_ID", "5188146770730811392")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash-001")

LANGUAGES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('bn', 'Bengali'),
    ('mr', 'Marathi'),
]


LANGUAGE_CODE = 'en'

CSRF_TRUSTED_ORIGINS = [
    "https://*.run.app",
    "https://*.cloudshell.dev"
]

AUTH_USER_MODEL = 'users.CustomUser'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'ai_assistant',
    'scheme_finder',
    'learn_finance',
    'savings',
    'rag_admin',
    'users.apps.UsersConfig',
    'gamification',
    'about'
]

LOCALE_PATHS = [BASE_DIR / "locale"]
USE_I18N = True
USE_L10N = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'users.middleware.RequireUserProfileMiddleware', 
]

ROOT_URLCONF = 'backend.urls'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(BASE_DIR, 'templates')],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.template.context_processors.request',
            'django.contrib.auth.context_processors.auth',
            'django.contrib.messages.context_processors.messages',
        ],
    },
}]


WSGI_APPLICATION = 'backend.wsgi.application'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
