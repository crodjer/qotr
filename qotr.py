import os
import uuid

from collections import defaultdict
from tornado import ioloop, web, websocket, escape

# We don't need to override `data_received`
# pylint: disable=W0223
class ChatClient(websocket.WebSocketHandler):

    CHANNELS = defaultdict(set)

    nick = None
    channel_id = None

    def __init__(self, *args, **kwargs):
        super(ChatClient, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    @property
    def channel(self):
        return self.CHANNELS[self.channel_id]

    def broadcast(self, message_type, content=None, tell_me=False):
        '''
        Broadcast a message. Optionally, to myself as well.
        '''

        clients = self.channel
        if not tell_me:
            clients = clients - {self}

        for client in clients:
            client.write_message({
                "nick": self.nick,
                "type": message_type,
                "message": content
            })

    # Open allows for any number arguments, unlike what pylint thinks.
    # pylint: disable=W0221
    def open(self, channel_id):
        self.nick = str(uuid.uuid4())
        self.channel_id = channel_id
        self.channel.add(self)
        self.broadcast("join")

    def on_message(self, message):
        self.broadcast("chat", message)

    def on_close(self):
        self.channel.remove(self)
        if not self.channel:
            del self.CHANNELS[self.channel_id]
        self.broadcast("part")

def main():
    application = web.Application([
        (r"/([^/]+)", ChatClient),
    ], debug=True)

    port = int(os.environ.get("PORT", 5000))
    application.listen(port)
    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
