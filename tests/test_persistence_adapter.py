import pytz
import os

from unittest import TestCase
from unittest.mock import patch
from datetime import datetime

from chalicelib.slack_message import SlackMessage
from chalicelib.persistence_adapter import BotDB, PST_TIMEZONE

DB_NAME = "burrito_points_test"
DB_ENDPOINT_URL = "http://localhost:8000"


class PersistenceAdapterTestCase(TestCase):

    def setUp(self):
        os.environ['AWS_DEFAULT_REGION'] = 'us-west-2'
        self.db = BotDB(DB_NAME, DB_ENDPOINT_URL)
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

    def test_add_points_to_users(self):
        msg = SlackMessage(
            'testSender',
            ['testRecipient1'],
            'testMessage',
            'testChannel',
        )

        pst_dt1 = datetime(2022, month=1, day=15, hour=1, minute=0, tzinfo=PST_TIMEZONE)
        pst_dt2 = datetime(2022, month=1, day=15, hour=1, minute=1, tzinfo=PST_TIMEZONE)
        pst_dt3 = datetime(2022, month=1, day=15, hour=23, minute=1, tzinfo=PST_TIMEZONE)
        pst_dt4 = datetime(2022, month=1, day=16, hour=1, minute=1, tzinfo=PST_TIMEZONE)

        with patch('chalicelib.persistence_adapter.BotDB._utc_now') as mocked_dt:
            mocked_dt.return_value = pst_dt1.astimezone(pytz.utc)

            self.db.add_points_to_users(msg.sender, msg.recipients, msg.channel, 1)

            mocked_dt.reset_mock()
            mocked_dt.return_value = pst_dt2.astimezone(pytz.utc)

            given_today = self.db.get_number_of_points_given_so_far_today('testSender')
            self.assertEquals(given_today, 1)

            mocked_dt.reset_mock()
            mocked_dt.return_value = pst_dt2.astimezone(pytz.utc)

            self.db.add_points_to_users(msg.sender, ['testRecipient1'], msg.channel, 1)

            given_today = self.db.get_number_of_points_given_so_far_today('testSender')
            self.assertEquals(given_today, 2)

            mocked_dt.reset_mock()
            mocked_dt.return_value = pst_dt3.astimezone(pytz.utc)

            given_today = self.db.get_number_of_points_given_so_far_today('testSender')
            self.assertEquals(given_today, 2)

            mocked_dt.reset_mock()
            mocked_dt.return_value = pst_dt4.astimezone(pytz.utc)

            given_today = self.db.get_number_of_points_given_so_far_today('testSender')
            self.assertEquals(given_today, 0)

            leaderboard = self.db.get_user_points()
            self.assertEquals(len(leaderboard), 1)
            self.assertEquals(leaderboard[0][0], 'testRecipient1')
            self.assertEquals(leaderboard[0][1], 2)

    def test_number_of_points_given_so_far_today(self):
        msg = SlackMessage(
            'testSender',
            ['testRecipient1'],
            'testMessage',
            'testChannel',
        )

        pst_dt1 = datetime(2022, month=1, day=15, hour=23, tzinfo=PST_TIMEZONE)
        pst_dt2 = datetime(2022, month=1, day=16, hour=1, tzinfo=PST_TIMEZONE)

        with patch('chalicelib.persistence_adapter.BotDB._utc_now') as mocked_dt:
            mocked_dt.return_value = pst_dt1.astimezone(pytz.utc)

            self.db.add_points_to_users(msg.sender, ['testRecipient1'], msg.channel, 1)
            mocked_dt.assert_called_once()

            given_today = self.db.get_number_of_points_given_so_far_today('testSender')
            self.assertEquals(given_today, 1)

            mocked_dt.reset_mock()
            mocked_dt.return_value = pst_dt2.astimezone(pytz.utc)

            self.db.add_points_to_users(msg.sender, ['testRecipient1'], msg.channel, 1)
            mocked_dt.assert_called_once()

            given_today = self.db.get_number_of_points_given_so_far_today('testSender')
            self.assertEquals(given_today, 1)



