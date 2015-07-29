from collections import defaultdict

class Channel(set):
    '''
    A communication channel.
    A set, which also stores the channel information.
    '''

    salt = None

    @property
    def members(self):
        '''
        Get the list of members in the channel.
        '''

        return [client.nick
                for client in self]

class Channels(object):

    CHANNELS = defaultdict(Channel)

    @classmethod
    def get(cls, name):
        return cls.CHANNELS[name]

    @classmethod
    def remove(cls, name):
        try:
            del cls.CHANNELS[name]
        except KeyError:
            pass

    @classmethod
    def reset(cls):
        cls.CHANNELS = defaultdict(Channel)
