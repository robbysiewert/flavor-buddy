"""Module for retrieving and sending JSON formatted content"""
import json
"""AWS Module for interacting with AWS resources"""
import boto3
from botocore.exceptions import ClientError
import logging
import random

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize a DynamoDB session
dynamodb = boto3.resource('dynamodb')
# Create table object
table = dynamodb.Table('Metadata')
food_table = dynamodb.Table('Foods')

def handler(event, context):
    '''
    Delegate function to handle incoming HTTP requests based on the HTTP method.
    This function supports POST, GET, PUT, and DELETE operations.
    '''
    http_method = event['httpMethod']
    logger.info(f"htttpMethod: {http_method}")

    try:
        if http_method == 'POST':
            body = json.loads(event['body'])
            logger.info(f'Event body: {body}')
            return post(body)
        elif http_method == 'GET':
            # query_params = event['queryStringParameters']
            # logger.info(query_params)
            # return get(query_params)
            return get()
        # elif http_method == 'PUT':
        #     return PUT(event.get('key'), event.get('update_expression'), \
        #             event.get('expression_attribute_values'))
        elif http_method == 'DELETE':
            body = json.loads(event['body'])
            logger.info(f'Event body: {body}')
            return delete(body)
        else:
            return format_unsuccessful_response('Unsupported HTTP method')
    except Exception as e:
        return format_unsuccessful_response(e)

def post(body: dict):
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
    logger.info(f'identifier: {identifier_value}, attribute1: {attribute1_value}')

    # Temporary solution to add food data to the Foods table
    if identifier_value == 'add_food_data':
        logger.info('Calling add_food_data()')
        add_food_data()

    try:
        # Add an item to the table
        dynamodb_response = table.put_item(
            Item={
                'identifier': identifier_value,
                'attribute1': attribute1_value,
            }
        )
        logger.info("DynamoDB table updated")
        return format_successful_response({'message': 'Item added to DynamoDB table successfully'})
    except ClientError as e:
        return format_unsuccessful_response(e)
    except Exception as e:
        return format_unsuccessful_response(e)

def get() -> str:
    return get_random_food()

def get_depricated(query_params: dict) -> dict:
    """
    **Depricated**
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
        logger.info(identifier)

        # Retrieve an item from the table
        dynamodb_response = table.get_item(
            Key={
                'identifier': identifier,
            }
        )
        logger.info(dynamodb_response)
        if 'Item' in dynamodb_response:
            return format_successful_response(dynamodb_response['Item'])
        else:
            return format_unsuccessful_response('Item not found in table')
    except ClientError as e:
        return format_unsuccessful_response(e)

def delete(body: dict) -> dict:
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
    logger.info(identifier_value)
    try:
        # Add an item to the table
        response = table.delete_item(
            Key={
                'identifier': identifier_value,
            }
        )
        return format_successful_response('Item deleted successfully')
    except ClientError as e:
        return format_unsuccessful_response(e)

# def put(key, update_expression, expression_attribute_values):
    # TODO


def add_food_data() -> None:

    # Read the contents of the file into a list
    with open('food_data.txt', 'r') as file:
        food_data = json.load(file)
        logger.info(type(food_data))
    logger.info(food_data)
    if food_data:
        logger.info('Adding food data to the Foods table')
        # Insert each food item into the 'Foods' table
        for food in food_data:
            food_table.put_item(Item=food)
            logger.info(f"Added {food['id']} to the Foods table")


def format_successful_response(data: dict) -> dict:
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(data)
    }
    return response

def format_unsuccessful_response(exception) -> dict:
    logger.exception(exception)
    response = {
        'statusCode': 500,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(f"Error creating item: {exception}")
    }
    return response

def get_random_food() -> str:
    """Returns a random food item from the 'Foods' table."""
    # Use the scan operation to retrieve all items from the table
    response = food_table.scan()
    # Get the list of items from the response
    items = response['Items']
    # Randomly select an item from the list
    random_item = random.choice(items)
    logger.info(random_item)
    logger.info(type(random_item))
    logger.info(random_item['id'])
    return format_successful_response({'message': random_item['id']})