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
