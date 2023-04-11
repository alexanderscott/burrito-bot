from unittest import TestCase

from chalicelib.slack_message import SlackMessage
from tests.fixtures.messages import *


class SlackMessageTestCase(TestCase):

    def test_parse_single_emoji_single_recipient(self):
        msg = SlackMessage.parse(message_added_single_emoji_single_recipient())

        self.assertEquals(len(msg.recipients), 1)
        self.assertEquals(msg.recipients[0], 'U025RUT3QQM')
        self.assertEquals(msg.sender, 'U01AP4BM8SD')
        self.assertEquals(msg.count_emojis_in_message(), 1)

    def test_parse_multiple_emojis_single_recipient(self):
        msg = SlackMessage.parse(message_added_multiple_emojis_single_recipient())

        self.assertEquals(len(msg.recipients), 1)
        self.assertEquals(msg.recipients[0], 'U0G9QF9C6')
        self.assertEquals(msg.sender, 'U025RUT3QQM')
        self.assertEquals(msg.count_emojis_in_message(), 2)

    def test_parse_single_emoji_multiple_recipients(self):
        msg = SlackMessage.parse(message_added_single_emoji_multiple_recipients())

        self.assertEquals(len(msg.recipients), 2)
        self.assertEquals(msg.recipients[0], 'U0G9QF9C6')
        self.assertEquals(msg.recipients[1], 'U0G9QF9C7')
        self.assertEquals(msg.sender, 'U025RUT3QQM')
        self.assertEquals(msg.count_emojis_in_message(), 1)

    def test_parse_multiple_emojis_multiple_recipients(self):
        msg = SlackMessage.parse(message_added_multiple_emojis_multiple_recipients())

        self.assertEquals(len(msg.recipients), 2)
        self.assertEquals(msg.recipients[0], 'U0G9QF9C6')
        self.assertEquals(msg.recipients[1], 'U0G9QF9C7')
        self.assertEquals(msg.sender, 'U025RUT3QQM')
        self.assertEquals(msg.count_emojis_in_message(), 2)

    def test_parse_thread_message_single_emoji_single_participant(self):
        msg = SlackMessage.parse(thread_message_added_single_emoji_single_recipient())

        self.assertEquals(len(msg.recipients), 1)
        self.assertEquals(msg.recipients[0], 'U025RUT3QQM')
        self.assertEquals(msg.sender, 'U01AP4BM8SD')
        self.assertEquals(msg.count_emojis_in_message(), 1)
