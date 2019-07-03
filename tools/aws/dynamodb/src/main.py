import click
from util.dynamodb import DynamoDB


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@main.command(help='標準出力で指定した環境に存在するdynamodbテーブルを全て表示します')
@click.option('--profile', '-p', default='default', help='profileを指定します。')
def print_table_name(profile):
    dynamo = DynamoDB(profile)
    table_list = dynamo.get_table_list()
    print("********************************************************************")
    print(table_list)
    print("********************************************************************")


if __name__ == '__main__':
    main()
