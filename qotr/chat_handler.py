import logging

from qotr.message import Message, MessageTypes as MT
from qotr.channels import Channels
from qotr.exceptions import ChannelDoesNotExist
from tornado import websocket, gen

L = logging.getLogger(__name__)

# We don't need to override `data_received`
# pylint: disable=W0223
class ChatHandler(websocket.WebSocketHandler):

    nick = None
    channel = None
    channel_id = None
    authenticated = False

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
        try:
            self.channel = Channels.get(self.channel_id)
            self.channel.connections += 1
            self.nick = self.channel.new_id()

            # Tell the user the channel's salt.
            Message(MT.salt, body=self.channel.salt).send(self)
        except ChannelDoesNotExist:
            self.respond_with_error("Channel does not exist")
            self.channel.connections -= 1
            self.close()

    def respond_with_error(self, error="An error occured."):
        Message(MT.error, body=error).send(self)

    def broadcast(self, message):
        '''
        Broadcast a message, excluding the sender if present.
        '''

        for client in self.channel.clients - {message.sender}:
            message.send(client)

    def handle_nick(self, message):
        '''
        Handle a nick change for the client.
        '''

        self.nick = message.body
        if self.channel.has(self):
            self.broadcast(message)

    def handle_join(self, message):
        '''
        Handle a authentication message from the member.
        '''

        if self.channel.has(self):
            self.respond_with_error("Already in channel")
        elif message.body == self.channel.key_hash:
            self.channel.join(self)
            Message(MT.join, self.nick).send(self)
            self.broadcast(Message(MT.join, self.nick, sender=self))
            self.authenticated = True

    def handle_members(self, _):
        '''
        Handle a chat message.
        '''
        if not self.authenticated:
            self.respond_with_error("Not authenticated")
            return
        Message(MT.members, body=self.channel.members).send(self)

    def handle_chat(self, message):
        '''
        Re-broadcast any chat messages that come in.
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

    @gen.coroutine
    def on_close(self):
        if not self.channel:
            return

        self.channel.connections -= 1

        if self.channel.has(self):
            self.channel.part(self)
            self.broadcast(Message(MT.part, sender=self))

        if self.channel.connections <= 0:
            L.debug('Deleting channel: %s', self.channel_id)
            Channels.remove(self.channel_id)

    def __repr__(self):
        return 'Chat: {}@{}'.format(
            self.nick or '<unknown>',
            self.channel_id
        ) # pragma: no cover
