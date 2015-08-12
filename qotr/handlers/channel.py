import logging

from .base import Base, set_cors_headers
from qotr.channels import Channels
from qotr.exceptions import ChannelAlreadyExists

L = logging.getLogger(__name__)

# pylint: disable=W0223
class Channel(Base):
    '''
    Allows creation of channels.
    '''

    def set_default_headers(self):
        set_cors_headers(self)
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
