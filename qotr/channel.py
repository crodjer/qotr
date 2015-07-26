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
