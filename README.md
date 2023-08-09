# burrito-bot
![build CI](https://github.com/alexanderscott/burrito-bot/actions/workflows/ci.yml/badge.svg)

Slack app for giving teammates the gratitude of burritos after doing something awesome.
Similar concept to [HeyTaco](https://www.heytaco.chat/)

![BurritoBot](assets/img/burrito-150x.png)

App is serverless, running via AWS lambda and using DynamoDB for storage.
Uses [Chalice](https://aws.github.io/chalice/index) serverless framework for lambda scaffolding and
[Bolt](https://slack.dev/bolt-python/concepts) for reacting to Slack @mentions and new emoji reactions.



## Install Locally
Create a python virtualenv and install python deps
```shell
# Python 3.6+ required
python -m venv .venv
source .venv/bin/activate

pip install -U pip
pip install -r requirements.txt
```

Install local dynamodb and run it:
```shell
brew install dynamodb-local && dynamodb-local
```

Run dynamo migration to insert the table:
```shell
python scripts/migrate_db.py
```

## Configure a New Slack App
Follow the [Bolt guide here](https://slack.dev/bolt-python/tutorial/getting-started) for details on how to create and configure a new
Slack app. The oauth tokens provided by Slack during setup are needed in app configuration.

Note: you must be a Slack admin or receive approval from an admin in order to install to a Slack workspace.


## Configure
Copy `.chalice/config.json.sample` to `.chalice/config.json` and add Slack tokens/secrets.

```
export SLACK_SIGNING_SECRET=
export SLACK_BOT_TOKEN=
export VERIFICATION_TOKEN=
export BOT_NAME=BurritoBot
export EMOJI_PLURAL=burritos
export EMOJI=burrito
export SLASH_COMMAND=burritobot
export MAX_POINTS_PER_SENDER_PER_DAY=5
export DYNAMO_TABLE_NAME=burrito_points
export DYNAMO_ENDPOINT_URL=http://localhost:8000
export ADMIN_SLACK_USER=U01AP4BM8SD
export LOG_LEVEL=DEBUG
```


## Run Locally
```shell
# start local dynamodb
dynamodb-local

# start the app
chalice local --port 3000

# in another terminal
ngrok http 3000
```

Then edit the Event Subscriptions callback URL in Slack App settings to point to local ngrok tunnel.

See the `scripts` directory for db helpers to create the dynamodb table locally and seed it.


## Run Tests
These are primarily integration tests and rely on having dynamodb-local running
```shell
python -m unittest discover ./tests "test_*.py"
```



## Deploy to AWS with Chalice
Create the dynamodb table in AWS using CloudFormation:
```shell
aws cloudformation create-stack --stack-name burrito-points \
  --template-body file://cloudformation.yaml
```

Fill in the environment variables in `.chalice/config.json`.

Then to deploy:
```
chalice deploy --stage dev --no-autogen-policy
```



## TODO
- ~~[ ] Handle direct messages to the bot similar to slash command request types~~
- [ ] Clear explanation & help text from `/burritobot help` or DM to @BurritoBot
- [ ] Weekly leaderboard roll-up message to individuals (or channel)
- [ ] [Sentry integration](https://docs.sentry.io/platforms/python/guides/chalice/) for observability
- [ ] Message or reaction deletion handling
- [ ] Reactions should look for direct mentions in message text and award to those users?
- [x] Testing for messages and reactions inside threads
- [x] [CI/CD for autotest + autodeploy](https://aws.github.io/chalice/topics/cd.html)
- [x] Display emoji points remaining (under the max cap) inside the response to sender
- [x] AWS Cloudformation template for deploy/teardown (chalice integration)
- [x] Monthly and all-time leaderboards in addition to weekly
- [x] Direct messages to recipients to notify of emoji reward

## Future Enhancement Ideas
- [ ] Cronjob to send leaderboard update using [scheduled jobs](https://aws.github.io/chalice/api.html#Cron)?
- [ ] Message text storage for context?
- [ ] Lookup for [readable usernames](https://api.slack.com/methods/users.identity) and persist to db?
- [ ] Webpage for viewing leaderboard?


## License
MIT
