from tornado import testing, httpserver
from qotr.channels import Channels
from qotr.server import make_application

# This test uses coroutine style.
class BaseAsyncTest(testing.AsyncTestCase):

    port = None
    channel_id = 'test-channel'
    salt = 'common'
    key_hash = 'test-key-hmac'

    def setUp(self):
        super(BaseAsyncTest, self).setUp()
        Channels.reset()

        application = make_application()
        server = httpserver.HTTPServer(application)
        socket, self.port = testing.bind_unused_port()
        server.add_socket(socket)
