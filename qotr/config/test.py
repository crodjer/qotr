from .base import Base

class Test(Base):
    '''
    QOTR test configuration.
    '''

    host = 'localhost'
    # For Ember tests in future, Python tests will use a random port.
    port = 9191
