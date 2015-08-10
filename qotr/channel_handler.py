import logging

from .base_handler import BaseHandler
from .channels import Channels
from .config import config
from .exceptions import ChannelAlreadyExists

L = logging.getLogger(__name__)

# pylint: disable=W0223
class ChannelHandler(BaseHandler):
    '''
    Allows creation of channels.
    '''

    def set_default_headers(self):
        if config.allowed_origin:

            self.set_header("Access-Control-Allow-Origin",
                            config.allowed_origin)
            self.set_header("Access-Control-Allow-Methods", "POST")
            self.set_header("Access-Control-Allow-Headers", "Content-Type")

        self.set_header('Content-Type', 'application/json')

    def get(self):

        self.write({
            "connections": Channels.connections(),
            "channels": Channels.count()
        })

    def post(self):
        channel_id = self.get_argument('id')
        salt = self.get_argument('salt')

        try:
            Channels.create(channel_id, salt)
            self.write({
                "id": channel_id,
                "salt": salt
            })
        except ChannelAlreadyExists:
            self.set_status(409) # Conflict
            self.write({
                "error": "The requested channel already exists."
            })
