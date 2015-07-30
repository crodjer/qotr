import json

from tornado import websocket, testing, httpserver, gen
from qotr.server import make_application
from qotr.channels import Channels
from qotr.exceptions import ChannelDoesNotExist

from .utils import m

def send(client, obj):
    return client.write_message(json.dumps(obj))

# This test uses coroutine style.
class TestChatHandler(testing.AsyncTestCase):

    port = None
    channel_id = 'test-channel'
    salt = 'common'
    key_hash = 'test-key-hmac'

    def setUp(self):
        super(TestChatHandler, self).setUp()
        Channels.reset()
        Channels.create(self.channel_id, self.salt, self.key_hash)

        application = make_application()
        server = httpserver.HTTPServer(application)
        socket, self.port = testing.bind_unused_port()
        server.add_socket(socket)

    def _mk_connection(self):
        return websocket.websocket_connect(
            'ws://localhost:{}/c/{}'.format(self.port, self.channel_id)
        )

    @gen.coroutine
    def _mk_client(self, nick, join=True):
        c = yield self._mk_connection()
        # Discard the salt.
        yield c.read_message()

        if nick:
            send(c, m('nick', nick))

        if join:
            send(c, m('join', self.key_hash))
            # Discard the join message
            yield c.read_message() # C1's join

        return c

    @testing.gen_test
    def test_connect(self):
        c = yield self._mk_connection()
        response = yield c.read_message()
        message = json.loads(response)

        self.assertEqual('salt', message['kind'])
        self.assertEqual(self.salt, message['body'])

    @testing.gen_test
    def test_join(self):
        channel = Channels.get(self.channel_id)
        self.assertEqual(0, len(channel.clients))

        c1 = yield self._mk_client('foo')
        yield self._mk_client('bar')
        yield c1.read_message() # C2's join

        self.assertEqual(2, len(channel.clients))

    @testing.gen_test
    def test_nick(self):
        channel = Channels.get(self.channel_id)
        nick_1 = 'foo'
        nick_2 = 'bar'

        c1 = yield self._mk_client(nick_1)
        yield self._mk_client(nick_2)
        yield c1.read_message() # C2's join

        self.assertEqual([nick_1, nick_2], channel.members)

    @testing.gen_test
    def test_chat(self):
        channel = Channels.get(self.channel_id)
        self.assertEqual(0, len(channel.clients))

        c1 = yield self._mk_client('foo')
        c2 = yield self._mk_client('bar')
        yield c1.read_message() # C2's join

        send(c1, m('chat', 'hey!'))
        response = yield c2.read_message()

        self.assertEqual({
            'sender': 'foo',
            'kind': 'chat',
            'body': 'hey!'
        }, json.loads(response))

    @testing.gen_test
    def test_part(self):
        channel = Channels.get(self.channel_id)
        self.assertEqual(0, len(channel.clients))

        c1 = yield self._mk_client('foo')
        c2 = yield self._mk_client('bar')
        yield c1.read_message() # C2's join

        c2.close()
        response = yield c1.read_message()

        self.assertEqual({
            'sender': 'bar',
            'kind': 'part',
            'body': None
        }, json.loads(response))

        c1.close()

        # Wait for the channel to be removed.
        yield gen.sleep(0.001)
        with self.assertRaises(ChannelDoesNotExist):
            Channels.get(self.channel_id)
