from boto3.session import Session
from util import _time


class Cloudwatch:
    def __init__(self, profile):
        session = Session(profile_name=profile)
        self.cloudwatch = session.client('cloudwatch')

    def get_dynamodb_read_capacity_metrics(self, table_name, start_time=None, end_time=None):
        """
        対象環境のdynamodbのテーブル名を全て取得します。
        :return: result
        """
        if not start_time:
            start_time = _time.get_how_many_days_ago(5)

        if not end_time:
            end_time = _time.get_now()

        response = self.cloudwatch.get_metric_statistics(
            Namespace="AWS/DynamoDB",
            MetricName="ConsumedReadCapacityUnits",
            Dimensions=[{
                "Name": "TableName",
                "Value": table_name
            }],
            StartTime=start_time,
            EndTime=end_time,
            Period=1800,
            Statistics=["Maximum"]
        )
        return response
