import json

from tornado import websocket, testing, httpserver
from qotr.server import make_application

# This test uses coroutine style.
class TestChannel(testing.AsyncTestCase):

    port = None

    def setUp(self):
        super(TestChannel, self).setUp()
        application = make_application()
        server = httpserver.HTTPServer(application)
        socket, self.port = testing.bind_unused_port()
        server.add_socket(socket)

    def _make_client(self, key):
        return websocket.websocket_connect(
            'ws://localhost:{}/{}'.format(self.port, key)
        )

    @testing.gen_test
    def test_connect(self):
        client = yield self._make_client('foo')
        response = yield client.read_message()
        message = json.loads(response)

        self.assertEqual('salt', message['kind'])
        self.assertEqual(None, message['body'])

    @testing.gen_test
    def test_salt(self):
        salt = 'common'

        client_1 = yield self._make_client('foo')
        client_1.write_message(json.dumps({'kind': 'salt', 'body': salt}))

        client_2 = yield self._make_client('foo')
        response = yield client_2.read_message()
        message = json.loads(response)

        self.assertEqual('salt', message['kind'])
        self.assertEqual(salt, message['body'])
