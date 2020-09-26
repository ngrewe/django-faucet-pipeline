from pathlib import Path

DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:", "TEST": {}}
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django_faucet_pipeline",
    "django_faucet_pipeline.tests.testapp",
]

STATIC_URL = "/static/"

SECRET_KEY = "test"

PUBLIC_SERVER_FQDN = ""

ROOT_URLCONF = "django_faucet_pipeline.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

FAUCET_PIPELINE_MANIFEST = str((Path(__file__) / ".." / "manifest.json").resolve())
