import click
import json
from util.dynamodb import DynamoDB
from util.cloudwatch import Cloudwatch
from util import _time
from util._csv import Csv


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@main.command(help='display to dynamodb tables')
@click.option('--profile', '-p', default='default', help='profileを指定します。')
def print_dynamo_metrics(profile):
    dynamodb = DynamoDB(profile)
    table_names = dynamodb.get_table_list()

    csv = Csv("output/metrics.csv")

    for table_name in table_names:
        if table_name == "lupin2-myauapp-prd-messaging-event-status":
            dynamo_read_capacity_metrics = _get_metrics_dynamo_read_capacity(profile, table_name)
            _write_csv_from_dynamo_read_capacity_metrics(csv, dynamo_read_capacity_metrics)


@main.command(help='display to dynamodb tables')
@click.option('--profile', '-p', default='default', help='profileを指定します。')
def print_sqs_metrics(profile):
    csv = Csv("output/sqs_metrics.csv")
    sqs_message_sent_metrics = _get_metrics_sqs_message_sent(profile,
                                                             "lupin2-myauapp-prd-routing-agent01-receiver-request.fifo")
    _write_csv_from_sqs_message_sent_metrics(csv, sqs_message_sent_metrics)


def _get_metrics_dynamo_read_capacity(profile, table_name):
    """

    :param profile:
    :param table_name:
    :return:
    """
    cloudwatch = Cloudwatch(profile)
    response = cloudwatch.get_dynamodb_read_capacity_metrics(table_name)
    response["Datapoints"] = sorted(response["Datapoints"], key=lambda x: x["Timestamp"])
    for i, _date in enumerate(response["Datapoints"]):
        response["Datapoints"][i]["Timestamp"] = _time.convert_iso_to_jst(_date["Timestamp"])

    return response


def _get_metrics_sqs_message_sent(profile, queue_name):
    """

    :param profile:
    :param table_name:
    :return:
    """
    cloudwatch = Cloudwatch(profile)
    response = cloudwatch.get_sqs_message_sent_metrics(queue_name)
    response["Datapoints"] = sorted(response["Datapoints"], key=lambda x: x["Timestamp"])
    for i, _date in enumerate(response["Datapoints"]):
        response["Datapoints"][i]["Timestamp"] = _time.convert_iso_to_jst(_date["Timestamp"])

    return response


def _write_csv_from_dynamo_read_capacity_metrics(csv: Csv, metrics_data_list):
    """

    :param csv:
    :param metrics_data_list:
    :return:
    """
    csv.write("Timestamp,readCapacity\n")

    for metrics_data in metrics_data_list["Datapoints"]:
        time_stamp = metrics_data["Timestamp"]
        value = metrics_data["Maximum"]
        csv.write(f"{time_stamp},{value}\n")


def _write_csv_from_sqs_message_sent_metrics(csv: Csv, metrics_data_list):
    """

    :param csv:
    :param metrics_data_list:
    :return:
    """
    csv.write("Timestamp,numberOfMessageSent\n")

    for metrics_data in metrics_data_list["Datapoints"]:
        time_stamp = metrics_data["Timestamp"]
        value = metrics_data["Sum"]
        csv.write(f"{time_stamp},{value}\n")


if __name__ == '__main__':
    main()
