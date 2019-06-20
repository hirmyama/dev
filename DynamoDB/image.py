import json
import boto3
dynamodb = boto3.resource('dynamodb')
rekognition = boto3.client('rekognition')
translate = boto3.client('translate')

def en_ja(text):
    return translate.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode='ja'
    )['TranslatedText']

def detect_labels(bucket, key):
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        }
    )
    return [en_ja(label['Name']) for label in response['Labels']]

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        labels = detect_labels(bucket, key)
        labels_str = ' '.join(['#' + label.replace('[', '').replace(']', '') for label in labels])
        dynamodb.Table('images').put_item(Item={'key': key, 'labels': labels_str})
    return {
        'statusCode': 200,
        'body': json.dumps(labels)
    }
