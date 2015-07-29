import json

from tornado import websocket, testing, httpserver
from qotr.server import make_application
from qotr.channels import Channels

from .utils import m

def send(client, obj):
    return client.write_message(json.dumps(obj))

# This test uses coroutine style.
class TestChatHandler(testing.AsyncTestCase):

    port = None
    channel = 'test-channel'

    def setUp(self):
        super(TestChatHandler, self).setUp()
        Channels.reset()
        application = make_application()
        server = httpserver.HTTPServer(application)
        socket, self.port = testing.bind_unused_port()
        server.add_socket(socket)

    def _c(self):
        return websocket.websocket_connect(
            'ws://localhost:{}/{}'.format(self.port, self.channel)
        )

    @testing.gen_test
    def test_connect(self):
        c = yield self._c()
        response = yield c.read_message()
        message = json.loads(response)

        self.assertEqual('salt', message['kind'])
        self.assertEqual(None, message['body'])

    @testing.gen_test
    def test_salt(self):
        salt = 'common'

        c1 = yield self._c()
        send(c1, m('salt', salt))

        c2 = yield self._c()
        response = yield c2.read_message()
        self.assertEqual(m('salt', salt), json.loads(response))
