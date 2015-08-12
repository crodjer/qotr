import unittest

from qotr.channels import Channels
from qotr.config import config
from qotr.exceptions import ChannelAlreadyExists, ChannelDoesNotExist

from tornado import testing, gen
from mock import Mock

from .base_async_test import BaseAsyncTest

class TestChannels(unittest.TestCase):

    channel_id = 'test-channel'
    meta = 'common'
    member = Mock(nick='foo')

    def setUp(self):
        super(TestChannels, self).setUp()
        Channels.reset()

    def test_create(self):
        Channels.create(self.channel_id, self.meta)
        channel = Channels.get(self.channel_id)
        self.assertEqual(self.meta, channel.meta)

    def test_existing(self):
        self.assertFalse(Channels.exists(self.channel_id))
        Channels.create(self.channel_id, self.meta)
        self.assertTrue(Channels.exists(self.channel_id))

        with self.assertRaises(ChannelAlreadyExists):
            Channels.create(self.channel_id, self.meta)

    def test_does_not_exist(self):
        with self.assertRaises(ChannelDoesNotExist):
            Channels.get(self.channel_id)

    def test_remove(self):
        Channels.create(self.channel_id, self.meta)
        self.assertEqual(1, Channels.count())
        Channels.remove(self.channel_id)
        self.assertEqual(0, Channels.count())
        Channels.remove(self.channel_id)
        self.assertEqual(0, Channels.count())

    def test_join_part(self):
        channel = Channels.create(self.channel_id, self.meta)
        channel.join(self.member)
        self.assertTrue(channel.has(self.member))
        self.assertEqual({
            self.member.id: self.member.nick
        }, channel.members)
        channel.part(self.member)
        self.assertEqual({}, channel.members)

    def test_reset(self):
        Channels.create(self.channel_id, self.meta)
        self.assertTrue(Channels.exists(self.channel_id))
        Channels.reset()
        self.assertFalse(Channels.exists(self.channel_id))

class TestChannelDeletion(BaseAsyncTest):

    @testing.gen_test
    def test_channel_delete(self):
        key = 'test-channel'
        Channels.create(key, 'common')
        yield gen.sleep(config.cleanup_period * 1.1)
        self.assertFalse(Channels.exists(key))


    @testing.gen_test
    def test_channel_no_delete(self):
        key = 'test-channel'
        c = Channels.create(key, 'common')
        c.join(Mock(nick='foo'))
        yield gen.sleep(config.cleanup_period * 1.1)
        self.assertTrue(Channels.exists(key))
