from boto3.session import Session


class DynamoDB:
    def __init__(self, profile):
        session = Session(profile_name=profile)
        self.dynamodb = session.client('dynamodb')

    def get_table_list(self):
        """
        対象環境のdynamodbのテーブル名を全て取得します。
        :return: result
        """
        table_names = []
        last_evaluated_table_name = None

        while not table_names or last_evaluated_table_name:
            response = self._get_table_names(last_evaluated_table_name)
            if not response['TableNames']:
                break
            table_names.extend(response['TableNames'])
            last_evaluated_table_name = response.get('LastEvaluatedTableName', None)

        return table_names

    def delete_table(self, table_name):
        """
        引数で指定したテーブルを削除します。
        :param table_name:
        :return:
        """
        self.dynamodb.delete_table(TableName=table_name)

    def _get_table_names(self, exclusive_start_table_name=None):
        response = self.dynamodb.list_tables(
            ExclusiveStartTableName=exclusive_start_table_name) if exclusive_start_table_name else self.dynamodb.list_tables()
        print(response)
        return response
