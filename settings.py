import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ...existing code...

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # ...existing code...
            ],
        },
    },
]

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']  # Asegúrate de tener esta línea
STATIC_ROOT = BASE_DIR / 'staticfiles'