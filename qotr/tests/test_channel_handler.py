import json
from tornado import testing, gen

from qotr.server import make_application
from qotr.channels import Channels

class TestChannelHandler(testing.AsyncHTTPTestCase):
    '''
    Test the channel creation handler.
    '''

    port = None
    application = None

    def get_app(self):
        Channels.reset()
        return make_application()

    def test_create(self):
        salt = "common"
        channel_id = "test-channel"

        body = "&".join([
            "id={channel_id}",
            "salt={salt}",
        ]).format(**locals())

        response = json.loads(self.fetch(
            '/channels/new', method='POST',
            body=body
        ).body.decode('utf8'))

        self.assertEqual({
            "salt": salt,
            "id": channel_id
        }, response)

        channel = Channels.get(channel_id)
        self.assertEqual(salt, channel.salt)

    def test_stats(self):
        channel = Channels.create("test-channel", "common")
        response = json.loads(self.fetch(
            '/channels/'
        ).body.decode('utf8'))

        self.assertEqual({
            "connections": 0,
            "channels": 1
        }, response)

        channel.connections += 1
        response = json.loads(self.fetch(
            '/channels/'
        ).body.decode('utf8'))

        self.assertEqual({
            "connections": 1,
            "channels": 1
        }, response)

    def test_confict(self):
        body = "&".join([
            "id=test-channel",
            "salt=common",
        ])

        self.fetch('/channels/new', method='POST', body=body)
        gen.sleep(0.001) # Wait for the fetch
        response = json.loads(self.fetch(
            '/channels/new', method='POST',
            body=body
        ).body.decode('utf8'))

        self.assertTrue("error" in response)
