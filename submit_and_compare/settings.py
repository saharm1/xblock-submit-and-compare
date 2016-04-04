DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

INSTALLED_APPS = (
    'django_nose',
)

SECRET_KEY = 'DJANGO_SECRET_KEY'
