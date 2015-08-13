==============
How QOTR works
==============

Channel creation
================

 - A client (browser) generates two ids using shortid_, one is the channel id
   and the other is the password to channel.
 - A 128 byte salt is created using forge_.
 - The client then makes a post request to the server with the channel id and
   the base 64 encoded salt. The server encodes these.

Connecting to channel
=====================

 - The clients connect to a channel via websockets. The channel should have been
   created already on the server.
 - As soon as a connection is established, the server sends back a member id
   and the salt.
 - The client then using the salt and the key (shared through an independent
   way, certainly not through the QOTR servers), generate an AES key.

Messages
========

 - The communication happens in form of JSON messages.
 - Messages have a sender, which will be the sender id that the server
   generated. In case the message is coming from the server, the sender is null.
 - There are various kinds of messages the server/clients understand: join,
   ping, pong, nick, config, chat, part, members, error. The message kind is not
   encrypted.
 - Each message also may or may not have a body. A message from a member will
   always be encrypted or be null. Unencrypted messages/wrongly encrypted
   messages result in errors for other members to see as warnings.
 - The message body is made of three parts, separated by '|'s: A 32 byte IV,
   the IV - channel key hmac, and the encrypted message.
 - The IV hmac is supposed to prove that you and the sender are using the same
   keys.
 - The server is completely unaware of any encryption whatsoever, except storing
   the salt. Although, it is stored under the name 'meta', which need not be an
   encryption salt.

.. _shortid: https://github.com/dylang/shortid
.. _forge: https://github.com/digitalbazaar/forge
