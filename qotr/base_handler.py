from tornado import web
from .config import config

# pylint: disable=W0223
class BaseHandler(web.RequestHandler):
    '''
    A base request handler.
    '''

    def prepare(self):

        if self.request.protocol == "http" and config.redirect_to_https:
            self.redirect(
                self.request.full_url().replace('http:', 'https:'),
                permanent=True
            )
