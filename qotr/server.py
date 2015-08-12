import logging

from qotr.channels import Channels
from qotr.config import config
from qotr import handlers

from tornado import ioloop, web

L = logging.getLogger('qotr')

def make_application():
    ioloop.PeriodicCallback(Channels.cleanup,
                            config.cleanup_period * 1000).start()

    return web.Application([
        (r"/()", handlers.Home),
        (r"/c/([^/]+)", handlers.Home),
        (r"/channels/", handlers.Channel),
        (r"/channels/new", handlers.Channel),
        (r"/channels/([^/]+)", handlers.Chat),
        (r"/(.*)", handlers.Static, {'path': 'dist/'})

    ], debug=config.debug)

if __name__ == "__main__":
    make_application().listen(config.port) # pragma: no cover
    L.debug('http://%s:%s using %s configuration', config.host, config.port,
            config.name)                   # pragma: no cover
    ioloop.IOLoop.instance().start()       # pragma: no cover
