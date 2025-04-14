import json
import os
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    body = json.loads(event['body'])
    long_url = body['url']
    
    short_code = str(uuid.uuid4())[:6]
    table.put_item(Item={'short_code': short_code, 'long_url': long_url})
    
    return {
        'statusCode': 200,
        'body': json.dumps({'short_url': f"https://{event['headers']['Host']}/{short_code}"})
    }
