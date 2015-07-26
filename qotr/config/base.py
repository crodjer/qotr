import logging.config

class Base(object):
    '''
    QOTR basic configuration.
    '''

    host = None
    port = None
    debug = True
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '[%(levelname)s] %(asctime)s [%(module)s] %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'handlers': {
            'stream': {
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'qotr': {
                'handlers': ['stream'],
                'level': 'DEBUG',
            },
            'tornado': {
                'handlers': ['stream'],
                'level': 'DEBUG',
            }
        },
    }

    def __init__(self):
        if self.port:
            self.port = int(self.port)
        logging.config.dictConfig(self.log_config)

    @property
    def name(self):
        return self.__class__.__name__.lower()
