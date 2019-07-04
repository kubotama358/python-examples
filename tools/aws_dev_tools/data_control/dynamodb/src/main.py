import click
from util.dynamodb import DynamoDB


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())


@main.command(help='display to dynamodb tables')
@click.option('--profile', '-p', default='default', help='profileを指定します。')
def print_table_name(profile):
    dynamo = DynamoDB(profile)
    table_list = dynamo.get_table_list()
    print("********************************************************************")
    for table_name in table_list:
        print(table_name)
    print("********************************************************************")


@main.command(help='display to dynamodb tables delete command')
@click.option('--profile', '-p', default='default', help='profileを指定します。')
def make_delete_table_cmd(profile):
    dynamo = DynamoDB(profile)
    table_list = dynamo.get_table_list()

    print("********************************************************************")
    for table_name in table_list:
        print(f"aws dynamodb delete-table --table-name {table_name} --profile {profile}")
    print("********************************************************************")


if __name__ == '__main__':
    main()
