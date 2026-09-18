# Development settings for farmer_market

from .base import *  # noqa: F401,F403

# Override database to use MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "farmer_market",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}

# MongoDB connection settings (used by market app)
MONGODB_SETTINGS = {
    "host": "mongodb://127.0.0.1:27017/price_data",
}

# Debug mode for development
DEBUG = True

# Allowed hosts for local dev
ALLOWED_HOSTS = ["*"]
