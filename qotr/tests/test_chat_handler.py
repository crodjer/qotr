import json

from tornado import websocket, testing, gen
from qotr.channels import Channels
from qotr.exceptions import ChannelDoesNotExist

from .base_async_test import BaseAsyncTest
from .utils import m

def send(client, obj):
    return client.write_message(json.dumps(obj))

# This test uses coroutine style.
class TestChatHandler(BaseAsyncTest):

    port = None
    channel_id = 'test-channel'
    meta = 'common'

    def setUp(self):
        super(TestChatHandler, self).setUp()
        Channels.create(self.channel_id, self.meta)

    def _mk_connection(self):
        return websocket.websocket_connect(
            'ws://localhost:{}/channels/{}'.format(self.port, self.channel_id)
        )

    @gen.coroutine
    def _mk_client(self, nick, join=True):
        c = yield self._mk_connection()
        # Discard the config
        response = yield c.read_message()
        c.config = json.loads(response)['body']

        if join:
            send(c, m('join', nick))
            # Discard the join message
            yield c.read_message() # C1's join

        raise gen.Return(c)

    @testing.gen_test
    def test_connect(self):
        c = yield self._mk_connection()
        response = yield c.read_message()
        message = json.loads(response)

        self.assertEqual('config', message['kind'])
        self.assertEqual(self.meta, message['body']['meta'])

    @testing.gen_test
    def test_join(self):
        channel = Channels.get(self.channel_id)
        self.assertEqual(0, len(channel.clients))

        c1 = yield self._mk_client('foo')
        yield self._mk_client('bar')
        yield c1.read_message() # C2's join

        self.assertEqual(2, len(channel.clients))

    @testing.gen_test
    def test_ping(self):
        channel = Channels.get(self.channel_id)
        self.assertEqual(0, len(channel.clients))

        c = yield self._mk_client('foo')
        send(c, m('ping'))
        response = yield c.read_message()

        self.assertEqual({
            "kind": "pong",
            "body": None,
            "sender": None
        }, json.loads(response))

    @testing.gen_test
    def test_nick(self):
        channel = Channels.get(self.channel_id)
        nick_1 = 'foo'
        nick_2 = 'bar'

        c1 = yield self._mk_client(nick_1)
        yield self._mk_client(nick_2)
        yield c1.read_message() # C2's join

        self.assertEqual({nick_1, nick_2}, set(channel.members.values()))

    @testing.gen_test
    def test_nick_change(self):
        channel = Channels.get(self.channel_id)
        self.assertEqual(0, len(channel.clients))

        c1 = yield self._mk_client('foo')
        c2 = yield self._mk_client('bar')

        send(c1, m('nick', 'foo-new'))
        response = yield c2.read_message()

        self.assertEqual({
            "kind": "nick",
            "body": "foo-new",
            "sender": c1.config['id']
        }, json.loads(response))

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
            'sender': c1.config['id'],
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
            'sender': c2.config['id'],
            'kind': 'part',
            'body': None
        }, json.loads(response))

        c1.close()

        # Wait for the channel to be removed.
        yield gen.sleep(0.001)

        with self.assertRaises(ChannelDoesNotExist):
            Channels.get(self.channel_id)

    @testing.gen_test
    def test_members(self):
        c = yield self._mk_client('foo')
        send(c, m('members'))
        response = yield c.read_message()
        self.assertEqual(m('members', {
            c.config['id']: 'foo'
        }), json.loads(response))

    @testing.gen_test
    def test_invalid_message_object(self):
        c = yield self._mk_client('foo')
        c.write_message('not-a-json-object')
        response = yield c.read_message()
        self.assertEqual('error', json.loads(response)['kind'])

    @testing.gen_test
    def test_invalid_kind(self):
        c = yield self._mk_client('foo')
        send(c, m('invalid-kind'))
        response = yield c.read_message()
        self.assertEqual('error', json.loads(response)['kind'])

    @testing.gen_test
    def test_double_join(self):
        c = yield self._mk_client('foo')
        send(c, m('join'))
        response = yield c.read_message()
        self.assertEqual('error', json.loads(response)['kind'])
