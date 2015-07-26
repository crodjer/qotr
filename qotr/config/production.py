import os
from .base import Base


class Production(Base):
    '''
    QOTR production configuration.
    '''

    host = os.environ.get('HOST')
    port = os.environ.get('PORT')
    debug = False
