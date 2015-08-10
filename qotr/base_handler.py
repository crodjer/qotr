from tornado import web
from .config import config

# pylint: disable=W0223
class BaseHandler(web.RequestHandler):
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
