# dynamodb.py

import boto3
from pprint import pprint

dynamodb = boto3.resource('dynamodb')

# Users（ユーザー）テーブル
def create_users_table():
    dynamodb.create_table(
        TableName='Users',
        KeySchema=[{'AttributeName': 'UserId', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'UserId', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
    )

# Orders（注文）テーブル
def create_orders_table():
    dynamodb.create_table(
        TableName='Orders',
        KeySchema=[{'AttributeName': 'UserId', 'KeyType': 'HASH'},
                   {'AttributeName': 'OrderDate', 'KeyType': 'RANGE'}],
        AttributeDefinitions=[{'AttributeName': 'UserId', 'AttributeType': 'S'},
                              {'AttributeName': 'OrderDate', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
    )

# 項目を作成（put_item）
def put_item():
    dynamodb.Table('Users').put_item(Item={'UserId': '1', 'Name': 'Taro'})
    dynamodb.Table('Users').put_item(Item={'UserId': '2', 'Name': 'Jiro'})
    dynamodb.Table('Orders').put_item(Item={'UserId': '1', 'OrderDate': '20190101', 'Detail': {'Apple': 10}})
    dynamodb.Table('Orders').put_item(Item={'UserId': '1', 'OrderDate': '20190202', 'Detail': {'Apple': 20}})
    dynamodb.Table('Orders').put_item(Item={'UserId': '2', 'OrderDate': '20190303', 'Detail': {'Orange': 30}})

# 項目を取得（get_item）
def get_item():
    result = dynamodb.Table('Users').get_item(Key={'UserId': '1'})
    pprint(result['Item'])
    result = dynamodb.Table('Orders').get_item(Key={'UserId': '1', 'OrderDate': '20190101'})
    pprint(result['Item'])

# Filesテーブルを作成（LSI、GSIあり）
def create_files_table():
    dynamodb.create_table(
        TableName='Files',
        KeySchema=[{'AttributeName': 'Folder', 'KeyType': 'HASH'},
                   {'AttributeName': 'File', 'KeyType': 'RANGE'}],
        AttributeDefinitions=[{'AttributeName': 'Folder', 'AttributeType': 'S'},
                              {'AttributeName': 'File', 'AttributeType': 'S'},
                              {'AttributeName': 'Size', 'AttributeType': 'N'},
                              {'AttributeName': 'Type', 'AttributeType': 'S'}],
        ProvisionedThroughput={'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10},
        LocalSecondaryIndexes=[
            {'IndexName': 'FilesBySize',
             'KeySchema': [{'AttributeName': 'Folder', 'KeyType': 'HASH'},
                          {'AttributeName': 'Size', 'KeyType': 'RANGE'}],
             'Projection': {'ProjectionType': 'ALL'}}],
        GlobalSecondaryIndexes=[
            {'IndexName': 'FilesByType',
             'KeySchema': [{'AttributeName': 'Type', 'KeyType': 'HASH'},
                           {'AttributeName': 'Size', 'KeyType': 'RANGE'}],
             'Projection': {'ProjectionType': 'ALL'},
             'ProvisionedThroughput': {'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}}]
    )

# Filesテーブルに項目を作成（batch_write_item）
def batch_write_item():
    dynamodb.batch_write_item(
        RequestItems={
            'Files': [
                {'PutRequest':
                     {'Item': {'Folder': '/home/taro/', 'File': 'index.html', 'Type': 'text/html', 'Size': 200}}},
                {'PutRequest':
                     {'Item': {'Folder': '/home/taro/', 'File': 'apple.png', 'Type': 'image/png', 'Size': 100}}},
                {'PutRequest':
                     {'Item': {'Folder': '/home/taro/', 'File': 'cat.png', 'Type': 'image/png', 'Size': 300}}},
                {'PutRequest':
                     {'Item': {'Folder': '/home/jiro/', 'File': 'dog.png', 'Type': 'image/png', 'Size': 500}}},
                {'PutRequest':
                     {'Item': {'Folder': '/home/jiro/', 'File': 'readme.md', 'Type': 'text/markdown', 'Size': 400}}}
            ]
        }
    )

# テーブルに対するクエリ
def query_table():
    print('query table:')
    result = dynamodb.Table('Files').query(
        KeyConditionExpression='Folder = :folder',
        ExpressionAttributeValues={':folder': '/home/taro/'})
    for i in result['Items']:
        print('{Folder}{File} ({Type}) {Size}'.format(**i))

# LSI（ローカルセカンダリインデックス）に対するクエリ
def query_lsi():
    print('query lsi:')
    result = dynamodb.Table('Files').query(
        IndexName='FilesBySize',
        KeyConditionExpression='Folder = :folder',
        ExpressionAttributeValues={':folder': '/home/taro/'})
    for i in result['Items']:
        print('{Folder}{File} ({Type}) {Size}'.format(**i))

# GSI（グローバルセカンダリインデックス）に対するクエリ
def query_gsi():
    print('query gsi:')
    result = dynamodb.Table('Files').query(
        IndexName='FilesByType',
        KeyConditionExpression='#type = :type',
        ExpressionAttributeNames={'#type': 'Type'},
        ExpressionAttributeValues={':type': 'image/png'})
    for i in result['Items']:
        print('{Folder}{File} ({Type}) {Size}'.format(**i))


# create_users_table()
# create_orders_table()
# put_item()
# get_item()
# create_files_table()
# batch_put_item()
# query_table()
# query_lsi()
# query_gsi()
