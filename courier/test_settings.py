SECRET_KEY = "test-secret-key"
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "courier",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
USE_TZ = True
