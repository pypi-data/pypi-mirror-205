from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-1=9rra#bge4g1rt$lxylq@%n*0ai@sl^qb%*ih(6i)9te24&ne'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'kfsd.apps.frontend',
    'kfsd.apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'kfsd.apps.core.middleware.config.KubefacetsConfigMiddleware',
    'kfsd.apps.core.middleware.token.KubefacetsTokenMiddleware',
    'kfsd.apps.core.middleware.key.KubefacetsAPIKeyMiddleware',
]

ROOT_URLCONF = 'kfsd.urls'

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

WSGI_APPLICATION = 'kfsd.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'KUBEFACETS': {
        "STACKTRACE": False
    },
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'KFSD Utils as a Service',
    'VERSION': '1.0.0',
    "COMPONENT_SPLIT_REQUEST": True,
    "ENUM_ADD_EXPLICIT_BLANK_NULL_CHOICE": False,
    'SERVE_INCLUDE_SCHEMA': False,
    "POSTPROCESSING_HOOKS": [],
    'SERVE_AUTHENTICATION': None,
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-APIKey"
            }
        }
    },
    "SECURITY": [{"ApiKeyAuth": [], }],
}

KUBEFACETS = {
    "config": {
        "is_local_config": True,
        "lookup_dimension_keys": ["env"],
        "local": [
            {
                "setting": ["master"],
                "gateway": {
                    "host": "http://localhost:8000/api/",
                    "api_key": "9a02f7923aa22e69e0e2858d682a0c227ae0f3ce125a41c61d",
                    "auth": {
                        "token": {
                            "verify_token": "auth/token/verify"
                        }
                    }
                },
                "certs": {
                    "host": "http://localhost:8002",
                    "jwt_authority_id": "ORG=Kubefacets,APP=Certs,PRJ=Auth,COLL=Login,JWT=Login",
                    "token_gen_uri": "jwt-authorities/{}/token/gen/",
                    "token_publickey_uri": "jwt-authorities/{}/publickey/",
                    "token_decode_uri": "jwt-authorities/{}/token/dec/",
                    "tokens": {
                        "access": {
                            "lifetime_in_mins": 30
                        },
                        "refresh": {
                            "lifetime_in_mins": 300
                        }
                    }
                },
                "auth_fe": {
                    "host": "http://localhost:8000",
                    "login_url": "accounts/signin/",
                    "verify_email_url": "accounts/register/email/",
                    "register_verify_success_url": "http://localhost:8000/accounts/index"
                },
                "auth_api": {
                    "host": "http://localhost:8001",
                    "api_key": "9a02f7923aa22e69e0e2858d682a0c227ae0f3ce125a41c61d",
                    "user_login_url": "login/user/",
                    "user_register_url": "user/",
                    "user_exists_url": "user/{}/",
                    "verify_email_url": "verify/",
                    "verify_tmp_tokens_url": "verify/{}/tokens/",
                    "user_tokens_url": "tokens/{}/login/",
                    "token_extract_url": "tokens/extract/",
                    "access_token_refresh_url": "tokens/access/renew/",
                    "user_identifier_prefix": "USER={}"
                },
                "cookie": {
                    "access": {
                        "key": "access_token",
                        "secure": False,
                        "http_only": True,
                        "same_site": "lax"
                    },
                    "refresh": {
                        "key": "refresh_token",
                        "secure": False,
                        "http_only": True,
                        "same_site": "lax"
                    }
                }
            },
            {
                "setting": ["env:dev"],
                "certs": {
                    "host": "http://localhost:8002/"
                }
            }
        ]
    }
}
