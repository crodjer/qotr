from .exceptions import ChannelAlreadyExists

class Channel(object):
    '''
    A communication channel.
    A set, which also stores the channel information.
    '''

    def __init__(self, salt, key_hash):
        self.clients = set()
        self.salt = salt
        self.key_hash = key_hash

    @property
    def members(self):
        '''
        Get the list of members in the channel.
        '''

        return [client.nick
                for client in self]

class Channels(object):

    CHANNELS = {}

    @classmethod
    def get(cls, name):
        return cls.CHANNELS[name]

    @classmethod
    def exists(cls, name):
        return name in cls.CHANNELS

    @classmethod
    def create(cls, name, salt, hashed_key):
        if cls.exists(name):
            raise ChannelAlreadyExists()

        cls.CHANNELS[name] = Channel(salt, hashed_key)
        return cls.CHANNELS[name]

    @classmethod
    def remove(cls, name):
        try:
            del cls.CHANNELS[name]
        except KeyError:
            pass

    @classmethod
    def reset(cls):
        cls.CHANNELS = {}
