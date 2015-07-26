import os

from .development import Development
from .test import Test
from .production import Production

ENV_MAP = {
    'production': Production,
    'test': Test,
    'development': Development
}

config = ENV_MAP.get(os.environ.get('QOTR_ENV'), Development)()
