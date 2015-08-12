from tornado import web

from .base import set_cors_headers

# pylint: disable=W0223
class Static(web.StaticFileHandler):

    def set_extra_headers(self, _):
        set_cors_headers(self)
