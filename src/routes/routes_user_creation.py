# Standard library imports
import traceback

# Third party imports
import ujson
from pydash import py_
from loguru import logger

# User based imports
from engine import dynamodb
from utils import cognito, utils
from constants import constants

# Constants
GLOBAL = 'routes_user_creation'


def handle_request(event, body):
    """[it handle request based on routes]

    Args:
        event ([dict]): [incoming event from api gateway]
        body ([dict]): [incoming body payload from api gateway]

    Returns:
        [dict, status_code]: [return response and status code]
    """

    response = None
    status_code = 404
    email = body['email']
    user_name = body['userName'] if 'userName' in body else email.split('@')[0]
    name = py_.get(body, 'name', 'Not Assigned')
    client_id = body['client_id']
    customer_id = py_.get(event, 'queryStringParameters.customerId', None)
    logger.debug(f'ROUTE {event["resource"]}')

    try:
        if event['resource'] == '/security/create-admin-user/client':
            user_attributes = utils.get_user_attributes(client_id=client_id,
                                                        customer_id=customer_id,
                                                        is_client_admin='True',
                                                        is_customer_admin='False',
                                                        user_name=user_name,
                                                        name=name,
                                                        email=email)

            client_exists = dynamodb.get_item(table=constants.CLIENT_TABLE,
                                              key={'id': client_id})
            logger.trace(f'CLIENT_EXIST {ujson.dumps(client_exists)}')

            if client_exists:
                limit = utils.check_client_user_limit(client_exists)
                logger.trace(f'MAX_LIMIT {limit}')
                if limit is not True:
                    status_code = 403
                    raise Exception('Maximum users for client reached')

                logger.debug(f'CALL_COGNITO_USER_CREATE {ujson.dumps(user_attributes)}')

                cognito_response = cognito.create_user(email,
                                                       user_attributes)

                logger.info(f'COGNITO_USER_CREATED {ujson.dumps(cognito_response)}')

                dynamodb_item = {
                    'id': cognito_response['User']['Username'],
                    'clientId': client_id,
                    'isClientAdmin': True
                }

                dynamodb.put_item(table=constants.CLIENT_USER_TABLE,
                                  item=dynamodb_item)

                dynamodb.update_item(table=constants.CLIENT_TABLE,
                                     key={
                                        'id': client_exists['id']
                                     },
                                     update_expression=constants.UPDATE_EXPRESSION,
                                     expression_attribute_values={
                                        ':inc': 1,
                                        ':start': 0,
                                     })
            else:
                status_code = 404
                raise Exception('Client does not exist')

            logger.success(f'SERVICE_EXIST user created with email {email}')
            response = {
                'message': f'User {email} created successfully.'
            }
            status_code = 201

        elif event['resource'] == '/security/create-admin-user/customer':
            user_attributes = utils.get_user_attributes(client_id=client_id,
                                                        customer_id=customer_id,
                                                        is_client_admin='False',
                                                        is_customer_admin='True',
                                                        user_name=user_name,
                                                        name=name,
                                                        email=email)

            client_exists = dynamodb.get_item(table=constants.CLIENT_TABLE,
                                              key={'id': client_id})

            logger.trace(f'CLIENT_EXIST {ujson.dumps(client_exists)}')

            if client_exists:
                limit = utils.check_client_user_limit(client_exists)
                logger.trace(f'MAX_LIMIT {limit}')
                if limit is not True:
                    status_code = 403
                    raise Exception('Maximum users for client reached')

                logger.debug(f'CALL_COGNITO_USER_CREATE {ujson.dumps(user_attributes)}')

                customer_exists = dynamodb.get_item(table=constants.CUSTOMER_TABLE,
                                                    key={'id': customer_id,
                                                         'clientId': client_id})

                logger.trace(f'CUSTOMER_EXIST {ujson.dumps(customer_exists)}')

                if customer_exists:
                    cognito_response = cognito.create_user(email,
                                                           user_attributes)

                    logger.info(f'COGNITO_USER_CREATED {ujson.dumps(cognito_response)}')

                    dynamodb_item = {
                        'id': cognito_response['User']['Username'],
                        'customerId': customer_id,
                        'isCustomerAdmin': True
                    }

                    dynamodb.put_item(table=constants.USER_TABLE,
                                      item=dynamodb_item)

                    dynamodb.update_item(table=constants.CLIENT_TABLE,
                                         key={
                                            'id': client_exists['id']
                                         },
                                         update_expression=constants.UPDATE_EXPRESSION,
                                         expression_attribute_values={
                                            ':inc': 1,
                                            ':start': 0,
                                         })
                else:
                    status_code = 404
                    raise Exception('Customer does not exist')

            else:
                status_code = 404
                raise Exception('Client does not exist')

            logger.success(f'SERVICE_EXIST user created with email {email}')
            response = {
                'message': f'User {email} created successfully.'
            }
            status_code = 201

    except Exception as error:
        response = {
            'status': 'failure',
            'component': f'{GLOBAL}.py',
            'exception': str(error),
            'traceback': traceback.format_exc()
        }
        logger.opt(exception=True).error('API_FAILURE')

    return {"message": "invalid route"} if not response else response, status_code
