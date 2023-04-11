import pytz
import boto3

from collections import Counter
from datetime import datetime, timedelta, date, timezone

from typing import List, Tuple, Optional
from boto3.dynamodb.conditions import Key

PST_TIMEZONE = pytz.timezone("America/Los_Angeles")


class BotDB:
    def __init__(self, table_name: str, endpoint_url: Optional[str] = None):
        self.table_name = table_name

        # hack to use localhost dynamo which doesn't import AWS env vars
        if endpoint_url:
            self.dynamo_client = boto3.client('dynamodb', endpoint_url=endpoint_url)
            self.dynamo_resource = boto3.resource('dynamodb', endpoint_url=endpoint_url)
        else:
            self.dynamo_client = boto3.client('dynamodb')
            self.dynamo_resource = boto3.resource('dynamodb')

        self.dynamo_table = self.dynamo_resource.Table(table_name)

    @staticmethod
    def _utc_to_pst(utc_dt: datetime) -> datetime:
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(PST_TIMEZONE)

    @staticmethod
    def _pst_to_utc(pst_dt: datetime) -> datetime:
        return pst_dt.replace(tzinfo=PST_TIMEZONE).astimezone(pytz.utc)

    def _utc_now(self) -> datetime:
        return datetime.utcnow()

    def create_table(self):
        table = self.dynamo_resource.create_table(
            TableName=self.table_name,
            KeySchema=[
                {
                    'AttributeName': 'sender',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'datetime_given',
                    'KeyType': 'RANGE'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'sender',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'datetime_given',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        # Wait until the table exists.
        table.wait_until_exists()

        # Print out some data about the table.
        print("Dynamo tables: ")
        print(list(self.dynamo_resource.tables.all()))
        print(table.item_count)

    def destroy_table(self):
        self.dynamo_client.delete_table(TableName=self.table_name)

    def truncate_table(self):
        table = self.dynamo_resource.Table(self.table_name)

        # get the table keys
        tableKeyNames = [key.get("AttributeName") for key in table.key_schema]

        # Only retrieve the keys for each item in the table (minimize data transfer)
        projectionExpression = ", ".join('#' + key for key in tableKeyNames)
        expressionAttrNames = {'#' + key: key for key in tableKeyNames}

        counter = 0
        page = table.scan(ProjectionExpression=projectionExpression, ExpressionAttributeNames=expressionAttrNames)
        with table.batch_writer() as batch:
            while page["Count"] > 0:
                counter += page["Count"]
                # Delete items in batches
                for itemKeys in page["Items"]:
                    batch.delete_item(Key=itemKeys)
                # Fetch the next page
                if 'LastEvaluatedKey' in page:
                    page = table.scan(
                        ProjectionExpression=projectionExpression, ExpressionAttributeNames=expressionAttrNames,
                        ExclusiveStartKey=page['LastEvaluatedKey'])
                else:
                    break
        print(f"Deleted {counter}")

    def add_points_to_users(self, sender: str, recipients: List[str], channel: str, points: int):
        for recipient in recipients:
            for _ in range(points):
                now = self._utc_now().isoformat()
                self.dynamo_client.put_item(TableName=self.table_name, Item={
                    'sender': {'S': sender},
                    'recipient': {'S': recipient},
                    'datetime_given': {'S': str(now)},
                    'channel': {'S': channel}
                })

    def get_user_points(self, period: Optional[str] = None) -> List[Tuple[str, int]]:
        start = None
        end = (self._utc_now().date() + timedelta(1)).isoformat()
        if period == 'week':
            start = (self._utc_now().date() - timedelta(days=7)).isoformat()
        elif period == 'month':
            start = (self._utc_now().date() - timedelta(days=31)).isoformat()

        if start:
            results = self.dynamo_table.scan(
                TableName=self.table_name,
                ProjectionExpression='recipient',
                FilterExpression=Key('datetime_given').between(start, end),
            )['Items']
        else:
            results = self.dynamo_table.scan(
                TableName=self.table_name,
                ProjectionExpression='recipient',
            )['Items']

        recipients = [recipient['recipient'] for recipient in results]

        return Counter(recipients).most_common()

    def get_number_of_points_given_so_far_today(self, user_id: str) -> int:
        now = self._utc_now()

        # Convert to PST and back, as we want point totals to refresh at midnight in local PST timezone
        now_pst_dt = self._utc_to_pst(now)
        now_pst_date = now_pst_dt.date()
        start_of_day_pst_dt = datetime(now_pst_date.year, month=now_pst_date.month, day=now_pst_date.day, hour=0, minute=0, second=0, tzinfo=PST_TIMEZONE)
        end_of_day_pst_dt = start_of_day_pst_dt + timedelta(days=1)
        start_utc = self._pst_to_utc(start_of_day_pst_dt).isoformat()
        end_utc = self._pst_to_utc(end_of_day_pst_dt).isoformat()

        results = self.dynamo_table.query(
            TableName=self.table_name,
            KeyConditionExpression=Key('sender').eq(user_id) & Key('datetime_given').between(start_utc, end_utc)
        )['Items']

        return len(results)

