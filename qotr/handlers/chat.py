import logging

from qotr.message import Message, MessageTypes as MT
from qotr.channels import Channels
from qotr.exceptions import ChannelDoesNotExist

from tornado import websocket, gen

L = logging.getLogger(__name__)

# We don't need to override `data_received`
# pylint: disable=W0223
class Chat(websocket.WebSocketHandler):

    id = None
    nick = None
    channel = None
    channel_id = None

    def __init__(self, *args, **kwargs):
        super(Chat, self).__init__(*args, **kwargs)

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
            self.id = self.channel.new_id()
            # Tell the user their id and the channel's meta data.
            Message(MT.config, body={
                "id": self.id,
                "meta": self.channel.meta
            }).send(self)
            self.channel.connections += 1
        except ChannelDoesNotExist:
            self.respond_with_error("Channel does not exist.")
            self.close()

    def respond_with_error(self, error="An error occured."):
        L.warn("Error response @%s: %s", self.channel_id, error)
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

        if self.channel.has(self):
            self.broadcast(message)
        self.nick = message.body

    def handle_join(self, message):
        '''
        Handle a authentication message from the member.
        '''

        if self.channel.has(self):
            self.respond_with_error("Already in the channel.")

        self.nick = message.body
        self.channel.join(self)
        Message(MT.join, self.nick).send(self)
        self.broadcast(Message(MT.join, self.nick, sender=self))

    def handle_members(self, _):
        '''
        Handle a chat message.
        '''
        Message(MT.members, body=self.channel.members).send(self)

    def handle_chat(self, message):
        '''
        Re-broadcast any chat messages that come in.
        '''
        self.broadcast(message)

    def handle_ping(self, _):
        '''
        Re-broadcast any chat messages that come in.
        '''
        Message(MT.pong).send(self)

    def on_message(self, message):
        try:
            message = Message.from_json(message)
            message.sender = self
            getattr(self, 'handle_' + message.kind.name)(message)
        except ValueError:
            self.respond_with_error("Invalid message format.")
        except KeyError:
            self.respond_with_error("Invalid message kind.")

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
