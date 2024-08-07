import json
import boto3
from botocore.exceptions import ClientError

# Initialize a DynamoDB session
dynamodb = boto3.resource('dynamodb')
# Create table object
table = dynamodb.Table('Metadata')

def handler(event, context):
    '''
    Handle interactions with the Database
    '''
    httpMethod = event['httpMethod']
    print(f"htttpMethod: {httpMethod}")
    
    body = json.loads(event['body'])
    print("Event Body")
    print(body)
    print(type(body))

    if httpMethod == 'POST':
        return POST(body)
    elif httpMethod == 'GET':
        return GET()
    elif httpMethod == 'PUT':
        return PUT(event.get('key'), event.get('update_expression'), event.get('expression_attribute_values'))
    elif httpMethod == 'DELETE':
        return DELETE(event.get('key'))
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid operation')
        }

def POST(body):
    identifier_value = body['identifier']
    print(identifier_value)
    try:
        # Add an item to the table
        response = table.put_item(
            Item={
                'identifier': identifier_value,  # Replace 'test_identifier' with your actual identifier value
                'Attribute1': 'Value1',            # Replace with your actual attribute names and values
                'Attribute2': 'Value2',
            }
        )
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

        # Retrieve an item from the table
        response = table.get_item(
            Key={
                'identifier': 'test_identifier',  # Replace 'test_identifier' with your actual identifier value
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