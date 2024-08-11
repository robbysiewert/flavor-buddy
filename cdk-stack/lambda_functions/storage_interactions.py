"""Module for retrieving and sending JSON formatted content"""
import json
"""AWS Module for interacting with AWS resources"""
import boto3
from botocore.exceptions import ClientError

# Initialize a DynamoDB session
dynamodb = boto3.resource('dynamodb')
# Create table object
table = dynamodb.Table('Metadata')

def handler(event, context):
    '''
    Delegate function to handle incoming HTTP requests based on the HTTP method.
    This function supports POST, GET, PUT, and DELETE operations.
    '''
    http_method = event['httpMethod']
    print(f"htttpMethod: {http_method}")

    if http_method == 'POST':
        body = json.loads(event['body'])
        print("Event Body")
        print(body)
        print(type(body))
        return post(body)
    elif http_method == 'GET':
        query_params = event['queryStringParameters']
        print(query_params)
        return get(query_params)
    elif http_method == 'PUT':
        return PUT(event.get('key'), event.get('update_expression'), \
                   event.get('expression_attribute_values'))
    elif http_method == 'DELETE':
        body = json.loads(event['body'])
        print("Event Body")
        print(body)
        print(type(body))
        return delete(body)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid operation')
        }

def post(body):
    """
    Handles an HTTP POST request to add an item to a DynamoDB table.

    This function extracts the 'identifier' value from the provided body,
    constructs an item with attributes, and attempts to insert
    the item into the DynamoDB table.

    Parameters:
        body (dict): A dictionary containing the data sent in the POST request body.
            It must include an 'identifier' key with its associated value.

    Returns:
        dict: A dictionary with the HTTP status code and a JSON-encoded message.

    Raises:
        ClientError: If an error occurs while interacting with the DynamoDB table.
    """

    identifier_value = body['identifier']
    attribute1_value = body['attribute1']
    print(identifier_value)
    try:
        # Add an item to the table
        dynamodb_response = table.put_item(
            Item={
                'identifier': identifier_value,
                'Attribute1': attribute1_value,
            }
        )

        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps('Item created successfully')
        }
        return response
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error creating item: {e.response['Error']['Message']}")
        }

def get(query_params: dict):
    """
    Retrieves an item from a DynamoDB table based on the provided identifier.

    Args:
        query_params (dict): A dictionary containing the query parameters,
            including the 'identifier' key.

    Returns:
        dict: A dictionary containing the following keys:
            - 'statusCode' (int): The HTTP status code of the response.
            - 'body' (str): The response body, which is a JSON-encoded string.

    Raises:
        ClientError: If an error occurs while interacting with the DynamoDB table.
    """
    try:
        identifier = query_params['identifier']
        print(identifier)

        # Retrieve an item from the table
        dynamodb_response = table.get_item(
            Key={
                'identifier': identifier,  # Replace 'test_identifier' with your actual identifier value
            }
        )
        if 'Item' in dynamodb_response:
            response = {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
                },
                'body': json.dumps(dynamodb_response['Item'])
            }
            return response
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

def delete(body):
    """
    Deletes an item from a DynamoDB table based on the provided identifier.

    Args:
        body (dict): A dictionary containing the request body, which should
            include the 'identifier' key with the value of the item to delete.

    Returns:
        dict: A dictionary containing the following keys:
            - 'statusCode' (int): The HTTP status code of the response.
            - 'body' (str): The response body, which is a JSON-encoded string.

    Raises:
        ClientError: If an error occurs while interacting with the DynamoDB table.
    """

    identifier_value = body['identifier']
    print(identifier_value)
    try:
        # Add an item to the table
        response = table.delete_item(
            Key={
                'identifier': identifier_value,
            }
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Item deleted successfully')
        }
    except ClientError as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {e.response['Error']['Message']}")
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
