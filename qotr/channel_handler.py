import json
import logging

from .channels import Channels
from .exceptions import ChannelAlreadyExists
from tornado import web

L = logging.getLogger(__name__)

# pylint: disable=W0223
class ChannelHandler(web.RequestHandler):
    '''
    Allows creation of channels.
    '''

    def set_default_headers(self):
        self.set_header('Content-Type', 'application/json')

    def post(self):
        channel_id = self.get_argument('id')
        salt = self.get_argument('salt')
        key_hash = self.get_argument('key_hash')

        try:
            Channels.create(channel_id, salt, key_hash)
            self.write({
                "id": channel_id,
                "salt": salt
            })
        except ChannelAlreadyExists:
            self.set_status(409) # Conflict
            self.write({
                "error": "The requested channel already exists."
            })
