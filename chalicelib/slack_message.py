from chalicelib.global_constants import EMOJI


class SlackMessage:
    def __init__(self, sender, recipients, message, channel):
        self.sender = sender
        self.recipients = recipients
        self.message = message
        self.channel = channel

    @staticmethod
    def parse(event):
        sender = event['user']
        message = event['text']

        # if this message is a thread, we want the thread message text instead of original text
        # if 'thread_ts' in event:
        #     message = event['blocks'][0]['elements'][0]['elements'][0]['text']

        recipients = []
        for b in event['blocks']:
            for e1 in b['elements']:
                for e2 in e1['elements']:
                    if e2['type'] == 'user':
                        recipients.append(e2['user_id'])

        return SlackMessage(
            sender,
            recipients,
            message,
            event['channel'],
        )

    def count_emojis_in_message(self) -> int:
        return self.message.count(f":{EMOJI}:")
