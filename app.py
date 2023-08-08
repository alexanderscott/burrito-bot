import json
import logging

from typing import Dict

from slack_bolt import App
from slack_bolt.adapter.aws_lambda.chalice_handler import ChaliceSlackRequestHandler

from chalice import Chalice, Response, Cron

from chalicelib.bot_service import BotService
from chalicelib.slack_message import SlackMessage
from chalicelib.slack_reaction import SlackReaction
from chalicelib.global_constants import *
from chalicelib.response_generator import *

bolt_app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
    process_before_response=True,
)

log_levels: Dict[str, int] = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARN': logging.WARN,
    'ERROR': logging.ERROR
}


@bolt_app.middleware
def log_request(logger, body, next):
    app.log.debug(json.dumps(body, indent=2))
    return next()


@bolt_app.event("reaction_added")
def handle_emoji_reaction_added(client, event, logger):
    app.log.debug("*** EMOJI ADDED ***")
    app.log.debug(json.dumps(event, indent=2))

    if event['reaction'] != EMOJI:
        return

    msg = SlackReaction.parse(event)

    bot_service = BotService(client, DYNAMO_TABLE_NAME, DYNAMO_ENDPOINT_URL)
    bot_service.award_emoji_points_from_msg(msg)


# @app.event("reaction_removed")
# def handle_emoji_reaction_removed(ack, respond, message, event, client, command, say, logger):
#     logger.debug(json.dumps(event, indent=2))
#     # TODO figure out how/if to remove points upon removing a reaction
#     return


@bolt_app.message(f":{EMOJI}:")
def handle_emoji_message(client, message, logger):
    app.log.debug("*** MESSAGE ADDED ***")
    app.log.debug(json.dumps(message, indent=2))

    if 'bot_id' in message:
        app.log.warning("Ignore bot event")
        return

    msg = None
    try:
        msg = SlackMessage.parse(message)
    except Exception as e:
        app.log.error(e)
        return

    bot_service = BotService(client, DYNAMO_TABLE_NAME, DYNAMO_ENDPOINT_URL)
    bot_service.award_emoji_points_from_msg(msg)


@bolt_app.command(f"/{SLASH_COMMAND.lower()}")
def handle_slash_command(client, ack, respond, command):
    # Acknowledge command request
    ack()
    app.log.debug(json.dumps(command, indent=2))

    subcommand = command['text']
    if subcommand == 'help':
        # TODO
        respond("Help text will go here!")
        return

    bot_service = BotService(client, DYNAMO_TABLE_NAME, DYNAMO_ENDPOINT_URL)

    if subcommand == EMOJI_PLURAL:
        points_sent = bot_service.get_user_points_sent_today(command['user_id'])
        respond(f"You've given {count_with_emoji_text(points_sent)} today.")
    elif 'weekly' in subcommand:
        respond(bot_service.weekly_leaderboard())
    elif 'monthly' in subcommand:
        respond(bot_service.monthly_leaderboard())
    else:
        respond(bot_service.all_time_leaderboard())


ChaliceSlackRequestHandler.clear_all_log_handlers()
app = Chalice(app_name=BOT_NAME.lower())
slack_handler = ChaliceSlackRequestHandler(app=bolt_app, chalice=app)

app.log.setLevel(log_levels[LOG_LEVEL.upper()])


@app.route(
    "/slack/events",
    methods=["POST"],
    content_types=["application/x-www-form-urlencoded", "application/json"],
)
def events() -> Response:
    return slack_handler.handle(app.current_request)


@app.route("/slack/install", methods=["GET"])
def install() -> Response:
    return slack_handler.handle(app.current_request)


@app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect() -> Response:
    return slack_handler.handle(app.current_request)


# Send weekly leaderboard every Monday morning
@app.schedule(Cron(0, 14, '*', '?', '1', '*'))
def handle_weekly_leaderboard_message(event):
    app.log.warning("*** WEEKLY LEADERBOARD TRIGGERED ***")
    pass

# def handler(event, context):
#     slack_handler = SlackRequestHandler(app=app)
#     return slack_handler.handle(event, context)
#
#
# if __name__ == "__main__":
#     app.start(port=int(os.environ.get("PORT", 3000)))
