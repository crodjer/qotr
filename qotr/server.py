import logging

from qotr.config import config
from qotr.channel_handler import ChannelHandler
from qotr.chat_handler import ChatHandler
from tornado import ioloop, web

L = logging.getLogger('qotr')

def make_application():
    return web.Application([
        (r"/c/new", ChannelHandler),
        (r"/c/([^/]+)", ChatHandler),
    ], debug=config.debug)

if __name__ == "__main__":
    make_application().listen(config.port) # pragma: no cover
    L.debug('http://%s:%s using %s configuration', config.host, config.port,
            config.name)                   # pragma: no cover
    ioloop.IOLoop.instance().start()       # pragma: no cover
