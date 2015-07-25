from tornado import ioloop, websocket

if __name__ == '__main__':
    conn = websocket.websocket_connect('ws://localhost:5000/foo')
    ioloop.IOLoop.instance().start()
