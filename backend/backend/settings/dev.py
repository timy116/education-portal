from .base import *

# Debug toolbar settings
INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

if DEBUG:
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_COLLAPSED": True,
}

INTERNAL_IPS = [
    "127.0.0.1",
]

# kolo settings.
KOLO_DISABLE = bool(env('KOLO_DISABLE'))

if not KOLO_DISABLE:
    MIDDLEWARE += [
        "kolo.middleware.KoloMiddleware",
    ]

# RECAPTCHA settings
SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

# Logging settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'formatters': {
        'simple': {
            'format': 'X X %(levelname)s [%(asctime)s] %(message)s',
            'datefmt': '%d/%b/%Y:%H:%M:%S %z'
        },
    },
    'handlers': {
        'log': {
            'level': 'DEBUG',
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
        },
        'db_log': {
            'level': 'DEBUG',
            'formatter': 'simple',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'rules': {
            'handlers': [],
            'level': 'INFO',
        },
        'signup': {
            'handlers': [],
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['db_log'],
            'level': 'DEBUG',
            'propagate': False
        },
    },
}

# Email settings
EMAIL_ADDR = "no-reply@domain.com"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False
