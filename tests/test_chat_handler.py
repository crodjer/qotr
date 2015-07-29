import json

from tornado import websocket, testing, httpserver
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

    def _c(self):
        return websocket.websocket_connect(
            'ws://localhost:{}/c/{}'.format(self.port, self.channel_id)
        )

    @testing.gen_test
    def test_connect(self):
        c = yield self._c()
        response = yield c.read_message()
        message = json.loads(response)

        self.assertEqual('salt', message['kind'])
        self.assertEqual(self.salt, message['body'])

    @testing.gen_test
    def test_auth(self):
        channel = Channels.get(self.channel_id)
        self.assertEqual(0, len(channel.clients))

        c1 = yield self._c()
        c2 = yield self._c()

        # Discard the salts.
        yield c1.read_message()
        yield c2.read_message()

        send(c1, m('join', self.key_hash))
        send(c2, m('join', self.key_hash))

        yield c1.read_message()
        yield c2.read_message()

        self.assertEqual(2, len(channel.clients))


    @testing.gen_test
    def test_nick(self):
        channel = Channels.get(self.channel_id)
        nick = 'foo'
        self.assertEqual(0, len(channel.clients))

        c = yield self._c()
        yield c.read_message()

        send(c, m('nick', nick))
        send(c, m('join', self.key_hash))
        yield c.read_message()

        self.assertEqual([nick], channel.members)


    @testing.gen_test
    def test_chat(self):
        channel = Channels.get(self.channel_id)
        self.assertEqual(0, len(channel.clients))

        c1 = yield self._c()
        c2 = yield self._c()

        # Discard the salts.
        yield c1.read_message()
        yield c2.read_message()

        send(c1, m('nick', 'foo'))
        send(c2, m('nick', 'bar'))
        send(c1, m('join', self.key_hash))
        send(c2, m('join', self.key_hash))

        # Own and the other's join messagse. c2 gets it first because of the
        # way tornado works.
        yield c1.read_message()
        yield c2.read_message()
        yield c2.read_message()

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

        c1 = yield self._c()
        c2 = yield self._c()

        # Discard the salts.
        yield c1.read_message()
        yield c2.read_message()

        send(c1, m('nick', 'foo'))
        send(c2, m('nick', 'bar'))
        send(c1, m('join', self.key_hash))
        send(c2, m('join', self.key_hash))

        # Own and the other's join messagse. c2 gets it first because of the
        # way tornado works.
        yield c1.read_message()
        yield c2.read_message()
        yield c2.read_message()

        c2.close()
        response = yield c1.read_message()

        self.assertEqual({
            'sender': 'bar',
            'kind': 'part',
            'body': None
        }, json.loads(response))

        # Somehow need to figure out how to wait for the raise here.
        # with self.assertRaises(ChannelDoesNotExist) as context:
        #     c1.close()
        #     Channels.get(self.channel_id)
