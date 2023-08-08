from typing import Tuple, Optional

from slack_sdk import WebClient

from chalicelib.persistence_adapter import BotDB
from chalicelib.global_constants import *
from chalicelib.response_generator import *


class BotService:

    def __init__(self, slack_client: WebClient, table_name: str, **kwargs):
        self.db = BotDB(table_name, **kwargs)
        self.client = slack_client

    def _post_channel_message_to_user(self, channel: str, user: str, text: str, thread_ts: Optional[str] = None):
        self.client.chat_postEphemeral(
            channel=channel,
            user=user,
            text=text,
            thread_ts=thread_ts,
        )

    def _post_dm_to_user(self, user, text):
        self.client.chat_postMessage(
            channel=user,
            text=text,
        )

    def _post_channel_message(self, channel: str, text: str, thread_ts: Optional[str] = None):
        # TODO determine whether or not to use reply_broadcast to send to all channel members
        self.client.chat_postMessage(
            channel=channel,
            text=text,
            thread_ts=thread_ts,
        )

    @staticmethod
    def _leaderboard_user_points_txt(leaderboard: List[Tuple[str, int]], limit: Optional[int]) -> str:
        txt = ""
        for row in leaderboard[:limit]:
            txt += f"\n <@{row[0]}>: {row[1]}"
        return txt

    def get_weekly_users_with_points(self):
        leaderboard = self.db.get_user_points('week')
        return [l[0] for l in leaderboard]

    def send_weekly_leaderboard_direct_messages(self, user):
        leaderboard = self.db.get_user_points('week')
        msg_receivers = [l[0] for l in leaderboard]

        txt = f"This past week's :{EMOJI}: leaderboard: \n"
        txt = f"{txt}\n{self._leaderboard_user_points_txt(leaderboard)}"

        for r in [l[0] for l in leaderboard]:
            self._post_dm_to_user(
                # FIXME replace this once tested with sending to admin user
                #user=r,
                user=ADMIN_SLACK_USER,
                text=txt,
            )

    def all_time_leaderboard(self, limit: Optional[int] = None) -> str:
        leaderboard = self.db.get_user_points()

        txt = f"All-time :{EMOJI}: leaderboard:"
        return f"{txt}\n{self._leaderboard_user_points_txt(leaderboard, limit)}"

    def monthly_leaderboard(self, limit: Optional[int] = None) -> str:
        leaderboard = self.db.get_user_points('month')

        txt = f"This month's :{EMOJI}: leaderboard: \n"
        return f"{txt}\n{self._leaderboard_user_points_txt(leaderboard, limit)}"

    def weekly_leaderboard(self, limit: Optional[int] = None) -> str:
        leaderboard = self.db.get_user_points('week')

        txt = f"This week's :{EMOJI}: leaderboard: \n"
        return f"{txt}\n{self._leaderboard_user_points_txt(leaderboard, limit)}"

    def get_user_points_sent_today(self, user: str) -> int:
        return self.db.get_number_of_points_given_so_far_today(user)

    def award_emoji_points_from_msg(self, msg):
        if len(msg.recipients) == 0:
            return
        elif msg.sender in msg.recipients and msg.sender != ADMIN_SLACK_USER:
            # Cannot send to yourself
            self._post_channel_message_to_user(msg.channel, msg.sender, sender_in_recipients())
            return

        points = msg.count_emojis_in_message()
        count_to_send = (points * len(msg.recipients))

        # Avoid db lookup if we know we can't send this many points
        if count_to_send > MAX_POINTS_PER_SENDER_PER_DAY:
            self._post_channel_message_to_user(msg.channel, msg.sender, sender_point_limit_response(count_to_send))
            return

        # Validate sender hasn't reached their daily max
        sent_today = self.get_user_points_sent_today(msg.sender)
        if sent_today + count_to_send > MAX_POINTS_PER_SENDER_PER_DAY and msg.sender != ADMIN_SLACK_USER:
            self._post_channel_message_to_user(msg.channel, msg.sender, sender_point_limit_response(count_to_send))
            return

        self.db.add_points_to_users(msg.sender, msg.recipients, msg.channel, points)

        left_to_send = (MAX_POINTS_PER_SENDER_PER_DAY - sent_today - count_to_send)

        self._post_channel_message_to_user(
            user=msg.sender,
            channel=msg.channel,
            text=generate_random_response(points, msg.recipients, left_to_send),
        )

        for r in msg.recipients:
            self._post_dm_to_user(
                user=r,
                text=recipient_direct_message(points, msg.sender),
            )
