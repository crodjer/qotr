import os

from qotr.chat_handler import ChatHandler
from tornado import ioloop, web

def make_application():
    return web.Application([
        (r"/([^/]+)", ChatHandler),
    ], debug=True)

if __name__ == "__main__":
    make_application().listen(int(os.environ.get("PORT", 5000)))

    ioloop.IOLoop.instance().start()
