DEBUG = True

SECRET_KEY = "bootstrap4isawesome"

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}

INSTALLED_APPS = (
    # Default Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    # We test this one
    "bootstrap4",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

ROOT_URLCONF = None

STATIC_URL = "/static/"

BOOTSTRAP4 = {
    "theme_url": "//example.com/theme.css",
    "javascript_in_head": True,
    "required_css_class": "bootstrap4-req",
    "error_css_class": "bootstrap4-err",
    "success_css_class": "bootstrap4-bound",
}
