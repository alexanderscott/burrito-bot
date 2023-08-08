import re


class SlackReaction:
    MENTION_REGEX = '<@(|[WU].+?)>'

    def __init__(self, sender, recipients, channel, timestamp):
        self.sender = sender
        self.recipients = recipients
        self.channel = channel
        self.timestamp = timestamp

    @staticmethod
    def parse(event):
        sender = event['user']

        # Try to look for @ mentioned users in message text to serve as recipients
        # If no @ mentions in message text, gift to original message author
        recipients = [event['item_user']]
        if event.get('text'):
            recipients_tmp = SlackReaction._extract_recipients_from_message(event['text'])
            if recipients_tmp is not None:
                recipients = recipients_tmp

        channel = event['item']['channel']
        timestamp = event['event_ts']

        return SlackReaction(
            sender,
            recipients,
            channel,
            timestamp
        )

    def count_emojis_in_message(self) -> int:
        # A reaction is always worth 1 point
        return 1

    @classmethod
    def _extract_recipients_from_message(cls, message_text):
        matches = re.findall(cls.MENTION_REGEX, message_text)
        return matches if matches else None

