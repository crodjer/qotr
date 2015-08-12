import logging

from fnmatch import fnmatch
from tornado import web
from qotr.config import config

L = logging.getLogger(__name__)
ALLOWED_ORIGINS = [o.strip() for o in config.allowed_origins.split(',')]

def set_cors_headers(handler):
    '''
    Given a handler, set the CORS headers on it.
    '''


    origin = handler.request.headers.get('Origin', '')

    if not origin:
        return

    L.debug('Setting CORS headers for: %s based on %s', origin,
            ALLOWED_ORIGINS)
    if origin in ALLOWED_ORIGINS or any(fnmatch(origin, o)
                                        for o in ALLOWED_ORIGINS):
        handler.set_header("Access-Control-Allow-Origin", origin)
        handler.set_header("Access-Control-Allow-Headers", "Content-Type")

# pylint: disable=W0223
class Base(web.RequestHandler):
    '''
    A base request handler.
    '''

    def prepare(self):

        protocol = self.request.headers.get('x-forwarded-proto')

        if config.redirect_to_https and \
           self.request.method == 'GET' and \
           protocol == 'http':
            self.redirect('https://{}{}'.format(
                self.request.host.split(':')[0], self.request.path
            ), permanent=True)
