from tornado import testing

from qotr.server import make_application
from qotr.config import config

class TestChannelHandler(testing.AsyncHTTPTestCase):
    '''
    Test the channel creation handler.
    '''

    port = None
    application = None

    def get_app(self):
        return make_application()

    # def test_index(self):
    #     response = self.fetch('/')
    #     self.assertEqual(200, response.code)

    # def test_channel(self):
    #     response = self.fetch('/c/foo')
    #     self.assertEqual(200, response.code)

    # def test_arbitrary(self):
    #     response = self.fetch('/arbitrary-page')
    #     self.assertEqual(404, response.code)

    def test_https_redirect(self):
        _old_cfg = config.redirect_to_https
        config.redirect_to_https = True
        response = self.fetch('/c/foo', follow_redirects=False, headers={
            'x-forwarded-proto': 'http'
        })
        config.redirect_to_https = _old_cfg
        self.assertEqual(301, response.code)
