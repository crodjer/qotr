import unittest

from qotr.channels import Channels
from qotr.exceptions import ChannelAlreadyExists, ChannelDoesNotExist

from unittest.mock import Mock

class TestChannels(unittest.TestCase):

    channel_id = 'test-channel'
    salt = 'common'
    key_hash = 'test-key-hmac'
    member = Mock(nick='foo')

    def setUp(self):
        super(TestChannels, self).setUp()
        Channels.reset()

    def test_create(self):
        Channels.create(self.channel_id, self.salt, self.key_hash)
        channel = Channels.get(self.channel_id)
        self.assertEqual(self.salt, channel.salt)
        self.assertEqual(self.key_hash, channel.key_hash)

    def test_existing(self):
        self.assertFalse(Channels.exists(self.channel_id))
        Channels.create(self.channel_id, self.salt, self.key_hash)
        self.assertTrue(Channels.exists(self.channel_id))

        with self.assertRaises(ChannelAlreadyExists):
            Channels.create(self.channel_id, self.salt, self.key_hash)

    def test_does_not_exist(self):
        with self.assertRaises(ChannelDoesNotExist):
            Channels.get(self.channel_id)

    def test_join_part(self):
        channel = Channels.create(self.channel_id, self.salt, self.key_hash)
        channel.join(self.member)
        self.assertTrue(channel.has(self.member))
        self.assertEqual([self.member.nick], channel.members)
        channel.part(self.member)
        self.assertEqual([], channel.members)

    def test_reset(self):
        Channels.create(self.channel_id, self.salt, self.key_hash)
        self.assertTrue(Channels.exists(self.channel_id))
        Channels.reset()
        self.assertFalse(Channels.exists(self.channel_id))
