import logging.config

class Base(object):
    '''
    QOTR basic configuration.
    '''

    host = None
    port = None
    debug = False
    redirect_to_https = False

    allowed_origin = "*"
    channel_timeout = 600 # A channel is kept for 10 minutes.
    cleanup_period = channel_timeout / 2

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
