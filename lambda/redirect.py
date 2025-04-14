import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    short_code = event['pathParameters']['short_code']
    response = table.get_item(Key={'short_code': short_code})
    
    if 'Item' in response:
        return {
            'statusCode': 301,
            'headers': {
                'Location': response['Item']['long_url']
            }
        }
    else:
        return {
            'statusCode': 404,
            'body': "URL not found"
        }
