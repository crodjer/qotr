import os
from .base import Base


class Production(Base):
    '''
    QOTR production configuration.
    '''

    host = os.environ.get('HOST', 'localhost')
    port = os.environ.get('PORT')

    debug = False
    allowed_origins = os.environ.get('CORS_ALLOWED_ORIGINS', '')
    redirect_to_https = True
