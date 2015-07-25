import logging

from collections import defaultdict
from qotr.message import Message, MessageTypes as MT
from qotr.channel import Channel
from tornado import websocket

L = logging.getLogger(__name__)

# We don't need to override `data_received`
# pylint: disable=W0223
class ChatHandler(websocket.WebSocketHandler):

    CHANNELS = defaultdict(Channel)

    nick = None
    channel = None
    channel_id = None

    def __init__(self, *args, **kwargs):
        super(ChatHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def _handle_request_exception(self, e):
        L.exception('An error occured: %s', repr(e))

    # Open allows for any number arguments, unlike what pylint thinks.
    # pylint: disable=W0221
    def open(self, channel_id):
        self.channel_id = channel_id
        self.channel = self.CHANNELS[self.channel_id]

        # Tell the user the channel's salt.
        self.send_salt()
        self.broadcast(Message(MT.join, sender=self))

    def send_salt(self):
        Message(MT.salt, body=self.channel.salt).send(self)

    def respond_with_error(self, error="An error occured."):
        Message(MT.error, body=error).send(self)

    def broadcast(self, message):
        '''
        Broadcast a message, excluding the sender if present.
        '''

        for client in self.channel - {message.sender}:
            message.send(client)

    def handle_salt(self, message):
        '''
        Set the server's encryption salt.
        '''

        if self.channel.salt:
            self.respond_with_error("Already have an encryption salt")
        else:
            self.channel.salt = message.body
            self.broadcast(message)

    def handle_join(self, message):
        '''
        Handle a join with the nick provided in the body.
        '''

        if self in self.channel:
            self.respond_with_error("Already in channel")

        self.nick = message.body
        self.channel.add(self)
        self.broadcast(Message(MT.join, sender=self))

    def handle_members(self, _):
        '''
        Handle a chat message.
        '''
        Message(MT.members, body=self.channel.members).send(self)

    def handle_chat(self, message):
        '''
        Handle a chat message.
        '''
        self.broadcast(message)

    def on_message(self, message):
        try:
            message = Message.from_json(message)
            message.sender = self
            getattr(self, 'handle_' + message.kind.name)(message)
        except ValueError:
            self.respond_with_error("Invalid message format")
        except KeyError:
            self.respond_with_error("Invalid message kind")

    def on_close(self):
        if self in self.channel:
            self.channel.remove(self)

        if not self.channel:
            try:
                del self.CHANNELS[self.channel_id]
            except KeyError:
                pass

        self.broadcast(Message(MT.part, sender=self))
