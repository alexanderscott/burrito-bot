import os

EMOJI = os.environ.get('EMOJI', 'burrito')
EMOJI_PLURAL = os.environ.get('EMOJI_PLURAL', 'burritos')
MAX_POINTS_PER_SENDER_PER_DAY = int(os.environ.get('MAX_POINTS_PER_SENDER_PER_DAY', 5))
BOT_NAME = os.environ.get('BOT_NAME', 'BurritoBot')
SLASH_COMMAND = os.environ.get('SLASH_COMMAND', 'burritobot')
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN')
DYNAMO_TABLE_NAME = os.environ.get("DYNAMO_TABLE_NAME")
DYNAMO_ENDPOINT_URL = os.environ.get("DYNAMO_ENDPOINT_URL")
ADMIN_SLACK_USER = os.environ.get("ADMIN_SLACK_USER")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "DEBUG")
