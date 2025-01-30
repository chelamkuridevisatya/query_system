from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Add your allowed hosts

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",  # Added Django Rest Framework
    "rest_framework_simplejwt",  # Added JWT support
    "api",  # Your app
    'corsheaders',  # CORS headers for allowing Angular to connect
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',  # CORS middleware
]

# Allow all origins to access the API during development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:4200",  # Angular development server URL
    "http://127.0.0.1:4200",  # Same as above
    # You can add more URLs if needed (for production or other environments)
]

# CORS settings for credentials
CORS_ALLOW_CREDENTIALS = True  # Allow sending credentials (cookies, headers, etc.)

ROOT_URLCONF = "query_system.urls"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add the templates directory path here
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

WSGI_APPLICATION = "query_system.wsgi.application"

# Database (MongoDB setup)
DATABASES = {
    "default": {
        "ENGINE": "djongo",  # Use Djongo for MongoDB support in Django
        "NAME": "sample_mflix",  # MongoDB database name
        "ENFORCE_SCHEMA": False,
        "CLIENT": {
            "host": os.getenv("MONGO_URI"),
            "username": os.getenv("MONGO_USERNAME"),
            "password": os.getenv("MONGO_PASSWORD"),
            "authSource": os.getenv("MONGO_AUTH_SOURCE"), # Authentication source database
        },
    }
}

# JWT Authentication (using 'rest_framework_simplejwt' for JWT token authentication)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Password validation
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

# Static files
STATIC_URL = "static/"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'api.CustomUser'
