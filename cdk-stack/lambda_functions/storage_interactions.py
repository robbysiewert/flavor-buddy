import json
import boto3
from botocore.exceptions import ClientError

# Initialize a DynamoDB session  
dynamodb = boto3.resource('dynamodb')
# Create table object
table = dynamodb.Table('YourTableName')

def handler(event, context):
    '''
    Handle interactions with the Database
    '''
    operation = event.get('operation')
    
    if operation == 'POST':
        return POST(event.get('item'))
    elif operation == 'GET':
        return GET()
    elif operation == 'PUT':
        return PUT(event.get('key'), event.get('update_expression'), event.get('expression_attribute_values'))
    elif operation == 'DELETE':
        return DELETE(event.get('key'))
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid operation')
        }

def POST(item):
    try:
        response = table.put_item(Item=item)
        return {
            'statusCode': 200,
            'body': json.dumps('Item created successfully')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error creating item: {e.response['Error']['Message']}")
        }

def GET():
    try:
        response = table.get_item(
            Key={
                'identifer': 'Test'
            }
        )
        if 'Item' in response:
            return {
                'statusCode': 200,
                'body': json.dumps(response['Item'])
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps('Item not found')
            }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error reading item: {e.response['Error']['Message']}")
        }

def PUT(key, update_expression, expression_attribute_values):
    try:
        response = table.update_item(
            Key=key,
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return {
            'statusCode': 200,
            'body': json.dumps(response['Attributes'])
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error updating item: {e.response['Error']['Message']}")
        }

def DELETE(key):
    try:
        response = table.delete_item(Key=key)
        return {
            'statusCode': 200,
            'body': json.dumps('Item deleted successfully')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {e.response['Error']['Message']}")
        }