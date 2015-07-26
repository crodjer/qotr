import json
from enum import Enum

MessageTypes = Enum('MessageTypes', [
    'salt',
    'join',
    'chat',
    'part',
    'members',
    'error'
])

class Message(object):
    '''
    A message.

    ``kind`` is can be one off ``MessageTypes``.
    ``body`` stores the content body.
    ``sender`` identifies who the message is from.
    '''

    def __init__(self, kind, body=None, sender=None):
        self.kind = kind
        self.body = body
        self.sender = sender

    def as_json(self):
        '''
        Convert a message into a JSON serializable object.
        '''

        return {
            "kind": self.kind.name,
            "body": self.body,
            "sender": self.sender.nick if self.sender else None,
        }

    def send(self, client):
        '''
        Send self to the client.
        '''
        client.write_message(self.as_json())

    @classmethod
    def from_object(cls, obj):
        obj['kind'] = MessageTypes[obj['kind']]
        return cls(**obj)

    @classmethod
    def from_json(cls, string):
        return cls.from_object(json.loads(string))
