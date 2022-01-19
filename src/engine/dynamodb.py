# Third party imports
import ujson
import boto3
from loguru import logger

from botocore.config import Config

# DynamoDB Config
config = Config(
    retries={
        'max_attempts': 5,
        'mode': 'standard'
    }
)

dynamodb = boto3.resource('dynamodb', config=config)

# 

def get_item(table, key):
    """[Perform to get item from dynamodb]

    Args:
        table ([str]): [name of table]
        key ([dict]): [dictionary for query dynamodb table]

    Returns:
        [dict]: [response from dynamodb]
    """
    logger.trace(f'ARGUMENTS {ujson.dumps(locals())}')
    dynamodb_table = dynamodb.Table(table)
    response = dynamodb_table.get_item(Key=key)
    logger.info(f'DYNAMODB {ujson.dumps(response)}')
    return response.get('Item', None)


def put_item(table, item):
    """[Perform to put item in dynamodb]

    Args:
        table ([str]): [name of table]
        item ([dict]): [dict to insert in dynamodb]

    Returns:
        [dict]: [response from dynamodb]
    """
    logger.trace(f'ARGUMENTS {ujson.dumps(locals())}')
    dynamodb_table = dynamodb.Table(table)
    response = dynamodb_table.put_item(Item=item)
    logger.info(f'DYNAMODB {ujson.dumps(response)}')
    return response


def update_item(table, key, update_expression, expression_attribute_values):
    """[Perform to update item in dynamodb]

    Args:
        table ([str]): [name of table]
        key ([dict]): [dict object for the key identifier]
        update_expression ([str]): [expression for updating item]
        expression_attribute_values ([dict]): [keys to update for expression]

    Returns:
        [dict]: [response from dynamodb]
    """
    logger.trace(f'ARGUMENTS {ujson.dumps(locals())}')
    dynamodb_table = dynamodb.Table(table)
    response = dynamodb_table.update_item(
        Key=key,
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )
    logger.info(f'DYNAMODB {ujson.dumps(response)}')
    return response
