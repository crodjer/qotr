# pylint: disable=W0223, W0221
import logging

from qotr.config import config
from qotr.channels import Channels
from qotr.channel_handler import ChannelHandler
from qotr.chat_handler import ChatHandler
from tornado import ioloop, web

L = logging.getLogger('qotr')

class IndexHandler(web.RequestHandler):

    def get(self, _=None):
        self.render('../dist/index.html')

def make_application():
    ioloop.PeriodicCallback(Channels.cleanup,
                            config.cleanup_period * 1000).start()

    return web.Application([
        (r"/()", IndexHandler),
        (r"/c/([^/]+)", IndexHandler),
        (r"/channels/new", ChannelHandler),
        (r"/channels/([^/]+)", ChatHandler),
        (r"/(.*)", web.StaticFileHandler, {'path': 'dist/'})

    ], debug=config.debug)

if __name__ == "__main__":
    make_application().listen(config.port) # pragma: no cover
    L.debug('http://%s:%s using %s configuration', config.host, config.port,
            config.name)                   # pragma: no cover
    ioloop.IOLoop.instance().start()       # pragma: no cover
