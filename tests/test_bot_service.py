import os

from unittest import TestCase
from unittest.mock import MagicMock

from chalicelib.bot_service import BotService
from chalicelib.slack_message import SlackMessage
from chalicelib.persistence_adapter import BotDB
from chalicelib.global_constants import EMOJI

DB_NAME = "burrito_points_test"
DB_ENDPOINT_URL = "http://localhost:8000"


class BotServiceTests(TestCase):

    def setUp(self):
        os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
        self.db = BotDB(DB_NAME, DB_ENDPOINT_URL)
        self.client_mock = MagicMock()
        self.client_mock.chat_postMessage = MagicMock(return_value=None)
        self.client_mock.chat_postEphemeral = MagicMock(return_value=None)
        self.service = BotService(self.client_mock, DB_NAME, DB_ENDPOINT_URL)

        try:
            self.db.destroy_table()
        except Exception as e:
            print(e)

        try:
            self.db.create_table()
        except Exception as e:
            print(e)

    # def tearDown(self):
    #     self.db.destroy_table()

    def _reset_client_mocks(self):
        self.client_mock.chat_postEphemeral.reset_mock()
        self.client_mock.chat_postMessage.reset_mock()

    def test_add_points_to_user(self):
        msg = SlackMessage(
            "testSender",
            ["testRecipient"],
            f"<@testRecipient> testMessage :{EMOJI}: :{EMOJI}:",
            "testChannel",
        )

        self.service.award_emoji_points_from_msg(msg)
        given_today = self.service.get_user_points_sent_today('testSender')
        self.assertEquals(given_today, 2)

        leaderboard = self.db.get_user_points()
        self.assertEquals(len(leaderboard), 1)
        self.assertEquals(leaderboard[0][1], 2)

    def test_add_multiple_points_to_multiple_users(self):
        # Give two emojis to two recipients
        msg1 = SlackMessage(
            "testSender",
            ["testRecipient1", "testRecipient2"],
            f"<@testRecipient1> <@testRecipient2> testMessage :{EMOJI}: :{EMOJI}:",
            "testChannel",
        )

        self.service.award_emoji_points_from_msg(msg1)
        self.client_mock.chat_postEphemeral.assert_called_once()
        self.assertEquals(self.client_mock.chat_postMessage.call_count, 2)

        given_today = self.service.get_user_points_sent_today('testSender')
        self.assertEquals(given_today, 4)

        self._reset_client_mocks()

        # Give 1 more emoji to first recipient
        msg2 = SlackMessage(
            "testSender",
            ["testRecipient1"],
            f"<@testRecipient1> testMessage :{EMOJI}:",
            "testChannel",
        )

        self.service.award_emoji_points_from_msg(msg2)
        self.client_mock.chat_postMessage.assert_called_once()
        self.client_mock.chat_postEphemeral.assert_called_once()

        given_today = self.service.get_user_points_sent_today('testSender')
        self.assertEquals(given_today, 5)

        self._reset_client_mocks()

        # Attempt to go over maximum allowed sends for the day
        self.service.award_emoji_points_from_msg(msg2)
        self.client_mock.chat_postEphemeral.assert_called_once()
        self.client_mock.chat_postMessage.assert_not_called()

        given_today = self.service.get_user_points_sent_today('testSender')
        self.assertEquals(given_today, 5)

        leaderboard = self.db.get_user_points()
        self.assertEquals(len(leaderboard), 2)
        self.assertEquals(leaderboard[0][0], 'testRecipient1')
        self.assertEquals(leaderboard[0][1], 3)
        self.assertEquals(leaderboard[1][0], 'testRecipient2')
        self.assertEquals(leaderboard[1][1], 2)
