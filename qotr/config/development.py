from .base import Base

class Development(Base):
    '''
    QOTR development configuration.
    '''

    host = 'localhost'
    port = '5000'
    debug = True
