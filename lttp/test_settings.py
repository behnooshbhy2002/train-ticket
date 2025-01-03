from .settings import *  # Import all settings from the main settings file

# Use an in-memory SQLite database for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # In-memory database
    }
}

# Optional: Speed up tests by using a fast password hasher
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Optional: Disable migrations during tests for faster execution
MIGRATION_MODULES = {
    app: None for app in INSTALLED_APPS
}
