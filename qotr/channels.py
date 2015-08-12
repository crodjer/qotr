import logging

from datetime import datetime, timedelta
from hashids import Hashids
from .config import config
from .exceptions import ChannelAlreadyExists, ChannelDoesNotExist

L = logging.getLogger(__name__)

class Channel(object):
    '''
    A communication channel.
    A set, which also stores the channel information.
    '''

    connections = 0
    id_source = 0


    def __init__(self, meta):
        self.clients = set()
        self.meta = meta
        self.hash_ids = Hashids(salt=str(meta), min_length=6)
        self.created_at = datetime.now()

    def new_id(self):
        self.id_source += 1
        return self.hash_ids.encode(self.id_source)

    def has(self, client):
        return client in self.clients

    def join(self, client):
        self.clients.add(client)

    def part(self, client):
        self.clients.remove(client)

    def is_empty(self):
        return not self.clients

    @property
    def members(self):
        '''
        Get the list of members in the channel.
        '''

        return {
            client.id: client.nick
            for client in self.clients
        }

class Channels(object):

    CHANNELS = {}

    @classmethod
    def get(cls, name):
        try:
            return cls.CHANNELS[name]
        except KeyError:
            raise ChannelDoesNotExist()

    @classmethod
    def exists(cls, name):
        return name in cls.CHANNELS

    @classmethod
    def create(cls, name, meta):
        if cls.exists(name):
            raise ChannelAlreadyExists()

        cls.CHANNELS[name] = Channel(meta)
        return cls.CHANNELS[name]

    @classmethod
    def remove(cls, name):
        try:
            del cls.CHANNELS[name]
        except KeyError:
            pass

    @classmethod
    def connections(cls):
        return sum(c.connections for c in cls.CHANNELS.values())

    @classmethod
    def count(cls):
        return len(cls.CHANNELS)

    @classmethod
    def reset(cls):
        cls.CHANNELS = {}

    @classmethod
    def cleanup(cls):
        delta = timedelta(seconds=config.channel_timeout)
        now = datetime.now()

        for key, channel in set(cls.CHANNELS.items()):
            if channel.is_empty() and delta > (now - channel.created_at):
                cls.remove(key)
