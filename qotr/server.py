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
    make_application().listen(config.port)
    L.debug('http://%s:%s using %s configuration', config.host, config.port,
            config.name)
    ioloop.IOLoop.instance().start()
