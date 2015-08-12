import os
from .base import Base


class Production(Base):
    '''
    QOTR production configuration.
    '''

    host = os.environ.get('HOST', 'localhost')
    port = os.environ.get('PORT')

    debug = False
    allowed_origin = os.environ.get('CORS_ALLOWED_ORIGIN', '')
    redirect_to_https = True
